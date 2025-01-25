from qbittorrentapi import Unauthorized401Error

from modules.exceptions.exception import GGBotSentryCapturedException

sentry_ignored_errors = [
    AssertionError,
    Unauthorized401Error,
    GGBotSentryCapturedException,
]
