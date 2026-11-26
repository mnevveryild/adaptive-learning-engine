from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.paths import ENV_FILE


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",  # ilerde başka araçlar için de değişkenler olabilir burada hata vermemesi için ignore dedik
    )

    openai_api_key: SecretStr
    openai_model: str
