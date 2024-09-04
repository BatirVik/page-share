import os
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, field_validator


class Config(BaseSettings):
    DB_URL: PostgresDsn
    LOGS_PATH: Path
    PORT: int

    @field_validator("LOGS_PATH")
    def absolute_path(cls, value: Path):
        return Path(__file__).parent.parent / value


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

DOTENV_PATH = Path(__file__).parent.parent / "configuration" / DOTENV_FILENAMES[MODE]
config = Config(_env_file=DOTENV_PATH)  # type: ignore
