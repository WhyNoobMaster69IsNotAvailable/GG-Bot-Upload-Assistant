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

import logging
import os.path
from pprint import pformat
from typing import Optional, Dict, List, Any

from modules.config import UploaderConfig
from modules.constants import DESCRIPTION_FILE_PATH
from modules.description.template_manager import GGBotJinjaTemplateManager
from modules.exceptions.exception import GGBotFatalException


class GGBotDescriptionManager:
    def __init__(
        self,
        *,
        working_folder: str,
        sub_folder: str,
        tracker: str,
        bbcode_line_break: str,
        debug: bool = False,
    ):
        self.tracker = tracker
        self.debug = debug
        self.bbcode_line_break = bbcode_line_break

        heart_emoji = (
            "<3"
            if str(self.tracker).upper() in ("BHD", "BHDTV") or os.name == "nt"
            else "❤"
        )
        self.description_file_data = {
            "custom_description_components": "",
            "internal": {
                "center_start": "[center]",
                "center_end": "[/center]",
                "uploader_signature": f"Uploaded with [color=red]{heart_emoji}[/color] using GG-BOT Upload Assistant",
                "screenshot_header": " ---------------------- [size=22]Screenshots[/size] ---------------------- ",
                "bbcode_line_break": bbcode_line_break,
            },
            "mediainfo": "",
            "screenshots": "",
        }

        self._description_file_path = self._format_description_file(
            working_folder=working_folder, sub_folder=sub_folder, tracker=tracker
        )
        self.template_manager: GGBotJinjaTemplateManager = GGBotJinjaTemplateManager(
            working_folder=working_folder, template_file_name=tracker
        )

    def get_description_file_path(self) -> str:
        return self._description_file_path

    @staticmethod
    def _format_description_file(
        *, working_folder: str, sub_folder: str, tracker: str
    ) -> str:
        if len(sub_folder) > 0 and sub_folder[-1:] != os.path.sep:
            raise GGBotFatalException(
                f"Invalid sub_folder path provided :- {sub_folder}"
            )

        return DESCRIPTION_FILE_PATH.format(
            base_path=working_folder, sub_folder=sub_folder, tracker=tracker
        )

    def render(self):
        description_file_contents = self.template_manager.render(
            data=self.description_file_data
        )
        with open(self._description_file_path, "w") as description:
            description.write(description_file_contents)

    def prepare_description_file(
        self,
        custom_user_inputs,
        tracker_description_components,
        screenshots_data_types,
        screenshot_type,
        mediainfo: str,
    ):
        # Just a cleanup to ensure that the description file doesn't exist
        if os.path.isfile(self._description_file_path):
            os.remove(self._description_file_path)

        # -------- Add custom descriptions to description.txt --------
        self.set_custom_user_inputs(
            custom_user_inputs=custom_user_inputs,
            tracker_description_components=tracker_description_components,
        )

        # -------- Add bbcode images to description.txt --------
        self.set_screenshots(
            screenshots_data_types=screenshots_data_types,
            screenshot_type=screenshot_type,
        )

        # -------- Add custom uploader signature to description.txt --------
        self.set_custom_uploader_signature()

        self.description_file_data["mediainfo"] = mediainfo

    def set_custom_uploader_signature(self):
        uploader_signature = UploaderConfig().SIGNATURE
        if uploader_signature is None or len(uploader_signature) == 0:
            logging.debug(
                "[GGBotDescriptionManager] User has not provided custom uploader signature."
            )
            return

        logging.debug(
            "[GGBotDescriptionManager] User has provided custom uploader signature to use."
        )
        # the user has provided a custom signature to be used. hence we'll use that.
        logging.debug(f"[Utils] User provided signature :: {uploader_signature}")
        if not uploader_signature.startswith(
            "[center]"
        ) and not uploader_signature.endswith("[/center]"):
            uploader_signature = f"[center]{uploader_signature}[/center]"

        self.description_file_data["internal"]["uploader_signature"] = (
            f"{uploader_signature}{self.bbcode_line_break}[center]Powered by GG-BOT Upload Assistant[/center]"
        )

    def set_screenshots(
        self,
        *,
        screenshots_data_types: Optional[Dict[str, str]],
        screenshot_type: Optional[str],
    ):
        if screenshots_data_types is None:
            logging.info(
                "[GGBotDescriptionManager] No screenshots available for description file"
            )
            return

        if screenshot_type is None or screenshot_type not in screenshots_data_types:
            logging.info(
                f"[GGBotDescriptionManager] Expected screenshot type [{screenshot_type}] not present in "
                f"torrent info. Skipping adding screenshots."
            )
            return

        self.description_file_data["screenshots"] = self._process_screenshot_type(
            screenshot_type=screenshot_type,
            screenshot_data=screenshots_data_types[screenshot_type],
        )

    @staticmethod
    def _process_screenshot_type(*, screenshot_type, screenshot_data) -> str:
        if screenshot_type != "url_images":
            return screenshot_data

        processed_url_screenshots = ""
        for screenshot in screenshot_data.split("\n"):
            if len(screenshot.strip()) == 0:
                continue
            processed_url_screenshots = (
                f"{processed_url_screenshots}[img]{screenshot}[/img]\n"
            )

        return processed_url_screenshots

    def set_custom_user_inputs(
        self,
        *,
        custom_user_inputs: Optional[List[Dict[str, Any]]],
        tracker_description_components: Optional[Dict],
    ):
        if custom_user_inputs is None:
            logging.info(
                "[GGBotDescriptionManager] No custom user inputs available for the upload"
            )
            return

        # we need to make sure that the tracker supports custom description for torrents.
        # If tracker supports custom descriptions, the the tracker config will have the `description_components` key.
        if tracker_description_components is None:
            logging.info(
                f"[GGBotDescriptionManager] Tracker [{self.tracker}] doesn't support custom descriptions. Skipping "
                f"custom description placements."
            )
            return

        logging.info(
            "[GGBotDescriptionManager] User has provided custom inputs for torrent description"
        )
        # here we iterate through all the custom inputs provided by the user then we check whether this component
        # is supported by the target tracker. If tracker supports it then the `key` will be present in the
        # tracker config.
        logging.debug(
            f"[GGBotDescriptionManager] Custom Message components configured for tracker {self.tracker} are {pformat(tracker_description_components)}"
        )
        custom_user_input_data = ""
        for custom_user_input in custom_user_inputs:
            # getting the component type
            logging.debug(
                f"[GGBotDescriptionManager] Custom input data {pformat(custom_user_input)}"
            )
            if custom_user_input["key"] not in tracker_description_components:
                logging.debug(
                    "[GGBotDescriptionManager] This type of component is not supported by the tracker. Writing input "
                    "to description as plain text"
                )
                # the provided component is not present in the trackers list. hence we adds this to the description
                # directly (plain text)
                custom_user_input_data = (
                    custom_user_input_data + custom_user_input["value"]
                )
            else:
                # provided component is present in the tracker list, so first we'll format the content to be added to
                # the tracker template
                input_wrapper_type = tracker_description_components[
                    custom_user_input["key"]
                ]
                logging.debug(
                    f"[GGBotDescriptionManager] Component wrapper :: `{input_wrapper_type}`"
                )
                formatted_value = custom_user_input["value"].replace(
                    "\\n", self.bbcode_line_break
                )
                # next we need to check whether the text component has any title
                if custom_user_input.get("title") is not None:
                    logging.debug(
                        "[GGBotDescriptionManager] User has provided a title for this component"
                    )
                    # if user has provided title, next we'll make sure that the tracker supports title for the component.
                    if "TITLE_PLACEHOLDER" in input_wrapper_type:
                        logging.debug(
                            f'[GGBotDescriptionManager] Adding title [{custom_user_input["title"].strip()}] to this component'
                        )
                        input_wrapper_type = input_wrapper_type.replace(
                            "TITLE_PLACEHOLDER",
                            custom_user_input["title"].strip(),
                        )
                    else:
                        logging.debug(
                            f'[GGBotDescriptionManager] Title is not supported for this component {custom_user_input["key"]} in this tracker {self.tracker}. Skipping title placement'
                        )
                # in cases where tracker supports title and user hasn't provided any title, we'll just remove the title placeholder
                # note that the = is intentional. since title would be [spoiler=TITLE]. we need to remove =TITLE
                # if title has already been replaced the below statement won't do anything
                input_wrapper_type = input_wrapper_type.replace(
                    "=TITLE_PLACEHOLDER", ""
                )

                if self.debug:  # just for debugging purposes
                    if "][" in input_wrapper_type:
                        logging.debug(
                            "[GGBotDescriptionManager] ][ is present in the wrapper type"
                        )
                    elif "><" in input_wrapper_type:
                        logging.debug(
                            "[GGBotDescriptionManager] >< is present in the wrapper type"
                        )
                    else:
                        logging.debug(
                            "[GGBotDescriptionManager] No special characters present in the wrapper type"
                        )
                    logging.debug(
                        f"[GGBotDescriptionManager] Wrapper type before formatting {input_wrapper_type}"
                    )

                if "][" in input_wrapper_type:
                    final_formatted_data = input_wrapper_type.replace(
                        "][", f"]{formatted_value}["
                    )
                elif "><" in input_wrapper_type:
                    final_formatted_data = input_wrapper_type.replace(
                        "><", f">{formatted_value}<"
                    )
                else:
                    final_formatted_data = formatted_value

                custom_user_input_data = custom_user_input_data + final_formatted_data
                logging.debug(
                    f"[GGBotDescriptionManager] Formatted value being appended to torrent description {final_formatted_data}"
                )

            custom_user_input_data = custom_user_input_data + self.bbcode_line_break

        self.description_file_data["custom_description_components"] = (
            custom_user_input_data
        )
