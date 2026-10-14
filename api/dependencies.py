from services.provider_registry import provider_registry
from services.run_store import run_store


def get_provider_registry():
    return provider_registry


def get_run_store():
    return run_store
