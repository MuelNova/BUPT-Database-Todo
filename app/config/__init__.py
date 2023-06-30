import secrets

from typing import Any
from pydantic import BaseSettings


class Config(BaseSettings):
    host: str = '0.0.0.0'
    port: int = 16384
    mongo_uri: str = 'mongodb://localhost:27017'
    jwt_secret_key: str = secrets.token_hex(16)
    jwt_refresh_secret_key: str = secrets.token_hex(16)
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_minutes: int = 60 * 24 * 7
    
    class Config:
        env_file = '.env'


def get_config(**kwargs: Any) -> Config:
    global config
    if config is None:
        config = Config(**kwargs)
    return config


config: Config = None
