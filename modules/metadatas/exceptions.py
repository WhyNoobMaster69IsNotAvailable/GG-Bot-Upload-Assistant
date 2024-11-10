from modules.exceptions.exception import GGBotUploaderException


class GGBotMetadataSearchFailureException(GGBotUploaderException):
    def __init__(self, provider: str, message: str):
        super().__init__(f"Failed to fetch metadata from {provider}. Error: {message}")
