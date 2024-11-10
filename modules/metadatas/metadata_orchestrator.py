import logging
from typing import List, Optional

from modules.metadatas import GGBotExternalDbMetadata, GGBotMetadataOrchestratorRequest
from modules.metadatas.providers import (
    GGBotMetadataProviderBase,
    GGBotMetadataApiResponse,
)
from modules.metadatas.providers.imdb import IMDBMetadataProvider
from modules.metadatas.providers.mal import MALMetadataProvider
from modules.metadatas.providers.tmdb import TMDBMetadataProvider
from modules.metadatas.providers.tvdb import TVDBMetadataProvider
from modules.metadatas.providers.tvmaze import TvMazeMetadataProvider
from modules.utils import ContentType, MetadataProvider


class GGBotExternalDBMetadataOrchestrator:
    metadata_provider_list: [
        TMDBMetadataProvider,
        TVDBMetadataProvider,
        TvMazeMetadataProvider,
        IMDBMetadataProvider,
        MALMetadataProvider,
    ]

    def __init__(self, auto_mode: bool = False):
        self.metadata_providers: List[GGBotMetadataProviderBase] = [
            provider(auto_mode=auto_mode) for provider in self.metadata_provider_list
        ]

    def _enabled_metadata_providers(self) -> List[GGBotMetadataProviderBase]:
        return [provider for provider in self.metadata_providers if provider.is_enabled]

    @staticmethod
    def _get_external_db_metadata_with_user_ids_filled(
        metadata_ids: GGBotMetadataOrchestratorRequest,
    ) -> GGBotExternalDbMetadata:
        external_db_metadata = GGBotExternalDbMetadata()
        # Filling the metadata with user provided arguments.
        for provider, meta_id in metadata_ids:
            # check list contains element and check whether the first element is not blank
            if len(meta_id) == 0 or len(meta_id[0]) == 0:
                continue
            external_db_metadata.set_metadata_id(provider, meta_id[0])
        return external_db_metadata

    def get_metadata_for_upload(
        self,
        orchestrator_request: GGBotMetadataOrchestratorRequest,
        content_type: ContentType,
    ) -> GGBotExternalDbMetadata:
        external_db_metadata = self._get_external_db_metadata_with_user_ids_filled(
            orchestrator_request
        )
        search_response: Optional[GGBotMetadataApiResponse] = None
        if external_db_metadata.all_ids_filled():
            # all ids have been provided by the user. We can proceed with user provided value and skip all searches
            pass
        elif external_db_metadata.all_ids_missing():
            # none of the ids could be obtained from user input or mediainfo.
            # We need to search different databases to get a match.
            search_response = self._search_metadata_and_get_matches(
                orchestrator_request, content_type
            )

        self._fill_missing_ids(
            search_response=search_response,
            external_db_metadata=external_db_metadata,
            content_type=content_type,
        )
        # some ids are filled
        # now with the ids that we have, we need to fill in other ids, and metadata from each provider

        logging.info(
            f"[GGBotExternalDBMetadataOrchestrator] We have {external_db_metadata.filled_providers()} with us currently."
        )
        logging.info(
            f"[GGBotExternalDBMetadataOrchestrator] We are missing {external_db_metadata.missing_providers()} starting External Database API requests now"
        )

        # ----------------------------------------
        # Priority Order
        # 1 => Ids from Mediainfo TODO: For now this is extracted from mediainfo and set in the args.
        # 2 => Ids provided by user
        # 3 => Ids that are resolved by uploader
        # ----------------------------------------
        # First if any of the ids are available to us either from media info or user provided details,
        # we use them to resolve the other ids.
        # After this resolution we will try to get the missing ids
        # ----------------------------------------
        # External Ids calls
        # IMDB > TMDB > TVMAZE
        # ----------------------------------------
        # To get imdb id:   we need tmdb id or tvmaze
        # to get tmdb id:   we need imdb id or tvdb id
        # to get tvmaze id: we need imdb id or tvdb id
        # to get tvdb id:   we need imdb id or tmdb id or tvmaze id

        # with imdb id      we can get tmdb id and tvmaze id and tvdb id
        # with tmdb id      we can get imdb id and tvdb id
        # with tvmaze id    we can get imdb id and tvdb id
        # with tvdb id      we can get tmdb id
        return external_db_metadata

    def _search_metadata_and_get_matches(
        self,
        orchestrator_request: GGBotMetadataOrchestratorRequest,
        content_type: ContentType,
    ) -> GGBotMetadataApiResponse:
        # here we'll search each of the searchable metadata providers until we find a match.
        for provider in self._enabled_metadata_providers():
            if (
                provider.is_searchable is False
                or content_type not in provider.supported_content_types
            ):
                # if we cannot search for titles using this provider or
                # if the content type is not supported by the provider we skip it.
                continue

            api_response: GGBotMetadataApiResponse = provider.search(
                title=orchestrator_request.title,
                year=orchestrator_request.year,
                content_type=content_type,
            )
            if api_response.is_failure():
                continue

            processed_response = provider.process_search_results(
                api_response=api_response, content_type=content_type
            )
            return processed_response
        return GGBotMetadataApiResponse.empty(
            metadata_provider=self._enabled_metadata_providers()[0].metadata_provider
        )

    def _fill_missing_ids(
        self,
        *,
        search_response: Optional[GGBotMetadataApiResponse],
        external_db_metadata: GGBotExternalDbMetadata,
        content_type: ContentType,
    ):
        if search_response is not None:
            pass
        else:
            ids_missing_provider = external_db_metadata.missing_providers()
            ids_available_provider = external_db_metadata.filled_providers()

            for available_provider in ids_available_provider:
                provider: Optional[GGBotMetadataProviderBase] = (
                    self._get_provider_impl_if_enabled(available_provider)
                )
                if provider is None:
                    continue

                resolvable_ids: List[MetadataProvider] = (
                    self._get_missing_ids_resolvable_by_provider(
                        ids_missing_provider, provider
                    )
                )

                for metadata_id in resolvable_ids:
                    pass
                    # Commenting the below code for ruff githook
                    # api_response = provider.resolve_external_ids(
                    #     content_type=content_type,
                    #     db_id=external_db_metadata.get_metadata_id(available_provider),
                    # )

    @staticmethod
    def _get_missing_ids_resolvable_by_provider(
        ids_missing_provider: List[MetadataProvider],
        provider: GGBotMetadataProviderBase,
    ) -> List[MetadataProvider]:
        return [
            resolvable_id
            for resolvable_id in provider.resolvable_external_ids
            if resolvable_id in ids_missing_provider
        ]

    def _get_provider_impl_if_enabled(
        self, provider: MetadataProvider
    ) -> Optional[GGBotMetadataProviderBase]:
        provider = [
            enabled_provider
            for enabled_provider in self._enabled_metadata_providers()
            if enabled_provider.metadata_provider == provider
        ]
        return provider[0] if len(provider) > 0 else None


if __name__ == "__main__":
    orchestrator_request = GGBotMetadataOrchestratorRequest()
    GGBotExternalDBMetadataOrchestrator().get_metadata_for_upload(
        orchestrator_request=orchestrator_request, content_type=ContentType.MOVIE
    )
