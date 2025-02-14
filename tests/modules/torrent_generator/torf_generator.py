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

from pathlib import Path

import pytest
from torf import Torrent

from modules.config import UploaderTweaksConfig

working_folder = Path(__file__).resolve().parent.parent.parent
data_file_location = "/resources/rar/data.rar"


def uploader_tweaks_16kb_64mb(param, default=None):
    if param == "torf_min_piece_size":
        return "KB_16"
    if param == "torf_max_piece_size":
        return "MB_64"
    return default


def uploader_tweaks_1mb_16mb(param, default=None):
    if param == "torf_min_piece_size":
        return "MB_1"
    if param == "torf_max_piece_size":
        return "MB_16"
    return default


class TestGGBOTTorrent:
    @pytest.fixture()
    def gg_bot_torrent(self, uploader_config):
        yield Torrent(
            path=f"{working_folder}{data_file_location}",
            trackers=["https://ggbot.com"],
            source="GG-BOT",
            piece_size_min=uploader_config.TORF_MIN_PIECE_SIZE,
            piece_size_max=uploader_config.TORF_MAX_PIECE_SIZE,
        )

    @pytest.fixture()
    def uploader_config(self):
        yield UploaderTweaksConfig()

    def test_gg_bot_torrent_creation(self, gg_bot_torrent, uploader_config):
        assert gg_bot_torrent is not None
        assert gg_bot_torrent.piece_size_min == uploader_config.TORF_MIN_PIECE_SIZE
        assert gg_bot_torrent.piece_size_max == uploader_config.TORF_MAX_PIECE_SIZE

    @pytest.mark.parametrize(
        ("torrent_size", "piece_size"),
        [
            pytest.param(2500, 16384, id="less_than_1gb_2500"),
            pytest.param(12500, 16384, id="less_than_1gb_12500"),
            pytest.param(112500, 16384, id="less_than_1gb_112500"),
            pytest.param(1112500, 16384, id="less_than_1gb_1112500"),
            pytest.param(9737418, 32768, id="less_than_1gb_9737418"),
            pytest.param(13741824, 32768, id="less_than_1gb_13741824"),
            pytest.param(33741824, 131072, id="less_than_1gb_33741824"),
            pytest.param(53741824, 131072, id="less_than_1gb_53741824"),
            pytest.param(73741824, 262144, id="less_than_1gb_73741824"),
            pytest.param(83741824, 262144, id="less_than_1gb_83741824"),
            pytest.param(93741824, 262144, id="less_than_1gb_93741824"),
            pytest.param(103741824, 262144, id="less_than_1gb_103741824"),
            pytest.param(143741824, 524288, id="less_than_1gb_143741824"),
            pytest.param(183741824, 524288, id="less_than_1gb_183741824"),
            pytest.param(283741824, 1048576, id="less_than_1gb_283741824"),
            pytest.param(383741824, 1048576, id="less_than_1gb_383741824"),
            pytest.param(483741824, 1048576, id="less_than_1gb_483741824"),
            pytest.param(583741824, 2097152, id="less_than_1gb_583741824"),
            pytest.param(683741824, 2097152, id="less_than_1gb_683741824"),
            pytest.param(783741824, 2097152, id="less_than_1gb_783741824"),
            pytest.param(973741824, 2097152, id="less_than_1gb_973741824"),
            pytest.param(
                983741824, 2097152, id="greater_than_1gb_less_than_4gb_983741824"
            ),
            pytest.param(
                1093741824, 2097152, id="greater_than_1gb_less_than_4gb_1093741824"
            ),
            pytest.param(
                2013741824, 2097152, id="greater_than_1gb_less_than_4gb_2013741824"
            ),
            pytest.param(
                2093741824, 2097152, id="greater_than_1gb_less_than_4gb_2093741824"
            ),
            pytest.param(
                3093741824, 4194304, id="greater_than_1gb_less_than_4gb_3093741824"
            ),
            pytest.param(
                4093741824, 4194304, id="greater_than_1gb_less_than_4gb_4093741824"
            ),
            pytest.param(
                4394967296, 8388608, id="greater_than_4gb_less_than_6gb_4394967296"
            ),
            pytest.param(
                5294967296, 8388608, id="greater_than_4gb_less_than_6gb_5294967296"
            ),
            pytest.param(
                6142450944, 8388608, id="greater_than_4gb_less_than_6gb_6142450944"
            ),
            pytest.param(
                6542450944, 8388608, id="greater_than_6gb_less_than_8gb_6542450944"
            ),
            pytest.param(
                7542450944, 8388608, id="greater_than_6gb_less_than_8gb_7542450944"
            ),
            pytest.param(
                8489934592, 8388608, id="greater_than_6gb_less_than_8gb_8489934592"
            ),
            pytest.param(
                8689934592, 8388608, id="greater_than_8gb_less_than_16gb_8689934592"
            ),
            pytest.param(
                9689934592, 8388608, id="greater_than_8gb_less_than_16gb_9689934592"
            ),
            pytest.param(
                10689934592, 8388608, id="greater_than_8gb_less_than_16gb_10689934592"
            ),
            pytest.param(
                15689934592, 16777216, id="greater_than_8gb_less_than_16gb_15689934592"
            ),
            pytest.param(
                17079869184, 16777216, id="greater_than_8gb_less_than_16gb_17079869184"
            ),
            pytest.param(
                17279869184, 16777216, id="greater_than_16gb_less_than_32gb_17279869184"
            ),
            pytest.param(
                18279869184, 16777216, id="greater_than_16gb_less_than_32gb_18279869184"
            ),
            pytest.param(
                27279869184, 16777216, id="greater_than_16gb_less_than_32gb_27279869184"
            ),
            pytest.param(
                33279869184, 16777216, id="greater_than_16gb_less_than_32gb_33279869184"
            ),
            pytest.param(
                34259738368, 16777216, id="greater_than_16gb_less_than_32gb_34259738368"
            ),
            pytest.param(
                34459738368, 33554432, id="greater_than_32gb_less_than_64gb_34459738368"
            ),
            pytest.param(
                44459738368, 33554432, id="greater_than_32gb_less_than_64gb_44459738368"
            ),
            pytest.param(
                54459738368, 33554432, id="greater_than_32gb_less_than_64gb_54459738368"
            ),
            pytest.param(
                68619476736, 33554432, id="greater_than_32gb_less_than_64gb_68619476736"
            ),
            pytest.param(78619476736, 67108864, id="greater_than_64gb_78619476736"),
            pytest.param(88619476736, 67108864, id="greater_than_64gb_88619476736"),
            pytest.param(108619476736, 67108864, id="greater_than_100gb"),
            pytest.param(208619476736, 67108864, id="greater_than_200gb"),
            pytest.param(308619476736, 67108864, id="greater_than_300gb"),
            pytest.param(408619476736, 67108864, id="greater_than_400gb"),
            pytest.param(508619476736, 67108864, id="greater_than_500gb"),
        ],
    )
    def test_gg_bot_torrent_piece_size_full_range(
        self, torrent_size, piece_size, mocker, gg_bot_torrent
    ):
        mocker.patch("os.getenv", side_effect=uploader_tweaks_16kb_64mb)
        uploader_config = UploaderTweaksConfig()

        actual_piece_size = gg_bot_torrent.calculate_piece_size(
            torrent_size,
            max_size=uploader_config.TORF_MAX_PIECE_SIZE,
            min_size=uploader_config.TORF_MIN_PIECE_SIZE,
        )
        assert actual_piece_size == piece_size

    @pytest.mark.parametrize(
        ("torrent_size", "piece_size"),
        [
            pytest.param(2500, 16384, id="less_than_1gb_2500"),
            pytest.param(12500, 16384, id="less_than_1gb_12500"),
            pytest.param(112500, 16384, id="less_than_1gb_112500"),
            pytest.param(1112500, 16384, id="less_than_1gb_1112500"),
            pytest.param(9737418, 32768, id="less_than_1gb_9737418"),
            pytest.param(13741824, 32768, id="less_than_1gb_13741824"),
            pytest.param(33741824, 131072, id="less_than_1gb_33741824"),
            pytest.param(53741824, 131072, id="less_than_1gb_53741824"),
            pytest.param(73741824, 262144, id="less_than_1gb_73741824"),
            pytest.param(83741824, 262144, id="less_than_1gb_83741824"),
            pytest.param(93741824, 262144, id="less_than_1gb_93741824"),
            pytest.param(103741824, 262144, id="less_than_1gb_103741824"),
            pytest.param(143741824, 524288, id="less_than_1gb_143741824"),
            pytest.param(183741824, 524288, id="less_than_1gb_183741824"),
            pytest.param(283741824, 1048576, id="less_than_1gb_283741824"),
            pytest.param(383741824, 1048576, id="less_than_1gb_383741824"),
            pytest.param(483741824, 1048576, id="less_than_1gb_483741824"),
            pytest.param(583741824, 2097152, id="less_than_1gb_583741824"),
            pytest.param(683741824, 2097152, id="less_than_1gb_683741824"),
            pytest.param(783741824, 2097152, id="less_than_1gb_783741824"),
            pytest.param(973741824, 2097152, id="less_than_1gb_973741824"),
            pytest.param(
                983741824, 2097152, id="greater_than_1gb_less_than_4gb_983741824"
            ),
            pytest.param(
                1093741824, 2097152, id="greater_than_1gb_less_than_4gb_1093741824"
            ),
            pytest.param(
                2013741824, 2097152, id="greater_than_1gb_less_than_4gb_2013741824"
            ),
            pytest.param(
                2093741824, 2097152, id="greater_than_1gb_less_than_4gb_2093741824"
            ),
            pytest.param(
                3093741824, 4194304, id="greater_than_1gb_less_than_4gb_3093741824"
            ),
            pytest.param(
                4093741824, 4194304, id="greater_than_1gb_less_than_4gb_4093741824"
            ),
            pytest.param(
                4394967296, 8388608, id="greater_than_4gb_less_than_6gb_4394967296"
            ),
            pytest.param(
                5294967296, 8388608, id="greater_than_4gb_less_than_6gb_5294967296"
            ),
            pytest.param(
                6142450944, 8388608, id="greater_than_4gb_less_than_6gb_6142450944"
            ),
            pytest.param(
                6542450944, 8388608, id="greater_than_6gb_less_than_8gb_6542450944"
            ),
            pytest.param(
                7542450944, 8388608, id="greater_than_6gb_less_than_8gb_7542450944"
            ),
            pytest.param(
                8489934592, 8388608, id="greater_than_6gb_less_than_8gb_8489934592"
            ),
            pytest.param(
                8689934592, 8388608, id="greater_than_8gb_less_than_16gb_8689934592"
            ),
            pytest.param(
                9689934592, 8388608, id="greater_than_8gb_less_than_16gb_9689934592"
            ),
            pytest.param(
                10689934592, 8388608, id="greater_than_8gb_less_than_16gb_10689934592"
            ),
            pytest.param(
                15689934592, 16777216, id="greater_than_8gb_less_than_16gb_15689934592"
            ),
            pytest.param(
                17079869184, 16777216, id="greater_than_8gb_less_than_16gb_17079869184"
            ),
            pytest.param(
                17279869184, 16777216, id="greater_than_16gb_less_than_32gb_17279869184"
            ),
            pytest.param(
                18279869184, 16777216, id="greater_than_16gb_less_than_32gb_18279869184"
            ),
            pytest.param(
                27279869184, 16777216, id="greater_than_16gb_less_than_32gb_27279869184"
            ),
            pytest.param(
                33279869184, 16777216, id="greater_than_16gb_less_than_32gb_33279869184"
            ),
            pytest.param(
                34259738368, 16777216, id="greater_than_16gb_less_than_32gb_34259738368"
            ),
            pytest.param(
                34459738368, 16777216, id="greater_than_32gb_less_than_64gb_34459738368"
            ),
            pytest.param(
                44459738368, 16777216, id="greater_than_32gb_less_than_64gb_44459738368"
            ),
            pytest.param(
                54459738368, 16777216, id="greater_than_32gb_less_than_64gb_54459738368"
            ),
            pytest.param(
                68619476736, 16777216, id="greater_than_32gb_less_than_64gb_68619476736"
            ),
            pytest.param(78619476736, 16777216, id="greater_than_64gb_78619476736"),
            pytest.param(88619476736, 16777216, id="greater_than_64gb_88619476736"),
            pytest.param(108619476736, 16777216, id="greater_than_100gb"),
            pytest.param(208619476736, 16777216, id="greater_than_200gb"),
            pytest.param(308619476736, 16777216, id="greater_than_300gb"),
            pytest.param(408619476736, 16777216, id="greater_than_400gb"),
            pytest.param(508619476736, 16777216, id="greater_than_500gb"),
        ],
    )
    def test_gg_bot_torrent_piece_size_clipped(
        self, torrent_size, piece_size, mocker, gg_bot_torrent
    ):
        mocker.patch("os.getenv", side_effect=uploader_tweaks_1mb_16mb)
        uploader_config = UploaderTweaksConfig()
        actual_piece_size = gg_bot_torrent.calculate_piece_size(
            torrent_size,
            max_size=uploader_config.TORF_MAX_PIECE_SIZE,
            min_size=uploader_config.TORF_MIN_PIECE_SIZE,
        )
        assert actual_piece_size == piece_size
