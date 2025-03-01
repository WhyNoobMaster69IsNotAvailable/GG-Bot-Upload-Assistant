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


class TorrentFailureStatus:
    RAR_EXTRACTION_FAILED = "RAR_EXTRACTION_FAILED"
    TMDB_IDENTIFICATION_FAILED = "TMDB_IDENTIFICATION_FAILED"
    DUPE_CHECK_FAILED = "DUPE_CHECK_FAILED"
    TYPE_AND_BASIC_INFO_ERROR = "TYPE_AND_BASIC_INFO_ERROR"
    UNKNOWN_FAILURE = "UNKNOWN_FAILURE"


class TorrentStatus:
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PARTIALLY_SUCCESSFUL = "PARTIALLY_SUCCESSFUL"
    TMDB_IDENTIFICATION_FAILED = "TMDB_IDENTIFICATION_FAILED"
    PENDING = "PENDING"
    DUPE_CHECK_FAILED = "DUPE_CHECK_FAILED"
    READY_FOR_PROCESSING = "READY_FOR_PROCESSING"
    KNOWN_FAILURE = "KNOWN_FAILURE"
    # unrecoverable error. Needs to check the log or console to resolve them. Not automatic fix available
    UNKNOWN_FAILURE = "UNKNOWN_FAILURE"


class TrackerUploadStatus:
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    DUPE = "DUPE"
    BANNED_GROUP = "BANNED_GROUP"
    PAYLOAD_ERROR = "PAYLOAD_ERROR"


class JobStatus:
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
