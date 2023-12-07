import logging
import pickle
import re
from json import JSONDecodeError
from pathlib import Path

import requests
from dotenv import load_dotenv
from rich import box
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from modules.config import TrackerConfig
from modules.exceptions.exception import GGBotException
from modules.tfa.tfa import get_totp_token


def user_choice_for_torrent_group(torrent_info, torrent_items):
    if len(torrent_items) == 0:
        return torrent_items
    console = Console()
    group_id_name_dict_list = []
    search_data = Table(
        show_header=True,
        header_style="bold cyan",
        box=box.HEAVY,
        border_style="dim",
    )
    search_data.add_column("Group #", justify="center")
    search_data.add_column("Group Id", justify="center")
    search_data.add_column("Group Name", justify="center")
    for idx, item in enumerate(torrent_items):
        group_id_name_dict_list.append(
            {
                "id": idx + 1,
                "groupId": item["groupId"],
                "groupName": item["groupName"],
            }
        )
        search_data.add_row(
            str(idx + 1), str(item["groupId"]), item["groupName"]
        )

    console.print(search_data, justify="center")

    list_of_num = []
    for i in range(len(group_id_name_dict_list)):
        i += 1
        list_of_num.append(str(i))

    user_input_group_id = Prompt.ask(
        "Input the correct Group # corresponding for this release",
        choices=list_of_num,
    )

    group_id = group_id_name_dict_list[int(user_input_group_id) - 1]["groupId"]
    logging.info(
        f"[CustomAction][UHDBits] User selected group {group_id} for this upload. Fetching torrents for this group"
    )
    cookiefile = f"{torrent_info['cookies_dump']}cookies/uhdb_cookie.dat"
    with requests.Session() as session:
        session.cookies.update(pickle.load(open(cookiefile, "rb")))
        group_response = session.get(
            f"https://uhdbits.org/ajax.php?action=torrentgroup&id={group_id}"
        )
        group_response = group_response.json()
        if group_response["status"] != "success":
            logging.error(
                "[CustomAction][UHDBits] Failed to get details of torrent group."
            )
            return []
        return [
            {
                "name": re.sub(
                    r"\{[^}]*\}",
                    "",
                    item[
                        "filePath" if len(item["filePath"]) > 0 else "fileList"
                    ],
                ).replace("}}", "")
            }
            for item in group_response["response"]["torrents"]
        ]


def login_and_get_cookie(torrent_info, tracker_settings, tracker_config):
    tracker_env_config = TrackerConfig("UHDB")

    if not Path(f"{torrent_info['cookies_dump']}cookies").is_dir():
        Path(f"{torrent_info['cookies_dump']}cookies").mkdir(
            parents=True, exist_ok=True
        )
    cookiefile = f"{torrent_info['cookies_dump']}cookies/uhdb_cookie.dat"

    with requests.Session() as session:
        # if we have a cookie file saved previously (user running with resume flag), then we can reuse it.
        if Path(cookiefile).is_file():
            session.cookies.update(pickle.load(open(cookiefile, "rb")))
            index_response = session.get(
                "https://uhdbits.org/ajax.php?action=index"
            )
            try:
                index_response = index_response.json()
                if index_response["status"] == "success":
                    logging.info(
                        "[CustomAction][UHDBits] Successfully validated stored cookie"
                    )
                    logging.info(
                        f"[CustomAction][UHDBits] User: {index_response['response']['username']}"
                    )
                    return cookiefile
                else:
                    logging.error(
                        "[CustomAction][UHDBits] Failed to validate stored cookie"
                    )
            except JSONDecodeError:
                logging.info(
                    "[CustomAction][UHDBits] Could not login to UHDBits using the stored cookies."
                )
                logging.error(
                    "[CustomAction][UHDBits] Invalid cookie data. Attempting to get new cookies."
                )

        logging.info(
            "[CustomActions][UHDBits] UHDBits Cookies not found. Creating new session."
        )
        data = {
            "username": tracker_env_config.get_config("UHDB_USER_NAME"),
            "password": tracker_env_config.get_config("UHDB_USER_PASSWORD"),
            "keeplogged": "1",
        }
        # adding tfa code if user has tfa enabled
        if (
            tracker_env_config.get_config_as_boolean("UHDB_2FA_ENABLED", False)
            is True
        ):
            logging.info(
                "[CustomActions][UHDBits] User has 2FA enabled. Trying to generate TOTP code."
            )
            data["two_step"] = get_totp_token(
                tracker_env_config.get_config("UHDB_2FA_CODE", "")
            )
        session_response = session.post(
            "https://uhdbits.org/login.php",
            data=data,
            headers={},
        )
        session_response = session_response.text
        title_match = re.search(
            r"<title>(.*?)</title>", session_response, re.DOTALL
        )
        if title_match:
            title = title_match.group(1)
            if title != "News :: UHDBits":
                raise GGBotException(
                    f"Failed to login to UHDBits. Bad 'username' / 'password' / '2fa_key' provided: {session_response}"
                )
        else:
            raise GGBotException(
                f"Failed to login to UHDBits. Bad 'username' / 'password' / '2fa_key' provided: {session_response}"
            )

        logging.info(
            "[CustomActions][UHDBits] Successfully logged in to UHDBits and obtained cookies."
        )
        pickle.dump(session.cookies, open(cookiefile, "wb"))
        return cookiefile


if __name__ == "__main__":
    load_dotenv("../../config.env")
    login_and_get_cookie(
        torrent_info={"cookies_dump": "./"},
        tracker_settings=None,
        tracker_config=None,
    )
