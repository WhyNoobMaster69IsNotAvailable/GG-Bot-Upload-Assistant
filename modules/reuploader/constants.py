# GG Bot Upload Assistant
# Copyright (C) 2025  Noob Master669
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

from modules.reuploader.enums import TorrentFailureStatus

TORRENT_DB_KEY_PREFIX = "ReUpload::Torrent"
JOB_REPO_DB_KEY_PREFIX = "ReUpload::JobRepository"
TMDB_DB_KEY_PREFIX = "MetaData::TMDB"
UPLOAD_RETRY_LIMIT = 3

torrent_failure_messages = {
    TorrentFailureStatus.RAR_EXTRACTION_FAILED: "Failed to extract rared contents",
    TorrentFailureStatus.TMDB_IDENTIFICATION_FAILED: "Failed to identify proper TMDb ID",
    TorrentFailureStatus.TYPE_AND_BASIC_INFO_ERROR: "Type and basic info of the torrent could not be identified.",
    TorrentFailureStatus.DUPE_CHECK_FAILED: "A dupe of this torrent already exists in tracker",
    TorrentFailureStatus.UNKNOWN_FAILURE: "Unknown Failure. Please get in touch with dev :(",
}

client_labels_for_failure = {
    TorrentFailureStatus.RAR_EXTRACTION_FAILED: "GGBOT_ERROR_RAR_EXTRACTION",
    TorrentFailureStatus.TMDB_IDENTIFICATION_FAILED: "TMDB_IDENTIFICATION_FAILED",
    TorrentFailureStatus.TYPE_AND_BASIC_INFO_ERROR: "GGBOT_ERROR_TYPE_AND_BASIC",
    TorrentFailureStatus.DUPE_CHECK_FAILED: "DUPE_CHECK_FAILED",
    TorrentFailureStatus.UNKNOWN_FAILURE: "GGBOT_ERROR_UNKNOWN_FAILURE",
}
