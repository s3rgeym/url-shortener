import uvicorn

from .application import app

if __name__ == "__main__":
    uvicorn.run(app)
