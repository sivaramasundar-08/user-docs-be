from pydantic_settings import BaseSettings


class EnvConfig(BaseSettings):
    db_username: str
    db_url: str
    db_name: str
    db_password: str
    secret_key: str
    algorithm: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        validate_assignment = True


env_config = EnvConfig()
