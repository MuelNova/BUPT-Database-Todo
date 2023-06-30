import uvicorn

from app import get_config


if __name__ == "__main__":
    config = get_config()
    uvicorn.run("app:app", host=config.host, port=config.port, reload=True)