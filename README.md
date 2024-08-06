<div align="center">
<h1 align="center">GG-BOT Upload Assistant & Auto ReUploader</h1>
  <a href="https://gitlab.com/NoobMaster669/gg-bot-upload-assistant">
    <img src="https://i.ibb.co/vsqPhLM/gg-bot-round.png" alt="Logo" width="128">
  </a>
</div>
<br>
<div align="center">
    One size fits all solution for automated torrent uploading
    <br />
    <a href="https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/home">Read Wiki</a>
    ·
    <a href="https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/issues/new">Report Bug</a>
    ·
    <a href="https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/issues/new">Request Feature</a>
</div>
<br>
<div align="center">
    <a href="https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/commits/master"><img alt="pipeline status" src="https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/badges/master/pipeline.svg" /></a>
    <a href="https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/releases"><img alt="Latest Release" src="https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/badges/release.svg" /></a>
    <a href="https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/commits/master"><img alt="coverage report" src="https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/badges/master/coverage.svg" /></a>
    <a href="https://hub.docker.com/r/noobmaster669/gg-bot-uploader/"><img alt="coverage report" src="https://img.shields.io/docker/pulls/noobmaster669/gg-bot-uploader" /></a>
    <a href="https://gitlab.com/NoobMaster669/gg-bot-upload-assistant"><img src="https://img.shields.io/badge/dynamic/json?color=green&logo=gitlab&label=stars&query=%24.star_count&url=https%3A%2F%2Fgitlab.com%2Fapi%2Fv4%2Fprojects%2F32631784"></a>
    <a href="https://codecov.io/gl/NoobMaster669/gg-bot-upload-assistant">
  <img src="https://codecov.io/gl/NoobMaster669/gg-bot-upload-assistant/branch/feature/swarmazon/graph/badge.svg?token=YORMWC9D77"/>
  <a href="https://www.codacy.com/gl/NoobMaster669/gg-bot-upload-assistant/dashboard?utm_source=gitlab.com&amp;utm_medium=referral&amp;utm_content=NoobMaster669/gg-bot-upload-assistant&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/474a4fa3f5b5483bbf464d82afefe7cf"/></a>
</a>
</div>

## Overview:
GG-BOT Upload Assistant is a torrent auto uploader to take the manual work out of uploading. The project is a fork of [XPBot](https://github.com/ryelogheat/xpbot) (huge credits to the original team), which has been modified to work with trackers using different codebases. GG-BOT Upload assistant is intended to be a one size fits all solution for automated torrent uploading.


> Please refer to the readme in `dev` branch to see updated roadmaps and new features.

> If you do not wish to use the docker version of the application, its recommended to checkout and use tags instead of branches for stability reasons.


<div align="center">
    <img src="https://imgs.xkcd.com/comics/standards.png">
</div>

<br>

# Main Features
* Generate, parse and attach Mediainfo or BDInfo to torrent uploads
* Support for Full Disk uploads
* Frame Accurate Screenshots
* Generates, uploads and attach screenshots to torrent description
* Ability to decide the thumbnail size for screenshots in bbcode
* Obtains TMDB/IMDB/MAL ids automatically
* Creates name following proper conventions
* Generate .torrent with pytor or mktorrent
* Uploads to various trackers seamlessly
* Multiple Image Host support
* Packed as a docker container. (No need to install any additional tools)
* Automatically move .torrent and media to specified folders after upload
* Customizable uploader signature for torrent descriptions
* Automatic upload to torrent client: Immediate cross-seeding
* Auto Re-Uploader flavour for uploading gods and tracker owners

<br>

## Supported Platforms And Trackers
<table>
    <tbody>
        <tr style="text-align: center; font-size:20px">
            <td><strong>Platform</strong></td>
            <td><strong>Acronym</strong></td>
            <td><strong>Site Name</strong></td>
        </th>
        <tr style="text-align: center">
            <td rowspan="20"><strong>UNIT3D</strong></td>
            <td><strong>ACM</strong></td>
            <td><strong><a href="https://asiancinema.me">AsianCinema</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>ATH</strong></td>
            <td><strong><a href="https://aither.cc">Aither</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>BHD</strong></td>
            <td><strong><a href="https://beyond-hd.me">Beyond-HD</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>BLU</strong></td>
            <td><strong><a href="https://blutopia.xyz">Blutopia</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>R4E</strong></td>
            <td><strong><a href="https://racing4everyone.eu">Racing4Everyone</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>Ntelogo</strong></td>
            <td><strong><a href="https://ntelogo.org">Ntelogo</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>DT</strong></td>
            <td><strong><a href="https://desitorrents.rocks/">DesiTorrents</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>STT</strong></td>
            <td><strong><a href="https://skipthetrailers.xyz/">SkipTheTrailers</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>STC</strong></td>
            <td><strong><a href="https://skipthecommericals.xyz/">SkipTheCommericals</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>RF</strong></td>
            <td><strong><a href="https://reelflix.xyz/">ReelFliX</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>LST</strong></td>
            <td><strong><a href="https://lst.gg">LST</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>TDC</strong></td>
            <td><strong><a href="https://thedarkcommunity.cc/">TheDarkCommunity</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>TELLY</strong></td>
            <td><strong><a href="https://telly.wtf">Telly</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>FNP</strong></td>
            <td><strong><a href="https://fearnopeer.com">Fearnooper</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>ULCX</strong></td>
            <td><strong><a href="https://upload.cx">Upload.cx</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>OE</strong></td>
            <td><strong><a href="https://onlyencodes.cc">OnlyEncodes</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>OTW</strong></td>
            <td><strong><a href="https://oldtoons.world">OldToonsWorld</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>SHRI</strong></td>
            <td><strong><a href="https://shareisland.org">Shareisland</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>VHD</strong></td>
            <td><strong><a href="https://vision-hd.org">Vision-HD</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>DL</strong></td>
            <td><strong><a href="https://darkland.top">DarkLand</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td rowspan="1"><strong>XBTIT</strong></td>
            <td><strong>TSP</strong></td>
            <td><strong><a href="https://thesceneplace.com/">TheScenePlace</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td rowspan="1"><strong>Swarmazon</strong></td>
            <td><strong>SZN</strong></td>
            <td><strong><a href="https://swarmazon.club/">Swarmazon</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>TBDev</strong></td>
            <td><strong>SPD</strong></td>
            <td><strong><a href="https://speedapp.io/">SpeedApp</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>TorrentDB</strong></td>
            <td><strong>TDB</strong></td>
            <td><strong><a href="https://torrentdb.net/">TorrentDB</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>BIT-HDTV</strong></td>
            <td><strong>BHDTV</strong></td>
            <td><strong><a href="https://www.bit-hdtv.com">BIT-HDTV</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td rowspan="4"><strong>Gazelle</strong></td>
            <td><strong>NBL</strong></td>
            <td><strong><a href="https://nebulance.io">Nebulance</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>ANT</strong></td>
            <td><strong><a href="https://anthelion.me">Anthelion</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>PTP</strong></td>
            <td><strong><a href="https://passthepopcorn.me">PassThePopcorn</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>GPW</strong></td>
            <td><strong><a href="https://greatposterwall.com">GreatPosterWall</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>TorrentLeech</strong></td>
            <td><strong>TL</strong></td>
            <td><strong><a href="https://www.torrentleech.org">TorrentLeech</a></strong></td>
        </tr>
    </tbody>
</table>

## Supported image Hosts
<table>
    <tbody>
        <tr style="text-align: center; font-size:20px">
            <td><strong>#</strong></td>
            <td><strong>Image Host</strong></td>
        </tr>
        <tr>
            <td>1</td>
            <td>imgbox</td>
        </tr>
        <tr>
            <td>2</td>
            <td>imgbb</td>
        </tr>
        <tr>
            <td>3</td>
            <td>freeimage</td>
        </tr>
        <tr>
            <td>4</td>
            <td>ptpimg</td>
        </tr>
        <tr>
            <td>5</td>
            <td>imgfi</td>
        </tr>
        <tr>
            <td>6</td>
            <td>imgur</td>
        </tr>
        <tr>
            <td>7</td>
            <td>snappie</td>
        </tr>
        <tr>
            <td>8</td>
            <td>pixhost</td>
        </tr>
        <tr>
            <td>9</td>
            <td>lensdump</td>
        </tr>
        <tr>
            <td>10</td>
            <td>ptscreens</td
        </tr>

    </tbody>
</table>

<br>

<!-- Basic setup -->
# Basic setup for Upload Assistant

## Docker (recommended):
1. Create new folder / dir [`mkdir GGBotUploader && cd GGBotUploader`]
2. Download `samples/assistant/config.env` to the newly created folder (`GGBotUploader`)
3. Fill out the required values in `config.env`
5. Run GG-Bot-Uploader using docker run command below. (For more samples refer to Wiki [Docker Run Command Examples](https://gitlab.com/gg-bot/gg-bot-uploader/-/wikis/Docker-Run-Command-Examples))
```
docker run --rm -it \
    -v <PATH_TO_YOUR_MEDIA>:/data \
    --env-file config.env \
    noobmaster669/gg-bot-uploader -t ATH TSP -p "/data/<YOUR_FILE_FOLDER>"
```
> See [DockerHub](https://hub.docker.com/r/noobmaster669/gg-bot-uploader/tags) for various tags
<br />

## Bare Metal / VM:
1. Clone this repository `git clone https://gitlab.com/NoobMaster669/gg-bot-upload-assistant.git`
> It is recommended to checkout a tag and use it instead of using as the master branch, as there is a possibility for master branch to have bug / error / conflicts during merges.<br>
> Checkout a tag using the command `git checkout tags/<TAG>`
2. Checkout a release tag/version that you wish to use `git checkout tags/2.0`
3. Install necessary packages ```pip install -r requirements/requirements.txt```
4. Grand execute permission for user. `chmod u+x auto_upload.py`
5. Copy `config.env` from `samples/assistant` folder to cloned project root.
6. Fill out the required values in `config.env`
> Ensure that you have optional dependencies installed. <br>
> - [MediaInfo](https://mediaarea.net/en/MediaInfo/Download/Ubuntu)
> - [FFmpeg](https://ffmpeg.org/download.html)
> - unrar
> - [mktorrent](https://github.com/pobrn/mktorrent): Use --use_mktorrent flag. (Create .torrent using mktorrent instead of torf)
7. Run the script using [Python3](https://www.python.org/downloads/) (If you're having issues or torf isn't installing, try python3.9)
> Run command template ```python3 auto_upload.py -t <TRACKERS> -p "<FILE_OR_FOLDER_TO_BE_UPLOADED>" [OPTIONAL ARGUMENTS 1] [OPTIONAL ARGUMENTS 2...]```
> Please see Bare Metal Installation and Upgrade Wiki for details instructions.

<br>

## Windows Setup (Upload Assistant):
> In Windows, it's recommended to use [Anaconda Distribution](https://www.anaconda.com/products/distribution) to create
> python environment and install packages.

> If you are not using anaconda, make sure to install the latest version
> of [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/). This is required for `python-Levenshtein` package.
> Skip to Step 4 if you are not using conda.
1. Create a new conda environment with Python 3.8.16.
2. Activate the newly created environment
```commandline
activate gg-bot
```
3. Install `python-levenshtein` using conda.
```commandline
conda install python-levenshtein
```
4. Clone this repository git clone https://gitlab.com/NoobMaster669/gg-bot-upload-assistant.git
>It is recommended to check out a tag and use it instead of using as the master branch, as there is a possibility for master branch to have bug / error / conflicts during merges.
Checkout a tag using the command `git checkout tags/<TAG>`
5. Checkout a release `tag/version` that you wish to use `git checkout tags/2.0`
6. Install GG-BOT python packages.
```commandline
pip install -r requirements/requirements.txt
```
7. Copy `config.env` from `samples/assistant` folder to cloned project root.
8. Fill out the required values in `config.env`
> NOTE: Disable `readable_temp_data` when working in windows <br>
> Set `readable_temp_data=False` in `config.env`
<br />

**Things to note:**
1. We use TMDb and IMDb for all things media related (Title, Year, External IDs, etc)
2. If you provide the IMDB ID via ```-imdb```, you must include the 'tt' that precedes the numerical ID
3. When providing multiple database (TMDB, IMDB, TVMAZE ) ids via optional arguments, uploader uses the ids with priority **`IMDB > TMDB > TVMAZE > TVDB`**
4. Full Disk uploads are supported ONLY in FAT version of the docker images. Look for image tags in the format **`:FullDisk-{TAG}`**
5. When running in windows, ensure that `readable_temp_data` is set to `False` (disabled).

<br>

**Known Issues / Limitations:** (See RoadMap for release plans)
1. Docker volume mounts in debian host system results in permission error in docker container. (No Proper Fix Available)
    * **Workaround**: Torrent file can be created in debian host os by using mktorrent. Use argument `--use_mktorrent or -mkt`
2. No support for Bluray distributors and Bluray disc regions
3. No official support for Blurays in .iso format
4. No support for 3D Bluray discs
5. Cannot pass `tmdb`, `imdb`, `tvmaze` and `mal` ids as command line arguments when running in `batch` mode.

<br>

# Roadmap
### v3.1.6
- [ ] New Tracker: UHDBits
- [ ] New Tracker: TMGHub
- [ ] Fixed BLU announce URL
- [ ] Template based custom description
- [ ] Issue#79: Not able to cross-seed rared releases
- [ ] Issue#93: Bit-hdtv doesn't allow ptpimg screenshots
- [ ] Issue#151: Re-uploader MongoDB with authentication

### v3.1.7
- [ ] EPIC: GG-Bot Auto Uploader
- [ ] EPIC: GG-Bot Visor for reports and failure recoveries
- [ ] Issue#96: DVD Remux not supported
- [ ] Issue#97: PTP uploads fail if no tags in IMDB
- [ ] Improved TMDB metadata search Phase 3
- [ ] Support for encrypted values from config
- [ ] Add support for adding primary language to title
- [ ] Use new search API for ANT

### Backlogs
- [ ] EPIC: GGBOT Metadata Aggregator
- [ ] EPIC: GGBOT P2P Network Relay
- [ ] EPIC: Migrate GG-BOT Runtime to work with GG-BOT Auto ReUploader
- [ ] EPIC: Refactor GG-BOT Admin to handle GG-BOT Auto ReUploader
- [ ] Better MAL id detection
- [ ] Ability to reuse already existing torrents.
- [ ] Improved Full Disk Support
    - [ ] Support for Bluray Distributors
    - [ ] Detect Bluray disk region automatically
- [ ] Support for communicating with torrent clients
    - [ ] Deluge
    - [ ] Transmission
- [ ] Add support for bitorrent v2 and v2 hybrid torrents
- [ ] Add Support for new platforms
    - [ ] MoreThanTV
    - [ ] DanishBytes
    - [ ] RetroFlix
    - [ ] PirateTheNet
- [ ] Add support for DVDs

<br>

# Contributors
This project exists thanks to all the people who contribute.

<a href="https://gitlab.com/NoobMaster669" title="NoobMaster669">
  <img width="50" src="https://secure.gravatar.com/avatar/94c4464ce0eb2b2792b6b3ff84c65ff7?s=192&d=identicon">
</a>
<a href="https://gitlab.com/LostRager" title="LostRager">
  <img width="50" src="https://secure.gravatar.com/avatar/4c31843c40dcb1e44db407a273709729?s=192&d=identicon">
</a>
<a href="https://gitlab.com/kvkv07" title="KV KV">
  <img width="50" src="https://secure.gravatar.com/avatar/963c6423dbf302f9385367ae7ecddefb?s=192&d=identicon">
</a>
<a href="https://gitlab.com/aeraeca" title="Aeraeca">
  <img width="50" src="https://secure.gravatar.com/avatar/8c850cc650185ac5169830cf60bed786?s=192&d=identicon">
</a>
<a href="https://gitlab.com/JerryLarry" title="Jerry">
  <img width="50" src="https://secure.gravatar.com/avatar/5879a189d87cb16d937ff307b0c829c9?s=192&d=identicon">
</a>
<a href="https://gitlab.com/starlight543" title="asedwfasfasfas">
  <img width="50" src="https://secure.gravatar.com/avatar/5b326cf39498822a2ef8fd8847121bc6?s=192&d=identicon">
</a>
<a href="https://gitlab.com/edge2020tgx" title="Edge Edge">
  <img width="50" src="https://secure.gravatar.com/avatar/f2cf30323908e2a379d918ab929cc7d3?s=192&d=identicon">
</a>
<a href="https://gitlab.com/ZMarkC" title="Mark C">
  <img width="50" src="https://secure.gravatar.com/avatar/2ac42c0f350e5f33c63f9a0c9e364b616fcf152a7866fd03e755a06c925da957?s=192&d=identicon">
</a>
<a href="https://gitlab.com/tiberio87" title="Tiberio">
  <img width="50" src="https://secure.gravatar.com/avatar/c98e56cdb1de7d72892ec848d2ed2f84351d9b555ee63b34a82e26e7cf837c49?s=384&d=identicon">
</a>
<a href="https://gitlab.com/marcusnyrog" title="ddaarree">
  <img width="50" src="https://gitlab.com/uploads/-/system/user/avatar/21731497/avatar.png?width=800">
</a>
<a href="https://gitlab.com/highlamb" title="highlamb">
  <img width="50" src="https://secure.gravatar.com/avatar/8ec7d3297d389bb0d08c857323479fd28106fce82a29205410386017ee70b22c?s=384&d=identicon">
</a>
<a href="https://gitlab.com/darklandy" title="darklandy">
  <img width="50" src="https://secure.gravatar.com/avatar/8624204464a8601f14cc20bfb8526b1a5dbf7bca7b7f6138a32bbc9e04ec6a7c?s=384&d=identicon">
</a>
<a href="https://gitlab.com/PTScreens" title="PTScreens">
  <img width="50" src="https://secure.gravatar.com/avatar/8468e07fddc384b050fc961496d7ad25e9738d0e4034da78048305c57a054684?s=384&d=identicon">
</a>
<br>

# Change Log
## **3.1.5**
    New Image host 
        * PTScreens -> [@PTScreens]
        
    New Tracker
        * DarkLand -> [@darklandy]
    
    Bug Fixes
        * Fixed Torrent.desi api -> [@highlamb]

<br>

## **3.1.4**
    New Trackers
        * Vision-HD -> [@marcusnyrog]

<br>

## **3.1.3**
    New Trackers
        * Shareisland -> [@tiberio87]

    Bug Fixes
        * Issue#155: Free-leech flag changes for Unit3d v7.0+

<br>

## **3.1.2**
    New Trackers
        * OldToonsWorld -> [@ZMarkC]

<br>

## **3.1.1**
    New Trackers
        * OnlyEncodes -> [@edge2020tgx]

    New Features
        * Upload report after completing an upload job

    Bug Fixes
        * Issue#130: TMDB to MAL Flask app appears to down
        * Issue#150: Uploader crash if `spoken_languages` not available from tmdb

<br>

## **3.1.0**
    New Trackers
        * Fearnooper
        * Upload.cx -> [@starlight543]

    New Features
        * Support adding language title to upload title -> [@aeraeca]

    Bug Fixes
        * Issue#134: PTP uploads fails if 2FA is disabled
        * Issue#135: PTP uploads for 10-bit releases if no tags are

<br>

## **3.0.9**
    Bug Fixes
        * Bug Fix: Uploader having difficulty when file title has `AKA` -> [@aeraeca]
        * Issue#126: PTP: Bot does not add 10-bit and Dual Audio edition tags
        * Issue#132: GPW Incorrect source

<br>

## **3.0.8**
    New Trackers
        * TorrentLeech

    New Features
        * Support for ATH exclusive flag

    Bug Fixes
        * Issue#114: Not detecting Opus audio codec
        * Issue#116: Error on image upload: json KeyError: 'url_viewer'
        * Issue#118: GPW upload failures
        * Issue#120: Unable to upload web-dls to GPW

<br>

## **3.0.7**
    Underhood Changes
        * Code refactor v3

    New Features
        * Support for trumpable flags for PTP
        * Updated banned groups for TSP
        * Initial windows support (_might be buggy_)

    Bug Fixes
        * Issue#98: Season Packs Not using 1st episode for Mediainfo
        * Issue#106: Releases tagged incorrectly as scene
        * Issue#107: Streaming service names being ignored
        * Issue#108: SpeedApp SD and HD TV episode mismatch
        * Issue#110: GGBotException when connection to mongo fails
        * Issue#111: SpeedApp cross seed torrents not registered

<br>

## **3.0.6**
    New Trackers
        * TheDarkCommunity

    New Features
        * Support for Anamorphic videos and screenshots in display resolution

    Bug Fixes
        * Fixed an issue where release groups was not identified for AV1 releases
        * Issue#67: Torf fails due to invalid characters in torrent title
        * Issue#92: Reuploader has issues with folders starting with [ ]

<br>

## **3.0.5**
    New Features
        * Support for DVD and HD-DVD PTP uploads
        * Support for custom upload tags from argument
        * Skipping upload of banned groups

    Bug Fixes
        * Issue#80: DDH releases are not identified and is marked as no group
        * Issue#84: Multi tag added to release with unknown audio
        * Issue#86: Application crash if srrdb api call fails
        * Issue#87: reuploading ptpimg and imgbox screens when uploading to gpw
        * Issue#90: Certain remuxes identified as full discs

<br>

## **3.0.4**
    New Trackers (Only for Upload Assistant)
        * PassThePopcorn
        * GreatPosterWall

    New Image Hosts
        * Lensdump

    New Features
        * Get movie/tv youtube trailers
        * Support for providing external tracker templates
        * Updated banned groups for BLU
        * New dry run mode to test uploader without uploading payload to trackers
        * Support for tagging `Multi` audio releases for DT
        * Support for tagging `Dual-Audio` for BLU and ATH

    Underhood Changes
        * JSONSchema for template validations
        * Introduced new 2FA module
        * Support for detecting and identifying subtitle information.
        * Visor server module (ALPHA) (ReUploader)

    Bug Fixes
        * Issue#41: Incorrect channel count detected
        * Issue#42: Support for Dual Audio Detection
        * Issue#82: Thumbnail for BHD screenshots

<br>

## **3.0.3**
    New Image Hosts
        * Pixhost

    New Features
        * Support for IMDB api
        * Improved TMDB metadata search Phase 2
        * Accept TVDB id from runtime argument
        * Updated source for lst
        * Restored tracker: Telly

    Bug Fixes
        * Issue#77: NOGROUP identified as group when title has spaces instead of dot

<br>

## **3.0.2**
    Bug Fixes
        * Issue#70: Support SDTV uploads to TDB
        * Issue#71: Unable to upload to PTPImg

<br>

## **3.0.1**
    New Trackers
        * 3Evils
        * LST

    New Features
        * Added support for tag generation and use for tracker uploads

    Bug Fixes
        * Fixing the broken reuploader in v3.0
        * Issue#52: ANT upload does not detect/set Atmos or other parameters
        * Issue#69: Release group not identified when uploading movie folders

<br>

## **3.0**
    New Trackers
        * Swarmazon

    New Features
        * Open Source GG-BOT Uploaders
        * Hybrid Mapping v2
        * GG-BOT Auto ReUploader
        * Auto ReUploader: Dynamic Tracker Selection
        * Auto ReUploader: Caching
            * Mongo DB
        * Auto ReUploader: Bug Fixes and Testing Phase 1
        * Auto ReUploader: Bug Fixes and Testing Phase 2
        * Removed discord webhook and notifications
        * Accept MAL id as user argument
        * Human readable sub folder for temporary data
        * Ability to force add multiple files in movie dot torrent
        * Support for 32MB piece size for torrents larger than 64 GB (mktorrent only)

    Underhood Changes
        * Improved dupe check - Phase 1
        * Improved TMDB metadata search Phase 1
        * Improved screenshots url management
        * Code cleanup for better code quality
        * Codecov and Codacy integrations
        * More unit tests for stability and reduced bugs
        * Improved tests coverage

    Bug Fixes
        * Issue#18: Invalid name for BHDTV uploads
        * Issue#32: Atmos not detected if not present in file name
        * Issue#37: Automatic cross-seeding not working
        * Issue#39: Info log says translation needed even when disabled
        * Issue#40: False positive DV detection
        * Issue#47: TDB uploads fails from auto-reuploader
        * Issue#51: Setting DV as release group instead of NOGROUP
        * Issue#61: TVMaze ID argument overridden when no result returned

<br>

## **2.0.7**
    Removed Trackers
        * Telly - ShutDown

    New Features
        * Ability to resume / reuse assets from previous uploads
        * Improved watch folder movement during post-processing
        * Support for immediate corss-seeding to torrent clients
        * Support for communicating with torrent clients [ immediate-cross-seeding ]
            * Qbittorrent
            * Rutorrent
        * Migrated torrent client feature from v3.0 alpha version

    Underhood Changes
        * Refactored dupe check logic
        * Refactored screenshots and image upload logic
        * Add unit tests to existing code
        * Add unit tests to the cicd pipeline
        * Refactored cicd for better performance and faster builds
        * Introded pre-built base images for cicd improvements

    Bug Fixes
        * Issue#10: Prevent unnecessary folders from being added in movie uploads
        * Issue#12: 4K WEB-DLs video codec are named as HEVC instead of H.265
        * Issue#33: Dupe check error when dealing with DV HDR release
        * Issue#34: Cross-Seeding uploading torrents for failed uploads
        * Issue#35: HEVC codec being used for web releases
        * Issue#36: Broken screenshots after new UNIT3D update
        * Issue:38: Cross-seeding error with multiple trackers

<br>

## **2.0.6**
    New Trackers
        * Anthelion
        * ReelFlix

    New Features
        * Refactoring code in anticipation to v3.0 release
        * Improved dupe check with HDR Support
        * Improved dupe check with support for REPACKS and PROPER
        * Dynamic piece size calculation for mktorrent
        * Implemented a Skip Screenshots feature

    Bug Fixes
        * Issue#25: Unhashable list error when uploading tv shows
        * Issue#26: NBL dupe check issue
        * Issue#28: 720p contents being tagged as SD for UNIT3D trackers
        * Issue#30: Application crash while making TMDB API Call
        * Issue#31: Uploads to BIT-HDTV failing

<br>

## **2.0.5**
    New Trackers
        * SkipTheTrailers

    New Features
        * Support for default trackers
        * Ability to upload to all available trackers (USE WITH CAUTION)
        * Improved TMDB search results filtering

    Bug Fixes
        * Issue#19: Multiple episode naming bug fixed
        * Issue#20: Uploader crash when handling complete packs from tracker
        * Issue#23: IMDB Id cannot be obtained from TVMaze

<br>

## **2.0.4**

    New Trackers
        * BIT-HDTV
        * Nebulance

    New Image Hosts
        * Snappie

    New Features
        * Added new bugs to be fixed :p
        * Support for TVMaze and a database for TV Shows
        * Improved key translations and mapping for tracker specific jobs
        * Support for screenshots without thumbnail size limit
        * New Hybrid Mapping for tracker SkipTheCommercials
        * Added support for more streaming services

    Bug Fixes
        * Issue#9: Multiple dupe prompt being asked bug fixed
        * Issue#11: DTS-X audio codec naming error bug fixed
        * Issue#14: BHDTV <3 symbol missing bug fixed
        * Issue#15: HLG not detected from file name bug fixed

<br>

## **2.0.3**

    New Image Hosts
        * Imgur

    Bug Fixes
        * ptp image uploads not working bug fix

<br>

## **2.0.2**

    New Trackers
        * TorrentDB

    New Features
        * Support for custom messages / descriptions during upload
        * Support for custom upload signatures for regular uploaders

    Bug Fixes
        * SpeedApp screenshots missing bug fixed

<br>

## **2.0.1**

    New Trackers
        * SkipTheCommercials

    New Image Hosts
        * Imgfi

    Underhood changes
        * Improved batch processing
        * Refactor tracker acronyms and api keys to config file

<br>

## **2.0**

    New Trackers
        * SpeedApp
        * UHD-Heaven

    Underhood changes
        * Performance Optimizations
        * Platform based site tagging
        * Improved argument description and help
        * Dynamic media summary based on the extracted metadata
        * Frame accurate screenshots
        * Environment file key validations
        * Code refactor
        * Masking sensitive data in log file
        * Various steps added to reduce the coupling with UNIT3D codebase

    New Features
        * Hybrid category mapping [See Site-Templates Wiki]
        * Support for Blu-ray Full Disc uploads [fat image required]
        * Ability to choose playlist manually for full disk uploads
        * Improved BDInfo parsing
        * Extended BluRay regions list as configurable json
        * Debug mode for detailed analysis
        * Extended Scene Groups list as configurable json
        * Extended Streaming Services list as configurable json
        * Audio Codec list as configurable json
        * Extended audio codec list for full disk codecs
        * TSP internal uploads
        * Move dot torrents based on type after upload
        * Feature merges from XPBot
            * Improved dupe check
            * Improved screenshot upload process
            * Added support for ptpimg
            * Removed support for imgyukle

    Bug Fixes
        * No dupe message not being shown in certain cases
        * Invalid PA streaming service tagging
        * PQ10, HLG and WCG HDR Formats not being detected
        * TSP dupe check for web sourced contents

<br>

##  **1.1**
    New Trackers
        * DesiTorrents
    New Features
        * No spoiler screenshot feature
        * CICD pipeline optimizations
        * Default screenshots count changes
        * Strip text feature for torrent dupe checks
    Bug Fixes
        * Full season tv-show upload bug fix
        * Updated tag naming bug fix

<br>

##  **1.0.1**
    Bug Fixes
        * Updated naming conventions for HDR, Atmos Audio, and BluRay source

<br>

##  **1.0**
    New Features
        * Initial Release
        * Added docker images for aarch64 and armhf OS Architectures
        * CICD Pipeline Changes
        * Updated Templates
        * Support for Xbtit Platform with custom API
        * Screenshot thumbnail feature

<br>

# Wiki
### [Video usage examples](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Usage:-Video-Examples)
### [Arguments and User Inputs](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Arguments-and-User-Inputs)
### [Environment Configuration File (config.env breakdown)](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Environment-Configuration-File)
### [/site_templates/*.json guide](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Tracker-Templates)
### [Automatic re-uploading (autodl)](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/autodl-irssi-automatic-re-uploading)
### [Docker: Run Command Examples](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Docker-Run-Command-Examples)
### [Docker: Noob Friendly Setup Guide](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Noob-Friendly-Setup-Guide)
### [Support For New Trackers](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Support-For-New-Trackers)
<br>
