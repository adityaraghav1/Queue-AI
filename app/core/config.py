from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "QueueAI"
    app_version: str = "0.1.0"
    debug: bool = True

    # AI configuration
    groq_api_key: str = ""

    # Database configuration
    database_url: str = "sqlite:///./queueai.db"

    # Authentication configuration
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_min: int = 60

    # Email configuration
    email_enabled: bool = False
    email_from: str = ""
    email_host: str = ""
    email_port: int = 587
    email_username: str = ""
    email_password: str = ""
    email_use_tls: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()