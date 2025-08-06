from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class EnvConfig(BaseSettings):
    """
    Environment configuration using Pydantic BaseSettings.
    Automatically loads from environment variables and .env file.
    """

    # Environment settings
    environment: str = Field(
        default="development", description="Application environment"
    )

    # Logging configuration
    log_level: str = Field(default="INFO", description="Logging level")

    # API Keys
    openrouter_api_key: str = Field(default="", description="OpenRouter API key")

    @field_validator("environment")
    def validate_environment(cls, v):
        """Ensure environment is lowercase"""
        return v.lower()

    @field_validator("log_level")
    def validate_log_level(cls, v):
        """Ensure log level is uppercase"""
        return v.upper()

    @field_validator("openrouter_api_key")
    def validate_api_key(cls, v):
        """Validate API key format"""
        if not v or v.isspace():
            raise ValueError("OPENROUTER_API_KEY cannot be empty or whitespace")
        if len(v) < 10:  # Assuming minimum length
            raise ValueError("OPENROUTER_API_KEY appears to be too short")
        return v.strip()

    # Removed debug validator since there is no 'debug' field in the model

    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment == "production"

    class Config:
        # Configuration for Pydantic v2
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Singleton instance
_config_instance = None


def get_config() -> EnvConfig:
    """
    Get the singleton configuration instance.
    Creates the instance on first call.
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = EnvConfig()
    return _config_instance
