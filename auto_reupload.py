#!/usr/bin/env python3

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

import base64
import glob
import json
import logging
import os
import re
from datetime import datetime
from pprint import pformat
from typing import Dict, Tuple, Any, Union

# These packages need to be installed
import requests
import schedule
import sentry_sdk
from dotenv import load_dotenv
from pymediainfo import MediaInfo

# Rich is used for printing text & interacting with user input
from rich import box
from rich.console import Console
from rich.table import Table
from rich.traceback import install

import utilities.utils_metadata as metadata_utilities
from modules.constants import (
    COOKIES_DUMP_DIR,
    REUPLOADER_LOG,
    REUPLOADER_CONFIG,
    SITE_TEMPLATES_DIR,
    TRACKER_ACRONYMS,
    REUPLOADER_SAMPLE_CONFIG,
    TEMPLATE_SCHEMA_LOCATION,
    VALIDATED_SITE_TEMPLATES_DIR,
    MEDIAINFO_FILE_PATH,
    AUDIO_CODECS_MAP,
    STREAMING_SERVICES_MAP,
    STREAMING_SERVICES_REVERSE_MAP,
    SCENE_GROUPS_MAP,
    TAG_GROUPINGS,
    WORKING_DIR,
    SCREENSHOTS_RESULT_FILE_PATH,
    BLURAY_REGIONS_MAP,
    TRACKER_API_KEYS,
    REUPLOADER_ARGUMENTS_CONFIG,
)
from modules.description.description_manager import GGBotDescriptionManager
from modules.exceptions.exception import GGBotUploaderException, GGBotFatalException
from modules.reuploader.enums import (
    TrackerUploadStatus,
    TorrentFailureStatus,
    JobStatus,
)
from modules.reuploader.reupload_manager import AutoReUploaderManager
from modules.sentry_config import SentryConfig
from modules.sys_arguments.arg_parser import GGBotArgumentParser
from modules.sys_arguments.arg_reader import GGBotArgReader
from utilities.utils import GenericUtils
from utilities.utils_basic import BasicUtils
from utilities.utils_dupes import DupeUtils
from utilities.utils_miscellaneous import MiscellaneousUtils
import utilities.utils_translation as translation_utilities
from modules.cache import CacheFactory, CacheVendor, Cache
from modules.config import ReUploaderConfig, TrackerConfig, SentryErrorTrackingConfig

# processing modules
from modules.visor.server import Server

# Method that will search for dupes in trackers.
from modules.template_schema_validator import TemplateSchemaValidator
from modules.torrent_client import Clients, TorrentClientFactory, TorrentClient

# utility methods
# Method that will search for dupes in trackers.
# This is used to take screenshots and eventually upload them to either imgbox, imgbb, ptpimg or freeimage
from utilities.utils_screenshots import GGBotScreenshotManager
from utilities.utils_torrent import GGBotTorrentCreator

# ---------------------------------------------------------------------------------#
#  **START** This is the first code that executes when we run the script **START** #
# ---------------------------------------------------------------------------------#

# Used for rich.traceback
install()

# For more control over rich terminal content, import and construct a Console object.
console = Console()


class GGBotReUploader:
    # PTP is blacklisted for Reuploader since support for PTP is still a work in progress
    # GPW is blacklisted since the dupe check is pretty much a hit and miss since audio information
    # is not available from tracker
    # TODO: move this to a parameter and possibly with these message as reason and show them to user???
    blacklist_trackers = ["PTP", "GPW"]

    def __init__(self, env_file_path=None):
        # Import & set some global variables that we reuse later
        # This shows the full path to this files location
        self.working_folder = os.path.dirname(os.path.realpath(__file__))
        self.cookies_dump = COOKIES_DUMP_DIR.format(base_path=self.working_folder)

        # This is an important dict that we use to store info about the media file as we discover it
        # Once all necessary info has been collected we will loop through this dict and set the correct tracker API Keys to it
        self.torrent_info = {}

        # Load the .env file that stores info like the tracker/image host API Keys & other info needed to upload
        if env_file_path is None:
            load_dotenv(
                REUPLOADER_CONFIG.format(base_path=self.working_folder), override=True
            )
        else:
            load_dotenv(env_file_path, override=True)

        # Initialize decryptor (if key is provided) after loading environment variables
        GenericUtils.initialize_decryptor()

        self._initialize_sentry_sdk()

        # By default, we load the templates from site_templates/ path
        # If user has provided load_external_templates argument then we'll update this path to a different one
        self.site_templates_path = SITE_TEMPLATES_DIR.format(
            base_path=self.working_folder
        )

        # Used to correctly select json file
        # the value in this dictionary must correspond to the file name of the site template
        self.acronym_to_tracker = json.load(
            open(TRACKER_ACRONYMS.format(base_path=self.working_folder))
        )

        self.auto_mode = "true"

        # Setup args
        self.args = self._read_system_arguments_config(
            REUPLOADER_ARGUMENTS_CONFIG.format(base_path=self.working_folder)
        )

        # Setup Loggers
        self._setup_loggers(args=self.args, working_folder=self.working_folder)

        # the `prepare_tracker_api_keys_dict` prepares the api_keys_dict and also does mandatory property validations
        self.api_keys_dict = GenericUtils.prepare_and_validate_tracker_api_keys_dict(
            TRACKER_API_KEYS.format(base_path=self.working_folder)
        )

        self._display_banner()

        # Getting the keys present in the config.env.sample
        # These keys are then used to compare with the env variable keys provided during runtime.
        # Presently we just displays any missing keys, TODO in the future do something more useful with this information
        GenericUtils.validate_env_file(
            REUPLOADER_SAMPLE_CONFIG.format(base_path=self.working_folder)
        )

        self.reuploader_config = ReUploaderConfig()

        console.line(count=2)
        console.rule("Establishing Connections", style="red", align="center")
        console.line(count=1)

        self.torrent_client: TorrentClient = self._initialize_torrent_client(
            reuploader_config=self.reuploader_config
        )
        self.cache: Cache = self._initialize_cache(
            reuploader_config=self.reuploader_config
        )

        self.reupload_manager: AutoReUploaderManager = AutoReUploaderManager(
            cache=self.cache, client=self.torrent_client
        )

        # creating the schema validator for validating all the template files
        self.template_validator = TemplateSchemaValidator(
            TEMPLATE_SCHEMA_LOCATION.format(base_path=self.working_folder)
        )
        # we are going to validate all the built-in templates
        self.valid_templates = GenericUtils.validate_templates_in_path(
            self.site_templates_path, self.template_validator
        )
        # copy all the valid templates to workdir.
        GenericUtils.copy_template(
            self.valid_templates,
            self.site_templates_path,
            VALIDATED_SITE_TEMPLATES_DIR.format(base_path=self.working_folder),
        )
        # now we set the site templates path to the new temp dir
        self.site_templates_path = VALIDATED_SITE_TEMPLATES_DIR.format(
            base_path=self.working_folder
        )

        if self.args.load_external_templates:
            self._load_external_templates()

        # getting the list of trackers that the user wants to upload to.
        # If there are any configuration errors for a particular tracker, then they'll not be used
        self.upload_to_trackers = GenericUtils().get_and_validate_configured_trackers(
            self.args.trackers,
            self.args.all_trackers,
            self.api_keys_dict,
            self.acronym_to_tracker.keys(),
        )
        for tracker in self.blacklist_trackers:
            if tracker in self.upload_to_trackers:
                self.upload_to_trackers.remove(tracker)
                console.print(
                    f"[red bold] Uploading to [yellow]{tracker}[/yellow] not supported in GGBOT Auto ReUploader"
                )

        if len(self.upload_to_trackers) < 1:
            raise GGBotFatalException(
                "Provide at least 1 tracker we can upload to (e.g. BHD, BLU, ACM)"
            )

        self.server = None
        # now that we have verified that the client and cache connections have been created successfully
        #  - we can optionally start gg-bot visor server
        #  - we can start the reupload job (At the end of this file xD)
        if self.reuploader_config.ENABLE_VISOR_SERVER:
            self.server: Server = self._start_visor_server(self.cache)

    def _load_external_templates(self):
        logging.info(
            "[GGBotReUploader] User wants to load external site templates. Attempting to load and validate these "
            "templates..."
        )
        # Here we validate the external templates and copy all default and external templates to a different folder.
        # The method will modify the `api_keys_dict` and `acronym_to_tracker` to include the external trackers as well.
        (
            valid_ext_templates,
            ext_api_keys_dict,
            ext_acronyms,
        ) = GenericUtils().validate_and_load_external_templates(
            self.template_validator, self.working_folder
        )
        if len(valid_ext_templates) > 0:
            self.valid_templates.extend(valid_ext_templates)
            self.api_keys_dict.update(ext_api_keys_dict)
            self.acronym_to_tracker.update(ext_acronyms)

    @staticmethod
    def _start_visor_server(cache: Cache) -> Server:
        logging.info("[GGBotReUploader] Starting GG-BOT Visor server...")
        server = Server(cache)
        server.start(detached=True)
        console.print("[cyan]Started GG-BOT Visor server...[/cyan]")
        logging.info("[GGBotReUploader] GG-BOT Visor server started successfully")
        return server

    def run(self):
        schedule.every(10).seconds.do(self._run)

        print(f"Starting reupload process at {datetime.now()}")
        logging.info("Started GG-BOT Auto-Reuploader")

        while True:
            schedule.run_pending()

    def _run(self):
        logging.info("---------------------------------------------------------------")
        logging.info("------------------ Starting new reupload job ------------------")
        logging.info("---------------------------------------------------------------")
        logging.info(f"[GGBotReUploader] Starting reupload job at {datetime.now()}")

        torrents = self.reupload_manager.get_processable_torrents()
        if torrents is None or len(torrents) == 0:
            logging.info(
                "[GGBotReUploader] There are no completed torrents for re-uploading. Snoozing..."
            )
            return

        logging.info(
            f"[GGBotReUploader] There are a total of {len(torrents)} completed torrents that needs to be re-uploaded"
        )

        for torrent in torrents:
            try:
                self._process_torrent(torrent)
            except GGBotUploaderException as e:
                logging.exception(
                    "[GGBotReUploader] Failed to reupload torrent.", exc_info=e
                )

        logging.info("---------------------------------------------------------------")
        logging.info("------------------ Finished one reupload job ------------------")
        logging.info(
            "---------------------------------------------------------------\n\n"
        )

    # ---------------------------------------------------------------------- #
    #                          Dupe Check in Tracker                         #
    # ---------------------------------------------------------------------- #
    def check_for_dupes_in_tracker(self, tracker, temp_tracker_api_key):
        """
        Method to check for any duplicate torrents in the tracker.
        First we read the configuration for the tracker and format the title according to the tracker configuration
        Then invoke the `search_for_dupes_api` method and return the result.

        Returns True => Dupes are present in the tracker and cannot proceed with the upload
        Returns False => No dupes present in the tracker and upload can continue
        """
        # Open the correct .json file since we now need things like announce URL, API Keys, and API info
        config = json.load(
            open(
                self.site_templates_path
                + str(self.acronym_to_tracker.get(str(tracker).lower()))
                + ".json",
                encoding="utf-8",
            )
        )
        if config["dupes"].get("skip_dupe_check", False) is True:
            logging.info(
                f"[GGBotReUploader] Dupe check disabled for tracker {tracker}. SKipping dupe check..."
            )
            return False

        # -------- format the torrent title --------
        self.torrent_info["torrent_title"] = translation_utilities.format_title(
            config, self.torrent_info
        )

        # Call the function that will search each site for dupes and return a similarity percentage, if it exceeds
        # what the user sets in config.env we skip the upload
        try:
            return DupeUtils().search_for_dupes_api(
                tracker=tracker,
                search_site=self.acronym_to_tracker[str(tracker).lower()],
                imdb=self.torrent_info["imdb"],
                tmdb=self.torrent_info["tmdb"],
                tvmaze=self.torrent_info["tvmaze"],
                torrent_info=self.torrent_info,
                tracker_api=temp_tracker_api_key,
                config=config,
                auto_mode=self.auto_mode,
            )
        except Exception as e:
            logging.exception(
                f"[GGBotReUploader] Error occurred while performing dupe check for tracker {tracker}. Error: {e}"
            )
            console.print(
                "[bold red]Unexpected error occurred while performing dupe check. Assuming dupe exists on tracker and skipping[/bold red]"
            )
            return True  # marking that dupes are present in the tracker

    # ---------------------------------------------------------------------- #
    #                             Upload that shit!                          #
    # ---------------------------------------------------------------------- #
    def upload_to_site(self, upload_to, tracker_api_key, config, tracker_settings):
        logging.info(f"[GGBotReUploader] Attempting to upload to: {upload_to}")
        url = str(config["upload_form"]).format(api_key=tracker_api_key)
        url_masked = str(config["upload_form"]).format(api_key="REDACTED")
        payload = {}
        files = []
        display_files = {}

        logging.debug(
            "::::::::::::::::::::::::::::: Tracker settings that will be used for creating payload :::::::::::::::::::::::::::::"
        )
        logging.debug(f"\n{pformat(tracker_settings)}")

        # multiple authentication modes
        headers = None
        if config["technical_jargons"]["authentication_mode"] == "API_KEY":
            pass  # headers = None
        elif config["technical_jargons"]["authentication_mode"] == "API_KEY_PAYLOAD":
            # api key needs to be added in payload. the key in payload for api key can be obtained from `auth_payload_key`
            payload[config["technical_jargons"]["auth_payload_key"]] = tracker_api_key
        elif config["technical_jargons"]["authentication_mode"] == "BEARER":
            headers = {"Authorization": f"Bearer {tracker_api_key}"}
            logging.info(
                f"[GGBotReUploader] Using Bearer Token authentication method for tracker {upload_to}"
            )
        elif config["technical_jargons"]["authentication_mode"] == "HEADER":
            if len(config["technical_jargons"]["headers"]) > 0:
                headers = {}
                logging.info(
                    f"[TrackerUpload] Using Header based authentication method for tracker {upload_to}"
                )
                for header in config["technical_jargons"]["headers"]:
                    logging.info(
                        f"[GGBotReUploader] Adding header '{header['key']}' to request"
                    )
                    headers[header["key"]] = (
                        tracker_api_key
                        if header["value"] == "API_KEY"
                        else self.reuploader_config.get_config(
                            f"{upload_to}_{header['value']}", ""
                        )
                    )
            else:
                logging.fatal(
                    f"[GGBotReUploader] Header based authentication cannot be done without `header_key` for tracker {upload_to}."
                )
        # TODO add support for cookie based authentication
        elif config["technical_jargons"]["authentication_mode"] == "COOKIE":
            logging.fatal(
                "[GGBotReUploader] Cookie based authentication is not supported as for now."
            )

        for key, val in tracker_settings.items():
            # First check to see if it's a required or optional key
            req_opt = (
                "Required"
                if key in config["Required"]
                else "Optional"
                if key in config["Optional"]
                else "Default"
            )

            # Now that we know if we are looking for a required or optional key we can try to add it into the payload
            if str(config[req_opt][key]) == "file":
                if os.path.isfile(tracker_settings[key]):
                    post_file = f"{key}", open(tracker_settings[key], "rb")
                    files.append(post_file)
                    display_files[key] = tracker_settings[key]
                else:
                    logging.critical(
                        f"[GGBotReUploader] The file/path `{tracker_settings[key]}` for key {req_opt} does not exist!"
                    )
                    continue
            elif str(config[req_opt][key]) == "file|array":
                if os.path.isfile(tracker_settings[key]):
                    with open(tracker_settings[key]) as images_data:
                        for line in images_data.readlines():
                            post_file = f"{key}[]", open(line.strip(), "rb")
                            files.append(post_file)
                            display_files[key] = tracker_settings[key]
                else:
                    logging.critical(
                        f"[GGBotReUploader] The file/path `{tracker_settings[key]}` for key {req_opt} does not exist!"
                    )
                    continue
            elif str(config[req_opt][key]) == "file|string|array":
                """
                for file|array we read the contents of the file line by line, where each line becomes and element of the array or list
                """
                if os.path.isfile(tracker_settings[key]):
                    logging.debug(
                        f"[GGBotReUploader] Setting file {tracker_settings[key]} as string array for key '{key}'"
                    )
                    with open(tracker_settings[key]) as file_contents:
                        screenshot_array = []
                        for line in file_contents.readlines():
                            screenshot_array.append(line.strip())
                        payload[
                            f"{key}[]"
                            if config["technical_jargons"]["payload_type"]
                            == "MULTI-PART"
                            else key
                        ] = screenshot_array
                        logging.debug(
                            f"[GGBotReUploader] String array data for key {key} :: {screenshot_array}"
                        )
                else:
                    logging.critical(
                        f"[GGBotReUploader] The file/path `{tracker_settings[key]}` for key '{req_opt}' does not exist!"
                    )
                    continue
            elif str(config[req_opt][key]) == "string|array":
                """
                for string|array we split the data with by new line, where each line becomes and element of the array or list
                """
                logging.debug(
                    f"[GGBotReUploader] Setting data {tracker_settings[key]} as string array for key '{key}'"
                )
                screenshot_array = []
                for line in tracker_settings[key].split("\n"):
                    if len(line.strip()) > 0:
                        screenshot_array.append(line.strip())
                payload[
                    f"{key}[]"
                    if config["technical_jargons"]["payload_type"] == "MULTI-PART"
                    else key
                ] = screenshot_array
                logging.debug(
                    f"[GGBotReUploader] String array data for key '{key}' :: {screenshot_array}"
                )

            elif str(config[req_opt][key]) == "file|base64":
                # file encoded as base64 string
                if os.path.isfile(tracker_settings[key]):
                    logging.debug(f"[TrackerUpload] Setting file|base64 for key {key}")
                    with open(tracker_settings[key], "rb") as binary_file:
                        binary_file_data = binary_file.read()
                        base64_encoded_data = base64.b64encode(binary_file_data)
                        base64_message = base64_encoded_data.decode("utf-8")
                        payload[key] = base64_message
                else:
                    logging.critical(
                        f"[GGBotReUploader] The file/path `{tracker_settings[key]}` for key {req_opt} does not exist!"
                    )
                    continue
            else:
                # if str(val).endswith(".nfo") or str(val).endswith(".txt"):
                if str(val).endswith(".txt"):
                    if not os.path.exists(val):
                        create_file = open(val, "w+")
                        create_file.close()
                    with open(val) as txt_file:
                        val = txt_file.read()
                if req_opt == "Optional":
                    logging.info(
                        f"[GGBotReUploader] Optional key {key} will be added to payload"
                    )
                payload[key] = val

        logging.fatal(
            f"[GGBotReUploader] URL: {url_masked} \n Data: {payload} \n Files: {files}"
        )

        if config["technical_jargons"]["payload_type"] == "JSON":
            response = requests.request(
                "POST", url, json=payload, files=files, headers=headers
            )
        else:
            response = requests.request(
                "POST", url, data=payload, files=files, headers=headers
            )

        logging.info(f"[GGBotReUploader] POST Request: {url}")
        logging.info(f"[GGBotReUploader] Response code: {response.status_code}")

        console.print(f"\nSite response: [blue]{response.text}[/blue]")
        logging.info(f"[GGBotReUploader] {response.text}")

        if response.status_code in (200, 201):
            logging.info(
                f"[GGBotReUploader] Upload response for {upload_to}: {response.text.encode('utf8')}"
            )

            if "success" in response.json():
                if str(response.json()["success"]).lower() == "true":
                    logging.info(
                        f"[GGBotReUploader] Upload to {upload_to} was a success!"
                    )
                    console.line(count=2)
                    console.rule(
                        f"\n :thumbsup: Successfully uploaded to {upload_to} :balloon: \n",
                        style="bold green1",
                        align="center",
                    )
                    return True, response.json()
                else:
                    console.print("Upload to tracker failed.", style="bold red")
                    logging.critical(f"[GGBotReUploader] Upload to {upload_to} failed")
                    return False, response.json()
            elif "status" in response.json():
                if (
                    str(response.json()["status"]).lower() == "true"
                    or str(response.json()["status"]).lower() == "success"
                ):
                    logging.info(
                        f"[GGBotReUploader] Upload to {upload_to} was a success!"
                    )
                    console.line(count=2)
                    console.rule(
                        f"\n :thumbsup: Successfully uploaded to {upload_to} :balloon: \n",
                        style="bold green1",
                        align="center",
                    )
                    return True, response.json()
                else:
                    console.print("Upload to tracker failed.", style="bold red")
                    logging.critical(f"[GGBotReUploader] Upload to {upload_to} failed")
                    return False, response.json()
            elif "success" in str(response.json()).lower():
                if str(response.json()["success"]).lower() == "true":
                    logging.info(
                        f"[GGBotReUploader] Upload to {upload_to} was a success!"
                    )
                    console.line(count=2)
                    console.rule(
                        f"\n :thumbsup: Successfully uploaded to {upload_to} :balloon: \n",
                        style="bold green1",
                        align="center",
                    )
                    return True, response.json()
                else:
                    console.print("Upload to tracker failed.", style="bold red")
                    logging.critical(f"[GGBotReUploader] Upload to {upload_to} failed")
                    return False, response.json()
            elif "status" in str(response.json()).lower():
                if str(response.json()["status"]).lower() == "true":
                    logging.info(
                        f"[GGBotReUploader] Upload to {upload_to} was a success!"
                    )
                    console.line(count=2)
                    console.rule(
                        f"\n :thumbsup: Successfully uploaded to {upload_to} :balloon: \n",
                        style="bold green1",
                        align="center",
                    )
                    return True, response.json()
                else:
                    console.print("Upload to tracker failed.", style="bold red")
                    logging.critical(f"[GGBotReUploader] Upload to {upload_to} failed")
                    return False, response.json()
            else:
                console.print("Upload to tracker failed.", style="bold red")
                logging.critical(
                    f"[GGBotReUploader] Something really went wrong when uploading to {upload_to} and we didn't even get a 'success' json key"
                )
                return False, response.json()

        elif response.status_code == 404:
            console.print(
                f"[bold]HTTP response status code: [red]{response.status_code}[/red][/bold]"
            )
            console.print("Upload failed", style="bold red")
            logging.critical(
                f"[GGBotReUploader] 404 was returned on that upload, this is a problem with the site ({upload_to})"
            )
            logging.error("[GGBotReUploader] Upload failed")
            return False, response.status_code

        elif response.status_code == 500:
            console.print(
                f"[bold]HTTP response status code: [red]{response.status_code}[/red][/bold]"
            )
            console.print(
                "The upload might have [red]failed[/], the site isn't returning the uploads status"
            )
            # This is to deal with the 500 internal server error responses BLU has been recently returning
            logging.error(
                f"[GGBotReUploader] HTTP response status code '{response.status_code}' was returned (500=Internal Server Error)"
            )
            logging.info(
                "[GGBotReUploader] This doesn't mean the upload failed, instead the site simply isn't returning the upload status"
            )
            return False, response.status_code

        elif response.status_code == 400:
            console.print(
                f"[bold]HTTP response status code: [red]{response.status_code}[/red][/bold]"
            )
            console.print("Upload failed.", style="bold red")
            try:
                error = (
                    response.json()["error"]
                    if "error" in response.json()
                    else response.json()
                )
                logging.critical(
                    f"[GGBotReUploader] 400 was returned on that upload, this is a problem with the site ({upload_to})."
                    f" Error: Error {error}"
                )
                return False, error or response.status_code
            except Exception:
                logging.error(
                    f"[GGBotReUploader] 400 was returned on that upload, this is a problem with the site ({upload_to}).",
                    extra={"error": response.text},
                )
            logging.error(
                f"[TrackerUpload] Upload failed to tracker {upload_to}",
                extra={"error": response.text},
            )
            return False, response.text or response.status_code

        else:
            console.print(
                f"[bold]HTTP response status code: [red]{response.status_code}[/red][/bold]"
            )
            console.print(
                "The status code isn't [green]200[/green] so something failed, upload may have failed"
            )
            logging.error(
                "[GGBotReUploader] Status code is not 200, upload might have failed"
            )
            return False, f"Unknown Error. Status Code: {response.status_code}"
        # -------------- END of upload_to_site --------------

    # ---------------------------------------------------------------------- #
    #                          Analysing basic details!                      #
    # ---------------------------------------------------------------------- #
    def identify_type_and_basic_info(self, full_path, guess_it_result):
        """
        guessit is typically pretty good at getting the title, year, resolution, group extracted
        but we need to do some more work for things like audio channels, codecs, etc
            (Some groups (D-Z0N3 is a pretty big offender here)

        for example 'D-Z0N3' used to not include the audio channels in their filename so we need to use
            ffprobe to get that ourselves (pymediainfo has issues when dealing with atmos and more complex codecs)

        :param full_path: the full path for the file / folder

        Returns `skip_to_next_file` if there are no video files in thhe provided folder
        """
        console.line(count=2)
        console.rule("Analyzing & Identifying Video", style="red", align="center")
        console.line(count=1)

        # -------- Save obvious info we are almost guaranteed to get from guessit into torrent_info dict -------- #
        # But we can immediately assign some values now like Title & Year
        if not guess_it_result["title"]:
            raise AssertionError(
                "Guessit could not even extract the title, something is really wrong with this filename."
            )

        self.torrent_info["title"] = guess_it_result["title"]
        if (
            "year" in guess_it_result
        ):  # Most TV Shows don't have the year included in the filename
            self.torrent_info["year"] = str(guess_it_result["year"])

        # ------------ Save basic info we get from guessit into torrent_info dict ------------ #
        # We set a list of the items that are required to successfully build a torrent name later
        # if we are missing any of these keys then call another function that will use ffprobe, pymediainfo, regex, etc
        # to try and extract it ourselves, should that fail we can prompt the user
        # (only if auto_mode=false otherwise we just guess and upload what we have)
        keys_we_want_torrent_info = ["release_group", "episode_title"]
        keys_we_need_torrent_info = [
            "screen_size",
            "source",
            "audio_channels",
            "type",
        ]

        keys_we_need_but_missing_torrent_info = []
        # We can (need to) have some other information in the final torrent title like 'editions', 'hdr', etc
        # All of that is important but not essential right now so we will try to extract that info later in the script
        logging.debug(
            f"[GGBotReUploader] Attempting to detect the following keys from guessit :: {keys_we_need_torrent_info}"
        )
        for basic_key in keys_we_need_torrent_info:
            if basic_key in guess_it_result:
                self.torrent_info[basic_key] = str(guess_it_result[basic_key])
            else:
                keys_we_need_but_missing_torrent_info.append(basic_key)

        # As guessit evolves and adds more info we can easily support whatever they add
        # and insert it into our main torrent_info dict
        logging.debug(
            f"[GGBotReUploader] Attempting to detect the following keys from guessit :: {keys_we_want_torrent_info}"
        )
        for wanted_key in keys_we_want_torrent_info:
            if wanted_key in guess_it_result:
                self.torrent_info[wanted_key] = str(guess_it_result[wanted_key])

        self.torrent_info["release_group"] = (
            GenericUtils.sanitize_release_group_from_guessit(self.torrent_info)
        )

        if "type" not in self.torrent_info:
            raise AssertionError(
                "'type' is not set in the guessit output, something is seriously wrong with this filename"
            )

        # ------------ Format Season & Episode (Goal is 'S01E01' type format) ------------ #
        # Depending on if this is a tv show or movie we have some other 'required' keys that we need (season/episode)
        # guessit uses 'episode' for all tv related content (including seasons)
        if self.torrent_info["type"] == "episode":
            (
                s00e00,
                season_number,
                episode_number,
                complete_season,
                individual_episodes,
                daily_episodes,
            ) = BasicUtils().basic_get_episode_basic_details(guess_it_result)
            self.torrent_info["s00e00"] = s00e00
            self.torrent_info["season_number"] = season_number
            self.torrent_info["episode_number"] = episode_number
            self.torrent_info["complete_season"] = complete_season
            self.torrent_info["individual_episodes"] = individual_episodes
            self.torrent_info["daily_episodes"] = daily_episodes

        # ------------ If uploading folder, select video file from within folder ------------ #
        # First make sure we have the path to the actual video file saved in the torrent_info dict
        # for example someone might want to upload a folder full of episodes, we need to select at least 1 episode to use pymediainfo/ffprobe on
        if os.path.isdir(self.torrent_info["upload_media"]):
            # Add trailing forward slash if missing
            if not str(self.torrent_info["upload_media"]).endswith("/"):
                self.torrent_info["upload_media"] = (
                    f'{str(self.torrent_info["upload_media"])}/'
                )

            # the episode/file that we select will be stored under "raw_video_file" (full path + episode/file name)

            # Some uploads are movies within a folder and those folders occasionally contain non-video files nfo, sub, srt, etc files
            # we need to make sure we select a video file to use for mediainfo later

            # First check to see if we are uploading a 'raw bluray disc'
            # if args.disc: TODO uncomment this for full disk auto uploads
            #     # validating presence of bdinfo script for bare metal
            #     bdinfo_validate_bdinfo_script_for_bare_metal(bdinfo_script)
            #     # validating presence of BDMV/STREAM/
            #     bdinfo_validate_presence_of_bdmv_stream(torrent_info["upload_media"])

            #     raw_video_file, largest_playlist = bdinfo_get_largest_playlist(bdinfo_script, auto_mode, torrent_info["upload_media"])

            #     torrent_info["raw_video_file"] = raw_video_file
            #     torrent_info["largest_playlist"] = largest_playlist
            # else:
            raw_video_file = BasicUtils().basic_get_raw_video_file(
                self.torrent_info["upload_media"]
            )
            if raw_video_file is not None:
                self.torrent_info["raw_video_file"] = raw_video_file

            if "raw_video_file" not in self.torrent_info:
                logging.critical(
                    f"[GGBotReUploader] The folder {self.torrent_info['upload_media']} does not contain any video files"
                )
                console.print(
                    f"The folder {self.torrent_info['upload_media']} does not contain any video files\n\n",
                    style="bold red",
                )
                return "skip_to_next_file"

            self.torrent_info["raw_file_name"] = os.path.basename(
                os.path.dirname(f"{full_path}/")
            )  # this is used to isolate the folder name
        else:
            # For regular movies and single video files we can use the following the just get the filename
            self.torrent_info["raw_file_name"] = os.path.basename(
                full_path
            )  # this is used to isolate the file name

        # ---------------------------------Full Disk BDInfo Parsing--------------------------------------#
        # if the upload is for a full disk, we parse the bdinfo to identify more information before moving on to the existing logic.
        keys_we_need_but_missing_torrent_info_list = [
            "video_codec",
            "audio_codec",
        ]  # for disc we don't need mediainfo
        # if args.disc: TODO uncomment this for full disk auto uploads
        #     bdinfo_start_time = time.perf_counter()
        #     logging.debug(f"Generating and parsing the BDInfo for playlist {torrent_info['largest_playlist']}")
        #     console.print(f"\nGenerating and parsing the BDInfo for playlist {torrent_info['largest_playlist']}\n", style='bold blue')
        #     torrent_info["mediainfo"] = f'{working_folder}/temp_upload/{torrent_info["working_folder"]}mediainfo.txt'
        #     torrent_info["bdinfo"] = bdinfo_generate_and_parse_bdinfo(bdinfo_script, working_folder, torrent_info) # TODO handle non-happy paths
        #     logging.debug(f"::::::::::::::::::::::::::::: Parsed BDInfo output :::::::::::::::::::::::::::::")
        #     logging.debug(f"\n{pformat(torrent_info['bdinfo'])}")
        #     bdinfo_end_time = time.perf_counter()
        #     logging.debug(f"Time taken for full bdinfo parsing :: {(bdinfo_end_time - bdinfo_start_time)}")
        # else:

        # since this is not a disc, media info will be appended to the list
        keys_we_need_but_missing_torrent_info_list.append("mediainfo")

        # ------------ GuessIt doesn't return a video/audio codec that we should use ------------ #
        # For 'x264', 'AVC', and 'H.264' GuessIt will return 'H.264' which might be a little misleading
        # since things like 'x264' is used for encodes while AVC for Remuxs (usually) etc
        # For audio it will insert "Dolby Digital Plus" into the dict when what we want is "DD+"
        # ------------ If we are missing any other "basic info" we try to identify it here ------------ #
        if len(keys_we_need_but_missing_torrent_info) != 0:
            logging.warning(
                "[GGBotReUploader] Unable to automatically extract all the required info from the FILENAME"
            )
            logging.warning(
                f"[GGBotReUploader] We are missing this info: {keys_we_need_but_missing_torrent_info}"
            )
            # Show the user what is missing & the next steps
            console.print(
                f"[bold red underline]Unable to automatically detect the following info from the FILENAME:[/bold red "
                f"underline] [green]{keys_we_need_but_missing_torrent_info}[/green]"
            )

        # We do some extra processing for the audio & video codecs since they are pretty important for the upload
        # process & accuracy so they get appended each time ['mediainfo', 'video_codec', 'audio_codec'] or [
        # 'video_codec', 'audio_codec'] for disks
        for identify_me in keys_we_need_but_missing_torrent_info_list:
            if identify_me not in keys_we_need_but_missing_torrent_info:
                keys_we_need_but_missing_torrent_info.append(identify_me)

        # parsing mediainfo, this will be reused for further processing.
        # only when the required data is mediainfo, this will be computed again, but as `text` format to write to file.
        parse_me = self.torrent_info.get(
            "raw_video_file", self.torrent_info["upload_media"]
        )
        media_info_result = BasicUtils().basic_get_mediainfo(parse_me)

        # if args.disc: TODO uncomment this for full disk auto uploads
        #     # for full disk uploads the bdinfo summary itself will be set as the `mediainfo_summary`
        #     logging.info("[Main] Full Disk Upload. Setting bdinfo summary as mediainfo summary")
        #     with open(f'{working_folder}/temp_upload/{torrent_info["working_folder"]}mediainfo.txt', 'r') as summary:
        #         bdInfo_summary = summary.read()
        #         torrent_info["mediainfo_summary"] = bdInfo_summary
        # else:
        (
            self.torrent_info["mediainfo_summary"],
            tmdb,
            imdb,
            _,
            self.torrent_info["subtitles"],
            self.torrent_info["mediainfo_summary_data"],
        ) = BasicUtils().basic_get_mediainfo_summary(media_info_result.to_data())
        if tmdb != "0":
            # we will get movie/12345 or tv/12345 => we only need 12345 part.
            tmdb = tmdb[tmdb.find("/") + 1 :] if tmdb.find("/") >= 0 else tmdb
            self.torrent_info["tmdb"] = tmdb
            logging.info(
                f"[GGBotReUploader] Obtained TMDB Id from mediainfo summary. Proceeding with {self.torrent_info['tmdb']}"
            )
        if imdb != "0":
            self.torrent_info["imdb"] = imdb
            logging.info(
                f"[GGBotReUploader] Obtained IMDB Id from mediainfo summary. Proceeding with {self.torrent_info['imdb']}"
            )

        #  Now we'll try to use regex, mediainfo, ffprobe etc to try and auto get that required info
        for missing_val in keys_we_need_but_missing_torrent_info:
            # Save the analyze_video_file() return result into the 'torrent_info' dict
            self.torrent_info[missing_val] = self.analyze_video_file(
                missing_value=missing_val, media_info=media_info_result
            )

        logging.debug(
            "::::::::::::::::::::::::::::: Torrent Information collected so far :::::::::::::::::::::::::::::"
        )
        logging.debug(f"\n{pformat(self.torrent_info)}")
        # Show the user what we identified so far
        columns_we_want = {
            "type": "Type",
            "title": "Title",
            "s00e00": f'{("Season" if len(self.torrent_info["s00e00"]) == 3 else "Episode") if "s00e00" in self.torrent_info else ""}',
            "year": f'{"Year" if "year" in self.torrent_info and self.torrent_info["type"] == "movie" else ""}',
            "source": "Source",
            "screen_size": "Resolution",
            "video_codec": "Video Codec",
            "hdr": f'{"HDR Format" if "hdr" in self.torrent_info else ""}',
            "dv": f'{"Dolby Vision" if "dv" in self.torrent_info else ""}',
            "audio_codec": "Audio Codec",
            "audio_channels": "Audio Channels",
            "atmos": f'{"Dolby Atmos" if "atmos" in self.torrent_info else ""}',
            "release_group": f'{"Release Group" if "release_group" in self.torrent_info else ""}',
        }
        logging.debug(f"The columns that we want to show are {columns_we_want}")
        presentable_type = (
            "Movie" if self.torrent_info["type"] == "movie" else "TV Show"
        )

        codec_result_table = Table(
            box=box.SQUARE, title="Basic media summary", title_style="bold #be58bf"
        )

        for column_display_value in columns_we_want.values():
            if len(column_display_value) != 0:
                logging.debug(
                    f"Adding column {column_display_value} to the torrent details result table"
                )
                codec_result_table.add_column(
                    f"{column_display_value}", justify="center", style="#38ACEC"
                )

        basic_info = []
        # add the actual data now
        for column_query_key, column_display_value in columns_we_want.items():
            if len(column_display_value) != 0:
                torrent_info_key_failsafe = (
                    (
                        self.torrent_info[column_query_key]
                        if column_query_key != "type"
                        else presentable_type
                    )
                    if column_query_key in self.torrent_info
                    else None
                )
                logging.debug(
                    f"Getting value for {column_query_key} with display {column_display_value} as "
                    f"{torrent_info_key_failsafe} for the torrent details result table"
                )
                basic_info.append(torrent_info_key_failsafe)

        codec_result_table.add_row(*basic_info)

        console.line(count=2)
        console.print(codec_result_table, justify="center")
        console.line(count=1)
        # -------------- END of identify_type_and_basic_info --------------

    # ---------------------------------------------------------------------- #
    #                            Upload To Tracker!                          #
    # ---------------------------------------------------------------------- #
    def _upload_to_tracker(
        self, tracker: str, target_trackers, torrent: Dict
    ) -> Tuple[TrackerUploadStatus, Union[Dict, Any]]:
        tracker_env_config = TrackerConfig(tracker)
        tracker_name = str(self.acronym_to_tracker.get(str(tracker).lower()))

        self.torrent_info["shameless_self_promotion"] = (
            f'Uploaded with {"<3" if str(tracker).upper() in ("BHD", "BHDTV") or os.name == "nt" else "❤"} using GG-BOT Auto-ReUploader'
        )

        temp_tracker_api_key = self.api_keys_dict[f"{str(tracker).lower()}_api_key"]
        logging.info(f"[Main] Trying to upload to: {tracker}")

        # Create a new dictionary that we store the exact keys/vals that the site is expecting
        tracker_settings = {}
        # Open the correct .json file since we now need things like announce URL, API Keys, and API info
        config = json.load(
            open(
                f"{self.site_templates_path}{tracker_name}.json",
                encoding="utf-8",
            )
        )

        # checking for banned groups. If this group is banned in this tracker, then we stop
        if (
            "banned_groups" in config
            and self.torrent_info["release_group"] in config["banned_groups"]
        ):
            logging.fatal(
                f"[Main] Release group {self.torrent_info['release_group']} is banned in this at {tracker}. Skipping "
                f"upload... "
            )
            console.rule(
                f"[bold red] :warning: Group {self.torrent_info['release_group']} is banned on {tracker} :warning: ["
                f"/bold red]",
                style="red",
            )
            self.reupload_manager.mark_failed_upload(
                torrent, tracker, None, job_status=JobStatus.BANNED_GROUP
            )
            return TrackerUploadStatus.BANNED_GROUP, None

        # -------- format the torrent title --------
        self.torrent_info["torrent_title"] = translation_utilities.format_title(
            config, self.torrent_info
        )

        # (Theory) BHD has a different bbcode parser then BLU/ACM so the line break is different for each site
        # this is why we set it in each site *.json file then retrieve it here in this 'for loop' since it's
        # different for each site
        description_manager = GGBotDescriptionManager(
            working_folder=self.working_folder,
            sub_folder=self.torrent_info["working_folder"],
            tracker=tracker_name,
            source_type=self.torrent_info["source_type"],
            bbcode_line_break=config["bbcode_line_break"],
        )
        description_manager.prepare_description_file(
            custom_user_inputs=self.torrent_info.get("custom_user_inputs"),
            tracker_description_components=config.get("description_components"),
            screenshots_data_types=self.torrent_info.get("screenshots_data_types"),
            screenshot_type=config.get("screenshot_type"),
            torrent_info=self.torrent_info,
        )
        description_manager.render()

        # Add the finished file to the 'torrent_info' dict
        self.torrent_info["description"] = (
            description_manager.get_description_file_path()
        )

        # -------- Check for Dupes Multiple Trackers --------
        # when the user has configured multiple trackers to upload to
        # we take the screenshots and uploads them, then do dupe check for the trackers.
        # dupe check need not be performed if user provided only one tracker.
        # in cases where only one tracker is provided, dupe check will be performed prior to taking screenshots.
        if self.reuploader_config.CHECK_FOR_DUPES and len(target_trackers) > 1:
            console.line(count=2)
            console.rule(
                f"Dupe Check [bold]({tracker})[/bold]",
                style="red",
                align="center",
            )
            # Call the function that will search each site for dupes and return a similarity percentage,
            # if it exceeds what the user sets in config.env we skip the upload
            dupe_check_response = self.check_for_dupes_in_tracker(
                tracker, temp_tracker_api_key
            )
            # True == dupe_found
            # False == no_dupes/continue upload
            if dupe_check_response:
                logging.warning(
                    f"[Main] Could not upload to: {tracker} because we found a dupe on site"
                )
                # If dupe was found & the script is auto_mode OR if the user responds with 'n' for the 'dupe
                # found, continue?' prompt we will essentially stop the current 'for loops' iteration & jump back
                # to the beginning to start next cycle (if exists else quits)
                self.reupload_manager.mark_failed_upload(
                    torrent, tracker, None, job_status=JobStatus.DUPE_UPLOAD
                )
                return TrackerUploadStatus.DUPE, None

        # -------- Generate .torrent file --------
        console.print(
            f"\n[bold]Generating .torrent file for [chartreuse1]{tracker}[/chartreuse1][/bold]"
        )
        logging.debug(
            f"[Main] Torrent info just before dot torrent creation. \n {pformat(self.torrent_info)}"
        )
        # If the type is a movie, then we only include the `raw_video_file` for torrent file creation. If type is
        # an episode, then we'll create torrent file for the `upload_media` which could be an single episode
        # or a season folder
        if (
            self.torrent_info["type"] == "movie"
            and "raw_video_file" in self.torrent_info
        ):
            torrent_media = self.torrent_info["raw_video_file"]
        else:
            torrent_media = self.torrent_info["upload_media"]

        GGBotTorrentCreator(
            media=torrent_media,
            announce_urls=tracker_env_config.ANNOUNCE_URL.split(" "),
            source=config["source"],
            working_folder=self.working_folder,
            hash_prefix=self.torrent_info["working_folder"],
            use_mktorrent=self.args.use_mktorrent,
            tracker=tracker,
            torrent_title=self.torrent_info["torrent_title"],
        ).generate_dot_torrent()

        # TAGS GENERATION. Generations all the tags that are applicable to this upload
        translation_utilities.generate_all_applicable_tags(self.torrent_info)

        # -------- Assign specific tracker keys -------- This function takes the info we have the dict
        # torrent_info and associates with the right key/values needed for us to use X trackers API if for some
        # reason the upload cannot be performed to the specific tracker, the method returns "STOP"
        if (
            translation_utilities.choose_right_tracker_keys(
                config,
                tracker_settings,
                tracker,
                self.torrent_info,
                self.args,
                self.working_folder,
            )
            == "STOP"
        ):
            self.reupload_manager.mark_failed_upload(
                torrent, tracker, None, job_status=JobStatus.INVALID_PAYLOAD
            )
            return TrackerUploadStatus.PAYLOAD_ERROR, None

        logging.debug(
            "::::::::::::::::::::::::::::: Final torrent_info with all data filled :::::::::::::::::::::::::::::"
        )
        logging.debug(f"\n{pformat(self.torrent_info)}")
        # -------- Upload everything! --------
        # 1.0 everything we do in this for loop isn't persistent, its specific to each site that you upload to
        # 1.1 things like screenshots, TMDB/IMDB ID's can & are reused for each site you upload to
        # 2.0 we take all the info we generated outside of this loop (mediainfo, description, etc.)
        # and combine it with tracker specific info and upload it all now
        upload_status, upload_response = self.upload_to_site(
            upload_to=tracker,
            tracker_api_key=temp_tracker_api_key,
            config=config,
            tracker_settings=tracker_settings,
        )

        # Tracker Settings
        if not upload_status:
            self.reupload_manager.mark_failed_upload(torrent, tracker, upload_response)
            return TrackerUploadStatus.FAILED, upload_response

        if "success_processor" in config["technical_jargons"]:
            logging.info(
                f"[Main] Upload to tracker {tracker} is successful and success processor is configured"
            )
            action = config["technical_jargons"]["success_processor"]
            logging.info(
                f"[Main] Performing success processor action '{action}' for tracker {tracker}"
            )
            custom_action = GenericUtils.load_custom_actions(action)
            logging.info(f"[Main] Loaded custom action :: {action} :: Executing...")
            custom_action(
                self.torrent_info, tracker_settings, config, self.working_folder
            )

        self.reupload_manager.mark_successful_upload(torrent, tracker, upload_response)

        # -------- Post Processing --------
        save_path: str = torrent["save_path"]
        logging.fatal(
            f'[Main] `upload_media` :: {self.torrent_info["upload_media"]} `save_path` :: {save_path}'
        )
        if "raw_video_file" in self.torrent_info:
            logging.fatal(
                f'[Main] `raw_video_file` :: {self.torrent_info["raw_video_file"]}'
            )

        if self.torrent_info["type"] == "movie":
            if "raw_video_file" in self.torrent_info:
                save_path = self.torrent_info["upload_media"]
                logging.info(
                    f"[Main] `raw_video_file` is present in torrent_info. Hence updating client save path to {save_path}"
                )
            else:
                save_path = self.torrent_info["upload_media"].replace(
                    f'/{self.torrent_info["raw_file_name"]}', ""
                )
                logging.info(
                    f"[Main] `raw_video_file` is missing in torrent_info. Hence updating client save path to {save_path}"
                )

        working_dir = WORKING_DIR.format(base_path=self.working_folder)
        normalized_path = GenericUtils.normalize_for_system_path(
            self.torrent_info["torrent_title"]
        )

        self.torrent_client.upload_torrent(
            torrent=f'{working_dir}{self.torrent_info["working_folder"]}{tracker}-{normalized_path}.torrent',
            save_path=save_path,
            use_auto_torrent_management=False,
            is_skip_checking=True,
        )
        return TrackerUploadStatus.SUCCESS, upload_response
        # -------------- END of _upload_to_tracker --------------

    def analyze_video_file(self, missing_value, media_info):
        """
        This method is being called in loop with mediainfo calculation all taking place multiple times.
        Optimize this code for better performance
        """
        logging.debug(f"[Main] Trying to identify the {missing_value}...")

        # ffprobe/mediainfo need to access to video file not folder, set that here using the 'parse_me' variable
        parse_me = self.torrent_info.get(
            "raw_video_file", self.torrent_info["upload_media"]
        )

        # In pretty much all cases "media_info.tracks[1]" is going to be the video track and media_info.tracks[2] will be the primary audio track
        media_info_video_track = media_info.tracks[1]
        # I've encountered a media file without an audio track one time... this try/exception should handle any future situations like that
        try:
            media_info_audio_track = media_info.tracks[2]
        except IndexError:
            logging.info("[Main] No audio tracker info available for this release...")
            media_info_audio_track = None

        # ------------ Save mediainfo to txt ------------ #
        if missing_value == "mediainfo":
            return BasicUtils().basic_get_missing_mediainfo(
                self.torrent_info,
                parse_me,
                MEDIAINFO_FILE_PATH.format(
                    base_path=self.working_folder,
                    sub_folder=self.torrent_info["working_folder"],
                ),
            )

        # !!! [ Block tests/probes start now ] !!!

        # ------------------- Source ------------------- #
        if missing_value == "source":
            # source, source_type, user_input_source = basic_utilities.basic_get_missing_source(torrent_info, args.disc, auto_mode, missing_value)
            (
                source,
                source_type,
                user_input_source,
            ) = BasicUtils().basic_get_missing_source(
                self.torrent_info, False, self.auto_mode, missing_value
            )
            self.torrent_info["source"] = source
            self.torrent_info["source_type"] = source_type
            return user_input_source

        # ---------------- Video Resolution ---------------- #
        if missing_value == "screen_size":
            return BasicUtils().basic_get_missing_screen_size(
                self.torrent_info,
                False,
                media_info_video_track,
                self.auto_mode,
                missing_value,
            )

        # ---------------- Audio Channels ---------------- #
        if missing_value == "audio_channels":
            # return basic_utilities.basic_get_missing_audio_channels(torrent_info, args.disc, auto_mode, parse_me, media_info_audio_track, missing_value)
            return BasicUtils().basic_get_missing_audio_channels(
                self.torrent_info,
                False,
                self.auto_mode,
                parse_me,
                media_info_audio_track,
                missing_value,
            )

        # ---------------- Audio Codec ---------------- #
        if missing_value == "audio_codec":
            # audio_codec, atmos =  basic_utilities.basic_get_missing_audio_codec(torrent_info=torrent_info, is_disc=args.disc, auto_mode=auto_mode,
            audio_codec, atmos = BasicUtils().basic_get_missing_audio_codec(
                torrent_info=self.torrent_info,
                is_disc=False,
                auto_mode=self.auto_mode,
                audio_codec_file_path=AUDIO_CODECS_MAP.format(
                    base_path=self.working_folder
                ),
                media_info_audio_track=media_info_audio_track,
                parse_me=parse_me,
                missing_value=missing_value,
            )

            if atmos is not None:
                self.torrent_info["atmos"] = atmos
            if audio_codec is not None:
                return audio_codec

        # ---------------- Video Codec ---------------- #
        # I'm pretty confident that a video_codec will be selected automatically each time, unless mediainfo fails catastrophically we should always
        # have a codec we can return. User input isn't needed here
        if missing_value == "video_codec":
            (
                dv,
                hdr,
                video_codec,
                pymediainfo_video_codec,
            ) = BasicUtils().basic_get_missing_video_codec(
                torrent_info=self.torrent_info,
                is_disc=False,
                auto_mode=self.auto_mode,
                media_info_video_track=media_info_video_track,
            )
            if dv is not None:
                self.torrent_info["dv"] = dv
            if hdr is not None:
                self.torrent_info["hdr"] = hdr
            self.torrent_info["pymediainfo_video_codec"] = pymediainfo_video_codec

            if video_codec != pymediainfo_video_codec:
                logging.error(
                    f"[BasicUtils] Regex extracted video_codec [{video_codec}] and pymediainfo "
                    f"extracted video_codec [{pymediainfo_video_codec}] doesn't match!!"
                )
                logging.info(
                    "[BasicUtils] If `--force_pymediainfo` or `-fpm` is provided as argument, PyMediaInfo video_codec "
                    "will be used, else regex extracted video_codec will be used"
                )
            return (
                pymediainfo_video_codec if self.args.force_pymediainfo else video_codec
            )

    # -------------- END of analyze_video_file --------------

    # ---------------------------------------------------------------------- #
    #                      Analysing miscellaneous details!                  #
    # ---------------------------------------------------------------------- #
    def identify_miscellaneous_details(self, guess_it_result, file_to_parse):
        """
        This function is dedicated to analyzing the filename and extracting snippets such as "repack, "DV", "AMZN", etc
        Depending on what the "source" is we might need to search for a "web source" (amzn, nf, hulu, etc)

        We also search for "editions" here, this info is typically made known in the filename so we can use some simple regex to extract it
        (e.g. extended, Criterion, directors, etc)
        """
        logging.debug(
            "[MiscellaneousDetails] Trying to identify miscellaneous details for torrent."
        )

        # ------ Specific Source info ------ #
        if "source_type" not in self.torrent_info:
            self.torrent_info["source_type"] = MiscellaneousUtils.identify_source_type(
                self.torrent_info["raw_file_name"],
                self.auto_mode,
                self.torrent_info["source"],
            )

        # ------ WEB streaming service stuff here ------ #
        if self.torrent_info["source"] == "Web":
            # TODO check whether None needs to be set as `web_source`
            (
                self.torrent_info["web_source"],
                self.torrent_info["web_source_name"],
            ) = MiscellaneousUtils.identify_web_streaming_source(
                STREAMING_SERVICES_MAP.format(base_path=self.working_folder),
                STREAMING_SERVICES_REVERSE_MAP.format(base_path=self.working_folder),
                self.torrent_info["raw_file_name"],
                guess_it_result,
            )

        # --- Custom & extra info --- #
        # some torrents have 'extra' info in the title like 'repack', 'DV', 'UHD', 'Atmos', 'remux', etc
        # We simply use regex for this and will add any matches to the dict 'torrent_info', later when building the final title we add any matches (if they exist) into the title
        # repacks
        self.torrent_info["repack"] = MiscellaneousUtils.identify_repacks(
            self.torrent_info["raw_file_name"]
        )

        # --- Bluray disc type --- #
        if self.torrent_info["source_type"] == "bluray_disc":
            self.torrent_info["bluray_disc_type"] = (
                MiscellaneousUtils.identify_bluray_disc_type(
                    self.torrent_info["screen_size"], self.torrent_info["upload_media"]
                )
            )

        # Bluray disc regions
        # Regions are read from new json file
        bluray_regions = json.load(
            open(BLURAY_REGIONS_MAP.format(base_path=self.working_folder))
        )

        # Try to split the torrent title and match a few key words
        # End user can add their own 'key_words' that they might want to extract and add to the final torrent title
        key_words = {
            "remux": "REMUX",
            "hdr": self.torrent_info.get("hdr", "HDR"),
            "uhd": "UHD",
            "hybrid": "Hybrid",
            "atmos": "Atmos",
            "ddpa": "Atmos",
        }

        hdr_hybrid_remux_keyword_search = (
            str(self.torrent_info["raw_file_name"])
            .lower()
            .replace(" ", ".")
            .replace("-", ".")
            .split(".")
        )

        for word in hdr_hybrid_remux_keyword_search:
            word = str(word)
            if word in key_words:
                logging.info(f"extracted the key_word: {word} from the filename")
                # special case. TODO find a way to generalize and handle this
                if word == "ddpa":
                    self.torrent_info["atmos"] = key_words[word]
                else:
                    self.torrent_info[word] = key_words[word]

            # Bluray region source
            if "disc" in self.torrent_info["source_type"]:
                # This is either a bluray or dvd disc, these usually have the source region in the filename, try to extract it now
                if word.upper() in bluray_regions.keys():
                    self.torrent_info["region"] = word.upper()

            # Dolby vision (filename detection)
            # we only need to do this if user is having an older version of mediainfo, which can't detect dv
            if (
                "dv" not in self.torrent_info
                or self.torrent_info["dv"] is None
                or len(self.torrent_info["dv"]) < 1
            ):
                if any(x == word for x in ["dv", "dovi"]):
                    logging.info("Detected Dolby Vision from the filename")
                    self.torrent_info["dv"] = "DV"

        # trying to check whether Do-Vi exists in the title, again needed only for older versions of mediainfo
        if (
            "dv" not in self.torrent_info
            or self.torrent_info["dv"] is None
            or len(self.torrent_info["dv"]) < 1
        ):
            if (
                "do" in hdr_hybrid_remux_keyword_search
                and "vi" in hdr_hybrid_remux_keyword_search
            ):
                self.torrent_info["dv"] = "DV"
                logging.info(
                    "Adding Do-Vi from file name. Marking existing of Dolby Vision"
                )

        # use regex (sourced and slightly modified from official radarr repo) to find torrent editions
        # (Extended, Criterion, Theatrical, etc)
        # https://github.com/Radarr/Radarr/blob/5799b3dc4724dcc6f5f016e8ce4f57cc1939682b/src/NzbDrone.Core/Parser/Parser.cs#L21
        self.torrent_info["edition"] = MiscellaneousUtils.identify_bluray_edition(
            self.torrent_info["upload_media"]
        )

        # --------- Fix scene group tags --------- # Whilst most scene group names are just capitalized but
        # occasionally as you can see ^^ some are not (e.g. KOGi) either way we don't want to be capitalizing
        # everything (e.g. we want 'NTb' not 'NTB') so we still need a dict of scene groups and their proper
        # capitalization
        if "release_group" in self.torrent_info:
            (
                scene,
                release_group,
            ) = MiscellaneousUtils.perform_scene_group_capitalization(
                SCENE_GROUPS_MAP.format(base_path=self.working_folder),
                self.torrent_info,
            )
            self.torrent_info["release_group"] = release_group
            self.torrent_info["scene"] = scene

        # --------- SD? --------- #
        res = re.sub("[^0-9]", "", self.torrent_info["screen_size"])
        if int(res) < 720:
            self.torrent_info["sd"] = 1

        # --------- Dual Audio / Multi / Commentary --------- #
        media_info_result = BasicUtils().basic_get_mediainfo(file_to_parse)
        original_language = (
            self.torrent_info["tmdb_metadata"]["original_language"]
            if self.torrent_info["tmdb_metadata"] is not None
            else ""
        )
        (
            dual,
            multi,
            commentary,
        ) = MiscellaneousUtils.fill_dual_multi_and_commentary(
            original_language, media_info_result.audio_tracks
        )
        self.torrent_info["dualaudio"] = dual
        self.torrent_info["multiaudio"] = multi
        self.torrent_info["commentary"] = commentary
        # --------- Dual Audio / Dubbed / Multi / Commentary --------- #

        (
            self.torrent_info["language_str"],
            self.torrent_info["language_str_if_foreign"],
        ) = MiscellaneousUtils.get_upload_original_language_title(
            self.torrent_info["tmdb_metadata"]
        )

        # Video container information
        self.torrent_info["container"] = os.path.splitext(
            self.torrent_info.get("raw_video_file", self.torrent_info["upload_media"])
        )[1]

        # Video container information

        # Video bit-depth information
        self.torrent_info["bit_depth"] = MiscellaneousUtils.get_bit_depth(
            media_info_result.video_tracks[0]
        )
        # Video bit-depth information

        # Detecting Anamorphic Video
        MiscellaneousUtils.detect_anamorphic_video_and_pixel_ratio(
            media_info_result.video_tracks[0]
        )
        # Detecting Anamorphic Video

    # -------------- END of identify_miscellaneous_details --------------

    # ---------------------------------------------------------------------- #
    #                             Torrent Processor!                         #
    # ---------------------------------------------------------------------- #
    def _process_torrent(self, torrent: Dict):
        # for each completed torrents we start the processing
        logging.info(
            f'[Main] Starting processing of torrent {torrent["name"]} from path {torrent["save_path"]}'
        )

        cached_data: Dict = self.reupload_manager.get_cached_data(torrent["hash"])
        logging.debug(
            f"[Main] Cached data obtained from cache for torrent {torrent['hash']}: {pformat(cached_data)}"
        )

        if cached_data is None:
            # Initializing the torrent data to cache
            cached_data: Dict = self.reupload_manager.initialize_torrent(torrent)
        else:
            logging.info(
                f"[Main] Cached data found for torrent with hash {torrent['hash']}"
            )
            if self.reupload_manager.skip_reupload(cached_data):
                logging.info(
                    f"[Main] Skipping upload and processing of torrent {cached_data['name']} since retry limit has exceeded"
                )
                return

        # dynamic_tracker_selection
        target_trackers = self.reupload_manager.get_trackers_dynamically(
            torrent=torrent,
            original_upload_to_trackers=self.upload_to_trackers,
            api_keys_dict=self.api_keys_dict,
            all_trackers_list=self.acronym_to_tracker.keys(),
        )
        for tracker in self.blacklist_trackers:
            if tracker not in target_trackers:
                continue
            target_trackers.remove(tracker)
            console.print(
                f"[red bold] Uploading to [yellow]{tracker}[/yellow] not supported in GGBOT Auto ReUploader"
            )

        logging.info(
            f"[Main] Trackers this torrent needs to be uploaded to are {target_trackers}"
        )

        # before we start doing anything we need to check whether the media file can be accessed by the uploader.
        # to check whether the file is accessible we need to adhere to any path translations that user want to do
        torrent_path: str = self.reupload_manager.translate_torrent_path(
            torrent["content_path"]
        )

        self.torrent_info.clear()

        # This list will contain tags that are applicable to the torrent being uploaded.
        # The tags that are generated will be based on the media properties and tag groupings from `tag_grouping.json`
        # TODO: move these to a new metadata object
        self.torrent_info["tag_grouping"] = json.load(
            open(TAG_GROUPINGS.format(base_path=self.working_folder))
        )
        self.torrent_info["argument_tags"] = GenericUtils.add_argument_tags(
            self.args.tags
        )
        self.torrent_info["tags"] = []

        # Remove all old temp_files & data from the previous upload
        self.torrent_info["working_folder"] = GenericUtils().delete_leftover_files(
            self.working_folder, file=torrent_path, resume=False
        )
        self.torrent_info["cookies_dump"] = self.cookies_dump
        self.torrent_info["base_working_folder"] = self.working_folder
        self.torrent_info["absolute_working_folder"] = (
            f"{WORKING_DIR.format(base_path=self.working_folder)}{self.torrent_info['working_folder']}"
        )

        console.print(
            f"Re-Uploading File/Folder: [bold][blue]{torrent_path}[/blue][/bold]"
        )

        rar_file_validation_response = GenericUtils.check_for_dir_and_extract_rars(
            torrent_path
        )
        if not rar_file_validation_response[0]:
            # status is False, due to some error and hence we'll skip this upload
            # Skip this entire 'file upload' & move onto the next (if exists)
            self.reupload_manager.mark_torrent_failure(
                torrent["hash"], status=TorrentFailureStatus.RAR_EXTRACTION_FAILED
            )
            return

        self.torrent_info["upload_media"] = rar_file_validation_response[1]

        guess_it_result = GenericUtils.perform_guessit_on_filename(
            self.torrent_info["upload_media"]
        )

        nfo = glob.glob(f"{self.torrent_info['upload_media']}/*.nfo")
        if nfo and len(nfo) > 0:
            self.torrent_info["nfo_file"] = nfo[0]

        # File we're uploading
        console.print(
            f"Uploading File/Folder: [bold][blue]{torrent_path}[/blue][/bold]"
        )
        # -------- Basic info --------
        # So now we can start collecting info about the file/folder that was supplied to us (Step 1)
        # this guy will also try to set tmdb and imdb from media info summary
        if (
            self.identify_type_and_basic_info(
                self.torrent_info["upload_media"], guess_it_result
            )
            == "skip_to_next_file"
        ):
            # If there is an issue with the file & we can't upload we use this check to skip the current file & move
            # on to the next (if exists)
            logging.debug(
                f"[Main] Skipping {self.torrent_info['upload_media']} because type and basic information cannot be "
                f"identified. "
            )
            self.reupload_manager.mark_torrent_failure(
                torrent["hash"],
                status=TorrentFailureStatus.TYPE_AND_BASIC_INFO_ERROR,
            )
            return

        # the metadata items will be first obtained from cached_data. if it's not available then we'll go ahead with
        # mediainfo_summary data and tmdb search
        movie_db = self.reupload_manager.cached_moviedb_details(
            cached_data,
            self.torrent_info["title"],
            self.torrent_info["year"] if "year" in self.torrent_info else "",
            self.torrent_info["type"],
        )

        metadata_tmdb = self.reupload_manager.get_external_moviedb_id(
            movie_db, self.torrent_info, cached_data, "tmdb"
        )
        metadata_imdb = self.reupload_manager.get_external_moviedb_id(
            movie_db, self.torrent_info, cached_data, "imdb"
        )
        metadata_tvmaze = self.reupload_manager.get_external_moviedb_id(
            movie_db, self.torrent_info, cached_data, "tvmaze"
        )

        # tmdb, imdb and tvmaze in torrent_info will be filled by this method
        possible_matches = metadata_utilities.fill_database_ids(
            self.torrent_info,
            [metadata_tmdb],
            [metadata_imdb],
            [metadata_tvmaze],
            self.auto_mode,
        )

        if (
            self.torrent_info["tmdb"] == "0"
            and self.torrent_info["imdb"] == "0"
            and self.torrent_info["tvmaze"] == "0"
        ):
            # here we couldn't select a tmdb id automatically / no results from tmdb. Hence we mark this as a special
            # case and stop the upload of the torrent updating the overall status of the torrent
            logging.error("[Main] Marking upload as TMDB Identification failed.")
            self.reupload_manager.update_torrent_field(
                torrent["hash"], "possible_matches", possible_matches, True
            )
            self.reupload_manager.mark_torrent_failure(
                torrent["hash"],
                status=TorrentFailureStatus.TMDB_IDENTIFICATION_FAILED,
            )
            return
        else:
            logging.info(
                "[Main] Obtained metadata database ids. Proceeding with upload process"
            )

        original_title = self.torrent_info["title"]
        original_year = self.torrent_info["year"] if "year" in self.torrent_info else ""

        # -------- Use official info from TMDB --------
        (
            title,
            year,
            tvdb,
            mal,
        ) = metadata_utilities.metadata_compare_tmdb_data_local(self.torrent_info)
        self.torrent_info["title"] = title
        if year is not None:
            self.torrent_info["year"] = year
        # TODO try to move the tvdb and mal identification along with `metadata_get_external_id`
        self.torrent_info["tvdb"] = tvdb
        self.torrent_info["mal"] = mal

        # saving the updates to moviedb in cache
        self.reupload_manager.cache_moviedb_data(
            movie_db,
            self.torrent_info,
            torrent["hash"],
            original_title,
            original_year,
        )

        # -------- Fix/update values --------
        # set the correct video & audio codecs (Dolby Digital --> DDP, use x264 if encode vs remux etc)
        self.identify_miscellaneous_details(
            guess_it_result,
            self.torrent_info.get("raw_video_file", self.torrent_info["upload_media"]),
        )

        # Fix some default naming styles
        translation_utilities.fix_default_naming_styles(self.torrent_info)

        # -------- Dupe check for single tracker uploads -------- If user has provided only one Tracker to upload to,
        # then we do dupe check prior to taking screenshots. [if dupe_check is enabled] If there are duplicates in
        # the tracker, then we do not waste time taking and uploading screenshots.
        if self.reuploader_config.CHECK_FOR_DUPES and len(target_trackers) == 1:
            tracker = target_trackers[0]
            temp_tracker_api_key = self.api_keys_dict[f"{str(tracker).lower()}_api_key"]

            console.line(count=2)
            console.rule(
                f"Dupe Check [bold]({tracker})[/bold]",
                style="red",
                align="center",
            )

            dupe_check_response = self.check_for_dupes_in_tracker(
                tracker, temp_tracker_api_key
            )
            # If dupes are present and user decided to stop upload, for single tracker uploads we stop operation
            # immediately True == dupe_found False == no_dupes/continue upload
            if dupe_check_response:
                logging.warning(
                    f"[Main] Could not upload to: {tracker} because we found a dupe on site"
                )
                logging.info(
                    "[Main] Marking this torrent as dupe check failed in cache"
                )
                self.reupload_manager.mark_torrent_failure(
                    torrent["hash"], status=TorrentFailureStatus.DUPE_CHECK_FAILED
                )
                console.print(
                    "Dupe check failed. skipping this torrent upload..\n",
                    style="bold red",
                    highlight=False,
                )
                return

        # -------- Take / Upload Screenshots --------
        upload_media_for_screenshot = self.torrent_info.get(
            "raw_video_file", self.torrent_info["upload_media"]
        )

        media_info_duration = MediaInfo.parse(upload_media_for_screenshot).tracks[1]
        self.torrent_info["duration"] = str(media_info_duration.duration).split(".", 1)[
            0
        ]

        # This is used to evenly space out timestamps for screenshots
        # Call function to actually take screenshots & upload them (different file)

        is_screenshots_available = GGBotScreenshotManager(
            duration=self.torrent_info["duration"],
            torrent_title=self.torrent_info["title"],
            upload_media=upload_media_for_screenshot,
            base_path=self.working_folder,
            hash_prefix=self.torrent_info["working_folder"],
            skip_screenshots=self.args.skip_screenshots,
        ).generate_screenshots()

        if is_screenshots_available:
            screenshots_data = json.load(
                open(
                    SCREENSHOTS_RESULT_FILE_PATH.format(
                        base_path=self.working_folder,
                        sub_folder=self.torrent_info["working_folder"],
                    )
                )
            )
            screenshots_data_types = {
                "bbcode_images": screenshots_data["bbcode_images"],
                "bbcode_images_nothumb": screenshots_data["bbcode_images_nothumb"],
                "bbcode_thumb_nothumb": screenshots_data["bbcode_thumb_nothumb"],
                "url_images": screenshots_data["url_images"],
                "data_images": screenshots_data["data_images"],
            }
            self.torrent_info["screenshots_data_types"] = screenshots_data_types
            # TODO: check whether the below can be removed.
            self.torrent_info["bbcode_images"] = screenshots_data["bbcode_images"]
            self.torrent_info["bbcode_images_nothumb"] = screenshots_data[
                "bbcode_images_nothumb"
            ]
            self.torrent_info["bbcode_thumb_nothumb"] = screenshots_data[
                "bbcode_thumb_nothumb"
            ]
            self.torrent_info["url_images"] = screenshots_data["url_images"]
            self.torrent_info["data_images"] = screenshots_data["data_images"]
            self.torrent_info["screenshots_data"] = SCREENSHOTS_RESULT_FILE_PATH.format(
                base_path=self.working_folder,
                sub_folder=self.torrent_info["working_folder"],
            )

        # At this point the only stuff that remains to be done is site specific so we can start a loop here for each
        # site we are uploading to
        logging.info("[Main] Now starting tracker specific tasks")
        tracker_status_map: Dict[str, Tuple[TrackerUploadStatus, Union[Dict, Any]]] = {
            trkr: (TrackerUploadStatus.PENDING, None) for trkr in target_trackers
        }
        for current_tracker in target_trackers:
            tracker_status_map[current_tracker] = self._upload_to_tracker(
                tracker=current_tracker,
                target_trackers=target_trackers,
                torrent=torrent,
            )

        # saving tracker status to job repo and updating torrent status
        self.reupload_manager.update_jobs_and_torrent_status(
            torrent["hash"], tracker_status_map
        )
        # updating torrent label in torrent client
        self.torrent_client.update_torrent_category(
            info_hash=torrent["hash"],
            category_name=self.reupload_manager.get_client_label_for_torrent(
                tracker_status_map
            ),
        )

        # -------------- END of _process_torrent --------------

    @staticmethod
    def _initialize_cache(reuploader_config: ReUploaderConfig) -> Cache:
        logging.info(
            "[GGBotReUploader] Going to establish connection to the cache server configured"
        )

        # creating an instance of cache based on the users configuration
        # TODO if user hasn't provided any configuration then we need to use some other means to keep track
        # of these metadata
        # getting an instance of the torrent client factory
        cache_factory = CacheFactory()
        # creating the cache client using the factory based on the users configuration
        cache: Cache = cache_factory.create(CacheVendor[reuploader_config.CACHE])
        # checking whether the cache connection has been created successfully or not
        cache.hello()
        logging.info(
            "[GGBotReUploader] Successfully established connection to the cache server configured"
        )
        return cache

    @staticmethod
    def _initialize_torrent_client(
        reuploader_config: ReUploaderConfig,
    ) -> TorrentClient:
        logging.info(
            "[GGBotReUploader] Going to establish connection to the torrent client configured"
        )
        # getting an instance of the torrent client factory
        torrent_client_factory = TorrentClientFactory()
        # creating the torrent client using the factory based on the users configuration
        torrent_client: TorrentClient = torrent_client_factory.create(
            Clients[reuploader_config.TORRENT_CLIENT]
        )
        # checking whether the torrent client connection has been created successfully or not
        torrent_client.hello()
        logging.info(
            f"[GGBotReUploader] Successfully established connection to the torrent client {reuploader_config.TORRENT_CLIENT}"
        )
        return torrent_client

    @staticmethod
    def _initialize_sentry_sdk():
        sentry_config = SentryErrorTrackingConfig()
        if sentry_config.ENABLE_SENTRY_ERROR_TRACKING is False:
            return

        sentry_sdk.init(
            environment="production",
            server_name="GG Bot Auto Re-uploader",
            dsn="https://4093e406eb754b20a2a7f6d15e6b34c0@ggbot.bot.nu/1",
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
            attach_stacktrace=True,
            shutdown_timeout=20,
            ignore_errors=SentryConfig.sentry_ignored_errors(),
            before_send=SentryConfig.before_send,
        )

    @staticmethod
    def _read_system_arguments_config(config_file: str):
        arg_config_reader = GGBotArgReader(config_file)
        parser = GGBotArgumentParser(arg_config_reader.read_and_get_config())
        return parser.parse_args()

    @staticmethod
    def _setup_loggers(*, args, working_folder):
        # Debug logs for the upload processing
        # Logger running in "w" : write mode
        logging.basicConfig(
            filename=REUPLOADER_LOG.format(base_path=working_folder),
            filemode="w",
            level=logging.INFO,
            format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        )

        # Disabling the logs from cinemagoer
        logging.getLogger("imdbpy").disabled = True
        logging.getLogger("imdbpy.parser").disabled = True
        logging.getLogger("imdbpy.parser.http").disabled = True
        logging.getLogger("imdbpy.parser.http.piculet").disabled = True
        logging.getLogger("imdbpy.parser.http.build_person").disabled = True

        if not args.debug:
            return

        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("torf").setLevel(logging.INFO)
        logging.getLogger("rebulk.rules").setLevel(logging.INFO)
        logging.getLogger("rebulk.rebulk").setLevel(logging.INFO)
        logging.getLogger("rebulk.processors").setLevel(logging.INFO)
        logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)
        logging.debug(
            f"[GGBotReUploader] Arguments provided by user for reupload: {args}"
        )

    @staticmethod
    def _display_banner():
        console.line(count=2)
        GenericUtils.display_banner("  Auto  ReUploader  ")
        console.line(count=1)


if __name__ == "__main__":
    reuploader: GGBotReUploader = GGBotReUploader()
    reuploader.run()
