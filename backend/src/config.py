from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"

    admin_username: str = "admin"
    # bcrypt hash — never store or compare plain-text passwords
    admin_password_hash: str = "$2b$12$changeme"

    # Optional second admin account (empty string = disabled)
    admin_username_2: str = ""
    admin_password_hash_2: str = ""

    scraper_pages_per_run: int = 100
    scraper_request_delay: float = 1.0


settings = Settings()
