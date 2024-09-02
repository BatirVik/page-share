import os
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Config(BaseSettings):
    DB_URL: PostgresDsn
    LOGS_PATH: Path
    PORT: int


DOTENV_FILENAMES = dict(dev=".env", test=".env.test", prod=".env")

MODE = os.getenv("MODE")
if MODE is None:
    raise RuntimeError(
        "environment variable 'MODE' is not specified. Available values are ['dev', 'test', 'prod']"
    )
if MODE not in DOTENV_FILENAMES:
    raise RuntimeError(
        f"environment variable 'MODE' is specified with {MODE!r}."
        " Available values are ['dev', 'test', 'prod']"
    )

DOTENV_PATH = Path(__file__).parent.parent / DOTENV_FILENAMES[MODE]
config = Config(_env_file=DOTENV_PATH)  # type: ignore
