GG-BOT Upload Assistant provides various runtime arguments that can be used to customize the individual upload process. These are mainly classified into 4 different groups.
- Mandatory arguments
- Commonly used arguments
- Less commonly used arguments
- Internal upload arguments

NOTE: 
* If the **Value Needed** for any argument is **NO**, then only the argument flag needs to be provided in run command. 
* If the **Value Needed** for any argument is **YES**, then the argument flag followed by the value for the argument also needs to be provided. 

<br>

## Mandatory Arguments
These are the arguments that are required for each upload. All the arguments under this category must be provided for the upload assistant to start the upload process. For majority of the uploads only these mandatory arguments are needed.
| #| Flag | Value Needed | Description | Example |
| ------ | ------ | ------ | ------ | ------ |
| 1| **-p** or **--path** | Yes | Use this to provide path(s) to file/folder| **-p /data/movies/my.movie.mkv** |

<details><summary>Examples using the mandatory arguments</summary>

Upload a torrent to trackers ATH and BLU: The tracker acronyms **ATH** and **BLU** needs to be provided after mentioning the **-t** tag
```
docker run --rm -it --env-file config.env -v /movies:/movies noobmaster669/gg-bot-uploader:latest -t ATH BLU -p "/movies/my.movie.mkv"
```
or 
```
docker run --rm -it --env-file config.env -v /movies:/movies noobmaster669/gg-bot-uploader:latest --trackers ATH BLU -p "/movies/my.movie.mkv"
```

Upload a movie my.movie.new.mkv to tracker TSP: The file that needs the be uploads needs to be provided as the value for arguments -p. Please note that it is recommended to provide the --path arguments inside double quotes (") to accomodate for spaces and special characters.
```
docker run --rm -it --env-file config.env -v /movies:/movies noobmaster669/gg-bot-uploader:latest -t ATH BLU -p "/movies/my.movie.new.mkv"
```
or 
```
docker run --rm -it --env-file config.env -v /movies:/movies noobmaster669/gg-bot-uploader:latest --trackers ATH BLU --path "/movies/my.movie.mkv"
```

Upload a movie my.movie.new.mkv to the default trackers: When the `-t` or `--tracker` argument is not provided then, the default trackers will be taken from the `default_trackers_list` present in the config.env file.
```
docker run --rm -it --env-file config.env -v /movies:/movies noobmaster669/gg-bot-uploader:latest --path "/movies/my.movie.mkv"
```
</details>

<br>

## Commonly Used Arguments
This category contains the list of arguments that are used commonly.

> It's recommended to use the `-imdb` or `-tmdb` or `-tvmaze` arguments if `auto_mode=true` (auto-detection isn't always 100% accurate)

> Note that for the movie db, ids the priority order are **imdb**, **tmdb** and **tvmaze**. <br>
> Meaning <br>
> If both imdb and tmdb id are provided, then imdb id will be used to determine the tmdb and tvmaze id. <br>
> Similarly if tmdb and tvmaze ids are provided by the user, then the tmdb id will be used to identify the imdb id and tvmaze id.

| #| Flag | Value Needed | Description | Example |
| ------ | ------ | ------ | ------ | ------ |
| 1 | **-t** or **--trackers** | Yes | Tracker(s) to upload to. Space-separates if multiple (no commas)| **-t BHD BHDTV NBL** |
| 2 | **-a** or **--all_trackers** | No | Select all trackers that can be uploaded to automatically | **--all_trackers** |
| 3 | **-tmdb** | Yes | Use this to manually provide the TMDB ID | **-tmdb 566525** |
| 4 | **-imdb** | Yes | Use this to manually provide the IMDB ID | **-imdb tt7569576** |
| 5 | **-tvmaze** | Yes | Use this to manually provide the TVmaze ID | **-tvmaze 50603** |
| 6 | **-anon** | No | Used to mark the upload to be anonymous. | **-anon** |
<details><summary>Examples using the commonly used arguments</summary>

Upload a movie my.movie.new.mkv to all the possible trackers: To upload to all the trackers, simply add the `-a` or `--all_trackers` argument to the run command. The uploader will automatically select all the trackers that have been configured properly.
```
docker run --rm -it --env-file config.env -v /movies:/movies noobmaster669/gg-bot-uploader:latest -a --path "/movies/my.movie.mkv"
```
or
```
docker run --rm -it --env-file config.env -v /movies:/movies noobmaster669/gg-bot-uploader:latest --all_trackers --path "/movies/my.movie.mkv"
```

Upload a show anonymously to trackers: THe **-anon** flag needs to be provided to the run command.
```
docker run --rm -it --env-file config.env -v /movies:/movies noobmaster669/gg-bot-uploader:latest -t BLU -p "/movies/my.movie.mkv" -anon
```

Specify the IMDB ID for an upload. If any of the imdb, tmdb or tvmaze ids are provided then the upload assistant will not search tmdb to find out the id, the user provided id will be used in the upload process. The below example shows providing the database ids as arguments to the run command.
```
docker run --rm -it --env-file config.env -v /movies:/movies noobmaster669/gg-bot-uploader:latest -t BLU -p "/movies/my.movie.mkv" -imdb tt10767168
```
```
docker run --rm -it --env-file config.env -v /movies:/movies noobmaster669/gg-bot-uploader:latest -t BLU -p "/movies/my.movie.mkv" -tmdb 617708
```
```
docker run --rm -it --env-file config.env -v /movies:/movies noobmaster669/gg-bot-uploader:latest -t BLU -p "/movies/my.tv.show.mkv" -tvmaze 50603
```
Please note that more than one id can be provided as the run arguments. In such cases the highest preference will be given to the IMDB ID, followed by TMDB ID and the lower priority id is TVmaze ID.
```
docker run --rm -it --env-file config.env -v /movies:/movies noobmaster669/gg-bot-uploader:latest -t BLU -p "/movies/my.movie.mkv" -imdb tt10767168 -tmdb 617708
```
</details>

<br>

## Less Commonly Used Arguments
These are the list of arguments that can provide additional functionality to the upload assistant but on a day to day basis is almost never needed.
There are some rare cases where these arguments will come in use. Please see details below.
| #| Flag | Value Needed | Description | Example |
| ------ | ------ | ------ | ------ | ------ |
| 1 | **-title** | Yes | Custom title provided by the user. You **must** enclose the title you want in **double quotes** (to deal with spaces in title) | **-title "This.Is.My.Custom.Title.WEB-DL.DD+5.1.H.265-SomEGrouP"** |
| 2 | **-type** | Yes | Use to manually specify 'movie' or 'tv' | **-type tv** |
| 3 | **-reupload** | No | This is used in conjunction with autodl to automatically re-upload any filter matches. WILL BE DEPRECATED in v3.0 | **-reupload** |
| 4 | **-batch** | No| Pass this arg if you want to upload all the files/folder within the folder you specify with the '-p' arg. | **-batch** |
| 5 | **-disc** | No | If you are uploading a raw dvd/bluray disc you need to pass this arg | **-disc** |
| 6 | **-e or --edition** | Yes | Manually provide an 'edition' (e.g. Criterion Collection, Extended, Remastered, etc). You must enclose the edition you want in double quotes (to deal with possible spaces) | **-e "Extended"** |
| 7 | **-nfo** | Yes | Use this to provide the path to an nfo file you want to upload. **Note**:: *Don't ever **modify / add / remove** the actual file/folder of whatever you're re-uploading* | **-nfo "path/to/my-file.nfo"** |
| 8 | **-d or --debug** | No | Used for debugging. Writes debug lines to log file | **--debug** |
| 9 | **-mkt or --use_mktorrent** | No | Use mktorrent instead of torf (Latest git version only) | **--use_mktorrent** |
| 10 | **-fpm or --force_pymediainfo** | No | Force use PyMediaInfo to extract video codec over regex extraction from file name | **--force_pymediainfo** |
| 11 | **-3d** | No | Mark the upload as 3D content | **-3d**|
| 12 | **-foreign** | No | Mark the upload as foreign content [Non-English] | **-foreign** |
| 13 | **-ss or --skip_screenshots** | No | Override the configuration in config.env and proceed to upload without taking screenshots | **-ss** |

<details><summary>Important Notes</summary>

* `-batch` :track_next:  The requirements for `-batch`  argument to work are:
    * Pass the path to a **folder** (<u>not an individual file</u>) with `--path`
    * Need to have **more than 1** file / folder in the specified directory


* `-disc` :track_next:  `*.iso` bluray files are not currently supported, only `/BDMV/STREAM/` *"structured"* directories are. 

* `-reupload` :track_next:  This is only used by the **[automatic re-uploading](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/autodl-irssi-automatic-re-uploading)** function. Don't pass unless you know what you're doing.
</details>

<details><summary>Examples using the less commonly used arguments</summary>

Upload a full disk to trackers
```
docker run --rm -it --env-file config.env -v /movies:/movies noobmaster669/gg-bot-uploader:latest -t BLU -p "/movies/my.movie.with.bdstream/" -disc
```

Use `mktorrent` to generate torrent and use `pymediainfo` to extract video codec 
```
docker run --rm -it --env-file config.env -v /movies:/movies noobmaster669/gg-bot-uploader:latest -t BLU -p "/movies/my.movie.mkv" -fpm -mkt
```
</details>

<br>

## Internal Upload Arguments
> These flags are applicable only if your account is already in a **Internal** class

| #| Flag | Value Needed | Description | Example |
| ------ | ------ | ------ | ------ | ------ |
| 1| **-internal** | No| Used to mark an upload as 'Internal' | **-internal** |
| 2| **-freeleech** | No| Used to give a new upload freeleech | **-freeleech** |
| 3| **-featured** | No| Mark the upload as featured | **-featured** |
| 4| **-doubleup** | No| Give a new upload 'double up' status | **-doubleup** |
| 5| **-tripleup** | No| Give a new upload 'triple up' status [XBTIT Exclusive] | **-tripleup** |
| 6| **-sticky** | No| Pin the new upload / Mark the upload as sticky | **-sticky** |

> Please note that the arguments `-doubleup` and `-tripleup` cannot be used together

<details><summary>Examples using the internal arguments</summary>

Mark an upload as internal

```
docker run --rm -it --env-file config.env -v /movies:/movies noobmaster669/gg-bot-uploader:latest -t BLU -p "/movies/my.movie.mkv" -internal
```

Mark an upload as internal and grant it double upload status

```
docker run --rm -it --env-file config.env -v /movies:/movies noobmaster669/gg-bot-uploader:latest -t BLU -p "/movies/my.movie.mkv" -internal -doubleup
```
</details>

<br>