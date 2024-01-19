import os
from enum import Enum

from pydantic import BaseModel
from pydantic.networks import PostgresDsn
from starlette.config import Config


class Environment(str, Enum):
    DEV = "dev"
    PRODUCTION = "prod"


import os

root = os.path.abspath(os.sep)


def get_docker_secret(name_secret, secrets_dir=os.path.join(root, "run", "secrets")):
    # initiallize value
    value = None

    with open(os.path.join(secrets_dir, name_secret), "r") as secret_file:
        value = secret_file.read().rstrip("\n")

    return value


class Settings(BaseModel):
    ENVIRONMENT: Environment = Environment(os.environ.get("ENV_NAME", "dev"))

    config: Config = Config()

    DEBUG: bool = config("DEBUG", default=False, cast=bool)
    MOCK_OPENAI: bool = config("MOCK_OPENAI", default=False, cast=bool)

    DB_HOST: str = config("DB_HOST")
    DB_USER: str = config("DB_USER")
    DB_PASSWORD: str = get_docker_secret("db-password")
    DB_PORT: int = int(config("DB_PORT"))
    DB_NAME: str = config("DB_NAME")
    OPEN_AI_KEY: str = config("OPEN_AI_KEY")

    DB_URL: str = PostgresDsn.build(
        scheme="postgresql",
        host=DB_HOST,
        port=DB_PORT,
        path=f"{DB_NAME}",
        username=DB_USER,
        password=DB_PASSWORD,
    ).__str__()

    class Config:
        validate_default = True
        arbitrary_types_allowed = True


settings = Settings()
