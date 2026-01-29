# config.env Documentation

<!-- Auto-generated documentation for configuration file -->

## Table of Contents

- [](#)
- [](#)
- [](#)
- [](#)
- [](#)
- [---------------------------](#---------------------------)
- [](#)
- [------------------------------------------------------------](#------------------------------------------------------------)
- [](#)
- [------ If you aren't using docker containers for anything and your rtorrent path is the same as your system path, set 'translation_needed' equal to False -----](#-------if-you-aren't-using-docker-containers-for-anything-and-your-rtorrent-path-is-the-same-as-your-system-path,-set-'translation_needed'-equal-to-false------)
- [](#)

##

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `ENABLE_SENTRY_ERROR_TRACKING` | `True` | Enable sentry error tracking or not. You can disable this if you don't want<br>to send stack traces and errors to the project sentry error log.<br>This is aenabled by default to help with identifying any errors or exceptions pro-actively and take necessary actions.<br>Note: No personal information is collected from this tracking tool. No API_KEYS or PIDs will be sent to the repository.<br>Note: User tracking is not enabled in this project.<br>Note: Search for `if sentry_config.ENABLE_SENTRY_ERROR_TRACKING is True:` to see the configs enabled.<br>You can read more about Gitlab Sentry error tracking here: https://docs.gitlab.com/ee/operations/integrated_error_tracking.html<br>Unfortunately I couldn't find any way to make the error logs publicly available from gitlab. |

##

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `DL_API_KEY` | `# API_KEY` | DarkLand |
| `DL_ANNOUNCE_URL` | `https://darkland.top/announce/<TRACKER_PASS_KEY>` |  |
| `SHRI_API_KEY` | `# API_KEY` | Shareisland |
| `SHRI_ANNOUNCE_URL` | `https://shareisland.org/announce/<TRACKER_PASS_KEY>` |  |
| `ACM_API_KEY` | `# API_KEY` | AsianCinema |
| `ACM_ANNOUNCE_URL` | `https://eiga.moi/announce/<TRACKER_PASS_KEY>` |  |
| `BHD_API_KEY` | `# API_KEY` | Beyond-HD |
| `BHD_ANNOUNCE_URL` | `https://beyond-hd.me/announce/<TRACKER_PASS_KEY>` |  |
| `BLU_API_KEY` | `# API_KEY` | Blutopia |
| `BLU_ANNOUNCE_URL` | `https://blutopia.cc/announce/<TRACKER_PASS_KEY>` |  |
| `R4E_API_KEY` | `# API_KEY` | Racing4Everyone |
| `R4E_ANNOUNCE_URL` | `https://racing4everyone.eu/announce/<TRACKER_PASS_KEY>` |  |
| `ATH_API_KEY` | `# API_KEY` | Aither |
| `ATH_ANNOUNCE_URL` | `https://aither.cc/announce/<TRACKER_PASS_KEY>` |  |
| `TELLY_API_KEY` | `# API_KEY` | Telly.wtf |
| `TELLY_ANNOUNCE_URL` | `https://telly.wtf/announce/<TRACKER_PASS_KEY>` |  |
| `NTELOGO_API_KEY` | `# API_KEY` | Ntelogo |
| `NTELOGO_ANNOUNCE_URL` | `https://ntelogo.org/announce/<TRACKER_PASS_KEY>` |  |
| `TSP_API_KEY` | `# API_KEY` | TheScenePlace |
| `TSP_ANNOUNCE_URL` | `http://www.thesceneplace.com/announce.php?pid=<TRACKER_PASS_KEY>` |  |
| `DT_API_KEY` | `# API_KEY` | DesiTorrents |
| `DT_ANNOUNCE_URL` | `https://desitorrents.rocks/announce/<TRACKER_PASS_KEY>` |  |
| `STC_API_KEY` | `# API_KEY` | SkipTheCommericals |
| `STC_ANNOUNCE_URL` | `https://skipthecommericals.xyz/announce/<TRACKER_PASS_KEY>` |  |
| `STT_API_KEY` | `# API_KEY` | SkipTheTrailers |
| `STT_ANNOUNCE_URL` | `https://skipthetrailers.xyz/announce/<TRACKER_PASS_KEY>` |  |
| `SPD_API_KEY` | `# API_KEY` | SpeedApp |
| `SPD_ANNOUNCE_URL` | `https://ramjet.speedapp.io/<TRACKER_PASS_KEY>/announce` |  |
| `TDB_API_KEY` | `# Tracker Passkey` | TorrentDB |
| `TDB_ANNOUNCE_URL` | `https://reactor.torrentdb.net/announce/<TRACKER_PASS_KEY>` |  |
| `BHDTV_API_KEY` | `# API_KEY` | BIT-HDTV |
| `BHDTV_ANNOUNCE_URL` | `http://tracker.bit-hdtv.com:2710/<TRACKER_PASS_KEY>/announce` |  |
| `NBL_API_KEY` | `# API_KEY - Torrent List and Upload permissions required` | Nebulance |
| `NBL_ANNOUNCE_URL` | `https://nebulance.io:2001/<TRACKER_PASS_KEY>/announce` |  |
| `ANT_API_KEY` | `# API_KEY - Torrent List and Upload permissions required` | Anthelion |
| `ANT_ANNOUNCE_URL` | `https://tracker.anthelion.me:34001/<TRACKER_PASS_KEY>/announce` |  |
| `RF_API_KEY` | `# API_KEY` | ReelFliX |
| `RF_ANNOUNCE_URL` | `https://reelflix.xyz/announce/<TRACKER_PASS_KEY>` |  |
| `SZN_API_KEY` | `# API_KEY` | Swarmazon |
| `SZN_ANNOUNCE_URL` | `https://tracker.swarmazon.club:8443/<TRACKER_PASS_KEY>/announce` |  |
| `LST_API_KEY` | `# API_KEY` | LST |
| `LST_ANNOUNCE_URL` | `https://lst.gg/announce/<TRACKER_PASS_KEY>` |  |
| `3EVILS_API_KEY` | `# API_KEY` | 3Evils |
| `3EVILS_ANNOUNCE_URL` | `https://3evils.net/announce/<TRACKER_PASS_KEY>` |  |
| `PTP_API_USER` | `# API_USER` | PassThePopcorn |
| `PTP_API_KEY` | `# API_KEY` |  |
| `PTP_ANNOUNCE_URL` | `<TRACKER_ANNOUNCE_URL>` |  |
| `PTP_USER_NAME` | `# Username of your PTP Account` |  |
| `PTP_USER_PASSWORD` | `# Password to your account (encouraged to wrap it inside "" )` |  |
| `PTP_2FA_ENABLED` | `False # Set this to True if you have 2fa enabled for your account.` |  |
| `PTP_2FA_CODE` | `# The 2FA key to generate 2FA codes` |  |
| `PSS_API_KEY` | `# API_KEY` | PrivateSilverScreen |
| `PSS_ANNOUNCE_URL` | `https://privatesilverscreen.cc/announce/<TRACKER_PASS_KEY>` |  |
| `GPW_API_KEY` | `# API_KEY` | GreatPostertWall |
| `GPW_ANNOUNCE_URL` | `https://tracker.greatposterwall.com/<TRACKER_PASS_KEY>/announce` |  |
| `RTX_API_KEY` | `# API_KEY` | RetroFlix |
| `RTX_ANNOUNCE_URL` | `http://peer.retroflix.net/announce.php?passkey=<TRACKER_PASS_KEY>` |  |
| `TDC_API_KEY` | `# API_KEY` | TheDarkCommunity |
| `TDC_ANNOUNCE_URL` | `https://thedarkcommunity.cc/announce/<TRACKER_PASS_KEY>` |  |
| `NXT_API_KEY` | `# API_KEY` | N3XTDemoSite |
| `NXT_ANNOUNCE_URL` | `http://demo.n3xtsource.com/announce/<TRACKER_PASS_KEY>` |  |
| `TL_API_KEY` | `# TRACKER_PASS_KEY` | TorrentLeech |
| `TL_ANNOUNCE_URL` | `'https://tracker.torrentleech.org/a/<TRACKER_PASS_KEY>/announce https://tracker.tleechreload.org/a/<TRACKER_PASS_KEY>/announce'` |  |
| `ULCX_API_KEY` | `# API_KEY` | Upload.cx |
| `ULCX_ANNOUNCE_URL` | `http://upload.cx/announce/<TRACKER_PASS_KEY>` |  |
| `FNP_API_KEY` | `# API_KEY` | Fearnopeer |
| `FNP_ANNOUNCE_URL` | `https://fearnopeer.com/announce/<TRACKER_PASS_KEY>` |  |
| `OE_API_KEY` | `# API_KEY` | OnlyEncodes |
| `OE_ANNOUNCE_URL` | `https://onlyencodes.cc/announce/<TRACKER_PASS_KEY>` |  |
| `OTW_API_KEY` | `# API_KEY` | OldToonsWorld |
| `OTW_ANNOUNCE_URL` | `https://oldtoons.world/announce/<TRACKER_PASS_KEY>` |  |
| `VHD_API_KEY` | `# API_KEY` | Vision-HD |
| `VHD_ANNOUNCE_URL` | `https://vision-hd.org/announce/<TRACKER_PASS_KEY>` |  |
| `YOINK_API_KEY` | `# API_KEY` | Yoinked |
| `YOINK_ANNOUNCE_URL` | `https://yoinked.org/announce/<TRACKER_PASS_KEY>` |  |
| `TMG_API_KEY` | `# API_KEY` | TmGHuB |
| `TMG_ANNOUNCE_URL` | `https://tmghub.org/announce.php?pid=<TRACKER_PASS_KEY>` |  |
| `SPL_API_KEY` | `# API_KEY` | SeedPool |
| `SPL_ANNOUNCE_URL` | `https://seedpool.org/announce/<TRACKER_PASS_KEY>` |  |

##

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `TMDB_API_KEY` | `# https://www.themoviedb.org/documentation/api` | TMDB API key (Required) |
| `IMDB_API_KEY` | `# https://tv-api.com/api` | IMDB API key (Optional) |
| `TVDB_API_KEY` | `# https://www.thetvdb.com/api-information` | TVDB Api Key |
| `default_trackers_list` | `` | (Optional) Comma separated list of trackers which should be considered as default or fallback trackers in case `--trackers or -t`  flag is not provided.<br>eg: default_tracker_list=NBL,BLU,BHDTV -> This will by default uploads the torrent to NBL, BLU and BHDTV if `--trackers or -t` is not provided as command line argument.<br>please not that the command line argument `--trackers or -t` has higher priority and overrides `default_tracker_list` property. |

##

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `img_host_1` | `` | GG-BOT uploaders support uploading screenshots to 9 different image hosting services.<br>|  imgbox  |  imgbb  |  freeimage  |  ptpimg  |  imgfi  |  imgur  |  snappie  | pixhost | lensdump |<br>set their order below (spelling matters) (to remove a host just delete the value and leave it blank) |
| `img_host_2` | `` |  |
| `img_host_3` | `` |  |
| `img_host_4` | `` |  |
| `img_host_5` | `` |  |
| `img_host_6` | `` |  |
| `img_host_7` | `` |  |
| `img_host_8` | `` |  |
| `img_host_9` | `` |  |
| `pixhost_api_key` | `leave_blank # No API key needed here` | set the image hosts API keys below |
| `imgbox_api_key` | `leave_blank # No API key needed here` |  |
| `ptpimg_api_key` | `# follow https://github.com/theirix/ptpimg-uploader#api-key guide to get api key` |  |
| `imgbb_api_key` | `` |  |
| `freeimage_api_key` | `` |  |
| `snappie_api_key` | `# Get in touch with staff to get API KEY` |  |
| `imgfi_api_key` | `# Get in touch with staff to get API KEY` |  |
| `imgur_api_key` | `# this is your client_secret` |  |
| `imgur_client_id` | `# register your application (https://api.imgur.com/oauth2/addclient) with Anonymous usage without user authorization to get client id and secret` |  |
| `lensdump_api_key` | `` |  |
| `ptscreens_api_key` | `` |  |
| `num_of_screenshots` | `10` | pretty self explanatory, this will take number of screenshots you want, all evenly spaced depending on how long the video is<br>Set this to 0 if you want to upload without taking any screenshots |
| `thumb_size` | `350` |  |
| `no_spoilers` | `True` | when no_spoilers is enabled, screenshots will be taken from the first half of the file<br>when no_spoilers is disabled, screenshots will be taken from the whole file after equal intervals |

##

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `check_dupes` | `True` |  |

## ---------------------------

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `acceptable_similarity_percentage` | `75` |  |

##

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `auto_mode` | `False` | Set this to 'False' if you want an interactive & hands on experience<br>You'll be prompted to select the correct TMDB ID, Prompted to fix any small issues/discrepancies found during the upload process<br>!! It's recommended to keep this set to 'False' !! |
| `force_auto_upload` | `False` | !! THIS ONLY APPLIES IF ^^ "auto_mode=true" ^^  !!<br>Set this to 'true' if you want an upload to to be forced through unless a critical issue is found<br>e.g. If we can't auto detect 'audio_channels', we can still upload but we'll just omit that part from the torrent title<br>But if something like 'resolution' can't be detected then the upload will be cancelled since 'resolution' is a required API/Upload Key<br>!! It's recommended to keep this set to 'False' !! (Remember, you are responsible for following all tracker rules!) |

## ------------------------------------------------------------

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `live` | `False` | This only applies to BHD since they are the only site that have a 'draft'/'live on site' option<br>Its great for testing and verifying the script submits the correct info before posting it live<br>True == Live on site, everyone can see it<br>False == Goes to your private drafts https://beyond-hd.me/drafts |
| `bdinfo_script` | `` | This is required to upload raw bluray discs (.iso not supported)<br>download & install docker then clone https://github.com/zoffline/BDInfoCLI-ng<br>Inside the project files for BDInfoCLI-ng you'll find a folder called 'scripts' and in it you'll find the file 'bdinfo'<br>You want to paste the full system path to that 'bdinfo' file here<br>If you are using the docker version of the uploader, then there is not need to fill in this value<br>just use FullDisk-{TAG} docker image and you are good to go |

##

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `enable_post_processing` | `False` | GG-BOT Uploader is capable of 2 kinds of post processing steps<br>1. Immediate seeding via torrent client<br>Once a torrent has been uploaded, the uploader can add the dot torrent to a torrent client for immediate seeding.<br>2. Move media and torrents to watch folders<br>You can specify a "Watch Directory" in some torrent clients that will automatically add new .torrent files to its download queue<br>this could be used to automatically start seeding an upload using AutoTools (rtorrent)<br>Once a torrent has been uploaded, the uploader can add the dot torrent to a torrent client for immediate seeding.<br>this feature can be enabled or disabled based on the property below (True/False) |
| `post_processing_mode` | `CROSS_SEED` | you can select the mode using this property. (CROSS_SEED / WATCH_FOLDER) |
| `dot_torrent_move_location` | `` | WATCH_FOLDER_CONFIGS<br>Note: Please ensure that the below two paths (if configured) are available and writable.<br>Uploader will not create these paths. |
| `media_move_location` | `` |  |
| `enable_type_base_move` | `False` | when type based move is enabled,<br>--- torrents will be moved to sub folders within the dot_torrent_move_location<br>--- media will be moved to sub folders within the media_move_location<br>where the subfolder will be the type<br>eg: movies dot torrent will be moved to {dot_torrent_move_location}/movie/...torrent<br>episode dot torrent  will be moved to {dot_torrent_move_location}/episode/...torrent<br>movies file will be moved to {media_move_location}/movie/...file<br>episodes file will be moved to {media_move_location}/episode/...file |
| `client` | `Qbittorrent` | CROSS-SEEDING CONFIGS<br>Specifies the client to which torrents needs to be uploaded.<br>Possible Values: |  Qbittorrent  |  Rutorrent  |  Transmisison  |  Deluge  | |
| `client_host` | `# https://qbit.mydomain.com` | These are the configurations needed to connect to the torrent client |
| `client_port` | `# 443` |  |
| `client_username` | `# username` |  |
| `client_password` | `# my_password` |  |
| `client_path` | `/` | Applicable for Rutorrent and Transmisison.<br>Rutorrent: Default is /<br>Transmission: Default value must be configured as /transmission/rpc or a custom path as per your configuration |
| `cross_seed_label` | `` | The label / category to which cross-seeding torrents needs to be added to.<br>Default: GGBotCrossSeed |

## ------ If you aren't using docker containers for anything and your rtorrent path is the same as your system path, set 'translation_needed' equal to False -----

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `translation_needed` | `False` |  |
| `client_accessible_path` | `` |  |
| `uploader_accessible_path` | `` |  |

##

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `readable_temp_data` | `False` | This property decided whether or not the sub_folders in temp_upload containing screenshots, mediainfo, urls etc needs to be in a human readable format or not.<br>By default a unique hash will be generated for the input path and it'll be used.<br>If this property is enabled then the sub_folder will be created using the file name. |
| `uploader_signature` | `` | Uploader signature is added at the bottom of the torrent description. By default if no signature is provided the upload assistant will add<br>``` Uploaded with ❤ using GG-BOT Upload Assistant ``` as the uploader signature.<br>With this property you can add your own custom signature to torrent uploads.<br>Notes:<br>1. The signature provided has to be plain text or must be a valid bbcode<br>2. The signature will automatically be wrapped inside [center][/center] tag by the upload assistant<br>Sample: uploader_signature=[url=https://ibb.co/VH6n8tC][img]https://i.ibb.co/VH6n8tC/Manchester-United-Logo11.jpg[/img][/url] |
| `torf_mix_piece_size` | `KB_16` | Set the max / min allowed piece size when using torf to generate torrents.<br>See: https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/issues/159 for discussions.<br>This property can be used to set smaller max piece sizes in case you face memory issues in shared seedboxes.<br>Possible values: KB_16, KB_32, KB_64, MB_1, MB_2, MB_4, MB_8, MB_16, MB_32, MB_64<br>Defaults: min => KB_16  max => MB_32 |
| `torf_max_piece_size` | `MB_32` |  |
