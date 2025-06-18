from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic_settings_aws import SecretsManagerBaseSettings

# AWS Secrets Managerからの設定を取得するための設定
class Settings(BaseSettings):
    AWS_SECRET_NAME: str
    AWS_REGION: str

aws_settings = Settings()

class AppSettings(SecretsManagerBaseSettings):
    model_config = SettingsConfigDict(
        secrets_name=aws_settings.AWS_SECRET_NAME,  # AWS Secrets Managerのシークレット名
        aws_region=aws_settings.AWS_REGION  # AWSリージョン
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

