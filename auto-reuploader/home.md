<hr>

**GG-BOT Auto Re-Uploader** is a feature associated with GG-BOT Upload Assistant meant for lazy guys, tracker owners or people with tons and tons of storage who want to upload torrents to trackers autonomously. GG-BOT Auto Re-Uploader works in association with a torrent client (Supported Torrent Clients) and will automatically reuploads all torrents to configured tracker.

> Can you run GG-BOT Auto ReUploader on bare metal without using docker? <br><br> **Yes. But its really really not recommended.**<br>
Consider the auto reuploader as a baby, and if you plan on running it on bare metal you'll have to take care of it just like a baby. Using docker is like hiring a nanny to look after the baby.

# What can it do?
- Automatically reupload all / selected torrents added to a client to configured trackers
- Dynamic Tracker Selection Mode
- Generate, parse and attach Mediainfo to torrent uploads
- Frame Accurate Screenshots
- Generates, uploads and attach screenshots to torrent description
- Ability to decide the thumbnail size for screenshots in bbcode
- Obtains TMDB/IMDB/MAL ids automatically
- Creates name following proper conventions
- Generate .torrent with torf mktorrent
- Uploads to various trackers seamlessly
- Multiple Image Host support
- Packed as a docker container. (No need to install any additional tools)

# Limitations
- Full Disk uploads are not supported for Auto ReUploader

# Requirements
- Docker
- docker-compose

# Installation and setup
- Create a new folder and copy the contents of the `env-files-samples` in here.
- Choose one of the available compose file from the `env-files-samples` folder. [Qbittorrent or RuTorrent]
- Rename the selected compose file to `docker-compose.yml`
- Edit the environment variable files accordingly
- Start the uploader using the command `docker-compose up -d` or `docker compose up -d` (for latest versions for docker compose)

> To install docker and docker compose in linux machines, you can use the easy-install scripts in `dev_scripts` folder.
In windows, mac and linux you can also install [Docker Desktop](https://www.docker.com/products/docker-desktop/).

# Dynamic Tracker Selection
Dynamic tracker selection is a mode of GG-BOT Auto ReUploader, that allows users to control the trackers to which each torrents gets reuploaded. In normal mode, the auto reuploader is started with a bunch of default trackers, and uploaders will reupload torrents to those trackers.

In dynamic tracker selection mode, the uploader starts with default trackers, and uploads to those trackers. In addition to this, user can override this setting for each torrent through torrent labels / categories in torrent client.

For example: consider the default trackers are ABC, XYZ. And you wish to upload a torrent to tracker DEF and MNO only. In this case, you can set the label of that torrent to `GGBOT::DEF::MNO`. That particular torrent will be uploaded only to DEF and MNO (this torrent will not be uploaded to ABC and XYZ).

# Wiki Articles
### [Environment Configuration](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/auto-reuploader/Environment-Config-File)
### [Arguments and User Inputs](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/auto-reuploader/Arguments-and-User-Inputs)
### [Setup And Upgrade](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/auto-reuploader/Setup-And-Upgrade)
### [Authenticated MongoDB](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/auto-reuploader/Authenticate-Mongo-DB)
