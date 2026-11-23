"""Flagsmith configuration module."""

import os
from dataclasses import dataclass
from typing import Optional

from flagsmith import Flagsmith
from flagsmith.models import DefaultFlag


@dataclass
class FlagsmithConfig:
    environment_key: str
    enable_local_evaluation: bool = False
    api_url: str = "https://edge.api.flagsmith.com/api/v1/"
    request_timeout_seconds: int = 10
    environment_refresh_interval_seconds: int = 60
    custom_headers: Optional[dict] = None
    offline_mode: bool = False
    environment_document_path: Optional[str] = None

    @classmethod
    def from_env(cls) -> "FlagsmithConfig":
        environment_key = os.getenv("FLAGSMITH_SERVER_SIDE_ENVIRONMENT_KEY")
        if not environment_key:
            raise ValueError("FLAGSMITH_SERVER_SIDE_ENVIRONMENT_KEY environment variable is required")

        return cls(
            environment_key=environment_key,
            enable_local_evaluation=os.getenv("FLAGSMITH_ENABLE_LOCAL_EVALUATION", "false").lower() == "true",
            api_url=os.getenv("FLAGSMITH_API_URL", "https://edge.api.flagsmith.com/api/v1/"),
            request_timeout_seconds=int(os.getenv("FLAGSMITH_REQUEST_TIMEOUT_SECONDS", "10")),
            environment_refresh_interval_seconds=int(os.getenv("FLAGSMITH_ENV_REFRESH_INTERVAL_SECONDS", "60")),
            custom_headers=_parse_custom_headers(os.getenv("FLAGSMITH_CUSTOM_HEADERS")),
            offline_mode=os.getenv("FLAGSMITH_OFFLINE_MODE", "false").lower() == "true",
            environment_document_path=os.getenv("FLAGSMITH_ENVIRONMENT_DOCUMENT_PATH"),
        )


def _parse_custom_headers(headers_str: Optional[str]) -> Optional[dict]:
    if not headers_str:
        return None
    import json
    try:
        return json.loads(headers_str)
    except json.JSONDecodeError:
        return None


def create_default_flag_handler():
    def handler(feature_name: str) -> DefaultFlag:
        return DefaultFlag(enabled=False, value=None)
    return handler


def create_flagsmith_client(config: Optional[FlagsmithConfig] = None) -> Flagsmith:
    if config is None:
        config = FlagsmithConfig.from_env()

    kwargs = {
        "environment_key": config.environment_key,
        "enable_local_evaluation": config.enable_local_evaluation,
        "api_url": config.api_url,
        "request_timeout_seconds": config.request_timeout_seconds,
        "environment_refresh_interval_seconds": config.environment_refresh_interval_seconds,
        "default_flag_handler": create_default_flag_handler(),
    }

    if config.custom_headers:
        kwargs["custom_headers"] = config.custom_headers

    if config.offline_mode and config.environment_document_path:
        from flagsmith.offline_handlers import LocalFileHandler
        kwargs["offline_handler"] = LocalFileHandler(file_path=config.environment_document_path)

    return Flagsmith(**kwargs)