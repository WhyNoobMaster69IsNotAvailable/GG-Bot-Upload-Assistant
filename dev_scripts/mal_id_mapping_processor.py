import requests
from typing import Dict, Any
import json


class AnimeListIdMapper:
    github_url = "https://raw.githubusercontent.com/Fribb/anime-lists/master/anime-list-full.json"
    output_file_name = "parameters/mal_mapping/PROVIDER_ID_to_mal_mapping.json"

    def prepare_mal_id_mapping(self, write_to_file=False):
        raw_mapping = self._download_latest_mapping()
        processed_mapping = self._prepare_mapping_structure(raw_mapping)
        if write_to_file:
            self._write_to_file(processed_mapping)
        return processed_mapping

    def _write_to_file(self, mapping):
        print("Persisting processed mapping...")
        for provider, mapping in mapping.items():
            with open(
                self.output_file_name.replace("PROVIDER_ID", provider), "w"
            ) as output_file:
                json.dump(mapping, output_file)

    def _download_latest_mapping(self):
        print("Downloading latest mapping...")
        response = requests.get(self.github_url)
        if response.status_code != 200:
            print("Failed to download latest mapping")
            print(
                f"Status Code:: {response.status_code} => Response Text:: {response.text}"
            )
            return
        print("Successfully downloaded latest mapping...")
        return response.text

    def _prepare_mapping_structure(
        self, raw_mapping
    ) -> Dict[str, Dict[Any, Any]]:
        print("Processing latest mapping...")
        anime_list = json.loads(raw_mapping)
        id_to_mal_mapping = {}
        tmdb_to_mal_mapping = {}
        imdb_to_mal_mapping = {}
        tvdb_to_mal_mapping = {}

        for anime in anime_list:
            mal_id = anime.get("mal_id")
            if mal_id is None:
                continue
            mal_id = str(mal_id)

            themoviedb_id = anime.get("themoviedb_id")
            thetvdb_id = anime.get("thetvdb_id")
            imdb_id = anime.get("imdb_id")

            id_to_mal_mapping[mal_id] = mal_id
            if themoviedb_id:
                tmdb_to_mal_mapping[themoviedb_id] = mal_id
            if thetvdb_id:
                tvdb_to_mal_mapping[thetvdb_id] = mal_id
            if imdb_id:
                imdb_to_mal_mapping[imdb_id] = mal_id

        print("Successfully finished processing latest mapping...")
        return {
            "mal": id_to_mal_mapping,
            "tmdb": tmdb_to_mal_mapping,
            "imdb": imdb_to_mal_mapping,
            "tvdb": tvdb_to_mal_mapping,
        }


if __name__ == "__main__":
    AnimeListIdMapper().prepare_mal_id_mapping(True)
