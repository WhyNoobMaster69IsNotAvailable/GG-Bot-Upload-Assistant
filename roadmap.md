# Roadmap
### v2.0.7
- [X] Implement a restart/resume feature for uploads.
- [X] Refactor dupe check logic and hdr bug fix
- [X] Refactor screenshots code
- [X] Add unit tests to the code - phase 1
- [X] Add unit tests to the code - phase 2
- [X] CICD for automated tests
- [X] Improved watch folder movement post-processing
- [X] Add support for immediate cross-seeding to torrent clients
- [X] Support for communicating with torrent clients [ immediate-cross-seeding ]
    - [X] Qbittorrent
    - [X] Rutorrent
- [X] Migrate torrent client feature from v3.0 alpha version
- [X] Refactor and optimize build times for CICD pipelines
    - [X] Introduce GG-BOT base images for faster builds 
- [X] Issue#10: Prevent unnecessary folders from being added in movie uploads
- [X] Issue#12: 4K WEB-DLs video codec are named as HEVC instead of H.265
- [X] Issue#33: Dupe check error when dealing with DV HDR release
- [X] Issue#34: Cross-Seeding uploading torrents for failed uploads
- [X] Issue#35: HEVC codec being used for web releases

### v3.0
- [ ] Add support to apply hybrid mapping to multiple fields
- [X] Automatic torrent re-uploader
- [X] Improved dupe check - Phase 1
- [X] Improved TMDB metadata search
- [X] Support for communicating with torrent clients
    - [X] Qbittorrent
    - [X] Rutorrent
- [X] Implement a caching mechanism
    - [X] Mongo DB
- [ ] EPIC: GG-Bot Visor for reports and failure recoveries
- [ ] Support for overriding target tracker through categories
- [X] Bug Fixes and Testing Phase 1
- [ ] Bug Fixes and Testing Phase 2
- [ ] Discord notification for auto uploaded data

### Backlogs
- [ ] EPIC: Migrate GG-BOT Runtime to work with GG-BOT Auto ReUploader
- [ ] EPIC: Refactor GG-BOT Admin to handle GG-BOT Auto ReUploader
- [ ] Improved Full Disk Support
    - [ ] Support for Bluray Distributors
    - [ ] Detect Bluray disk region automatically
- [ ] Support for communicating with torrent clients
    - [ ] Deluge
    - [ ] Transmission
- [ ] Add support for bitorrent v2 and v2 hybrid torrents
- [ ] Add Support for new platforms
    - [ ] Anasch
    - [ ] MoreThanTV
    - [ ] GreatPosterWall
    - [ ] Swarmazon
- [ ] Add support for DVDs