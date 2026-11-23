"""Flagsmith integration for test-flagsmith."""

from flagsmith import Flagsmith
from flagsmith.models import Flag
from test_flagsmith.config import FlagsmithConfig, create_flagsmith_client

_client: Flagsmith | None = None


def get_client() -> Flagsmith:
    global _client
    if _client is None:
        _client = create_flagsmith_client()
    return _client


def get_flags(identity: str, traits: dict | None = None) -> dict[str, str | int | float | bool | None]:
    client = get_client()
    flags_obj = client.get_identity_flags(identifier=identity, traits=traits or {})
    flags_obj.all_flags()
    return {flag_name: flag.value for flag_name, flag in flags_obj.flags.items()}


def get_flag(identity: str, feature_name: str, default=None, traits: dict | None = None):
    client = get_client()
    flags_obj = client.get_identity_flags(identifier=identity, traits=traits or {})
    flag = flags_obj.get_flag(feature_name)
    return flag.value if flag else default


def is_enabled(identity: str, feature_name: str, default: bool = False, traits: dict | None = None) -> bool:
    client = get_client()
    flags_obj = client.get_identity_flags(identifier=identity, traits=traits or {})
    flag = flags_obj.get_flag(feature_name)
    return flag.enabled if flag else default


def get_flag_object(identity: str, feature_name: str, traits: dict | None = None) -> Flag | None:
    client = get_client()
    flags_obj = client.get_identity_flags(identifier=identity, traits=traits or {})
    flag = flags_obj.get_flag(feature_name)
    return flag if isinstance(flag, Flag) else None


def __getattr__(name: str):
    if name == "flagsmith":
        return get_client()
    raise AttributeError(f"module 'test_flagsmith' has no attribute '{name}'")


__all__ = [
    "get_client",
    "get_flags",
    "is_enabled",
    "get_flag",
    "get_flag_object",
    "flagsmith",
]