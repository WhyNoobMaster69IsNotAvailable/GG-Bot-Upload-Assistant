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

import functools
import hashlib
import sys
import traceback
from threading import Thread

from flask import Flask, request

from modules.cache import CacheFactory, CacheVendor
from modules.config import VisorConfig
from modules.visor.schema import GGBotTorrentSchema
from utilities.utils_visor_server import (
    VisorServerManager,
    Query,
)

stored_key = None


def api_required(function):
    @functools.wraps(function)
    def decorator(self, *args, **kwargs):
        api_key = request.headers.get("Authorization", None)
        if api_key is None:
            return {
                "status": "UNAUTHORIZED",
                "message": "Please provide an api key",
            }, 403

        if not self.is_valid(api_key):
            return {
                "status": "UNAUTHORIZED",
                "message": "Unauthorized Access",
            }, 403

        return function(*args, **kwargs)

    return decorator


def gg_bot_response(function):
    @functools.wraps(function)
    def decorator(*args, **kwargs):
        # TODO: figure out how to handle the exceptions
        try:
            return {"status": "OK", "data": function(*args, **kwargs)}, 200
        except Exception as e:
            print("Printing only the traceback above the current stack frame")
            print(
                "".join(
                    traceback.format_exception(
                        sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
                    )
                )
            )
            return {
                "status": "ERROR",
                "message": getattr(e, "message", repr(e)),
            }, 500

    return decorator


class EndpointAction:
    def __init__(self, action):
        self.action = action

    def __call__(self, *args, **kwargs):
        return self.action(*args, **kwargs)


class Server:
    def __init__(self, cache):
        self.app = Flask("GG-BOT Auto-ReUploader")
        self.visor_config = VisorConfig()
        self.visor_server_manager: VisorServerManager = VisorServerManager(cache)
        # healthcheck / status endpoint
        self.add_endpoint(
            endpoint="/status",
            endpoint_name="GG-BOT Status",
            handler=self.status,
        )
        # get all torrent details :: paginated
        self.add_endpoint(
            endpoint="/torrents/",
            endpoint_name="Get All Torrents",
            handler=self.torrents,
        )
        # get details of a particular torrent
        self.add_endpoint(
            endpoint="/torrents/<torrent_id>",
            endpoint_name="Get details of a particular torrent",
            handler=self.torrent_details,
        )
        # statistics of all the torrents
        self.add_endpoint(
            endpoint="/torrents/statistics",
            endpoint_name="Torrent Statistics",
            handler=self.torrent_statistics,
        )
        # details of all the successful torrents :: paginated
        self.add_endpoint(
            endpoint="/torrents/success",
            endpoint_name="Get All Successful Torrents",
            handler=self.successful_torrents,
        )
        # details of all the failed torrents :: paginated
        self.add_endpoint(
            endpoint="/torrents/failed",
            endpoint_name="Get All Failed Torrents",
            handler=self.failed_torrents,
        )
        # statistics of all the failed torrents
        self.add_endpoint(
            endpoint="/torrents/failed/statistics",
            endpoint_name="Get Failed Torrents Statistics",
            handler=self.failed_torrents_statistics,
        )
        # get all partially successful torrents
        # partially successful torrents are theose which were uploaded to only few of the configured trackers
        self.add_endpoint(
            endpoint="/torrents/partial",
            endpoint_name="Get All Partially Successful Torrents",
            handler=self.partially_successful_torrents,
        )
        # update the torrents metadata id
        self.add_endpoint(
            endpoint="/torrents/<torrent_id>/update.metadata",
            endpoint_name="Update the metadata id of the torrent",
            handler=self.update_metadata,
            methods=["POST"],
        )

    def run(self, host, port, threaded=False, use_reloader=False, debug=False):
        print(f" * Visor server started and listening for connection on {host}:{port}")
        self.app.run(
            port=port,
            host=host,
            threaded=threaded,
            use_reloader=use_reloader,
            debug=debug,
        )

    def add_endpoint(
        self, endpoint=None, endpoint_name=None, handler=None, methods=None
    ):
        if methods is None:
            methods = ["GET"]
        self.app.add_url_rule(
            endpoint, endpoint_name, EndpointAction(handler), methods=methods
        )

    def is_valid(self, api_key):
        global stored_key
        if stored_key is None:
            stored_key = hashlib.sha3_256(
                f"Bearer {self.visor_config.API_KEY}".encode()
            ).hexdigest()
        return stored_key == hashlib.sha3_256(api_key.encode()).hexdigest()

    def start(self, detached=False):
        kwargs = {
            "host": "0.0.0.0",
            "port": self.visor_config.PORT,
            "threaded": True,
            "use_reloader": False,
            "debug": False,
        }
        _ = (
            Thread(target=self.run, daemon=True, kwargs=kwargs).start()
            if detached
            else self.run(host="0.0.0.0", port=self.visor_config.PORT)
        )

    @api_required
    def status(self):  # YES
        return self.visor_server_manager.get_status()

    @api_required
    @gg_bot_response
    def torrent_statistics(self):  # YES
        return self.visor_server_manager.get_torrent_statistics()

    @api_required
    @gg_bot_response
    def failed_torrents_statistics(self):  # YES
        return self.visor_server_manager.failed_torrents_statistics()

    @api_required
    @gg_bot_response
    def torrents(self):
        sort = request.args.get("sort", "id")
        page = int(request.args.get("page", 1))
        items_per_page = int(request.args.get("items_per_page", 20))

        # validating user provided params
        if sort.lower() not in ["id", "name", "hash", "status", "date_created"]:
            return {"message": "Invalid sort option provided"}

        return self.visor_server_manager.all_torrents(
            sort=sort.lower(), page=page, items_per_page=items_per_page
        )

    @api_required
    @gg_bot_response
    def torrent_details(self, torrent_id):
        return self.visor_server_manager.torrent_details(torrent_id=torrent_id)

    @api_required
    @gg_bot_response
    def update_metadata(self, torrent_id):
        torrent_data = GGBotTorrentSchema().dump(request.get_json())
        return self.visor_server_manager.update_torrent(
            torrent_id=torrent_id, update_data=torrent_data
        )
        # db_metadata = {"tmdb": None, "imdb": None, "tvdb": None, "tvmaze": None, "mal": None, "title": None,
        # "year": None, "type": None}

    @api_required
    @gg_bot_response
    def successful_torrents(self):
        sort = request.args.get("sort", "id")
        page = int(request.args.get("page", 1))
        items_per_page = int(request.args.get("items_per_page", 20))

        # validating user provided params
        if sort.lower() not in ["id", "name", "hash", "status", "date_created"]:
            return {"message": "Invalid sort option provided"}

        return self.visor_server_manager.all_torrents(
            sort=sort.lower(),
            page=page,
            items_per_page=items_per_page,
            filter_query=Query.SUCCESS,
        )

    @api_required
    @gg_bot_response
    def failed_torrents(self):
        sort = request.args.get("sort", "id")
        page = int(request.args.get("page", 1))
        items_per_page = int(request.args.get("items_per_page", 20))

        # validating user provided params
        if sort.lower() not in ["id", "name", "hash", "status", "date_created"]:
            return {"message": "Invalid sort option provided"}

        return self.visor_server_manager.all_torrents(
            sort=sort.lower(),
            page=page,
            items_per_page=items_per_page,
            filter_query=Query.ALL_FAILED,
        )

    @api_required
    @gg_bot_response
    def partially_successful_torrents(self):
        sort = request.args.get("sort", "id")
        page = int(request.args.get("page", 1))
        items_per_page = int(request.args.get("items_per_page", 20))

        # validating user provided params
        if sort.lower() not in ["id", "name", "hash", "status", "date_created"]:
            return {"message": "Invalid sort option provided"}

        return self.visor_server_manager.all_torrents(
            sort=sort.lower(),
            page=page,
            items_per_page=items_per_page,
            filter_query=Query.PARTIALLY_SUCCESSFUL,
        )


if __name__ == "__main__":
    Server(cache=CacheFactory().create(cache_type=CacheVendor.Mongo)).start()
