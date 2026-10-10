import importlib.util

from core.data_manager.config import DataManagerConfig
from core.data_manager.sources import FTShareSource


def test_ftshare_is_exported_and_configured(monkeypatch):
    monkeypatch.setenv("FTSHARE_API_KEY", "test-key")
    monkeypatch.setenv("FTSHARE_ENABLED", "true")
    monkeypatch.setattr(importlib.util, "find_spec", lambda name: object())

    config = DataManagerConfig(duckdb_path=None)
    source_config = config.get_source_config("ftshare")

    assert FTShareSource.__name__ == "FTShareSource"
    assert source_config["api_key"] == "test-key"
    assert source_config["enabled"] is True
    assert "ftshare" in config.get_preferred_sources()
