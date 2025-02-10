from typing import Union, Sequence

from qbittorrentapi import Unauthorized401Error

from modules.exceptions.exception import GGBotSentryCapturedException

ignored_log_lines = ["Outdated config.env file"]


class SentryConfig:
    @staticmethod
    def sentry_ignored_errors() -> Sequence[Union[type, str]]:
        return [
            AssertionError,
            Unauthorized401Error,
            GGBotSentryCapturedException,
        ]

    @staticmethod
    def before_send(event, hint):
        if any(log_line in str(event) for log_line in ignored_log_lines):
            return None
        return event
