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
from enum import Enum
from typing import List


class ContentType(Enum):
    MOVIE = "movie"
    TV_SHOW = "episode"

    def __init__(self, uid):
        self._id = uid

    @property
    def id(self):
        return self._id


class MetadataProvider(Enum):
    TMDB = ("TMDB", "TheMovieDB", "https://api.themoviedb.org")
    IMDB = ("IMDB", "IMDb", "https://tv-api.com")
    TVMAZE = ("TVMAZE", "TV Maze", "https://api.tvmaze.com")
    TVDB = ("TVDB", "TVDb", "https://api4.thetvdb.com")
    MAL = ("MAL", "My Anime List", None)

    def __init__(self, uid, name, url):
        self._id = uid
        self._name = name
        self._url = url

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    @classmethod
    def values(cls) -> List["MetadataProvider"]:
        return list(cls)
