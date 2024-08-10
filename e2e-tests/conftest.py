import re
import time
from pathlib import Path
from typing import Dict

import pytest
import qbittorrentapi
import yaml
from testcontainers.core.container import DockerContainer
from requests_mock import Mocker
import requests
from testcontainers.core.network import Network

working_folder = Path(__file__).resolve().parent.parent
e2e_resources_dir = "/e2e-tests/resources"


@pytest.fixture(scope="module")
def docker_testing_network():
    network = Network()
    network.create()

    yield network

    network.remove()


@pytest.fixture(scope="module")
def qbittorrent_container():
    container = DockerContainer("linuxserver/qbittorrent:4.6.5")
    container.with_bind_ports(50001, 50001)

    container.with_env("WEBUI_PORT", "50001")
    container.with_env("PUID", "1000")
    container.with_env("PGID", "1000")
    container.with_env("TZ", "UTC")

    container.start()
    yield container
    container.stop()


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


# @pytest.fixture(scope="module")
# def rutorrent_container():
#     container = DockerContainer("linuxserver/rtorrent")
#     container.with_exposed_ports(5000)
#     container.start()
#     yield container
#     container.stop()


@pytest.fixture(scope="module")
def mock_server_config():
    with open(
        f"{working_folder}{e2e_resources_dir}/mock_server_config.yml", "r"
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

        # Register the mock response
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


@pytest.fixture(scope="module")
def mock_server(mock_server_config):
    with Mocker() as mock:
        _update_mock_server_based_on_config(
            server=mock, server_config=mock_server_config
        )
        yield mock


class TestE2ESetup:
    def test_qbittorrent_container_setup(
        self, qbittorrent_container, qbittorrent_credentials
    ):
        self.qbt_client = qbittorrentapi.Client(
            host=f"https://{qbittorrent_credentials['host']}",
            port=qbittorrent_credentials["port"],
            username=qbittorrent_credentials["username"],
            password=qbittorrent_credentials["password"],
            VERIFY_WEBUI_CERTIFICATE=False,
        )

        assert self.qbt_client.auth_log_in() is None, "Failed to login to qbittorrent"

    # def test_rtorrent_container_setup(self, rtorrent_container):
    #     host = rtorrent_container.get_container_host_ip()
    #     port = rtorrent_container.get_exposed_port(5000)
    #
    #     response = requests.get(f"http://{host}:{port}")
    #     assert response.status_code == 200, "rTorrent is not running properly"

    def test_mock_server_container_setup(self, mock_server):
        response = requests.get("http://example.com/api/test")
        assert response.status_code == 200
        assert response.json() == {"message": "mocked response 1"}

        response = requests.post("http://example.com/api/another")
        assert response.status_code == 201
        assert response.json() == {"message": "mocked response 2"}

        response = requests.get("http://example.com/api/error")
        assert response.status_code == 404
        assert response.json() == {"error": "Not Found"}
