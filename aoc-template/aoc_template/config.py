from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    aoc_session: str
    project_root: str = "/home/jtfidje/dev/advent_of_code"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
