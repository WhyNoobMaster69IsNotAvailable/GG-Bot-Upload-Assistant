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

import logging
import re
import time
from pathlib import Path
from typing import Dict
from unittest import mock

import pytest
import yaml
from pymongo import MongoClient
from testcontainers.core.container import DockerContainer
from requests_mock import Mocker
from testcontainers.core.network import Network

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
e2e_resources_dir = "/e2e-tests/resources"
deluge_auth_file_path = "deluge/auth"
deluge_conf_file_path = "deluge/core.conf"
deluge_plugins_dir = "deluge/plugins/"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="module", autouse=True)
def e2e_test_working_folder():
    yield Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module", autouse=True)
def docker_testing_network():
    network = Network()
    network.create()
    network_name = network.name

    logging.info(
        f"[TestContainers] Created new temporary docker network for e2e testing: {network_name}"
    )
    yield network
    network.remove()
    logging.info(
        f"[TestContainers] Removed the temporary docker network used for e2e testing: {network_name}"
    )


@pytest.fixture(scope="module", autouse=True)
def mongo_container(docker_testing_network):
    logging.info("[TestContainers]Creating MongoDB docker container")
    container = DockerContainer("mongo:latest")
    container.with_bind_ports(27017, 27017)
    container.with_network(docker_testing_network)
    container.with_network_aliases("mongo")

    container.start()
    container_id = container._container.id
    logging.info(
        f"[TestContainers] Created a MongoDB container for e2e testing: {container_id}"
    )
    yield container
    container.stop()
    logging.info(
        f"[TestContainers] Removed the MongoDB container used for e2e testing: {container_id}"
    )


@pytest.fixture(scope="module", autouse=True)
def mongo_container_with_auth(docker_testing_network, e2e_test_working_folder):
    logging.info(
        "[TestContainers]Creating MongoDB docker container with authentication"
    )
    container = DockerContainer("mongo:latest")
    container.with_bind_ports(27017, 27018)
    container.with_network(docker_testing_network)
    container.with_network_aliases("mongo_auth")
    container.with_volume_mapping(
        f"{e2e_test_working_folder}/{e2e_resources_dir}/mongo/mongo-init.js",
        "/docker-entrypoint-initdb.d/mongo-init.js",
        "ro",
    )

    container.start()
    container_id = container._container.id
    logging.info(
        f"[TestContainers] Created a MongoDB container with auth for e2e testing: {container_id}"
    )
    yield container
    container.stop()
    logging.info(
        f"[TestContainers] Removed the MongoDB container with auth used for e2e testing: {container_id}"
    )


@pytest.fixture(scope="module", autouse=True)
def qbittorrent_container(docker_testing_network, e2e_test_working_folder):
    logging.info("[TestContainers]Creating Qbittorrent docker container")
    container = DockerContainer("linuxserver/qbittorrent:4.6.5")
    container.with_bind_ports(50001, 50001)
    container.with_network(docker_testing_network)
    container.with_network_aliases("qbittorrent")

    container.with_env("WEBUI_PORT", "50001")
    container.with_env("PUID", "1000")
    container.with_env("PGID", "1000")
    container.with_env("TZ", "UTC")
    # the paths needs to be same to allow reuploader to access the media files
    container.with_volume_mapping(
        f"{e2e_test_working_folder}/{e2e_resources_dir}",
        f"{e2e_test_working_folder}/{e2e_resources_dir}",
    )

    container.start()
    container_id = container._container.id
    logging.info(
        f"[TestContainers] Created a qbittorrent container for e2e testing: {container_id}"
    )
    yield container
    container.stop()
    logging.info(
        f"[TestContainers] Removed the qbittorrent container used for e2e testing: {container_id}"
    )


@pytest.fixture(scope="module", autouse=True)
def deluge_container(docker_testing_network, e2e_test_working_folder):
    logging.info("[TestContainers]Creating Deluge docker container")
    container = DockerContainer("lscr.io/linuxserver/deluge:latest")
    container.with_bind_ports(58846, 58846)
    container.with_bind_ports(8112, 8112)
    container.with_network(docker_testing_network)
    container.with_network_aliases("deluge")

    container.with_env("PUID", "1000")
    container.with_env("PGID", "1000")
    container.with_env("TZ", "UTC")

    # the paths needs to be same to allow reuploader to access the media files
    container.with_volume_mapping(
        f"{e2e_test_working_folder}/{e2e_resources_dir}",
        f"{e2e_test_working_folder}/{e2e_resources_dir}",
    )
    container.with_volume_mapping(
        f"{e2e_test_working_folder}/{e2e_resources_dir}/{deluge_auth_file_path}",
        "/config/auth",
    )
    container.with_volume_mapping(
        f"{e2e_test_working_folder}/{e2e_resources_dir}/{deluge_conf_file_path}",
        "/config/core.conf",
    )
    container.with_volume_mapping(
        f"{e2e_test_working_folder}/{e2e_resources_dir}/{deluge_plugins_dir}",
        "/config/plugins/",
    )

    container.start()
    container_id = container._container.id
    logging.info(
        f"[TestContainers] Created Deluge container for e2e testing: {container_id}"
    )
    yield container
    container.stop()
    logging.info(
        f"[TestContainers] Removed the Deluge container used for e2e testing: {container_id}"
    )


@pytest.fixture
def transmission_container_function_scoped(
    docker_testing_network, e2e_test_working_folder
):
    logging.info(
        "[TestContainers]Creating Transmission docker container scoped to function"
    )
    container = DockerContainer("lscr.io/linuxserver/transmission:latest")
    container.with_bind_ports(9091, 9092)
    container.with_network(docker_testing_network)
    container.with_network_aliases("transmission_function")

    container.with_env("PUID", "1000")
    container.with_env("PGID", "1000")
    container.with_env("TZ", "UTC")
    container.with_env("USER", "TRANSMISSION_USER")
    container.with_env("PASS", "TRANSMISSION_USER_PASSWORD")

    # the paths needs to be same to allow reuploader to access the media files
    container.with_volume_mapping(
        f"{e2e_test_working_folder}/{e2e_resources_dir}",
        f"{e2e_test_working_folder}/{e2e_resources_dir}",
    )

    container.start()
    container_id = container._container.id
    logging.info(
        f"[TestContainers] Created Transmission container for e2e testing scoped to function: {container_id}"
    )
    yield container
    container.stop()
    logging.info(
        f"[TestContainers] Removed the Transmission container used for e2e testing scoped to function: {container_id}"
    )


@pytest.fixture(scope="module", autouse=True)
def transmission_container(docker_testing_network, e2e_test_working_folder):
    logging.info("[TestContainers]Creating Transmission docker container")
    container = DockerContainer("lscr.io/linuxserver/transmission:latest")
    container.with_bind_ports(9091, 9091)
    container.with_network(docker_testing_network)
    container.with_network_aliases("transmission")

    container.with_env("PUID", "1000")
    container.with_env("PGID", "1000")
    container.with_env("TZ", "UTC")
    container.with_env("USER", "TRANSMISSION_USER")
    container.with_env("PASS", "TRANSMISSION_USER_PASSWORD")

    # the paths needs to be same to allow reuploader to access the media files
    container.with_volume_mapping(
        f"{e2e_test_working_folder}/{e2e_resources_dir}",
        f"{e2e_test_working_folder}/{e2e_resources_dir}",
    )

    container.start()
    container_id = container._container.id
    logging.info(
        f"[TestContainers] Created Transmission container for e2e testing: {container_id}"
    )
    yield container
    container.stop()
    logging.info(
        f"[TestContainers] Removed the Transmission container used for e2e testing: {container_id}"
    )


@pytest.fixture(scope="module", autouse=True)
def rutorrent_container(docker_testing_network, e2e_test_working_folder):
    logging.info("[TestContainers]Creating rutorrent docker container")
    container = DockerContainer("crazymax/rtorrent-rutorrent:5.1.5-7.2")
    container.with_bind_ports(8080, 50002)
    container.with_network(docker_testing_network)
    container.with_network_aliases("rutorrent")
    # the paths needs to be same to allow reuploader to access the media files
    container.with_volume_mapping(
        f"{e2e_test_working_folder}/{e2e_resources_dir}",
        f"{e2e_test_working_folder}/{e2e_resources_dir}",
    )

    container.with_env("PUID", "1001")
    container.with_env("PGID", "1001")
    container.with_env("TZ", "UTC")

    container.start()
    container_id = container._container.id
    logging.info(
        f"[TestContainers] Created a rutorrent container for e2e testing: {container_id}"
    )
    yield container
    container.stop()
    logging.info(
        f"[TestContainers] Removed the rutorrent container used for e2e testing: {container_id}"
    )


@pytest.fixture
def mongo_credentials(mongo_container_with_auth):
    yield {
        "username": "gg_bot_user",
        "password": "gg_bot_password",
        "auth_db": "admin",
    }


@pytest.fixture
def rutorrent_credentials(rutorrent_container):
    # This needs more time when running in kubernetes cluster to start properly
    time.sleep(30)  # allowing time for rutorrent container to start and be ready

    rutorrent_logs = "".join(
        [
            log.decode("utf-8")
            for log in rutorrent_container.get_logs()
            if isinstance(log, bytes)
        ]
    )
    # search the logs to ensure that container and services have started
    service_done_message = re.search(
        r"NOTICE: ready to handle connections", rutorrent_logs
    )
    assert service_done_message is not None

    yield {
        "host": rutorrent_container.get_container_host_ip(),
        "port": rutorrent_container.get_exposed_port(8080),
        "hashed": "",
        # "hashed": base64.b64encode("admin:admin".encode("ascii")).decode("ascii"),
        "username": "",
        "password": "",
    }


@pytest.fixture(scope="module")
def deluge_credentials(deluge_container):
    time.sleep(5)  # allowing time for deluge container to start properly
    deluge_logs = "".join(
        [
            log.decode("utf-8")
            for log in deluge_container.get_logs()
            if isinstance(log, bytes)
        ]
    )

    webui_port = re.search(
        r"Connection to 127\.0\.0\.1 8112 port \[tcp/.*] succeeded!",
        deluge_logs,
    )
    daemon_rpc_port = re.search(
        r"Connection to 127\.0\.0\.1 58846 port \[tcp/.*] succeeded!",
        deluge_logs,
    )
    init_log = re.search(r"\[ls\.io-init] done\.", deluge_logs)
    assert bool(init_log) is True, "Deluge container didn't start as expected"
    assert bool(webui_port) is True, "Failed to connect to deluge webui port"
    assert bool(daemon_rpc_port) is True, "Failed to connect to deluge daemon rpc port"

    host = deluge_container.get_container_host_ip()
    port = deluge_container.get_exposed_port(58846)

    yield {
        "host": host,
        "port": port,
        "username": "localclient",
        "password": "46495af7aaba2b27a33002c596747e82bdf88450",
    }


@pytest.fixture
def transmission_credentials_function_scoped(transmission_container_function_scoped):
    time.sleep(2)  # allowing time for transmission container to start properly

    transmission_function_scoped_logs = "".join(
        [
            log.decode("utf-8")
            for log in transmission_container_function_scoped.get_logs()
            if isinstance(log, bytes)
        ]
    )
    match1 = re.search(
        r"Connection to localhost \(127\.0\.0\.1\) 9091 port \[tcp/.*] succeeded!",
        transmission_function_scoped_logs,
    )
    match2 = re.search(r"\[ls\.io-init] done\.", transmission_function_scoped_logs)

    assert bool(match1) is True, "Failed to connect to transmission host"
    assert bool(match2) is True, "Transmission container didn't start as expected"

    host = transmission_container_function_scoped.get_container_host_ip()
    port = transmission_container_function_scoped.get_exposed_port(9091)

    yield {
        "host": host,
        "port": port,
        "username": "TRANSMISSION_USER",
        "password": "TRANSMISSION_USER_PASSWORD",
    }


@pytest.fixture(scope="module")
def transmission_credentials(transmission_container):
    time.sleep(2)  # allowing time for transmission container to start properly

    transmission_logs = "".join(
        [
            log.decode("utf-8")
            for log in transmission_container.get_logs()
            if isinstance(log, bytes)
        ]
    )
    match1 = re.search(
        r"Connection to localhost \(127\.0\.0\.1\) 9091 port \[tcp/.*] succeeded!",
        transmission_logs,
    )
    match2 = re.search(r"\[ls\.io-init] done\.", transmission_logs)

    assert bool(match1) is True, "Failed to connect to transmission host"
    assert bool(match2) is True, "Transmission container didn't start as expected"

    host = transmission_container.get_container_host_ip()
    port = transmission_container.get_exposed_port(9091)

    yield {
        "host": host,
        "port": port,
        "username": "TRANSMISSION_USER",
        "password": "TRANSMISSION_USER_PASSWORD",
    }


@pytest.fixture(scope="module")
def qbittorrent_credentials(qbittorrent_container):
    time.sleep(2)  # allowing time for qbittorrent container to start properly

    qbittorrent_logs = "".join(
        [
            log.decode("utf-8")
            for log in qbittorrent_container.get_logs()
            if isinstance(log, bytes)
        ]
    )

    generated_password = re.search(
        r"A temporary password is provided for this session:\s(\w+)", qbittorrent_logs
    )
    generated_password = (
        generated_password.group(1) if generated_password is not None else ""
    )
    assert (
        generated_password is not None
    ), "Failed to get the generated password from qbittorrent container"

    host = qbittorrent_container.get_container_host_ip()
    port = qbittorrent_container.get_exposed_port(50001)

    yield {
        "host": host,
        "port": port,
        "username": "admin",
        "password": generated_password,
    }


@pytest.fixture(scope="module")
def mock_server_config(e2e_test_working_folder):
    with open(
        f"{e2e_test_working_folder}{e2e_resources_dir}/mock_server_config.yml", "r"
    ) as file:
        config = yaml.safe_load(file)
    return config


def _update_mock_server_based_on_config(server, server_config: Dict) -> None:
    for mock_item in server_config["mocks"]:
        method = mock_item["method"].lower()
        url = mock_item["url"]
        headers = mock_item.get("headers", {})
        response_text = mock_item["response"]["body"]
        status_code = mock_item["response"]["status_code"]

        if method == "get":
            server.get(
                url, text=response_text, status_code=status_code, headers=headers
            )
        elif method == "post":
            server.post(
                url, text=response_text, status_code=status_code, headers=headers
            )
        elif method == "put":
            server.put(
                url, text=response_text, status_code=status_code, headers=headers
            )
        elif method == "delete":
            server.delete(
                url, text=response_text, status_code=status_code, headers=headers
            )


@pytest.fixture(scope="module", autouse=True)
def mock_server(mock_server_config):
    with Mocker(real_http=True) as mock:
        _update_mock_server_based_on_config(
            server=mock, server_config=mock_server_config
        )
        yield mock


@pytest.fixture(scope="module", autouse=True)
def e2e_mongo_client_with_auth(mongo_container_with_auth):
    MONGO_URL = f"mongodb://{mongo_container_with_auth.get_container_host_ip()}:{mongo_container_with_auth.get_exposed_port(27017)}/gg-bot-reuploader-e2e-tests"
    yield MongoClient(MONGO_URL)


@pytest.fixture(scope="module", autouse=True)
def e2e_mongo_client(mongo_container):
    MONGO_URL = f"mongodb://{mongo_container.get_container_host_ip()}:{mongo_container.get_exposed_port(27017)}/gg-bot-reuploader-e2e-tests"
    yield MongoClient(MONGO_URL)


@pytest.fixture(scope="module", autouse=True)
def patched_mediainfo_libraries():
    lib_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "libs"))

    with mock.patch("pymediainfo.MediaInfo._get_library_paths") as mock_get_paths:
        if sys.platform == "darwin":
            mock_get_paths.return_value = (
                os.path.join(lib_dir, "libmediainfo.0.dylib"),
                os.path.join(lib_dir, "libmediainfo.dylib"),
            )
        else:
            mock_get_paths.return_value = ("libmediainfo.so.0",)
        yield
