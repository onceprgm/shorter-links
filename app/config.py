from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    bot_token: str
    bot_username: str
    database_url: str = "sqlite+aiosqlite:///./shorter_links.db"
    max_links_per_user: int = 100
    slug_length: int = 6


settings = Settings()
