# GG Bot Upload Assistant
# Copyright (C) 2025  Noob Master669

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from unittest.mock import patch, MagicMock

import pytest
from pymongo.errors import OperationFailure, ConnectionFailure

from modules.cache_vendors.cache_mongo import Mongo
from modules.exceptions.exception import GGBotCacheClientException


class TestMongoAuth:
    """Test MongoDB authentication functionality."""

    @patch("modules.cache_vendors.cache_mongo.MongoClient")
    @patch("modules.cache_vendors.cache_mongo.CacheConfig")
    def test_connection_without_auth(self, mock_config, mock_mongo_client):
        """Test MongoDB connection without authentication."""
        # Configure mocks
        mock_config_instance = MagicMock()
        mock_config_instance.CACHE_USERNAME = None
        mock_config_instance.CACHE_HOST = "localhost"
        mock_config_instance.CACHE_PORT = "27017"
        mock_config_instance.CACHE_DATABASE = "test_db"
        mock_config.return_value = mock_config_instance

        # Create mock client
        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client

        # Create MongoDB instance
        mongo = Mongo()
        assert mongo is not None

        # Assert connection string doesn't have auth
        mock_mongo_client.assert_called_once()
        args, kwargs = mock_mongo_client.call_args
        assert "mongodb://localhost:27017/test_db" == args[0]
        assert "serverSelectionTimeoutMS" in kwargs
        assert "connectTimeoutMS" in kwargs

    @patch("modules.cache_vendors.cache_mongo.MongoClient")
    @patch("modules.cache_vendors.cache_mongo.CacheConfig")
    def test_connection_with_auth(self, mock_config, mock_mongo_client):
        """Test MongoDB connection with authentication."""
        # Configure mocks
        mock_config_instance = MagicMock()
        mock_config_instance.CACHE_USERNAME = "testuser"
        mock_config_instance.CACHE_PASSWORD = "testpass"
        mock_config_instance.CACHE_HOST = "mongo.example.com"
        mock_config_instance.CACHE_PORT = "27017"
        mock_config_instance.CACHE_DATABASE = "test_db"
        mock_config_instance.CACHE_AUTH_DB = "admin"
        mock_config.return_value = mock_config_instance

        # Create mock client
        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client

        # Create MongoDB instance
        mongo = Mongo()
        assert mongo is not None

        # Assert connection string includes auth
        mock_mongo_client.assert_called_once()
        args, kwargs = mock_mongo_client.call_args
        assert (
            "mongodb://testuser:testpass@mongo.example.com:27017/test_db?authSource=admin"
            == args[0]
        )
        assert "serverSelectionTimeoutMS" in kwargs
        assert "connectTimeoutMS" in kwargs

    @patch("modules.cache_vendors.cache_mongo.MongoClient")
    @patch("modules.cache_vendors.cache_mongo.CacheConfig")
    def test_connection_with_auth_custom_auth_db(self, mock_config, mock_mongo_client):
        """Test MongoDB connection with authentication using a custom auth database."""
        # Configure mocks
        mock_config_instance = MagicMock()
        mock_config_instance.CACHE_USERNAME = "testuser"
        mock_config_instance.CACHE_PASSWORD = "testpass"
        mock_config_instance.CACHE_HOST = "mongo.example.com"
        mock_config_instance.CACHE_PORT = "27017"
        mock_config_instance.CACHE_DATABASE = "test_db"
        mock_config_instance.CACHE_AUTH_DB = "auth_db"
        mock_config.return_value = mock_config_instance

        # Create mock client
        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client

        # Create MongoDB instance
        mongo = Mongo()
        assert mongo is not None

        # Assert connection string includes auth with custom auth db
        mock_mongo_client.assert_called_once()
        args, kwargs = mock_mongo_client.call_args
        assert (
            "mongodb://testuser:testpass@mongo.example.com:27017/test_db?authSource=auth_db"
            == args[0]
        )
        assert "serverSelectionTimeoutMS" in kwargs
        assert "connectTimeoutMS" in kwargs

    @patch("modules.cache_vendors.cache_mongo.MongoClient")
    @patch("modules.cache_vendors.cache_mongo.CacheConfig")
    def test_auth_failure(self, mock_config, mock_mongo_client):
        """Test handling of authentication failures."""
        # Configure mocks
        mock_config_instance = MagicMock()
        mock_config_instance.CACHE_USERNAME = "wronguser"
        mock_config_instance.CACHE_PASSWORD = "wrongpass"
        mock_config_instance.CACHE_HOST = "mongo.example.com"
        mock_config_instance.CACHE_PORT = "27017"
        mock_config_instance.CACHE_DATABASE = "test_db"
        mock_config_instance.CACHE_AUTH_DB = "admin"
        mock_config.return_value = mock_config_instance

        # Mock client that raises auth error
        mock_client = MagicMock()
        mock_client.admin.command.side_effect = OperationFailure(
            "Authentication failed"
        )
        mock_mongo_client.return_value = mock_client

        # Test that correct exception is raised
        with pytest.raises(GGBotCacheClientException) as exc_info:
            Mongo()

        assert "Authentication failed" in str(exc_info.value)

    @patch("modules.cache_vendors.cache_mongo.MongoClient")
    @patch("modules.cache_vendors.cache_mongo.CacheConfig")
    def test_connection_refused(self, mock_config, mock_mongo_client):
        """Test handling of connection failures."""
        # Configure mocks
        mock_config_instance = MagicMock()
        mock_config_instance.CACHE_HOST = "nonexistent.host"
        mock_config_instance.CACHE_PORT = "27017"
        mock_config_instance.CACHE_DATABASE = "test_db"
        mock_config_instance.CACHE_USERNAME = None
        mock_config.return_value = mock_config_instance

        # Mock client that raises connection error
        mock_client = MagicMock()
        mock_client.admin.command.side_effect = ConnectionFailure("Connection refused")
        mock_mongo_client.return_value = mock_client

        # Test that correct exception is raised
        with pytest.raises(GGBotCacheClientException) as exc_info:
            Mongo()

        assert "Connection refused" in str(exc_info.value)

    @patch("modules.cache_vendors.cache_mongo.MongoClient")
    @patch("modules.cache_vendors.cache_mongo.CacheConfig")
    def test_empty_username_treated_as_no_auth(self, mock_config, mock_mongo_client):
        """Test that empty username is treated as no auth."""
        # Configure mocks
        mock_config_instance = MagicMock()
        mock_config_instance.CACHE_USERNAME = ""  # Empty string
        mock_config_instance.CACHE_PASSWORD = "password"
        mock_config_instance.CACHE_HOST = "localhost"
        mock_config_instance.CACHE_PORT = "27017"
        mock_config_instance.CACHE_DATABASE = "test_db"
        mock_config.return_value = mock_config_instance

        # Create mock client
        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client

        # Create MongoDB instance
        mongo = Mongo()
        assert mongo is not None

        # Assert connection string doesn't have auth
        mock_mongo_client.assert_called_once()
        args, kwargs = mock_mongo_client.call_args
        assert "mongodb://localhost:27017/test_db" == args[0]
        assert "serverSelectionTimeoutMS" in kwargs
        assert "connectTimeoutMS" in kwargs

    @patch("modules.cache_vendors.cache_mongo.logging")
    @patch("modules.cache_vendors.cache_mongo.MongoClient")
    @patch("modules.cache_vendors.cache_mongo.CacheConfig")
    def test_successful_connection_logs_info(
        self, mock_config, mock_mongo_client, mock_logging
    ):
        """Test that successful connection logs information."""
        # Configure mocks
        mock_config_instance = MagicMock()
        mock_config_instance.CACHE_USERNAME = "testuser"
        mock_config_instance.CACHE_PASSWORD = "testpass"
        mock_config_instance.CACHE_HOST = "mongo.example.com"
        mock_config_instance.CACHE_PORT = "27017"
        mock_config_instance.CACHE_DATABASE = "test_db"
        mock_config_instance.CACHE_AUTH_DB = "admin"
        mock_config.return_value = mock_config_instance

        # Create mock client
        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client

        # Create MongoDB instance
        mongo = Mongo()
        assert mongo is not None

        # Assert proper logging calls
        assert mock_logging.info.call_count >= 2

        # Check for connection log
        has_connect_log = False
        has_success_log = False

        for call_args in mock_logging.info.call_args_list:
            args, _ = call_args
            if "Connecting to MongoDB with authentication" in args[0]:
                has_connect_log = True
            elif "Successfully connected to MongoDB" in args[0]:
                has_success_log = True

        assert has_connect_log, "Should log about connecting with auth"
        assert has_success_log, "Should log successful connection"
