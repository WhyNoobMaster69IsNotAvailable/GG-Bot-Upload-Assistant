# GG Bot Upload Assistant
# Copyright (C) 2022  Noob Master669

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

import json
import logging
import platform
import re
from pprint import pformat

import requests
import sentry_sdk
from fuzzywuzzy import fuzz
from guessit import guessit
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table

from modules.config import UploaderConfig
from modules.exceptions.exception import GGBotSentryCapturedException
from utilities.utils import GenericUtils
from utilities.utils_miscellaneous import MiscellaneousUtils

console = Console()


class DupeUtils:
    @staticmethod
    def _prepare_post_payload(
        search_site, imdb, tmdb, tvmaze, tracker_api, payload, upload_type, title
    ):
        # -------------------------------------------------------------------------
        # Temporary fix for BIT-HDTV
        # TODO: need to find a better solution for this.
        if search_site == "bit-hdtv":
            url_replacer = f"https://www.imdb.com/title/{imdb}"
            if upload_type == "episode":
                url_replacer = f"https://www.tvmaze.com/shows/{tvmaze}"
            url_dupe_payload = payload.replace("<imdb>", url_replacer).replace(
                "<title>", title
            )
        else:
            url_dupe_payload = (
                payload.replace("<imdb>", str(imdb))
                .replace("<tvmaze>", str(tvmaze))
                .replace("<tmdb>", str(tmdb))
                .replace("<api_key>", tracker_api)
                .replace("<title>", title)
            )
        # -------------------------------------------------------------------------
        return url_dupe_payload

    @staticmethod
    def _make_request(
        url,
        method,
        search_site,
        site_name,
        json_data=None,
        multipart_data=None,
        headers=None,
        cloudflare_bypass=False,
    ):
        try:
            if cloudflare_bypass:
                headers = headers if headers is not None else {}
                headers["User-Agent"] = "Apidog/1.0.0 (https://apidog.com)"
            return requests.request(
                method, url, json=json_data, data=multipart_data, headers=headers
            )
        except Exception as ex:
            console.print(
                f"[bold red]:warning: Dupe check request to tracker [green]{site_name}[/green], failed. Hence skipping this tracker. :warning:[/bold red]\n {ex}"
            )
            logging.exception(
                f"[DupeCheck] Request to  {search_site} for dupe check Failed. Error {ex}"
            )
            logging.info(
                "[DupeCheck] Skipping upload to tracker since the dupe check request failed. The tracker might not be responding, hence skipping upload."
            )
            return True

    @staticmethod
    def _get_response_from_wrapper(dupe_check_response_wrapper, search_site, site_name):
        try:
            return dupe_check_response_wrapper.json()
        except Exception as ex:
            logging.exception(
                f"[DupeCheck] Error while reading response from tracker {search_site} for dupe check. Error {ex}"
            )
            logging.fatal(
                f"[DupeCheck] Text data from tracker {search_site} for dupe check {pformat(dupe_check_response_wrapper)}"
            )
            console.print(
                f"[bold red]:warning:  Could not parse the dupe check response from tracker [green]{site_name}[/green], hence skipping this tracker. :warning:[/bold red]\n"
            )
            return True

    @staticmethod
    def _get_torrent_item(dupe_check_response, parse_json):
        torrent_items = dupe_check_response
        if parse_json["is_needed"]:
            if parse_json["top_lvl"] not in dupe_check_response:
                logging.error(
                    f"[DupeCheck] Unexpected response obtained from tracker. top_lvl item {parse_json['top_lvl']} is not present in dupe check response"
                )
                logging.debug(
                    "[DupeCheck] Dumping dupe check response:::::::::::::::::::::::::\n"
                )
                logging.debug(pformat(dupe_check_response))
                logging.info(
                    "[DupeCheck] Proceeding with the 'EXPECTATION' that 'NO DUPES' are present in tracker"
                )
                return []
            else:
                torrent_items = dupe_check_response[parse_json["top_lvl"]]
                if "second_level" in parse_json:
                    torrent_items = torrent_items[parse_json["second_level"]]
        return torrent_items

    @staticmethod
    def _combine_field_for_title(fields, torrent_details):
        torrent_title = ""
        for field in fields:
            if field not in torrent_details:
                logging.error(
                    f"[DupeCheck] Combine field `{field}` is not present in the obtained torrent details response"
                )
                continue

            if isinstance(torrent_details[field], list):
                for field_data in torrent_details[field]:
                    # well we don't need these components in the torrent title
                    if str(field_data) in ["Commentary"]:
                        continue
                    torrent_title = f"{torrent_title} {str(field_data)}"
            else:
                torrent_title = f"{torrent_title} {str(torrent_details[field])}"
        return torrent_title

    @staticmethod
    def _fill_existing_release_types_with_source_data(
        existing_release_types,
        torrent_title,
        torrent_title_split,
        torrent_title_upper_split,
    ):
        # Bluray Encode
        if (
            all(x in torrent_title_split for x in ["bluray"])
            and any(
                x in torrent_title_split for x in ["720p", "1080i", "1080p", "2160p"]
            )
            and any(
                x in torrent_title_split for x in ["x264", "x265", "x 264", "x 265"]
            )
        ):
            existing_release_types[torrent_title] = "bluray_encode"

        # Bluray Remux
        if all(x in torrent_title_split for x in ["bluray", "remux"]) and any(
            x in torrent_title_split for x in ["720p", "1080i", "1080p", "2160p"]
        ):
            existing_release_types[torrent_title] = "bluray_remux"

        # WEB-DL
        if (
            any(x in torrent_title_upper_split for x in ["WEB"])
            or all(x in torrent_title_split for x in ["web", "dl"])
        ) and (
            any(
                x in torrent_title_split
                for x in [
                    "h.264",
                    "h264",
                    "h 264",
                    "h.265",
                    "h265",
                    "h 265",
                    "hevc",
                    "x264",
                    "x265",
                    "x.264",
                    "x.265",
                    "x 264",
                    "x 265",
                ]
            )
            or all(x in torrent_title_split for x in ["h", "265"])
            or all(x in torrent_title_split for x in ["h", "264"])
        ):
            existing_release_types[torrent_title] = "webdl"

        # WEBRip
        if all(x in torrent_title_split for x in ["webrip"]) and (
            any(
                x in torrent_title_split
                for x in [
                    "h.264",
                    "h264",
                    "h 264",
                    "h.265",
                    "h265",
                    "h 265",
                    "hevc",
                    "x264",
                    "x265",
                    "x.264",
                    "x.265",
                    "x 264",
                    "x 265",
                ]
            )
            or all(x in torrent_title_split for x in ["h", "265"])
            or all(x in torrent_title_split for x in ["h", "264"])
        ):
            existing_release_types[torrent_title] = "webrip"

        # HDTV
        if all(x in torrent_title_split for x in ["hdtv"]):
            existing_release_types[torrent_title] = "hdtv"

        # DVD
        if all(x in torrent_title_split for x in ["dvd"]):
            existing_release_types[torrent_title] = "dvd"

        return existing_release_types

    @staticmethod
    def _fill_hdr_format_types(hdr_format_types, torrent_title, torrent_title_split):
        # HDR
        if any(
            x in torrent_title_split
            for x in ["hdr", "hdr10", "hdr10+", "hdr10plus", "pq10", "hlg", "wcg"]
        ):
            hdr_format_types["hdr"].append(torrent_title)

        # DV
        if any(
            x in torrent_title_split
            for x in ["dv", "dovi", "dolbyvision", "dolby_vision"]
        ):
            hdr_format_types["dv"].append(torrent_title)

        # Non-HDR
        if all(
            x not in torrent_title_split
            for x in [
                "dv",
                "dovi",
                "dolbyvision",
                "dolby_vision",
                "hdr",
                "hdr10",
                "hdr10+",
                "hdr10plus",
                "pq10",
                "hlg",
                "wcg",
            ]
        ):
            hdr_format_types["normal"].append(torrent_title)

        # DV HDR
        if any(
            x in torrent_title_split
            for x in ["dv", "dovi", "dolbyvision", "dolby_vision"]
        ) and any(
            x in torrent_title_split
            for x in ["hdr", "hdr10", "hdr10+", "hdr10plus", "pq10", "hlg", "wcg"]
        ):
            hdr_format_types["dv_hdr"].append(torrent_title)
        return hdr_format_types

    @staticmethod
    def _get_our_hdr_format(torrent_info):
        our_format = "normal"
        if "dv" in torrent_info and torrent_info["dv"] is not None:
            our_format = (
                "dv_hdr"
                if "hdr" in torrent_info and torrent_info["hdr"] is not None
                else "dv"
            )
        elif "hdr" in torrent_info and torrent_info["hdr"] is not None:
            our_format = "hdr"
        return our_format

    @staticmethod
    def _fuzzy_similarity(
        our_title,
        check_against_title,
        release_title,
        release_year,
        release_screen_size,
    ):
        check_against_title_original = check_against_title
        # We will remove things like the title & year from the comparison stings since we know they will be exact matches anyways

        # replace DD+ with DDP from both our title and tracker results title to make the dupe check a bit more accurate since some sites like to use DD+ and others DDP but they refer to the same thing
        our_title = re.sub(r"dd\+", "ddp", str(our_title).lower())
        check_against_title = re.sub(r"dd\+", "ddp", str(check_against_title).lower())

        content_title = re.sub("[^0-9a-zA-Z]+", " ", str(release_title).lower())

        if release_year is not None:
            # Also remove the year because that *should* be an exact match, that's not relevant to detecting changes
            if str(int(release_year) + 1) in check_against_title:
                # some releases are occasionally off by 1 year, it's still the same media so it can be used for dupe check
                check_against_title_year = str(int(release_year) + 1)
            elif str(int(release_year) - 1) in check_against_title:
                check_against_title_year = str(int(release_year) - 1)
            else:
                check_against_title_year = str(release_year)
        else:
            check_against_title_year = ""

        our_title = (
            re.sub(r"[^A-Za-z0-9 ]+", " ", str(our_title))
            .lower()
            .replace(release_screen_size, "")
            .replace(check_against_title_year, "")
        )
        our_title = " ".join(our_title.split())

        check_against_title = (
            re.sub(r"[^A-Za-z0-9 ]+", " ", str(check_against_title))
            .lower()
            .replace(release_screen_size, "")
            .replace(check_against_title_year, "")
        )
        check_against_title = " ".join(check_against_title.split())

        token_set_ratio = fuzz.token_set_ratio(
            our_title.replace(content_title, ""),
            check_against_title.replace(content_title, ""),
        )
        logging.info(
            f"[DupeCheck] '{check_against_title_original}' was flagged with a {str(token_set_ratio)}% dupe probability"
        )

        # Instead of wasting time trying to create a 'low, medium, high' risk system we just have the user enter in a percentage they are comfortable with
        # if a torrent titles vs local title similarity percentage exceeds a limit the user set we immediately quit trying to upload to that site
        # since what the user considers (via token_set_ratio percentage) to be a dupe exists
        return token_set_ratio

    def search_for_dupes_api(
        self,
        tracker,
        search_site,
        imdb,
        tmdb,
        tvmaze,
        torrent_info,
        tracker_api,
        config,
        auto_mode,
    ):
        is_repack_or_proper = torrent_info["repack"]
        logging.info(
            f"[DupeCheck] We currently are tying to upload a repack type: '{is_repack_or_proper}'. Non '{is_repack_or_proper}' release will be ignored during dupe check"
        )

        imdb = imdb.replace("tt", "") if config["dupes"]["strip_text"] else imdb
        url_dupe_payload = (
            None  # this is here just for the log, It's not technically needed
        )

        # multiple authentication modes
        headers = GenericUtils.prepare_headers_for_tracker(
            config["dupes"]["technical_jargons"], tracker, tracker_api
        )
        headers["User-Agent"] = (
            f"GG-Bot Upload Assistant/{UploaderConfig().VERSION} ({platform.system()} {platform.release()})"
        )

        if (
            str(config["dupes"]["technical_jargons"]["request_method"]) == "POST"
        ):  # POST request (BHD)
            url_dupe_search = str(config["torrents_search"]).format(api_key=tracker_api)
            url_dupe_payload = self._prepare_post_payload(
                search_site,
                imdb,
                tmdb,
                tvmaze,
                tracker_api,
                config["dupes"]["payload"],
                torrent_info["type"],
                torrent_info["title"],
            )

            logging.debug(
                f"[DupeCheck] Formatted POST payload {url_dupe_payload} for {search_site}"
            )
            url_dupe_payload = json.loads(url_dupe_payload)

            if (
                config["dupes"]["technical_jargons"]["authentication_mode"]
                == "API_KEY_PAYLOAD"
            ):
                # adding Authentication api_key to payload
                url_dupe_payload[
                    config["dupes"]["technical_jargons"]["auth_payload_key"]
                ] = tracker_api

            if (
                str(config["dupes"]["technical_jargons"]["payload_type"])
                == "URL-ENCODED"
            ):
                headers["Content-Type"] = "application/x-www-form-urlencoded"

            if str(config["dupes"]["technical_jargons"]["payload_type"]) == "JSON":
                dupe_check_result = self._make_request(
                    url=url_dupe_search,
                    method="POST",
                    search_site=search_site,
                    site_name=str(config["name"]).upper(),
                    json_data=url_dupe_payload,
                    headers=headers,
                )
                if dupe_check_result is True:
                    return True  # being pessimistic and assuming dupes exist in tracker
            else:
                dupe_check_result = self._make_request(
                    url=url_dupe_search,
                    method="POST",
                    search_site=search_site,
                    site_name=str(config["name"]).upper(),
                    multipart_data=url_dupe_payload,
                    headers=headers,
                    cloudflare_bypass=config["dupes"]["technical_jargons"].get(
                        "cloudflare_bypass", False
                    ),
                )
                if dupe_check_result is True:
                    return True  # being pessimistic and assuming dupes exist in tracker

        else:  # GET request (BLU & ACM)
            url_dupe_search = str(config["dupes"]["url_format"]).format(
                search_url=str(config["torrents_search"]).format(api_key=tracker_api),
                title=torrent_info["title"],
                imdb=imdb,
                tmdb=tmdb,
            )
            dupe_check_result = self._make_request(
                url=url_dupe_search,
                method="GET",
                search_site=search_site,
                site_name=str(config["name"]).upper(),
                headers=headers,
            )
            if dupe_check_result is True:
                return True  # being pessimistic and assuming dupes exist in tracker

        logging.info(
            f'[DupeCheck] Dupe search request | Method: {str(config["dupes"]["technical_jargons"]["request_method"])} | URL: {url_dupe_search} | Payload: {url_dupe_payload}'
        )

        if dupe_check_result.status_code != 200:
            logging.error(
                f"[DupeCheck] {search_site} returned the status code: {dupe_check_result.status_code}"
            )
            logging.error(
                f"[DupeCheck] Payload response from {search_site} {pformat(dupe_check_result)}"
            )
            logging.info(
                f"[DupeCheck] Dupe check for {search_site} failed, assuming no dupes and continuing upload"
            )
            return False

        # Now that we have the response from tracker(X) we can parse the json and try to identify dupes We first break
        # down the results into very basic categories like "remux", "encode", "web" etc and store the title + results here
        existing_release_types = {}
        existing_releases_count = {
            "bluray_encode": 0,
            "bluray_remux": 0,
            "webdl": 0,
            "webrip": 0,
            "hdtv": 0,
            "hdr": 0,
            "dv": 0,
            "dvd": 0,
        }  # We also log the num each type shows up on site
        # this list will have the list of titles that are 100% dupes.
        # if we are trying to upload a single episode and a season pack already exist, then the season pack is 100% dupe
        # similarly if a repack or a proper release is already on tracker, then that's 100% dupe
        cent_percent_dupes = {}
        single_episode_upload_with_season_pack_available = False
        # to handle torrents with HDR and DV, we keep a separate dictionary to keep tracker of hdr. non-hdr and dv
        # releases the reason to go for a separate map is that in `existing_release_types` the keys are torrent titles
        # and that is not possible for hdr based filtering note that for hdr filtering we are not bothered about the
        # different formats (PQ10, HDR, HLG etc.), Since it's rare to see a show release in multiple formats. although not
        # impossible. (moon knight had PQ10 and HDR versions)
        hdr_format_types = {"hdr": [], "dv_hdr": [], "dv": [], "normal": []}

        # adding support for speedapp. SpeedApp just returns the torrents as a json array.
        # for compatibility with other trackers a new flag is added named `is_needed` under `parse_json`
        # as the name indicates, it decides whether the `dupe_check_result` returned from the tracker
        # needs any further parsing.
        logging.debug(
            f'[DupeCheck] DupeCheck config for tracker `{search_site}` \n {pformat(config["dupes"])}'
        )
        dupe_check_response = self._get_response_from_wrapper(
            dupe_check_result, search_site, str(config["name"]).upper()
        )
        if dupe_check_response is True:
            return True

        torrent_items = self._get_torrent_item(
            dupe_check_response, config["dupes"]["parse_json"]
        )

        for item in torrent_items:
            if "torrent_details" in config["dupes"]["parse_json"]:
                # BLU & ACM have us go 2 "levels" down to get torrent info -->  [data][attributes][name] = torrent title
                torrent_details = item[
                    str(config["dupes"]["parse_json"]["torrent_details"])
                ]
            else:
                # BHD only has us go down 1 "level" to get torrent info --> [data][name] = torrent title
                torrent_details = item

            torrent_name_key = (
                config["dupes"]["parse_json"]["torrent_name"]
                if "torrent_name" in config["dupes"]["parse_json"]
                else "name"
            )
            try:
                torrent_title = str(torrent_details[torrent_name_key])
            except TypeError as e:
                # SentryDebug: Sending more details to sentry for debugging
                with sentry_sdk.new_scope() as scope:
                    scope.set_extra("torrent_details", torrent_details)
                    sentry_sdk.capture_exception(e)
                raise GGBotSentryCapturedException(e)
            # certain trackers (NOT ANTHELION) won't give the details as one field. In such cases, we can combine the
            # data from multiple fields to create the torrent name ourselves If the configured fields are not present
            # then, we'll log the errors and then just skip it.
            if (
                "combine_fields" in config["dupes"]["parse_json"]
                and config["dupes"]["parse_json"]["combine_fields"] is True
            ):
                if "fields" in config["dupes"]["parse_json"]:
                    torrent_title = self._combine_field_for_title(
                        config["dupes"]["parse_json"]["fields"], torrent_details
                    )
                else:
                    # well that's a bummer, you want to combine fields, but haven't given any fields.
                    # so we just continue with the `torrent_name_key` that we have constructed till now.
                    pass

            torrent_title_split = re.split(
                r"[.\s]",
                torrent_title.lower().replace("blu-ray", "bluray").replace("-", " "),
            )
            torrent_title_upper_split = re.split(
                r"[.\s]", torrent_title.replace("-", " ")
            )

            logging.debug(
                f"[DupeCheck] Dupe check torrent title obtained from tracker {search_site} is {torrent_title}"
            )
            logging.debug(f"[DupeCheck] Torrent title split {torrent_title_split}")
            logging.debug(
                f"[DupeCheck] Torrent title split {torrent_title_upper_split}"
            )

            existing_release_types = self._fill_existing_release_types_with_source_data(
                existing_release_types,
                torrent_title,
                torrent_title_split,
                torrent_title_upper_split,
            )
            hdr_format_types = self._fill_hdr_format_types(
                hdr_format_types, torrent_title, torrent_title_split
            )

        logging.debug(
            f"[DupeCheck] Existing release types identified from tracker {search_site} are {existing_release_types}"
        )
        logging.debug(
            f"[DupeCheck] Existing release types based on hdr formats identified from tracker {search_site} are {hdr_format_types}"
        )

        # This just updates a dict with the number of a particular "type" of release exists on site (e.g. "2
        # bluray_encodes" or "1 bluray_remux" etc.)
        for onsite_quality_type in existing_release_types.values():
            existing_releases_count[onsite_quality_type] += 1
        for hdr_format in hdr_format_types:
            existing_releases_count[hdr_format] = len(hdr_format_types[hdr_format])
        logging.info(
            msg=f"[DupeCheck] Results from initial dupe query (all resolution): {existing_releases_count}"
        )

        # If we get no matches when searching via IMDB ID that means this content hasn't been upload in any format,
        # no possibility for dupes
        if len(existing_release_types.keys()) == 0:
            logging.info(
                msg="[DupeCheck] Dupe query did not return any releases that we could parse, assuming no dupes exist."
            )
            console.print(
                f":heavy_check_mark: Yay! No dupes found on [bold]{str(config['name']).upper()}[/bold], continuing the upload process now\n"
            )
            return False

        our_format = self._get_our_hdr_format(torrent_info)

        logging.info(
            f'[DupeCheck] Eliminating releases based on HDR Format. We are trying to upload: "{our_format}". All other formats will be ignored.'
        )
        for item in hdr_format_types:
            if item != our_format:
                for their_title in hdr_format_types[item]:
                    if (
                        their_title in existing_release_types
                        and their_title not in hdr_format_types[our_format]
                    ):
                        their_title_type = existing_release_types[their_title]
                        existing_releases_count[their_title_type] -= 1
                        existing_release_types.pop(their_title)
                existing_releases_count[item] = 0
                hdr_format_types[item] = []

        logging.info(
            f'[DupeCheck] After applying "HDR Format" filter: {existing_releases_count}'
        )

        our_title_guessit = guessit(torrent_info["torrent_title"])
        logging.debug(
            "::::::::::::::::::::::::::::: OUR GuessIt output result :::::::::::::::::::::::::::::"
        )
        logging.debug(f"\n{pformat(our_title_guessit)}")

        logging.debug(
            f'[DupeCheck] Uploading media properties ==> Resolution :: {torrent_info["screen_size"]}, Source ::: {torrent_info["source_type"]}'
        )
        logging.debug(
            "[DupeCheck] Filtering torrents from tracker that doesn't match the above properties"
        )
        # --------------- Filter the existing_release_types dict to only include correct res & source_type --------------- #
        # we wrap the dict keys in a "list()" so we can modify (pop) keys from it while the loop is running below
        for their_title in list(existing_release_types.keys()):
            # use guessit to get details about the release
            their_title_guessit = guessit(their_title)
            their_title_type = existing_release_types[their_title]

            logging.debug(
                "::::::::::::::::::::::::::::: THEIR GuessIt output result :::::::::::::::::::::::::::::"
            )
            logging.debug(f"\n{pformat(their_title_guessit)}")

            # elimination condition
            #   If resolution doesn't match then we can remove items
            logging.debug(
                f'[DupeCheck] Uploading media properties ==> Resolution :: {torrent_info["screen_size"]}, Source ::: {torrent_info["source_type"]}'
            )
            logging.debug(
                f'[DupeCheck] Checking media properties ==> Resolution :: {their_title_guessit["screen_size"] if "screen_size" in their_title_guessit else None}, Source ::: {their_title_type}'
            )

            # This next if statement does 2 things:
            #   1. If the torrent title from the API request doesn't have the same resolution as the file being uploaded we pop (remove) it from the dict "existing_release_types"
            #   2. If the API torrent title source type (e.g. bluray_encode) is not the same as the local file then we again pop it from the "existing_release_types" dict
            if (
                "screen_size" not in their_title_guessit
                or their_title_guessit["screen_size"] != torrent_info["screen_size"]
            ) or their_title_type != torrent_info["source_type"]:
                existing_releases_count[their_title_type] -= 1
                existing_release_types.pop(their_title)
                logging.debug(
                    f"[DupeCheck] Removing {their_title} since it failed `screen_size` and `source_type` filters"
                )
                continue  # if an item has been removed from the list at any point then there is no need to apply further checks

            # elimination conditiaon
            #   If audio codec doesn't match then we need to compare the audio channels. If our channel is better then we can remove item from list
            #       If 2.0 is already on tracker then we can upload 5.1 or 7.1 channels as these torrents will trump the lower channel releases
            logging.debug(
                f'[DupeCheck] Uploading media properties ==> Audio Channels :: {torrent_info["audio_channels"]}, Audio Codec ::: {torrent_info["audio_codec"]}'
            )
            logging.debug(
                f'[DupeCheck] Checking media properties ==> Audio Channels :: {their_title_guessit["audio_channels"] if "audio_channels" in their_title_guessit else None}'
            )

            # if audio channels is not present in their title then we cannot eliminate it.
            if (
                "audio_channels" in their_title_guessit
                and their_title_guessit["audio_channels"]
                != torrent_info["audio_channels"]
            ):
                # there is a mismatch in the audio channels, we can mark that as a possible dupe
                their_channels = their_title_guessit["audio_channels"]
                our_channels = torrent_info["audio_channels"]
                # 5.1 and 2.0 => comparing the channels
                if float(our_channels[0]) > float(their_channels[0]):
                    # if we have more channels than their release, then we can treat that as not a dupe.
                    existing_releases_count[their_title_type] -= 1
                    existing_release_types.pop(their_title)
                    logging.debug(
                        f"[DupeCheck] Removing {their_title} since it failed `audio_channels` filter"
                    )
                    continue
            # TODO implement this after comparing with lots of titles and samples
        logging.info(
            f'[DupeCheck] After applying "resolution", "source_type"," audio_channels" filter: {existing_releases_count}'
        )

        # next we are going to consider repack during dupe check.
        # 1. If we have a repack,
        #   1.a then non-repack releases on tracker is not conisdered for dupe check
        #   1.b if there is a repack, then we need to do further checks.
        #       1.b.a If and tracker torrent both are same (REPACK and REPACK) then that's a dupe.
        #       1.b.b If its different, we check whether the repacks are REPACK, RERIP or PROPER. (a simple starts with should do the trick)
        #           1.b.b.a If ours and theirs are different then we will consider their release as a dupe (being pessimistic).
        #                   We cannot say with certainty that that a RERIP is better than REPACK.
        #       1.b.c Next we check whether our_repack and their_repack ends with a digit (REPACK1, REPACK2 etc)
        #           1.b.c.a If we have a higher number than that on tracker, then can proceed to upload, and remove their from possible dupe
        #           1.b.c.b If we have a lower number then we cannot upload
        #           1.b.c.c The case when both are same will be handled in step 1.b.a
        # 2. If we don't have a repack,
        #   2.a and there are repacks on tracker then, we CANNOT upload our torrent
        #   2.b if there are no repacks on tracker, then we need to consider then for dupe check
        logging.info(
            f"[DupeCheck] We currently are tying to upload a repack type: '{is_repack_or_proper}'. Trying to eliminate releases based on repack/proper."
        )
        for onsite_title in list(existing_release_types.keys()):
            their_is_repack_or_proper = MiscellaneousUtils.identify_repacks(
                onsite_title
            )
            # if we have a repack
            if is_repack_or_proper is not None:
                if their_is_repack_or_proper is None:  # 1.a
                    logging.debug(
                        f"[DupeCheck] On site release '{onsite_title}' is not proper or repack. Hence not considering this as a dupe."
                    )
                    existing_releases_count[existing_release_types[onsite_title]] -= 1
                    existing_release_types.pop(onsite_title)
                elif their_is_repack_or_proper == is_repack_or_proper:  # 1.b.a
                    logging.debug(
                        f"[DupeCheck] Repack/Proper match found for on site release '{onsite_title}'"
                    )
                else:
                    # check for RERIP, PROPER and REPACK, then compare the digits at the end if present
                    # we just check whether the first 5 characters are the same. if same then we'll continue with other check
                    # otherwise we mark this as 100% dupe
                    if their_is_repack_or_proper[:5] != is_repack_or_proper[:5]:
                        logging.debug(
                            f"[DupeCheck] {their_is_repack_or_proper} found on tracker '{onsite_title}'. We want to upload '{is_repack_or_proper}'. This is 100% a dupe"
                        )
                        cent_percent_dupes[onsite_title] = (
                            f"{their_is_repack_or_proper} already exits"
                        )
                    logging.info(
                        f"[DupeCheck] We got a repack/proper from on site release '{onsite_title}' as '{their_is_repack_or_proper}'. But it doesn't match with our format of '{is_repack_or_proper}'"
                    )
                    # now lets check for REPACK2, 3 4 etc
                    # if the string ends in digits their_repack_end_digit and repack_end_digit will be a Match object, or None otherwise.
                    their_repack_end_digit = re.search(
                        r"\d+$", their_is_repack_or_proper
                    )
                    repack_end_digit = re.search(r"\d+$", is_repack_or_proper)
                    if (
                        repack_end_digit is not None
                    ):  # we have REPACK? => where ? could be any integer
                        if their_repack_end_digit is not None:
                            # they have REPACK? => where ? could be any integer
                            # eg: we have
                            #   Bosch.Legacy.S01E04.1080p.REPACK2.AMZN.WEB-DL.DDP5.1.H.264-NTb.mkv
                            # while they have
                            #   Bosch.Legacy.S01E04.1080p.REPACK3.AMZN.WEB-DL.DDP5.1.H.264-NTb.mkv
                            # since we both have numerical repacks lets compare the digits. If we have a higher number then we can upload. else we cannot
                            if int(repack_end_digit.group()) > int(
                                their_repack_end_digit.group()
                            ):  # 1.b.c.a
                                # we have higher repack
                                logging.debug(
                                    f"[DupeCheck] On site release '{onsite_title}' is older proper or repack. Hence not considering this as a dupe."
                                )
                                existing_releases_count[
                                    existing_release_types[onsite_title]
                                ] -= 1
                                existing_release_types.pop(onsite_title)
                            else:  # 1.b.c.b
                                logging.debug(
                                    f"[DupeCheck] Possible higher repack/proper found on tracker '{onsite_title}'. This is a possible dupe"
                                )
                        else:  # 1.b.c.a
                            logging.debug(
                                f"[DupeCheck] On site release '{onsite_title}' is not latest proper or repack. Hence not considering this as a dupe."
                            )
                            existing_releases_count[
                                existing_release_types[onsite_title]
                            ] -= 1
                            existing_release_types.pop(onsite_title)
                    elif (
                        their_repack_end_digit is not None
                    ):  # they have a number in repack and we don't
                        # they have REPACK? => where ? could be any integer
                        # since they have a possible updated repack, their is not point in uploading our version
                        # eg: we have
                        #   Bosch.Legacy.S01E04.1080p.REPACK.AMZN.WEB-DL.DDP5.1.H.264-NTb.mkv
                        # while they have
                        #   Bosch.Legacy.S01E04.1080p.REPACK2.AMZN.WEB-DL.DDP5.1.H.264-NTb.mkv
                        logging.debug(
                            f"[DupeCheck] Possible higher repack/proper found on tracker '{onsite_title}'. This is 100% a dupe"
                        )
                        cent_percent_dupes[onsite_title] = (
                            "Latest repack/proper release"
                        )
                        # once 100% dupe marking is enabled, this case can also be handled similarly
                    else:
                        # no digits for both parties. Ideally this case should not be happening as it will be handled in previous cases.
                        # thus we just log this and continue
                        logging.debug(
                            f"[DupeCheck] Well this shouldn't be happening. => Our: '{is_repack_or_proper}'  =>  Their: '{their_is_repack_or_proper}'"
                        )
            else:  # we don't have a repack
                if (
                    their_is_repack_or_proper is not None
                ):  # 2.b no repack. Consider for dupe check
                    logging.debug(
                        f"[DupeCheck] Repack / proper already exists on tracker '{onsite_title}'. This is 100% a dupe"
                    )
                    cent_percent_dupes[onsite_title] = "Repack/proper already exists"

        logging.info(
            f'[DupeCheck] After applying "REPACK/PROPER" filter: {existing_releases_count}'
        )

        # Movies (mostly blurays) are usually a bit more flexible with dupe/trump rules due to editions, regions, etc
        # TV Shows (mostly web) are usually only allowed 1 "version" onsite & we also need to consider individual episode uploads when a season pack exists etc
        # for those reasons ^^ we place this dict here that we will use to generate the Table we show the user of possible dupes
        # By keeping it out of the fuzzy_similarity() func/loop we are able to directly insert/modify data into it when dealing with tv show dupes/trumps below
        possible_dupe_with_percentage_dict = {}

        # If we are uploading a tv show we should only add the correct season to the existing_release_types dict
        if "s00e00" in torrent_info:
            # First check if what the user is uploading is a full season or not
            # We just want the season of whatever we are uploading so we can filter the results later
            # (Most API requests include all the seasons/episodes of a tv show in the response, we don't need all of them)
            is_full_season = bool(len(torrent_info["s00e00"]) == 3)
            if is_full_season:  # This is a full season
                season_num = str(torrent_info["s00e00"])
                episode_num = None
            else:
                # This is an episode (since a len of 3 would only leave room for 'S01' not 'S01E01' etc)
                season_num = str(torrent_info["s00e00"])[:-3]
                episode_num = str(torrent_info["s00e00"])[3:]
            logging.info(
                f"[DupeCheck] Filtering out results that are not from the same season being uploaded ({season_num})"
            )
            logging.debug(
                f'[DupeCheck] We have extracted the following from `torrent_info`. season_num: "{season_num}" and episode_num: "{episode_num}"'
            )

            # Loop through the results & discard everything that is not from the correct season
            number_of_discarded_seasons = 0
            # process of elimination
            for existing_release_types_key in list(existing_release_types.keys()):
                logging.debug(
                    f"[DupeCheck] Trying to eliminate `{existing_release_types_key}`"
                )
                if (
                    season_num is not None
                    and season_num not in existing_release_types_key
                ):  # filter our wrong seasons
                    logging.debug(
                        f"[DupeCheck] Filtering out `{existing_release_types_key}` since it belongs to different season"
                    )
                    existing_release_types.pop(existing_release_types_key)
                    number_of_discarded_seasons += 1
                    continue

                # at this point we've filtered out all the different resolutions/types/seasons
                # so now we check each remaining title to see if its a season pack or individual episode
                # endswith case added below to prevent failures when dealing with complete packs on trackers.
                # for most cases the first check of startswith itself will return true to get the season.
                logging.debug(
                    "[DupeCheck] Checking each remaining title to see if its a season pack or individual episode"
                )
                extracted_season_episode_from_title = list(
                    filter(
                        lambda x: x.startswith(season_num) or x.endswith(season_num),
                        re.split(r"[.\s]", existing_release_types_key),
                    )
                )[0]
                if len(extracted_season_episode_from_title) == 3:
                    logging.info(
                        f"[DupeCheck] Found a season pack for {season_num} on {search_site}"
                    )
                    # If a full season pack is onsite then in almost all cases individual episodes from that season are not allowed to be uploaded anymore
                    # check to see if that's ^^ happening, if it is then we will log it and if 'auto_mode' is enabled we also cancel the upload
                    # if 'auto_mode=false' then we prompt the user & let them decide
                    if not is_full_season:
                        if auto_mode:
                            # possible_dupe_with_percentage_dict[existing_release_types_key] = 100
                            logging.critical(
                                f"[DupeCheck] Canceling upload to {search_site} because uploading a full season pack is already available: {existing_release_types_key}"
                            )
                            return True
                        logging.error(
                            "[DupeCheck] Marking existence of season pack for single episode upload."
                        )
                        # marking this case when user is trying to upload a single episode when a season pack already exists on the tracker.
                        # when this flag is enabled, we'll show all the season packs in a table and prompt the user to decide whether or not to upload the torrent.
                        single_episode_upload_with_season_pack_available = True
                        cent_percent_dupes[existing_release_types_key] = (
                            "Season pack available"
                        )

                # now we just need to make sure the episode we're trying to upload is not already on site
                if not single_episode_upload_with_season_pack_available:
                    number_of_discarded_episodes = 0
                    if (
                        extracted_season_episode_from_title != torrent_info["s00e00"]
                    ) or (
                        episode_num is not None
                        and episode_num not in existing_release_types_key
                    ):
                        number_of_discarded_episodes += 1
                        existing_release_types.pop(existing_release_types_key)

                    logging.info(
                        f"[DupeCheck] Filtered out: {number_of_discarded_episodes} results for having different episode numbers (looking for {episode_num})"
                    )

            logging.info(
                f"[DupeCheck] Filtered out: {number_of_discarded_seasons} results for not being the right season ({season_num})"
            )

        uploader_config = UploaderConfig()
        possible_dupes_table = Table(show_header=True, header_style="bold cyan")
        possible_dupes_table.add_column(
            f"Exceeds Max % ({uploader_config.DUPE_CHECK_SIMILARITY_THRESHOLD}%)",
            justify="left",
        )
        possible_dupes_table.add_column(
            f"Possible Dupes ({str(config['name']).upper()})", justify="left"
        )
        possible_dupes_table.add_column("Similarity %", justify="center")
        possible_dupes_table.add_column("Dupe Reason", justify="center")

        max_dupe_percentage_exceeded = False
        is_dupes_present = False
        logging.debug(
            f"[DupeCheck] Existing release types that are dupes: {existing_release_types}"
        )
        for possible_dupe_title in existing_release_types:
            # If we get a match then run further checks
            if possible_dupe_title in cent_percent_dupes:
                possible_dupe_with_percentage_dict[possible_dupe_title] = 100
            else:
                possible_dupe_with_percentage_dict[possible_dupe_title] = (
                    self._fuzzy_similarity(
                        our_title=torrent_info["torrent_title"],
                        check_against_title=possible_dupe_title,
                        release_title=torrent_info["title"],
                        release_year=torrent_info.get("year", None),
                        release_screen_size=torrent_info["screen_size"],
                    )
                )

        for possible_dupe in sorted(
            possible_dupe_with_percentage_dict,
            key=possible_dupe_with_percentage_dict.get,
            reverse=True,
        ):
            mark_as_dupe = bool(
                possible_dupe_with_percentage_dict[possible_dupe]
                >= uploader_config.DUPE_CHECK_SIMILARITY_THRESHOLD
            )
            mark_as_dupe_color = "bright_red" if mark_as_dupe else "dodger_blue1"
            mark_as_dupe_percentage_difference_raw_num = (
                possible_dupe_with_percentage_dict[possible_dupe]
                - uploader_config.DUPE_CHECK_SIMILARITY_THRESHOLD
            )
            mark_as_dupe_percentage_difference = f'{"+" if mark_as_dupe_percentage_difference_raw_num >= 0 else "-"}{abs(mark_as_dupe_percentage_difference_raw_num)}%'

            possible_dupes_table.add_row(
                f"[{mark_as_dupe_color}]{mark_as_dupe}[/{mark_as_dupe_color}] ({mark_as_dupe_percentage_difference})",
                possible_dupe,
                f"{str(possible_dupe_with_percentage_dict[possible_dupe])}%",
                cent_percent_dupes[possible_dupe]
                if possible_dupe in cent_percent_dupes
                else "---",
            )

            # because we want to show the user every possible dupe (not just the ones that exceed the max percentage)
            # we just mark an outside var True & finish the for loop that adds the table rows
            #
            # Also if `single_episode_upload_with_season_pack_available`, then we mark the release as dupe
            if single_episode_upload_with_season_pack_available:
                max_dupe_percentage_exceeded = True
            elif not max_dupe_percentage_exceeded:
                max_dupe_percentage_exceeded = mark_as_dupe
            is_dupes_present = True

        if max_dupe_percentage_exceeded:
            console.print(
                "\n\n[bold red on white] :warning: Detected possible dupe! :warning: [/bold red on white]"
            )
            console.print(possible_dupes_table)

            if single_episode_upload_with_season_pack_available:
                # if this is an interactive upload then we can prompt the user & let them choose if they want to cancel or continue the upload
                logging.error(
                    "[DupeCheck] Almost all trackers don't allow individual episodes to be uploaded after season pack is released"
                )
                console.print(
                    "\n[bold red on white] :warning: Need user input! :warning: [/bold red on white]"
                )
                console.print(
                    f"You're trying to upload an [bold red]Individual Episode[/bold red] [bold green]({torrent_info['title']} {torrent_info['s00e00']})[/bold green] to [bold]{search_site}[/bold]",
                    highlight=False,
                )
                console.print(
                    f"[bold red]Season Packs[/bold red] are already available: [bold green]({existing_release_types_key})[/bold green]",
                    highlight=False,
                )
                console.print(
                    "Most sites [bold red]don't allow[/bold red] individual episode uploads when the season pack is available"
                )
                console.print(
                    "---------------------------------------------------------"
                )
                # If auto_mode is enabled then return true in all cases
                # If user chooses Yes / y => then we return False indicating that there are no dupes and processing can continue
                # If user chooses no / n => then we return Trueretu indicating that there are possible duplicates and stop the upload for the tracker
                return (
                    True
                    if auto_mode
                    else not bool(Confirm.ask("\nIgnore and continue upload?"))
                )
            else:
                # If auto_mode is enabled then return true in all cases
                # If user chooses Yes / y => then we return False indicating that there are no dupes and processing can continue
                # If user chooses no / n => then we return True indicating that there are possible duplicates and stop the upload for the tracker
                return (
                    True
                    if auto_mode
                    else not bool(
                        Confirm.ask("\nContinue upload even with possible dupe?")
                    )
                )
        else:
            if is_dupes_present:
                console.print(
                    "\n\n    [bold red] :warning:  Possible dupes ignored since threshold not exceeded! :warning: [/bold red]"
                )
                console.print(possible_dupes_table)
                console.line(count=2)
                console.print(
                    f":heavy_check_mark: Yay! No dupes identified on [bold]{str(config['name']).upper()}[/bold] that exceeds the configured threshold, continuing the upload process now\n"
                )
            else:
                console.print(
                    f":heavy_check_mark: Yay! No dupes identified on [bold]{str(config['name']).upper()}[/bold], continuing the upload process now\n"
                )

            return False  # no dupes proceed with processing
