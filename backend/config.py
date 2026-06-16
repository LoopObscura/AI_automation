"""Configuration module for AutoAgent backend."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    api_title: str = "AutoAgent - AI-Powered Workflow Automation"
    api_version: str = "0.1.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    api_key: str = "your-secret-api-key-here"

    # Database
    database_url: str = "postgresql://user:password@localhost:5432/autoagent"
    database_pool_size: int = 20

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Qdrant Vector DB
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "autoagent_documents"

    # LLM Configuration
    llm_model: str = "mistral-7b"
    llm_api_key: Optional[str] = None
    llm_temperature: float = 0.7
    llm_max_tokens: int = 1024
    llm_confidence_threshold: float = 0.9

    # Embeddings Model
    embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Gmail API
    gmail_credentials_path: str = "./credentials/gmail-credentials.json"
    gmail_token_path: str = "./credentials/gmail-token.json"

    # Slack API
    slack_bot_token: Optional[str] = None
    slack_signing_secret: Optional[str] = None

    # QuickBooks API
    quickbooks_client_id: Optional[str] = None
    quickbooks_client_secret: Optional[str] = None
    quickbooks_realm_id: Optional[str] = None

    # BambooHR API
    bamboohr_api_key: Optional[str] = None
    bamboohr_domain: Optional[str] = None

    # Observability
    jaeger_agent_host: str = "localhost"
    jaeger_agent_port: int = 6831
    prometheus_port: int = 9090
    log_level: str = "INFO"
    log_format: str = "json"

    # Feature Flags
    enable_rag: bool = True
    enable_human_in_loop: bool = True
    enable_metrics: bool = True
    enable_tracing: bool = True

    # File Upload
    max_upload_size: int = 104857600  # 100MB
    allowed_file_types: str = "pdf,xlsx,csv,txt,eml"
    upload_dir: str = "./data/uploads"

    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    celery_task_timeout: int = 3600

    # Rules Engine
    rules_config_path: str = "./configs/rules.yaml"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
