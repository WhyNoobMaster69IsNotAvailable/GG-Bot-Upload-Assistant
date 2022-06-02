GG-BOT Upload Assistant is a torrent auto uploader to take the manual work out of uploading. The project is a fork of [XPBot](https://github.com/ryelogheat/xpbot) (huge credits to the original team), which has been modified to work with trackers using different codebases. GG-BOT Upload assistant is intended to be a one size fits all solution for automated torrent uploading.

> Please refer to the readme in `dev` branch to see updated roadmaps and new features. <br>
> If you do not wish to use the docker version of the application, its recommended to checkout and use tags instead of branches for stability reasons.

![One Size Fits All](https://imgs.xkcd.com/comics/standards.png "One Size Fits All")

<br>

## Main Features For GG-BOT Uploaders
- Generate, parse and attach Mediainfo or BDInfo to torrent uploads
- Support for Full Disk uploads
- Frame Accurate Screenshots
- Generates, uploads and attach screenshots to torrent description
- Ability to decide the thumbnail size for screenshots in bbcode
- Obtains TMDB/IMDB/MAL ids automatically
- Creates name following proper conventions
- Generate .torrent with pytor or mktorrent
- Uploads to various trackers seamlessly
- Multiple Image Host support
- Packed as a docker container. (No need to install any additional tools)
- Automatically move .torrent and media to specified folders after upload
- Customizable uploader signature for torrent descriptions
- Automatic upload to torrent client: Immediate cross-seeding
- Auto Re-Uploader flavour for uploading gods

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
            <td rowspan="11"><strong>UNIT3D</strong></td>
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
            <td><strong>Telly</strong></td>
            <td><strong><a href="https://telly.wtf">Telly.wtf</a></strong></td>
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
            <td><strong>XBTIT</strong></td>
            <td><strong>TSP</strong></td>
            <td><strong><a href="https://thesceneplace.com/">TheScenePlace</a></strong></td>
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
            <td rowspan="2"><strong>Gazelle</strong></td>
            <td><strong>NBL</strong></td>
            <td><strong><a href="https://nebulance.io">Nebulance</a></strong></td>
        </tr>
        <tr style="text-align: center">
            <td><strong>ANT</strong></td>
            <td><strong><a href="https://anthelion.me">Anthelion</a></strong></td>
        </tr>
    </tbody>
</table>

<br>


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
    </tbody>
</table>

<br>

<!-- Basic setup -->
## Basic setup for Upload Assistant
### Bare Metal / VM:
1. Clone this repository `git clone https://gitlab.com/NoobMaster669/gg-bot-upload-assistant.git`
> It is recommended to checkout a tag and use it instead of using as the master branch, as there is a possibility for master branch to have bug / error / conflicts during merges.<br>
> Checkout a tag using the command `git checkout tags/<TAG>` 
2. Checkout a release tag/version that you wish to use `git checkout tags/2.0`
2. Install necessary packages ```pip install -r requirements.txt```
3. Grand execute permission for user. `chmod u+x auto_upload.py`
4. Copy `config.env` from `samples/assistant` folder to cloned project root.
5. Fill out the required values in `config.env`
> Ensure that you have optional dependencies installed. <br>
> - [MediaInfo](https://mediaarea.net/en/MediaInfo/Download/Ubuntu)
> - [FFmpeg](https://ffmpeg.org/download.html)
> - [unrar]
> - [mktorrent](https://github.com/pobrn/mktorrent): Use --use_mktorrent flag. (Create .torrent using mktorrent instead of torf)
6. Run the script using [Python3](https://www.python.org/downloads/) (If you're having issues or torf isn't installing, try python3.9)
> Run command template ```python3 auto_upload.py -t <TRACKERS> -p "<FILE_OR_FOLDER_TO_BE_UPLOADED>" [OPTIONAL ARGUMENTS 1] [OPTIONAL ARGUMENTS 2...]``

### Usage Examples Bare Metal / VMs
1. Upload to **Beyond-HD** & **Blutopia** with movie file in **/home/user/Videos/movie.title.year.bluray.1080p.etc.mkv**
    * ```python3 auto_upload.py -t BHD BLU -path /home/user/Videos/movie.title.year.bluray.1080p.etc.mkv```
2. Upload movie **anonymously** to **AsianCinema** with manually specified **TMDB** & **IMDB** IDs
    * ```python3 auto_upload.py -t acm -p /home/user/Videos/movie.title.year.bluray.1080p.etc.mkv -imdb tt0111161 -tmdb 278 -anon```

<br>

### Docker (recommended):
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

### Usage Examples Docker
1. Upload to **Beyond-HD** & **Blutopia** with movie file in **/home/user/Videos/movie.title.year.bluray.1080p.etc.mkv**
    * 
```
     docker run --rm -it \
    -v <PATH_TO_YOUR_MEDIA>:/data \
    --env-file config.env \
    noobmaster669/gg-bot-uploader -t BHD BLU -path /home/user/Videos/movie.title.year.bluray.1080p.etc.mkv
```
2. Upload movie **anonymously** to **AsianCinema** with manually specified **TMDB** & **IMDB** IDs
    * 
```
    docker run --rm -it \
    -v <PATH_TO_YOUR_MEDIA>:/data \
    --env-file config.env \
    noobmaster669/gg-bot-uploader -t acm -p /home/user/Videos/movie.title.year.bluray.1080p.etc.mkv -imdb tt0111161 -tmdb 278 -anon
```
<br /> 

**Things to note:**
1. We use TMDB API for all things media related (Title, Year, External IDs, etc)
2. If you provide the IMDB ID via ```-imdb```, you must include the 'tt' that precedes the numerical ID
3. When providing multiple database (TMDB, IMDB, TVMAZE ) ids via optional arguments, uploader uses the ids with priority **`IMDB > TMDB > TVMAZE`**
4. Full Disk uploads are supported ONLY in FAT version of the docker images. Look for image tags in the format **`:FullDisk-{TAG}`** 

<br>

**Known Issues / Limitations:** (See RoadMap for release plans)
1. Docker volume mounts in debian host system results in permission error in docker container. (No Proper Fix Available)
    * **Workaround**: Torrent file can be created in debian host os by using mktorrent. Use argument `--use_mktorrent or -mkt`
2. No support for Bluray distributors and Bluray disc regions
3. No official support for Blurays in .iso format
4. No support for 3D Bluray discs

<br>