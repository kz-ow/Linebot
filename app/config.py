from pydantic_settings import SettingsConfigDict
from pydantic_settings_aws import SecretsManagerBaseSettings

class AppSettings(SecretsManagerBaseSettings):
    model_config = SettingsConfigDict(
        secrets_name="fastapi_"  # AWS Secrets Managerのシークレット名
    )

    LINE_CHANNEL_SECRET: str
    LINE_CHANNEL_ACCESS_TOKEN: str
    POSTGRES_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    GEMINI_API_KEY: str
    GEMINI_REGION: str
    LIFF_ID_MODE: str
    LIFF_ID_SCHEDULER: str
    LIFF_ID_LANGUAGE: str
    LIFF_CHANNEL_ID: str
    TAVILY_API_KEY: str
    LANGUAGES: list[str] = [
        "日本語", "英語", "フランス語", "ドイツ語",
        "スペイン語", "韓国語", "中国語", "ロシア語"
    ]

settings = AppSettings()