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

import qbittorrentapi
import requests


class TestE2ESetup:
    def test_qbittorrent_container_setup(
        self, qbittorrent_container, qbittorrent_credentials
    ):
        self.qbt_client = qbittorrentapi.Client(
            host=f"https://{qbittorrent_credentials['host']}",
            port=qbittorrent_credentials["port"],
            username=qbittorrent_credentials["username"],
            password=qbittorrent_credentials["password"],
            VERIFY_WEBUI_CERTIFICATE=False,
        )

        assert self.qbt_client.auth_log_in() is None, "Failed to login to qbittorrent"

    def test_rutorrent_container_setup(self, rutorrent_credentials):
        response = requests.get(
            f"http://{rutorrent_credentials['host']}:{rutorrent_credentials['port']}/plugins/check_port/action.php?init",
            headers={"Authorization": f"Basic {rutorrent_credentials['hashed']}"},
        )
        assert response.status_code == 200, "rTorrent is not running properly"

    def test_mock_server_container_setup(self, mock_server):
        response = requests.get("http://example.com/api/test")
        assert response.status_code == 200
        assert response.json() == {"message": "mocked response 1"}

        response = requests.post("http://example.com/api/another")
        assert response.status_code == 201
        assert response.json() == {"message": "mocked response 2"}

        response = requests.get("http://example.com/api/error")
        assert response.status_code == 404
        assert response.json() == {"error": "Not Found"}

        response = requests.get(
            "http://example.com/3/search/movie?api_key=PLACEHOLDER_API_KEY&query='Deadpool & Wolverine'&page=1&include_adult=false&year=2024"
        )
        assert response.status_code == 200
        json_data = response.json()

        assert "page" in json_data
        assert "results" in json_data
        assert "total_pages" in json_data
        assert "total_results" in json_data
