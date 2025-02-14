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

import pytest

from modules.custom_actions.nbl_actions import season_pack_dupe


class TestNBLCustomActions:
    @pytest.mark.parametrize(
        ("torrent_info", "expected"),
        [
            pytest.param({"episode_number": "1"}, {}, id="single_episode_release"),
            pytest.param({"episode_number": 1}, {}, id="single_episode_release_2"),
            pytest.param(
                {"episode_number": "0"}, {"ignoredupes": "1"}, id="season_pack"
            ),
            pytest.param(
                {"episode_number": 0}, {"ignoredupes": "1"}, id="season_pack_2"
            ),
            pytest.param({}, {"ignoredupes": "1"}, id="season_pack_3"),
        ],
    )
    def test_season_pack_dupe(self, torrent_info, expected):
        tracker_settings = {}
        season_pack_dupe(torrent_info, tracker_settings, None)
        assert tracker_settings == expected
