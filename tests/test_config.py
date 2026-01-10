"""Tests for configuration management."""
import pytest
import os
from unittest.mock import patch

from app.config import DatabaseSettings, settings


class TestDatabaseSettings:
    """Tests for DatabaseSettings."""

    def test_default_values(self):
        """Test default configuration values."""
        config = DatabaseSettings()
        
        assert config.POSTGRES_USER == "postgres"
        assert config.POSTGRES_PASSWORD == "postgres"
        assert config.POSTGRES_HOST == "localhost"
        assert config.POSTGRES_PORT == 5432
        assert config.POSTGRES_DB == "library_db"

    def test_database_url_property(self):
        """Test database_url property construction."""
        config = DatabaseSettings()
        url = config.database_url
        
        assert "postgresql+asyncpg://" in url
        assert "postgres:postgres" in url
        assert "@localhost:5432/library_db" in url

    def test_sync_database_url_property(self):
        """Test sync_database_url property construction."""
        config = DatabaseSettings()
        url = config.sync_database_url
        
        assert "postgresql://" in url
        assert "postgresql+asyncpg://" not in url
        assert "postgres:postgres" in url
        assert "@localhost:5432/library_db" in url

    @patch.dict(os.environ, {
        "POSTGRES_USER": "test_user",
        "POSTGRES_PASSWORD": "test_pass",
        "POSTGRES_HOST": "test_host",
        "POSTGRES_PORT": "5433",
        "POSTGRES_DB": "test_db"
    }, clear=False)
    def test_environment_variable_loading(self):
        """Test loading configuration from environment variables."""
        config = DatabaseSettings()
        
        assert config.POSTGRES_USER == "test_user"
        assert config.POSTGRES_PASSWORD == "test_pass"
        assert config.POSTGRES_HOST == "test_host"
        assert config.POSTGRES_PORT == 5433
        assert config.POSTGRES_DB == "test_db"

    def test_settings_instance(self):
        """Test that global settings instance exists."""
        assert settings is not None
        assert isinstance(settings, DatabaseSettings)
        assert settings.POSTGRES_DB == "library_db"

