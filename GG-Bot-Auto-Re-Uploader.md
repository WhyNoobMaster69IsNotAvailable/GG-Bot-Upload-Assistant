<hr>

**GG-BOT Auto Re-Uploader** is a feature associated with GG-BOT Upload Assistant meant for lazy guys, tracker owners or people with tons and tons of storage who want to upload torrents to trackers autonomously. GG-BOT Auto Re-Uploader works in association with a torrent client (Supported Torrent Clients) and will automatically reuploads all torrents to configured tracker.

# Requirements
- Docker
- docker-compose

# Installation and setup
- Create a new folder and copy the contents of the `env-files-samples` in here.
- Choose one of the available compose file from the `env-files-samples` folder. [Qbittorrent or RuTorrent]
- Rename the selected compose file to `docker-compose.yml`
- Edit the environment variable files accordingly
- Start the uploader using the command `docker-compose up -d` or `docker compose up -d` (for latest versions for docker compose)