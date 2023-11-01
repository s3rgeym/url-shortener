# URL Shortener

Real-world app example and template for development in Docker.

Development Stack: VSCode, Docker, Postgres, Pgadmin, Python, FastAPI, Asyncpg.

Launch compose:

```bash
docker compose up -d
```

Then `F5` > `Python: Remote Attach` for Debugging. The application will start only after the debugger. This is a development template.

Code changes will take effect immediately.

Create SHORT URL via Curl:

```bash
$ curl -d'url=https://www.youtube.com/watch?v=capY9GLjVk8' localhost:8000
http://localhost:8000/u/5ZTmyEZZW0~HPJnfptY9f
```

| URL | Service |
| --- | --- |
| <http://localhost:8000/> | URL Shortener |
| <http://localhost:8000/docs> | Documentation |
| <http://localhost:5050/> | pgAdmin. Default credentials: `pgadmin4@pgadmin.org:admin` |

![image](https://user-images.githubusercontent.com/12753171/278887688-8d1a7627-5349-44a8-b314-4fbae730cf59.png)
![image](https://user-images.githubusercontent.com/12753171/278843106-a24e55bd-5c6f-4b60-b1b9-d188e7562d3c.png)

Add new dependency:

```bash
# at host
poetry add whatever

# rebuild service
docker compose up -d --build --force-recreate --no-deps url_shortener

# or you can enter into container and add dependency
docker compose exec url_shortener sh
(inside container) poetry add whatever
```

Follow logs:

```bash
docker compose logs -f url_shortener
```

Stop:

```bash
docker compose down
```

Delete all data:

```bash
docker compose down -v --rmi all
```

Links:

* <https://fastapi.tiangolo.com/tutorial/first-steps/>
* <https://github.com/MagicStack/asyncpg>
* <https://code.visualstudio.com/docs/containers/debug-common>
* <https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/337>
* <https://lightrun.com/answers/tiangolo-fastapi-question-how-to-setup-a-remote-debugger-with-vscode>
* <https://github.com/tiangolo/fastapi/issues/707#issuecomment-760581929>
* <https://code.visualstudio.com/docs/containers/debug-python>
