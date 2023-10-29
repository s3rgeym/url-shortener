from contextlib import asynccontextmanager
from typing import Annotated
from urllib.parse import urljoin

import asyncpg
from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import PlainTextResponse, RedirectResponse

from . import base62
from .config import settings

BANNER = r"""
 _   _ ____  _       ____  _                _
| | | |  _ \| |     / ___|| |__   ___  _ __| |_ ___ _ __   ___ _ __
| | | | |_) | |     \___ \| '_ \ / _ \| '__| __/ _ \ '_ \ / _ \ '__|
| |_| |  _ <| |___   ___) | | | | (_) | |  | ||  __/ | | |  __/ |
 \___/|_| \_\_____| |____/|_| |_|\___/|_|   \__\___|_| |_|\___|_|

Create short urls from the terminal.

Usage:

    curl -d'url=<url>' {base_url}
    command | curl -F'url=<-' {base_url}
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.pool: asyncpg.Pool = await asyncpg.create_pool(
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_pass,
        port=settings.db_port,
    )
    await app.pool.execute(
        """
        CREATE TABLE IF NOT EXISTS public.urls
        (
            id uuid NOT NULL DEFAULT gen_random_uuid(),
            url character varying(4095) COLLATE pg_catalog."default" NOT NULL,
            created_at timestamp without time zone DEFAULT now(),
            CONSTRAINT urls_pkey PRIMARY KEY (id),
            CONSTRAINT uniq_url UNIQUE (url)
        )
    """
    )
    yield
    await app.pool.close()


app = FastAPI(default_response_class=PlainTextResponse, lifespan=lifespan)


@app.get("/")
async def show_banner(request: Request) -> str:
    return BANNER.format(base_url=request.base_url)


@app.post("/")
async def create_short_url(
    request: Request, url: Annotated[str, Form(title="URL")]
) -> str:
    conn: asyncpg.Connection
    async with app.pool.acquire() as conn:
        rv = await conn.fetchval(
            """
            WITH inserted AS (
                INSERT INTO urls ("url") VALUES ($1)
                ON CONFLICT ("url") DO NOTHING
                RETURNING id
            ) 
            SELECT * FROM inserted
            UNION 
            SELECT id FROM urls WHERE url=$1;
            """,
            url,
        )
        return urljoin(
            request.base_url._url,
            app.url_path_for("resolve_short_url", short_code=base62.encode(rv)),
        )


@app.get("/{short_code}")
async def resolve_short_url(short_code: str) -> Response:
    if rv := await app.pool.fetchval(
        "SELECT url FROM urls WHERE id=$1", base62.decode(short_code)
    ):
        return RedirectResponse(url=rv, status_code=302)
    return Response("URL Not Found", status_code=404)
