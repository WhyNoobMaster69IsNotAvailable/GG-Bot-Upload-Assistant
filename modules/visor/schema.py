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

from marshmallow import Schema, fields, post_load
from marshmallow.validate import OneOf

from modules.cache_vendors.constants import available_actions, TorrentActions
from modules.visor.exceptions import GGBotVisorFieldValidationError


class GGBotReUploaderSchema(Schema):
    pass


class UpdateTmdbSchema(GGBotReUploaderSchema):
    tmdb = fields.Str(missing=None)
    imdb = fields.Str(missing=None)

    @post_load
    def validate(self, data):
        if data["tmdb"] is None and data["imdb"] is None:
            raise GGBotVisorFieldValidationError("One of TMDb or IMDb id is required")


class ActionItems(GGBotReUploaderSchema):
    action = fields.Str(required=True, validate=OneOf(available_actions))
    action_options = fields.Dict(required=True, default={})

    @post_load
    def parse_action_object(self, data):
        if data["action"] == TorrentActions.UPDATE_TMDB:
            data["action_options"] = UpdateTmdbSchema().dump(data["action_options"])
        return data


class GGBotTorrentSchema(GGBotReUploaderSchema):
    id = fields.Str(required=True)
    action_items = fields.Nested(ActionItems, required=True)
