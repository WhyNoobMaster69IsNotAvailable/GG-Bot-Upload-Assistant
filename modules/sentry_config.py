from typing import Union, Sequence

from qbittorrentapi import Unauthorized401Error

from modules.exceptions.exception import GGBotSentryCapturedException


class SentryConfig:
    @staticmethod
    def sentry_ignored_errors() -> Sequence[Union[type, str]]:
        return [
            AssertionError,
            Unauthorized401Error,
            GGBotSentryCapturedException,
        ]
