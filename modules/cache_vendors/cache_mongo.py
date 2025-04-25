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
import logging

from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

from modules.config import CacheConfig
from modules.exceptions.exception import (
    GGBotCacheClientException,
    GGBotCacheNotInitializedException,
)


def map_cursor_to_list(function):
    @functools.wraps(function)
    def decorator(*args, **kwargs):
        return list(map(lambda d: d, function(*args, **kwargs)))

    return decorator


class Mongo:
    mongo_client = None
    is_mongo_initialized = False
    database = None

    def __init__(self):
        """Initialize connection to MongoDB with authentication support."""
        self.config: CacheConfig = CacheConfig()
        if not self.is_mongo_initialized:
            try:
                self.mongo_client = self._get_mongo_client()
                self.mongo_client.admin.command("ping")
                self.database = self.mongo_client[self.config.CACHE_DATABASE]
                # Create required collections
                self._create_collections()
                self.is_mongo_initialized = True
                logging.info(
                    "[Cache] Successfully connected to MongoDB and initialized collections"
                )
            except Exception as ex:
                if "Authentication failed" in str(ex):
                    logging.fatal(
                        "[Cache] MongoDB authentication failed. Please check your username and password."
                    )
                elif "Connection refused" in str(ex):
                    logging.fatal(
                        "[Cache] MongoDB connection refused. Is the server running?"
                    )
                else:
                    logging.fatal(f"[Cache] Failed to connect to MongoDB. Error: {ex}")

                raise GGBotCacheClientException(
                    f"Failed to connect to MongoDB. Error: {ex}"
                )

    def _get_mongo_client(self):
        """Get a MongoDB client with authentication support if credentials are provided."""
        try:
            # Build connection string based on whether authentication is needed
            if (
                self.config.CACHE_USERNAME is not None
                and len(self.config.CACHE_USERNAME) > 0
            ):
                # With authentication
                MONGO_URL = (
                    f"mongodb://{self.config.CACHE_USERNAME}:{self.config.CACHE_PASSWORD}"
                    f"@{self.config.CACHE_HOST}:{self.config.CACHE_PORT}/{self.config.CACHE_DATABASE}"
                    f"?authSource={self.config.CACHE_AUTH_DB}"
                )
                logging.info(
                    f"[Cache] Connecting to MongoDB with authentication (user: {self.config.CACHE_USERNAME}, "
                    f"host: {self.config.CACHE_HOST}:{self.config.CACHE_PORT}, "
                    f"db: {self.config.CACHE_DATABASE}, authSource: {self.config.CACHE_AUTH_DB})"
                )
            else:
                # Without authentication
                MONGO_URL = f"mongodb://{self.config.CACHE_HOST}:{self.config.CACHE_PORT}/{self.config.CACHE_DATABASE}"
                logging.info(
                    f"[Cache] Connecting to MongoDB without authentication "
                    f"(host: {self.config.CACHE_HOST}:{self.config.CACHE_PORT}, "
                    f"db: {self.config.CACHE_DATABASE})"
                )

            # Create MongoDB client with connection options
            client = MongoClient(
                MONGO_URL,
                serverSelectionTimeoutMS=5000,  # 5 second timeout for server selection
                connectTimeoutMS=5000,  # 5 second timeout for connection
            )

            return client
        except Exception as e:
            logging.error(f"[Cache] Error creating MongoDB client: {e}")
            raise GGBotCacheClientException(
                f"Failed to create MongoDB client. Error: {e}"
            )

    def hello(self):
        if self.is_mongo_initialized:
            self.mongo_client.admin.command("ping")
            print("Mongo Server Connection Established Successfully")
            return True
        else:
            print("Failed to initialize connection to Mongo server")
            return False

    def _create_collection_if_not_exist(self, collection_name):
        try:
            self.database.create_collection(collection_name)
        except CollectionInvalid:
            # collection already exists. Let's suppress this
            pass

    def _create_collections(self):
        # This manual creation is needed because the collections created are not visible in external tools.
        collections = ["ReUpload_Torrent", "ReUpload_JobRepository", "MetaData_TMDB"]
        for collection in collections:
            self._create_collection_if_not_exist(collection)

    def __get_collection(self, key):
        if not self.is_mongo_initialized:
            raise GGBotCacheNotInitializedException()
        key = key.split("::")
        return self.database[key[0] + "_" + key[1]]

    def save(self, key, data):
        collection = self.__get_collection(key)
        if "_id" not in data:
            collection.insert_one(data)
        else:
            collection.replace_one({"_id": data["_id"]}, data, upsert=True)

    def delete(self, key, query=None):
        """Method to delete data from the cache stored against a key."""
        collection = self.__get_collection(key)
        if len(key.split("::")) <= 2:
            # no hash provided in key. hence we need to use the user provided query
            # if user has not provided any query then we'll raise an exception
            if query is None:
                raise Exception("No hash or query provided. Cannot delete document")
            # returns the number of documents deleted
            return collection.delete_many(query)
        else:
            collection.delete_one({"hash": key.split("::")[2]})
            return 1

    @map_cursor_to_list
    def get(self, key, filter=None):
        collection = self.__get_collection(key)
        # <=2 because keys are in the form of GROUP::COLLECTION::KEY
        filter = (
            ({} if filter is None else filter)
            if len(key.split("::")) <= 2
            else {"hash": key.split("::")[2]}
        )
        return collection.find(filter)

    @map_cursor_to_list
    def advanced_get(self, key, limit, page_number, sort_field, filter=None):
        collection = self.__get_collection(key)
        return (
            collection.find(filter if filter is not None else {})
            .skip((page_number - 1) * limit)
            .limit(limit)
            .sort(sort_field, -1)
        )

    def count(self, key, filter=None):
        collection = self.__get_collection(key)
        return collection.count_documents(filter if filter is not None else {})

    def close(self):
        """
        Method to close the connection to the redis server
        This is a wrapper around the redis `hgetall` operation
        """
        if not self.is_mongo_initialized:
            raise GGBotCacheNotInitializedException()
        self.mongo_client.close()
