# First time setup
## Pre-requisites
<details><summary>Install docker and docker compose</summary>

- For windows mac and linux docker desktop can be installed. If you don't have GUI for linux, the you can use the scripts provided in `dev_scripts` folder.
- If you already have `docker` installed and needs to install `docker-compose` only, then you can use the `install_compose.sh`.
- If you wish to install `docker` and `docker compose`, you can use the `install_docker.sh`.
</details>

## Setup Folders and config files
- Create a new folder `GGBOT_AUTO_REUPLOADER`
- Create a new file `.env` and copy the contents of `samples/reuploader/.env`
- Create a new file `reupload.config.env` and copy the contents of `samples/reuploader/reupload.config.env`
> Depending on the torrent client you plan on using, you'll need to select the appropriate `docker-compose-<CLIENT>.yml` and `.<CLIENT>.env`. The examples mentioned here uses qbittorrent as torrent client.
- Create a new file `docker-compose.yml` and copy the contents of `samples/reuploader/docker-compose-qbittorrent.yml`
- Create a new file `.qbittorrent.env` and copy the contents of `samples/reuploader/.qbittorrent.env`

<details><summary>Using rutorrent as the torrent client</summary>

- Create a new file `docker-compose.yml` and copy the contents of `samples/reuploader/docker-compose-rutorrent.yml`
- Create a new file `.rutorrent.env` and copy the contents of `samples/reuploader/.rutorrent.env`
- Create a new file `.htpasswd` and copy the contents of `samples/reuploader/.htpasswd`
> The default username and password for rutorrent will be `admin` and `admin123` respectively. To change this username and password, you can run the steps mentioned in `dev_scripts/create_htpasswd.txt`
</details>

## Configure GG-BOT Auto ReUploader
- Edit the `.env` and set the current working directory to `BASE_PATH`
    - In this file, the ports used by all the applications can be controlled.
    - Along with this, the version of GG-BOT Auto ReUploader can be updated here as well. [ `GG_BOT_REUPLOADER_VERSION` ]
- Edit the `reupload.config.env` file and fill in the values as per your need. You can refer to the [Environment Configuration](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/auto-reuploader/Environment-Configuration-File) page for more details on each property.
<details><summary>Default Torrent Client Configs</summary>

- When using Qbittorrent, you can set the client configs in `reupload.config.env` as below.
```
client=Qbittorrent
client_host=qbittorrent
client_port=8080
client_username=admin
client_password=adminadmin
client_path=/
```
> If you change the webui password from qbittorrent, then you'll need to set the same username and password to `client_username` and `client_password`.

- When using RuTorrent, you can set the client configs in `reupload.config.env` as below.
```
client=Rutorrent
client_host=http://rutorrent
client_port=80
client_username=admin
client_password=admin123
client_path=/
```
> If you change the default username and password in `.htpasswd` file, then you'll need to set the same values to `client_username` and `client_password`.
</details>
- Edit the `docker-compose.yml` file and scroll to the bottom. The default trackers and any additional command line arguments are provided here.

```
command: [ "-t", "<TRACKERS>", "<OPTIONAL_ARGUMENTS>" ]
```

<details><summary>Samples</summary>

Uploading to trackers ABC and XYZ and using mktorrent to generate torrent.
```
command: [ "-t", "ABC", "XYZ", "--use_mktorrent" ]
```

Uploading to trackers ABC and XYZ and using mktorrent to generate torrent.
```
command: [ "-t", "ABC", "XYZ", "--use_mktorrent" ]
```

Uploading to trackers ABC, PQR, and XYZ.
```
command: [ "-t", "ABC", "PQR", "XYZ" ]
```
</details>

## Start GG-BOT Auto ReUploader
- Run the following command to start gg-bot auto reuploader.
> Note that if you used `install_compose.sh`, you'll need to use `docker-compose`. <br> If you used `install_docker.sh` then you'll need to use `docker compose`

> This command need to be run from within the `GGBOT_AUTO_REUPLOADER` folder. (the folder where you have `docker-compose.yml` and `.env` files)
```
docker compose up -d
```

#### Stop GG-BOT Auto ReUploader
> Note that this command will stop the auto reuploader, torrent client and mongodb used by gg-bot.
```
docker compose stop
```

#### Remove GG-BOT Auto ReUploader
```
docker compose down
```

#### Restart GG-BOT Auto ReUploader or torrent client
```
docker compose restart
```

# Upgrade to new versions
### Upgrading from tags
- Set which version you plan to use to the `GG_BOT_REUPLOADER_VERSION` property in `.env` file.
- Run the below command
```
docker compose up -d
```

### Upgrading when using latest version
- Run the below commands
```
docker compose pull
docker compose up -d
```
