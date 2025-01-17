from pathlib import Path

import pytest

from modules.config import UploaderTweaksConfig
from modules.torrent_generator.torf_generator import GGBOTTorrent

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
    def gg_bot_torrent(self):
        yield GGBOTTorrent(
            path=f"{working_folder}{data_file_location}",
            trackers=["https://ggbot.com"],
            source="GG-BOT",
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
            pytest.param(2500, 16384, id="less_than_1gb"),
            pytest.param(12500, 16384, id="less_than_1gb"),
            pytest.param(112500, 16384, id="less_than_1gb"),
            pytest.param(1112500, 16384, id="less_than_1gb"),
            pytest.param(9737418, 16384, id="less_than_1gb"),
            pytest.param(973741824, 1048576, id="less_than_1gb"),
            pytest.param(983741824, 1048576, id="greater_than_1gb_less_than_4gb"),
            pytest.param(1093741824, 1048576, id="greater_than_1gb_less_than_4gb"),
            pytest.param(2093741824, 1048576, id="greater_than_1gb_less_than_4gb"),
            pytest.param(3093741824, 2097152, id="greater_than_1gb_less_than_4gb"),
            pytest.param(4093741824, 2097152, id="greater_than_1gb_less_than_4gb"),
            pytest.param(4394967296, 2097152, id="greater_than_4gb_less_than_6gb"),
            pytest.param(5294967296, 2097152, id="greater_than_4gb_less_than_6gb"),
            pytest.param(6142450944, 2097152, id="greater_than_4gb_less_than_6gb"),
            pytest.param(6542450944, 4194304, id="greater_than_6gb_less_than_8gb"),
            pytest.param(7542450944, 4194304, id="greater_than_6gb_less_than_8gb"),
            pytest.param(8489934592, 4194304, id="greater_than_6gb_less_than_8gb"),
            pytest.param(8689934592, 8388608, id="greater_than_8gb_less_than_16gb"),
            pytest.param(9689934592, 8388608, id="greater_than_8gb_less_than_16gb"),
            pytest.param(10689934592, 8388608, id="greater_than_8gb_less_than_16gb"),
            pytest.param(15689934592, 8388608, id="greater_than_8gb_less_than_16gb"),
            pytest.param(17079869184, 8388608, id="greater_than_8gb_less_than_16gb"),
            pytest.param(17279869184, 8388608, id="greater_than_16gb_less_than_32gb"),
            pytest.param(18279869184, 8388608, id="greater_than_16gb_less_than_32gb"),
            pytest.param(27279869184, 8388608, id="greater_than_16gb_less_than_32gb"),
            pytest.param(33279869184, 8388608, id="greater_than_16gb_less_than_32gb"),
            pytest.param(34259738368, 8388608, id="greater_than_16gb_less_than_32gb"),
            pytest.param(34459738368, 8388608, id="greater_than_32gb_less_than_64gb"),
            pytest.param(44459738368, 8388608, id="greater_than_32gb_less_than_64gb"),
            pytest.param(54459738368, 8388608, id="greater_than_32gb_less_than_64gb"),
            pytest.param(68619476736, 8388608, id="greater_than_32gb_less_than_64gb"),
            pytest.param(78619476736, 8388608, id="greater_than_64gb"),
            pytest.param(88619476736, 16777216, id="greater_than_64gb"),
            pytest.param(108619476736, 16777216, id="greater_than_100gb"),
            pytest.param(208619476736, 33554432, id="greater_than_200gb"),
            pytest.param(308619476736, 33554432, id="greater_than_300gb"),
            pytest.param(408619476736, 67108864, id="greater_than_400gb"),
            pytest.param(508619476736, 67108864, id="greater_than_500gb"),
        ],
    )
    def test_gg_bot_torrent_piece_size_full_range(
        self, torrent_size, piece_size, mocker, gg_bot_torrent
    ):
        mocker.patch("os.getenv", side_effect=uploader_tweaks_16kb_64mb)
        assert gg_bot_torrent.calculate_piece_size(torrent_size) == piece_size

    @pytest.mark.parametrize(
        ("torrent_size", "piece_size"),
        [
            pytest.param(2500, 16384, id="less_than_1gb"),
            pytest.param(12500, 16384, id="less_than_1gb"),
            pytest.param(112500, 16384, id="less_than_1gb"),
            pytest.param(1112500, 16384, id="less_than_1gb"),
            pytest.param(9737418, 16384, id="less_than_1gb"),
            pytest.param(973741824, 1048576, id="less_than_1gb"),
            pytest.param(983741824, 1048576, id="greater_than_1gb_less_than_4gb"),
            pytest.param(1093741824, 1048576, id="greater_than_1gb_less_than_4gb"),
            pytest.param(2093741824, 1048576, id="greater_than_1gb_less_than_4gb"),
            pytest.param(3093741824, 2097152, id="greater_than_1gb_less_than_4gb"),
            pytest.param(4093741824, 2097152, id="greater_than_1gb_less_than_4gb"),
            pytest.param(4394967296, 2097152, id="greater_than_4gb_less_than_6gb"),
            pytest.param(5294967296, 2097152, id="greater_than_4gb_less_than_6gb"),
            pytest.param(6142450944, 2097152, id="greater_than_4gb_less_than_6gb"),
            pytest.param(6542450944, 4194304, id="greater_than_6gb_less_than_8gb"),
            pytest.param(7542450944, 4194304, id="greater_than_6gb_less_than_8gb"),
            pytest.param(8489934592, 4194304, id="greater_than_6gb_less_than_8gb"),
            pytest.param(8689934592, 8388608, id="greater_than_8gb_less_than_16gb"),
            pytest.param(9689934592, 8388608, id="greater_than_8gb_less_than_16gb"),
            pytest.param(10689934592, 8388608, id="greater_than_8gb_less_than_16gb"),
            pytest.param(15689934592, 8388608, id="greater_than_8gb_less_than_16gb"),
            pytest.param(17079869184, 8388608, id="greater_than_8gb_less_than_16gb"),
            pytest.param(17279869184, 8388608, id="greater_than_16gb_less_than_32gb"),
            pytest.param(18279869184, 8388608, id="greater_than_16gb_less_than_32gb"),
            pytest.param(27279869184, 8388608, id="greater_than_16gb_less_than_32gb"),
            pytest.param(33279869184, 8388608, id="greater_than_16gb_less_than_32gb"),
            pytest.param(34259738368, 8388608, id="greater_than_16gb_less_than_32gb"),
            pytest.param(34459738368, 8388608, id="greater_than_32gb_less_than_64gb"),
            pytest.param(44459738368, 8388608, id="greater_than_32gb_less_than_64gb"),
            pytest.param(54459738368, 8388608, id="greater_than_32gb_less_than_64gb"),
            pytest.param(68619476736, 8388608, id="greater_than_32gb_less_than_64gb"),
            pytest.param(78619476736, 8388608, id="greater_than_64gb"),
            pytest.param(88619476736, 16777216, id="greater_than_64gb"),
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
        assert gg_bot_torrent.calculate_piece_size(torrent_size) == piece_size
