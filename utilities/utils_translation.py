# GG Bot Upload Assistant
# Copyright (C) 2022  Noob Master669
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import sys
from typing import Dict

from rich.console import Console

from modules.config import UploaderConfig
from modules.constants import WORKING_DIR
from utilities.utils import GenericUtils

console = Console()


def _identify_resolution_source(
    target_val, config, relevant_torrent_info_values, torrent_info
):
    # target_val is type (source) or resolution_id (resolution)
    possible_match_layer_1 = []
    for key in config["Required"][(config["translation"][target_val])]:
        # this key is the number provided under the target_val
        logging.debug(
            f"[ResolutionSourceMapping] Trying to match `{config['translation'][target_val]}` to configured key `{key}`"
        )

        total_num_of_required_keys = 0
        total_num_of_acquired_keys = 0

        # If we have a list of options to choose from, each match is saved here
        total_num_of_optionals_matched = 0
        optional_keys = []

        for sub_key, sub_val in config["Required"][(config["translation"][target_val])][
            key
        ].items():
            # for each sub key and its priority we
            logging.debug(
                f"[ResolutionSourceMapping] Considering item `{sub_key}` with priority `{sub_val}`"
            )
            # Sub-Key Priorities
            # ---------------------
            # 0 = optional
            # 1 = required
            # 2 = select from available items in list

            if sub_val == 1:
                total_num_of_required_keys += 1  # no of keys with priority 1 in config
                # Now check if the sub_key is in the relevant_torrent_info_values list
                if sub_key in str(relevant_torrent_info_values).lower():
                    total_num_of_acquired_keys += (
                        1  # no of keys with priority 1 identified
                    )
                    logging.debug(
                        f"[ResolutionSourceMapping] Required `{sub_key}` is present in relevant torrent info list. Considering key as acquired"
                    )
            elif sub_val == 2:
                if sub_key in str(relevant_torrent_info_values).lower():
                    total_num_of_optionals_matched += (
                        1  # indicates whether an optional key has been matched or not
                    )
                    logging.debug(
                        f"[ResolutionSourceMapping] SelectMultiple `{sub_key}` is present in relevant torrent info list. Considering key as acquired value"
                    )
                optional_keys.append(sub_key)  # number of optional keys configured

        logging.debug(
            f"[ResolutionSourceMapping] Total number of required keys: {total_num_of_required_keys}"
        )
        logging.debug(
            f"[ResolutionSourceMapping] Total number of acquired keys: {total_num_of_acquired_keys}"
        )
        logging.debug(f"[ResolutionSourceMapping] Optional keys: {optional_keys}")
        logging.debug(
            f"[ResolutionSourceMapping] Total number of optionals matched: {total_num_of_optionals_matched}"
        )

        if int(total_num_of_required_keys) == int(
            total_num_of_acquired_keys
        ):  # all required keys matched
            if len(optional_keys) > 0:
                if (
                    int(total_num_of_optionals_matched) > 0
                ):  # atlest one optional has been matched
                    logging.debug(
                        f'[ResolutionSourceMapping] Some {total_num_of_optionals_matched} of optional keys {optional_keys} were matched and no of required items and no of acquired items are equal. Hence considering key `{key}` as a match for `{config["translation"][target_val]}`'
                    )
                    possible_match_layer_1.append(key)
                else:  # required keys matched, but not optional keys
                    logging.debug(
                        f"[ResolutionSourceMapping] No optional keys {optional_keys} were matched."
                    )
            else:
                logging.debug(
                    f'[ResolutionSourceMapping] No of required items and no of acquired items are equal. Hence considering key `{key}` as a match for `{config["translation"][target_val]}`'
                )
                possible_match_layer_1.append(key)
            # We check for " == 0" so that if we get a profile that matches all the "1" then we can break immediately (2160p BD remux requires 'remux', '2160p', 'bluray')
            # so if we find all those values in optional_keys list then we can break
            # knowing that we hit 100% of the required values instead of having to cycle through the "optional" values and select one of them

            # Note: No idea what the below conditions are for. but it works
            # and if it ain't broken, don't fix it
            if len(optional_keys) == 0 and key != "other":
                break

            # TODO: try to find out in which scenario this condition gets satisfied
            if len(optional_keys) >= 2 and int(total_num_of_optionals_matched) == 1:
                break

        # We give higher priority to the non Other match
        # Removing other, if Other and another key was matched.
        if len(possible_match_layer_1) >= 2 and "Other" in possible_match_layer_1:
            possible_match_layer_1.remove("Other")

    # checking whether we were able to get a match in any of the configuration
    if len(possible_match_layer_1) == 1:
        val = possible_match_layer_1.pop()
        logging.debug(
            f'[ResolutionSourceMapping] Successfully matched one item for `{config["translation"][target_val]}` => `{val}`'
        )
        return val
    else:
        # this means we either have 2 potential matches or no matches at all (this happens if the media does not fit any of the allowed parameters)
        logging.critical(
            '[ResolutionSourceMapping] Unable to find a suitable "source" match for this file'
        )
        logging.error(
            "[ResolutionSourceMapping] Its possible that the media you are trying to upload is not allowed on site (e.g. DVDRip to BLU is not allowed)"
        )
        console.print(
            f'\nThis "Type" ([bold]{torrent_info["source"]}[/bold]) or this "Resolution" ([bold]{torrent_info["screen_size"]}[/bold]) is not allowed on this tracker',
            style="Red underline",
            highlight=False,
        )
        return "STOP"


def _get_hybrid_type(
    translation_value, tracker_settings, config, exit_program, torrent_info
):
    """
    Method to get a hybrid type from the source, resolution and type properties of the torrent
    """
    logging.info("[HybridMapping] Performing hybrid mapping now...")
    logging.debug("------------------ Hybrid mapping started ------------------")
    # logging all the Prerequisite data
    # if any of the Prerequisite data is not available, then this method will not be invoked
    for prerequisite in config["hybrid_mappings"][translation_value]["prerequisite"]:
        logging.info(
            f"[HybridMapping] Prerequisite :: '{prerequisite}' Value :: '{tracker_settings[prerequisite]}'"
        )

    for key in config["hybrid_mappings"][translation_value]["mapping"]:
        logging.debug(
            f"[HybridMapping] Trying to match '{translation_value}' to hybrid key '{key}'"
        )
        is_valid = None
        for sub_key, sub_val in config["hybrid_mappings"][translation_value]["mapping"][
            key
        ].items():
            if sub_key == "_comment":
                continue
            user_wants_negation = "not" in sub_val and sub_val["not"] is True
            if user_wants_negation:
                logging.debug(
                    f"[HybridMapping] The subkey '{sub_key}' from '{sub_val['data_source']}' must NOT be one of {sub_val['values']} for the mapping to be accepted."
                )
            else:
                logging.debug(
                    f"[HybridMapping] The subkey '{sub_key}' from '{sub_val['data_source']}' need to be one of {sub_val['values']} for the mapping to be accepted."
                )

            datasource = (
                tracker_settings
                if sub_val["data_source"] == "tracker"
                else torrent_info
            )
            if sub_key.startswith("$."):
                logging.info(
                    f"[HybridMapping] Identified json path '{sub_key}' as datasource key. Attempting to fetch data...`"
                )
                items = sub_key.replace("$.", "").split(".")
                try:
                    temp_datasource = datasource
                    for item in items:
                        temp_datasource = temp_datasource(item)
                        if temp_datasource is None:
                            selected_val = None
                            break
                    selected_val = temp_datasource
                except Exception as ex:
                    logging.error(
                        f"[HybridMapping] Invalid json path '{sub_key}' configured for hybrid mapping data key.",
                        exc_info=ex,
                    )
                    selected_val = None
            else:
                selected_val = datasource[sub_key] if sub_key in datasource else None

            logging.debug(
                f"[HybridMapping] Value selected from data source is '{selected_val}'"
            )
            if selected_val is not None:
                if len(sub_val["values"]) == 0:
                    logging.info(
                        f"[HybridMapping] For the subkey '{sub_key}' the values configured '{sub_val['values']}' is empty. Assuming by default as valid and continuing."
                    )
                    is_valid = True if is_valid is None else is_valid
                elif user_wants_negation and str(selected_val) not in sub_val["values"]:
                    logging.debug(
                        f"[HybridMapping] The subkey '{sub_key}' '{selected_val}' is not present in '{sub_val['values']}' for '{sub_key}' and '{key}'"
                    )
                    is_valid = True if is_valid is None else is_valid
                elif not user_wants_negation and str(selected_val) in sub_val["values"]:
                    logging.debug(
                        f"[HybridMapping] The subkey '{sub_key}' '{selected_val}' is present in '{sub_val['values']}' for '{sub_key}' and '{key}'"
                    )
                    is_valid = True if is_valid is None else is_valid
                elif (
                    sub_val["values"][0] == "IS_NOT_NONE_OR_IS_PRESENT"
                    and selected_val is not None
                    and len(str(selected_val)) > 0
                ):
                    logging.debug(
                        f"[HybridMapping] The subkey '{sub_key}' '{selected_val}' is present in '{sub_val['data_source']}' for '{sub_key}' and '{key}'"
                    )
                    is_valid = True if is_valid is None else is_valid
                else:
                    logging.debug(
                        f"[HybridMapping] The subkey '{sub_key}' '{selected_val}' is NOT present in '{sub_val['values']}' for '{sub_key}' and '{key}'"
                    )
                    is_valid = False
            else:
                is_valid = False
                logging.fatal(
                    f"[HybridMapping] Invalid configuration provided for hybrid key mapping. Key :: '{key}', sub key :: '{sub_key}', sub value :: '{sub_val}'"
                )

        if is_valid:
            logging.info(f"[HybridMapping] The hybrid key was identified to be '{key}'")
            logging.debug(
                "------------------ Hybrid mapping Completed ------------------"
            )
            # is_valid is true
            # all the categories match
            return key

    if config["hybrid_mappings"][translation_value]["required"] is False:
        # this hybrid mapping is optional. we can log this and return ""
        logging.info("[HybridMapping] Returning '' since this is an optional mapping.")
        logging.debug("------------------ Hybrid mapping Completed ------------------")
        return ""

    logging.debug(
        "------------------ Hybrid mapping Completed With ERRORS ------------------"
    )
    # this means we either have 2 potential matches or no matches at all (this happens if the media does not fit any of the allowed parameters)
    logging.critical(
        '[HybridMapping] Unable to find a suitable "hybrid mapping" match for this file'
    )
    logging.error(
        "[HybridMapping] Its possible that the media you are trying to upload is not allowed on site (e.g. DVDRip to BLU is not allowed)"
    )
    console.print(
        f"Failed to perform Hybrid Mapping for '{translation_value}'. This type of upload might not be allowed on this tracker.",
        style="Red underline",
    )
    if (
        exit_program
    ):  # TODO add check for required or optional. If required, then exit app
        sys.exit("Invalid hybrid mapping configuration provided.")
    return "HYBRID_MAPPING_INVALID_CONFIGURATION"


def should_delay_mapping(translation_value, prerequisites, tracker_settings):
    logging.info(
        f"[HybridMapping] Performing 'prerequisite' validation for '{translation_value}'"
    )
    for prerequisite in prerequisites:
        if prerequisite not in tracker_settings:
            logging.info(
                f"[HybridMapping] The prerequisite '{prerequisite}' for '{translation_value}' is not available currently. "
                + "Skipping hybrid mapping for now and proceeding with remaining translations..."
            )
            return True
    return False


def perform_delayed_hybrid_mapping(
    config, tracker_settings, torrent_info, exit_program
):
    no_of_hybrid_mappings = len(config["hybrid_mappings"].keys())
    logging.info(
        f"[HybridMapping] Performing hybrid mapping after all translations have completed. No of hybrid mappings :: '{no_of_hybrid_mappings}'"
    )

    for _ in range(0, no_of_hybrid_mappings):
        for translation_value in config["hybrid_mappings"].keys():
            # check whether the particular field can be undergoing hybrid mapping
            delay_mapping = should_delay_mapping(
                translation_value=translation_value,
                prerequisites=config["hybrid_mappings"][translation_value][
                    "prerequisite"
                ],
                tracker_settings=tracker_settings,
            )
            if translation_value not in tracker_settings and not delay_mapping:
                tracker_settings[translation_value] = _get_hybrid_type(
                    translation_value=translation_value,
                    tracker_settings=tracker_settings,
                    config=config,
                    exit_program=exit_program,
                    torrent_info=torrent_info,
                )


# ---------------------------------------------------------------------- #
#           !!! WARN !!! This Method has side effects. !!! WARN !!!
# ---------------------------------------------------------------------- #
def __create_imdb_without_tt_key(torrent_info):
    torrent_info["imdb_with_tt"] = torrent_info["imdb"]
    if len(torrent_info["imdb"]) >= 2:
        if str(torrent_info["imdb"]).startswith("tt"):
            torrent_info["imdb"] = str(torrent_info["imdb"]).replace("tt", "")
        else:
            torrent_info["imdb_with_tt"] = f'tt{torrent_info["imdb"]}'
    else:
        torrent_info["imdb"] = "0"
        torrent_info["imdb_with_tt"] = "0"


def __get_relevant_items_for_tracker_keys(torrent_info):
    relevant_torrent_info_values = []
    for relevant_items in ["source_type", "screen_size", "bluray_disc_type"]:
        if relevant_items in torrent_info:
            relevant_torrent_info_values.append(torrent_info[relevant_items])
    logging.debug(
        f"The relevant torrent info values for resolution / source identification are {relevant_torrent_info_values}"
    )
    return relevant_torrent_info_values


def _get_url_type_data(translation_key, torrent_info):
    url = ""
    if translation_key == "imdb":
        url = f"https://www.imdb.com/title/{torrent_info['imdb_with_tt']}"
    elif translation_key == "tmdb":
        url = f"https://www.themoviedb.org/{'movie' if torrent_info['type'] == 'movie' else 'tv'}/{torrent_info['tmdb']}"
    elif translation_key == "tvdb" and torrent_info["type"] == "episode":
        url = f"https://www.thetvdb.com/?tab=series&id={torrent_info['tvdb']}"
    elif translation_key == "mal":
        url = f"https://myanimelist.net/anime/{torrent_info['mal']}"
    elif translation_key == "tvmaze" and torrent_info["type"] == "episode":
        url = f"https://www.tvmaze.com/shows/{torrent_info['tvmaze']}"
    else:
        logging.error(
            f"[Translation] Invalid key for url translation provided -- Key {translation_key}"
        )
    logging.debug(f"[Translation] Created url type data for {translation_key} as {url}")
    return url


def _get_bluray_region(optional_value, region_from_torrent_info):
    for region in optional_value:
        if str(region).upper() == str(region_from_torrent_info).upper():
            return region
    return None


# ---------------------------------------------------------------------- #
#           !!! WARN !!! This Method has side effects. !!! WARN !!!
# ---------------------------------------------------------------------- #
def _validate_and_do_hybrid_mapping(
    translation_value,
    config,
    tracker_settings,
    torrent_info,
    is_hybrid_translation_needed,
):
    logging.info(
        f"[HybridMapping] Identified 'hybrid_type' for tracker attribute '{translation_value}'"
    )
    logging.info(
        f"[HybridMapping] Validating the hybrid mapping settings for '{translation_value}'"
    )
    if "hybrid_mappings" in config and translation_value in config["hybrid_mappings"]:
        delayed_mapping = False
        # to do hybrid translation we might need certain prerequisite fields to be resolved before hand in tracker settings.
        # we first check whether they have been resolved or not.
        # If those values have been resolved then we can just call the `_get_hybrid_type` to resolve it.
        # otherwise we mark the present of this hybrid type and do the mapping after all required and optional
        # value mapping have been completed.
        # prerequisite needed only for tracker_settings. Not for torrent_info data
        if "prerequisite" in config["hybrid_mappings"][translation_value]:
            delayed_mapping = should_delay_mapping(
                translation_value=translation_value,
                prerequisites=config["hybrid_mappings"][translation_value][
                    "prerequisite"
                ],
                tracker_settings=tracker_settings,
            )
            is_hybrid_translation_needed = (
                delayed_mapping
                if is_hybrid_translation_needed is False
                else is_hybrid_translation_needed
            )
        else:
            logging.info(
                f"[HybridMapping] No 'prerequisite' required for '{translation_value}'"
            )

        if delayed_mapping:
            return True, is_hybrid_translation_needed

        logging.info(
            f"[HybridMapping] Going to perform hybrid mapping for :: '{translation_value}'"
        )
        tracker_settings[translation_value] = _get_hybrid_type(
            translation_value=translation_value,
            tracker_settings=tracker_settings,
            config=config,
            exit_program=True,
            torrent_info=torrent_info,
        )
    else:
        logging.error(
            f"[HybridMapping] No hybrid mapping configurations provided for '{translation_value}'."
            + "\nFor all `hybrid_type` hybrid mapping is required irrepective whether the value is required or optional."
        )
        sys.exit("Invalid hybrid mapping configuration provided.")
    return False, is_hybrid_translation_needed


# ---------------------------------------------------------------------- #
#                  Set correct tracker API Key/Values                    #
# ---------------------------------------------------------------------- #
# ---------------------------------------------------------------------- #
#           !!! WARN !!! This Method has side effects. !!! WARN !!!
# ---------------------------------------------------------------------- #
def choose_right_tracker_keys(
    config, tracker_settings, tracker, torrent_info, args, working_folder
):
    required_items = config["Required"]
    optional_items = config["Optional"]

    # BLU requires the IMDB with the "tt" removed so we do that here, BHD will automatically put the "tt" back in... so we don't need to make an exception for that
    if "imdb" in torrent_info:
        __create_imdb_without_tt_key(torrent_info)

    # torrent title
    tracker_settings[config["translation"]["torrent_title"]] = torrent_info[
        "torrent_title"
    ]

    # Save a few key values in a list that we'll use later to identify the resolution and type
    relevant_torrent_info_values = __get_relevant_items_for_tracker_keys(torrent_info)

    # Filling in data for all the keys that have mapping/translations
    # Here we iterate over the translation mapping and for each translation key, we check the required and optional items for that value
    # once identified we handle it
    logging.info(
        "[Translation] Starting translations from torrent info to tracker settings."
    )
    is_hybrid_translation_needed = False
    hybrid_translation_keys = []
    for translation_key, translation_value in config["translation"].items():
        logging.debug(
            f"[Translation] Trying to translate {translation_key} to {translation_value}"
        )

        # ------------ required_items start ------------
        for required_key, required_value in required_items.items():
            # get the proper mapping, the elements that doesn't match can be ignored
            if str(required_key) == str(translation_value):
                # hybrid_type is managed by hybrid_mapping.
                if required_value == "hybrid_type":
                    break

                logging.debug(
                    f"[Translation] Key {translation_key} mapped to required item {required_key} with value type as {required_value}"
                )

                # the torrent file is always submitted as a file
                if required_value in (
                    "file",
                    "file|base64",
                    "file|array",
                    "file|string|array",
                ):
                    # adding support for base64 encoded files
                    # the actual encoding will be performed in `upload_to_site` method
                    if translation_key in torrent_info:
                        tracker_settings[config["translation"][translation_key]] = (
                            torrent_info[translation_key]
                        )
                    # Make sure you select the right .torrent file
                    if translation_key == "dot_torrent":
                        tracker_settings[config["translation"]["dot_torrent"]] = (
                            f'{WORKING_DIR.format(base_path=working_folder)}{torrent_info["working_folder"]}{tracker}-{GenericUtils.normalize_for_system_path(torrent_info["torrent_title"])}.torrent'
                        )

                # The reason why we keep this elif statement here is because the conditional right above is also technically a "string"
                # but its easier to keep mediainfo and description in text files until we need them so we have that small exception for them
                elif required_value in ("string", "string|array"):
                    # BHD requires the key "live" (0 = Sent to drafts and 1 = Live on site)
                    if required_key == "live":
                        # BHD Live/Draft
                        # TODO: move this to a BHD custom action
                        live = "1" if UploaderConfig().BHD_LIVE else "0"
                        logging.info(
                            f"Upload live status: {'Live (Visible)' if UploaderConfig().BHD_LIVE else 'Draft (Hidden)'}"
                        )
                        tracker_settings[config["translation"][translation_key]] = live

                    # If the user supplied the "-anon" argument then we want to pass that along when uploading
                    elif translation_key == "anon":
                        if args.anon:
                            logging.info("[Translation] Uploading anonymously")
                            tracker_settings[config["translation"][translation_key]] = (
                                "1"
                            )
                        else:
                            tracker_settings[config["translation"][translation_key]] = (
                                "0"
                            )

                    elif translation_key == "freeleech":
                        tracker_settings[config["translation"][translation_key]] = (
                            "100" if getattr(args, "freeleech", False) is True else "0"
                        )

                    # Adding support for internal args
                    elif translation_key in [
                        "doubleup",
                        "featured",
                        "personal",
                        "internal",
                        "sticky",
                        "tripleup",
                        "foreign",
                        "3d",
                    ]:
                        tracker_settings[config["translation"][translation_key]] = (
                            "1"
                            if getattr(args, translation_key, False) is True
                            else "0"
                        )
                    elif translation_key in ["exclusive"]:
                        arg_value = getattr(args, translation_key, None)
                        tracker_settings[config["translation"][translation_key]] = (
                            arg_value[0] if arg_value is not None else "0"
                        )

                    # We dump all the info from torrent_info in tracker_settings here
                    elif translation_key in torrent_info:
                        tracker_settings[config["translation"][translation_key]] = (
                            torrent_info[translation_key]
                        )
                    # This work as a sort of 'catch all', if we don't have the correct data in torrent_info, we just send a 0 so we can successfully post
                    else:
                        tracker_settings[config["translation"][translation_key]] = "0"

                elif required_value == "url":
                    # we need this check because some trackers accepts media database urls from the same key, thereby overwriting the previous data
                    if (
                        config["translation"][translation_key] not in tracker_settings
                        or len(tracker_settings[config["translation"][translation_key]])
                        == 0
                    ):
                        # URLs can be set only to for certain media databases
                        tracker_settings[config["translation"][translation_key]] = (
                            _get_url_type_data(translation_key, torrent_info)
                        )
                else:
                    logging.error(
                        f"[Translation] Invalid value type {required_value} configured for required item {required_key} with translation key {required_key}"
                    )

                # Set the category ID, this could be easily hardcoded in (1=movie & 2=tv) but I chose to use JSON data just in case a future tracker switches this up
                if translation_key == "type":
                    for key_cat, val_cat in config["Required"][required_key].items():
                        if torrent_info["type"] == val_cat:
                            tracker_settings[config["translation"][translation_key]] = (
                                key_cat
                            )
                        elif val_cat in torrent_info and torrent_info[val_cat] == "1":
                            # special case whether we can check for certain values in torrent info to decide the type
                            # eg: complete_season, individual_episodes etc
                            tracker_settings[config["translation"][translation_key]] = (
                                key_cat
                            )

                    if config["translation"][translation_key] not in tracker_settings:
                        # this type of upload is not permitted in this tracker
                        logging.critical(
                            '[Translation] Unable to find a suitable "category/type" match for this file'
                        )
                        logging.error(
                            "[Translation] Its possible that the media you are trying to upload is not allowed on site (e.g. DVDRip to BLU is not allowed"
                        )
                        console.print(
                            f'\nThis "Category" ([bold]{torrent_info["type"]}[/bold]) is not allowed on this tracker',
                            style="Red underline",
                            highlight=False,
                        )
                        return "STOP"

                if translation_key in ("source", "resolution", "resolution_id"):
                    return_value = _identify_resolution_source(
                        target_val=translation_key,
                        config=config,
                        relevant_torrent_info_values=relevant_torrent_info_values,
                        torrent_info=torrent_info,
                    )
                    if return_value == "STOP":
                        return return_value
                    tracker_settings[config["translation"][translation_key]] = (
                        return_value
                    )
        # ------------ required_items end ------------

        # ------------ optional_items start ------------
        # This mainly applies to BHD since they are the tracker with the most 'Optional' fields,
        # BLU/ACM only have 'nfo_file' as an optional item which we take care of later
        for optional_key, optional_value in optional_items.items():
            if str(optional_key) == str(translation_value):
                # hybrid_type is managed by hybrid_mapping.
                if optional_value == "hybrid_type":
                    break

                logging.debug(
                    f"[Translation] Key {translation_key} mapped to optional item {optional_key} with value type as {optional_value}"
                )
                # -!-!- Editions -!-!- #
                if optional_key == "edition" and "edition" in torrent_info:
                    # First we remove any 'fluff' so that we can try to match the edition to the list BHD has, if not we just upload it as a custom edition
                    local_edition_formatted = (
                        str(torrent_info["edition"])
                        .lower()
                        .replace("edition", "")
                        .replace("cut", "")
                        .replace("'", "")
                        .replace(" ", "")
                    )
                    # Remove extra 's'
                    if local_edition_formatted.endswith("s"):
                        local_edition_formatted = local_edition_formatted[:-1]
                    # Now check to see if what we got out of the filename already exists on BHD
                    for bhd_edition in optional_value:
                        if str(bhd_edition).lower() == local_edition_formatted:
                            # If its a match we save the value to tracker_settings here
                            tracker_settings[optional_key] = bhd_edition
                            break
                        else:
                            # We use the 'custom_edition' to set our own, again we only do this if we can't match what BHD already has available to select
                            tracker_settings["custom_edition"] = torrent_info["edition"]

                # -!-!- Region -!-!- # (Disc only)
                elif optional_key == "region" and "region" in torrent_info:
                    # This will only run if you are uploading a bluray_disc
                    region = _get_bluray_region(optional_value, torrent_info["region"])
                    if region is not None:
                        tracker_settings[optional_key] = region

                # -!-!- Tags -!-!- #
                elif translation_key == "tags":
                    # The uploader will generate all the tags that are applicable to the current upload.
                    # each tracker will specify the list of tags that are accepted by it.
                    # here we select only those tags which are accepted by the tracker from the tags list generated
                    logging.info("[Translation] Identified tags key for tracker.")
                    upload_these_tags_list = []
                    for tag in torrent_info["tags"]:
                        if tag in optional_value["tags"]:
                            upload_these_tags_list.append(tag)
                    logging.info(
                        f"[Translation] Tags selected for tracker: {upload_these_tags_list}"
                    )
                    if len(upload_these_tags_list) != 0:
                        # currently we support sending tags as string or as an array
                        if optional_value["type"] == "string":
                            # if user wants to send tags as string, then a separator needs to be configured.
                            # Default separator is ,
                            # Note: If user wants TAG1 | TAG2 ie: <space>|<space> then user must
                            # configure separator as " | "
                            separator = (
                                ","
                                if "separator" not in optional_value
                                or len(optional_value["separator"]) < 1
                                else optional_value["separator"]
                            )
                            tracker_settings[optional_key] = separator.join(
                                upload_these_tags_list
                            )
                        elif optional_value["type"] == "array":
                            tracker_settings[optional_key] = upload_these_tags_list

                # TODO figure out why .nfo uploads fail on BHD & don't display on BLU...
                # if optional_key in ["nfo_file", "nfo"] and "nfo_file" in torrent_info:
                #     # So far
                #     tracker_settings[optional_key] = torrent_info["nfo_file"]

                elif optional_key == "sd" and "sd" in torrent_info:
                    tracker_settings[optional_key] = 1

                # checking whether the optional key is for mediainfo or bdinfo
                # TODO make changes to save bdinfo to bdinfo and move the existing bdinfo metadata to someother key
                # for full disks the bdInfo is saved under the same key as mediainfo
                elif translation_key == "mediainfo":
                    logging.debug(
                        f"[Translation] Identified {optional_key} for tracker with {'FullDisk' if args.disc else 'File/Folder'} upload"
                    )
                    if args.disc:
                        logging.debug(
                            "[Translation] Skipping mediainfo for tracker settings since upload is FullDisk."
                        )
                    else:
                        logging.debug(
                            f"[Translation] Setting mediainfo from torrent_info to tracker_settings for optional_key {optional_key}"
                        )
                        tracker_settings[optional_key] = torrent_info.get(
                            "mediainfo", "0"
                        )
                        continue
                elif translation_key == "bdinfo":
                    logging.debug(
                        f"[Translation] Identified {optional_key} for tracker with {'FullDisk' if args.disc else 'File/Folder'} upload"
                    )
                    if args.disc:
                        logging.debug(
                            f"[Translation] Setting mediainfo from torrent_info to tracker_settings for optional_key {optional_key}"
                        )
                        tracker_settings[optional_key] = torrent_info.get(
                            "mediainfo", "0"
                        )
                        continue
                    else:
                        logging.debug(
                            "[Translation] Skipping bdinfo for tracker settings since upload is NOT FullDisk."
                        )
                else:
                    tracker_settings[optional_key] = torrent_info.get(
                        translation_key, ""
                    )
        # ------------ optional_items end ------------

        # ----------- hybrid_mapping_v2 start -----------
        # using in instead of == since multiple hybrid mappings can be configured
        # such as hybrid_type_1, hybrid_type_2, hybrid_type_3 ....
        if "hybrid_type" in translation_key:
            (
                should_continue,
                is_hybrid_translation_needed,
            ) = _validate_and_do_hybrid_mapping(
                translation_value,
                config,
                tracker_settings,
                torrent_info,
                is_hybrid_translation_needed,
            )
            if should_continue:
                hybrid_translation_keys.append(translation_value)
                continue
        # ------------ hybrid_mapping_v2 end ------------

    # Adding default values from template to tracker settings
    for default_key, default_value in config["Default"].items():
        if default_key in tracker_settings:
            continue
        logging.debug(
            f"[Translation] Adding default key `{default_key}` with value `{default_value}` to tracker settings"
        )
        tracker_settings[default_key] = default_value

    # at this point we have finished iterating over the translation key items
    if is_hybrid_translation_needed:
        perform_delayed_hybrid_mapping(
            tracker_settings=tracker_settings,
            config=config,
            exit_program=True,
            torrent_info=torrent_info,
        )


# -------------- END of choose_right_tracker_keys --------------


# ---------------------------------------------------------------------- #
#           !!! WARN !!! This Method has side effects. !!! WARN !!!
# ---------------------------------------------------------------------- #
def fix_default_naming_styles(torrent_info):
    # ------------------ Set some default naming styles here ------------------ #
    # Fix BluRay
    if "bluray" in torrent_info["source_type"]:
        if "disc" in torrent_info["source_type"]:
            # Raw bluray discs have a "-" between the words "Blu" & "Ray"
            if "uhd" in torrent_info:
                torrent_info["source"] = f"{torrent_info['uhd']} Blu-ray"
            else:
                torrent_info["source"] = "Blu-ray"
        else:
            # BluRay encodes & Remuxes just use the complete word "BluRay"
            torrent_info["source"] = "BluRay"

    # Now fix WEB
    if str(torrent_info["source"]).lower() == "web":
        if torrent_info["source_type"] == "webrip":
            torrent_info["web_type"] = "WEBRip"
        else:
            torrent_info["web_type"] = "WEB-DL"

    # Fix DVD
    if str(torrent_info["source"]).lower() == "dvd":
        if torrent_info["source_type"] in ("dvd_remux", "dvd_disc"):
            # later in the script if this ends up being a DVD Remux we will add the tag "Remux" to the torrent title
            torrent_info["source"] = "DVD"
        else:
            # Anything else is just a dvdrip
            torrent_info["source"] = "DVDRip"


# ---------------------------------------------------------------------- #
#                           Format torrent title!                        #
# ---------------------------------------------------------------------- #
def format_title(json_config, torrent_info):
    # ------------------ Load correct "naming config" ------------------ # Here we open the uploads corresponding
    # .json file and using the current uploads "source" we pull in a custom naming config this "naming config" can
    # individually be tweaked for each site & "content_type" (bluray_encode, web, etc)

    # Because 'webrips' & 'web-dls' have basically the same exact naming style we convert the 'source_type' to just
    # 'web' (we do something similar to DVDs as well)
    if str(torrent_info["source"]).lower() == "dvd":
        config_profile = "dvd"
    elif str(torrent_info["source"]).lower() == "web":
        config_profile = "web"
    else:
        config_profile = torrent_info["source_type"]

    tracker_torrent_name_style = json_config["torrent_title_format"][
        torrent_info["type"]
    ][str(config_profile)]

    # ------------------ Actual format the title now ------------------ #
    # This dict will store the "torrent_info" response for each item in the "naming config"
    generate_format_string = {}
    separator = json_config["title_separator"] or " "

    temp_load_torrent_info = (
        tracker_torrent_name_style.replace("{", "").replace("}", "").split(" ")
    )
    for item in temp_load_torrent_info:
        upper = False
        if item[0] == "!":
            item = item[1:]
            upper = True

        # Here is were we actual get the torrent_info response and add it to the "generate_format_string" dict we
        # declared earlier
        generate_format_string[item] = (
            torrent_info[item].replace(" ", separator)
            if item in torrent_info and torrent_info[item] is not None
            else ""
        )
        if upper:
            generate_format_string[item] = generate_format_string[item].upper()

    formatted_title = ""  # This is the final torrent title, we add any info we get from "torrent_info" to it using
    # the "for loop" below
    for key, value in generate_format_string.items():
        # ignore no matches (e.g. most TV Shows don't have the "year" added to its title so unless it was directly specified in the filename we also ignore it)
        if len(value) != 0:
            formatted_title = f'{formatted_title}{"-" if key == "release_group" else separator}{value}'

    # Custom title translations specific to tracker Certain terms might not be allowed in certain trackers. Such
    # terms are configured in a separate config in the tracker template. Eg: DD+ might not be allowed in certain
    # trackers. Instead, they'll use DDP These translations are then applied here.
    if "torrent_title_translation" in json_config:
        torrent_title_translation = json_config["torrent_title_translation"]
        logging.info(
            f"Going to apply title translations to generated title: {formatted_title}"
        )
        for key, val in torrent_title_translation.items():
            formatted_title = formatted_title.replace(key, val)

    logging.info(f"Torrent title after formatting and translations: {formatted_title}")
    # Finally save the "formatted_title" into torrent_info which later will get passed to the dict "tracker_settings"
    # which is used to store the payload for the actual POST upload request
    return str(formatted_title[1:])


# -------------- END of format_title --------------


def __add_applicable_tags(torrent_info: Dict, group: str, subkey: str):
    if group is None or subkey is None:
        return

    if "tags" not in torrent_info:
        torrent_info["tags"] = []

    group = group.lower()
    subkey = subkey.lower().replace("'", "")
    tag_grouping = (
        torrent_info["tag_grouping"] if "tag_grouping" in torrent_info else {}
    )
    if group in tag_grouping and subkey in tag_grouping[group]:
        logging.info(f"[Tags] Adding tags for group '{group}' and subkey '{subkey}'")
        torrent_info["tags"].extend(tag_grouping[group][subkey])
        torrent_info["tags"] = sorted(torrent_info["tags"])


# ---------------------------------------------------------------------- #
#           !!! WARN !!! This Method has side effects. !!! WARN !!!
# ---------------------------------------------------------------------- #
def generate_all_applicable_tags(torrent_info):
    """
    What is this tag_grouping.json file?
    ------------------------------------
    The `tag_grouping` groups the tags by `groupkeys` and `subkeys`.
    `hdr_format`, `edition` etc are referred to as `groupkeys`
    `hdr`, `hdr10+`, `uncut`, `bluray_remux` etc are referred to as the `subkeys` of the corresponding `groupkeys`

    The value of a subkey are a list of string. Where each of these strings are tags that are applicable to the
    upload for the given groupkey and subkey.

    How are tags handled in GGBOT?
    ------------------------------
    The upload process will fill in all the required information in the torrent info.
    Once all the details have been collected, both upload assistant and reuploader will invoke this method to
    generate and add tags that are applicable to the current upload.

    Note: The tags added here are not specific to any trackers.

    All the tags that are applicable to the upload based on the groupkey and subkey are added to the torrent_info.

    Later during `tracker_settings` preparation the tags that are applicable to a particular tracker
    are selected from this list of all applicable tags.

    """
    logging.debug("[Tags] Generating tags for the upload")
    logging.debug("[Tags] Creating tags for hdr_format")
    __add_applicable_tags(
        torrent_info,
        "hdr_format",
        torrent_info["hdr"] if "hdr" in torrent_info else None,
    )
    __add_applicable_tags(
        torrent_info,
        "hdr_format",
        torrent_info["dv"] if "dv" in torrent_info else None,
    )

    logging.debug("[Tags] Creating tags for bit_depth")
    __add_applicable_tags(
        torrent_info,
        "bit_depth",
        torrent_info["bit_depth"] if "bit_depth" in torrent_info else None,
    )

    logging.debug("[Tags] Creating tags for source_type")
    __add_applicable_tags(
        torrent_info,
        "source_type",
        torrent_info["source_type"] if "source_type" in torrent_info else None,
    )

    logging.debug("[Tags] Creating tags for audio")
    __add_applicable_tags(
        torrent_info,
        "audio",
        torrent_info["atmos"] if "atmos" in torrent_info else None,
    )
    __add_applicable_tags(
        torrent_info,
        "audio",
        "commentary"
        if "commentary" in torrent_info and torrent_info["commentary"] is True
        else None,
    )
    __add_applicable_tags(
        torrent_info,
        "audio",
        "dualaudio"
        if "dualaudio" in torrent_info and torrent_info["dualaudio"] == "Dual-Audio"
        else None,
    )
    __add_applicable_tags(
        torrent_info,
        "audio",
        "multiaudio"
        if "multiaudio" in torrent_info and torrent_info["multiaudio"] == "Multi"
        else None,
    )

    logging.debug("[Tags] Creating tags for edition")
    __add_applicable_tags(
        torrent_info,
        "edition",
        torrent_info["edition"] if "edition" in torrent_info else None,
    )

    if "argument_tags" in torrent_info and torrent_info["argument_tags"] is not None:
        logging.info("[Tags] Adding any custom tags from argument to tags.")
        torrent_info["tags"].extend(torrent_info["argument_tags"])
        torrent_info["tags"] = sorted(torrent_info["tags"])

    logging.info(f"[Tags] Generated tags: {torrent_info['tags']}")
