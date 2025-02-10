import pytest
from qbittorrentapi import Unauthorized401Error

from modules.exceptions.exception import GGBotSentryCapturedException
from modules.sentry_config import SentryConfig


class TestSentryConfig:
    @pytest.fixture
    def sentry_config(self):
        yield SentryConfig()

    def test_sentry_ignored_errors(self):
        expected_ignored_errors = [
            AssertionError,
            Unauthorized401Error,
            GGBotSentryCapturedException,
        ]
        assert SentryConfig.sentry_ignored_errors() == expected_ignored_errors
