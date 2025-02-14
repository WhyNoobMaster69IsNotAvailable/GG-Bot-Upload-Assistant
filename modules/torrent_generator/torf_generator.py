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
from functools import cached_property
from typing import Callable

from torf import Torrent

from modules.torrent_generator.generator_base import GGBotTorrentGeneratorBase
from modules.config import UploaderTweaksConfig


class GGBotTorfTorrentGenerator(GGBotTorrentGeneratorBase):
    def __init__(
        self,
        *,
        media,
        announce,
        source,
        torrent_title,
        torrent_path_prefix,
        progress_callback: Callable,
    ):
        super().__init__(
            media=media,
            announce=announce,
            source=source,
            torrent_title=torrent_title,
            torrent_path_prefix=torrent_path_prefix,
        )
        config = UploaderTweaksConfig()
        self.piece_size_min = config.TORF_MIN_PIECE_SIZE
        self.piece_size_max = config.TORF_MAX_PIECE_SIZE

        self.torrent = Torrent(
            path=self.media,
            trackers=self.announce,
            source=self.source,
            comment=self.comment,
            created_by=self.created_by,
            exclude_globs=self.default_exclude_globs,
            private=self.private,
            piece_size_min=self.piece_size_min,
            piece_size_max=self.piece_size_max,
            creation_date=self.created_at,
        )
        self.progress_callback = progress_callback

    @cached_property
    def size(self):
        return self.torrent.size

    def get_piece_size(self) -> int:
        return self.torrent.piece_size

    def generate_torrent(self) -> None:
        print("Using python torf to generate the torrent")
        logging.info(
            f"[GGBotTorfTorrentGenerator] Size of the torrent: {self.torrent.size}"
        )
        logging.info(
            f"[GGBotTorfTorrentGenerator] Piece Size of the torrent: {self.torrent.piece_size}"
        )
        self.torrent.generate(callback=self.progress_callback)
        self.torrent.write(self.torrent_path)

    def do_post_generation_task(self) -> None:
        self.torrent.verify_filesize(self.media)
        logging.info(
            "[GGBotTorfTorrentGenerator] Trying to write into {}".format(
                "[" + self.source + "]" + self.torrent_title + ".torrent"
            )
        )
