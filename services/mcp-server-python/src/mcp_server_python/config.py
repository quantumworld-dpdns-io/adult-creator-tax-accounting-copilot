"""Structured configuration via pydantic-settings."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="MCP_", extra="ignore")

    transport: str = "stdio"
    port: int = 8000
    host: str = "0.0.0.0"
    log_level: str = "info"
    oauth_issuer: str = ""
    oauth_audience: str = ""


settings = Settings()
