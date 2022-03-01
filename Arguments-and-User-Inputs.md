GG-BOT Upload Assistant provides various runtime arguments that can be used to customize the individual upload process. These are mainly classified into 5 different groups.
- Mandatory arguments
- Commonly used arguments
- Less commonly used arguments
- Experimental arguments
- Internal upload arguments

NOTE: 
* If the **Value Needed** for any argument is **NO**, then only the argument flag needs to be provided in run command. 
* If the **Value Needed** for any argument is **YES**, then the argument flag followed by the value for the argument also needs to be provided. 

<br>

## Mandatory Arguments
These are the arguments that are required for each upload. All the arguments under this category must be provided for the upload assistant to start the upload process. For majority of the uploads only these mandatory arguments are needed.
| #| Flag | Value Needed | Description | Example |
| ------ | ------ | ------ | ------ | ------ |
| 1| **-t** or **--trackers** | Yes | Tracker(s) to upload to. Space-separates if multiple (no commas)| **-t BHD BHDTV NBL** |
| 2| **-p** or **--path** | Yes | Use this to provide path(s) to file/folder| **-p /data/movies/my.movie.mkv** |

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
</details>

<br>

## Commonly Used Arguments
This category contains the list of arguments that are used commonly.
| #| Flag | Value Needed | Description | Example |
| ------ | ------ | ------ | ------ | ------ |
| 1 | **-tmdb** | Yes | Use this to manually provide the TMDB ID | **-tmdb 566525** |
| 2 | **-imdb** | Yes | Use this to manually provide the IMDB ID | **-imdb tt7569576** |
| 3 | **-tvmaze** | Yes | Use this to manually provide the TVmaze ID | **-tvmaze 50603** |
| 4 | **-anon** | No | Used to mark the upload to be anonymous. | **-anon** |
<details><summary>Examples using the commonly used arguments</summary>

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
| 1 | **-title** | cell | cell | cell |
| 2 | **-type** | cell | cell | cell |
| 3 | **-reupload** | cell | cell | cell |
| 4 | **-batch** | cell | cell | cell |
| 5 | **-disc** | cell | cell | cell |
| 6 | **-e or --edition** | cell | cell | cell |
| 7 | **-nfo** | cell | cell | cell |
| 8 | **-d or --debug** | cell | cell | cell |
| 9 | **-mkt or --use_mktorrent** | cell | cell | cell |
| 10 | **-fpm or --force_pymediainfo** | cell | cell | cell |
| 11 | **-3d** | cell | cell | cell |
| 12 | **-foreign** | cell | cell | cell |


# Args / user input
* **Do not** include **commas** or **quotes** with your args
* Certain options are **flags** that don't require any other input
  * `-anon` `-batch` `-disc` are all flags that don't require any other input
  * e.g. `python3 auto_upload.py -t ABC -anon` to upload anonymously
***
### Required:
* `-t` / `--trackers`
  * This is how you specify which site to upload to
  * `python3 auto_upload.py -t BHD BLU`
  

* `-p` / `--path`
  * Use this to specify which file or folder you want to upload
  * `python3 auto_upload.py -t ABC -p /home/user/Videos/file.mkv`

***

### Optional Args:
* `-tmdb` | [**themoviedb.org**](https://www.themoviedb.org/)
  * Manually provide the **TMDB ID** instead of using built in auto-detection / prompt
  * It's recommended to use this arg if `auto_mode=true` (auto-detection isn't always 100% accurate)
  * `python3 auto_upload.py -t ABC -tmdb 1892`
  

* `-imdb` | [**imdb.com**](https://www.imdb.com/)
  * Using the **IMDB ID** we can utilize the **TMDB API** `/find/{external_id}` endpoint to get the corresponding **TMDB ID**
  * `python3 auto_upload.py -t ABC -imdb tt0086190`
  

* `-e` / `--edition`
  * If it's **not** auto-extracted *(via this [regex from radarr](https://github.com/Radarr/Radarr/blob/5799b3dc4724dcc6f5f016e8ce4f57cc1939682b/src/NzbDrone.Core/Parser/Parser.cs#L21))* or just not included in the filename, you can **manually** specify the **edition**
  * You must enclose the edition you want in double quotes (to deal with possible spaces)
  * `python3 auto_upload.py -t ABC -e "Criterion Collection"`
  

* `-title`
  * Manually set the torrent title instead of using auto-generator
  * You **must** enclose the title you want in **double quotes** (to deal with spaces in title)
  * `python3 auto_upload.py -t ABC -title "Movie Title 2010 1080p WEB-DL"`
  

* `-type`
  * Sometimes the script & occasionally **TMDB** misidentifies content as a **Movie** when it's really a  **TV Show** and vice versa 
  * You can **manually override** the **content type** by passing the `-type` arg **&** `movie` or `tv` as the value
  * `python3 auto_upload.py -t ABC -type movie`
  

* `-nfo`
  * Use this arg to **manually** provide the path to a relevant `.nfo` file if it's not included in the folder you're uploading
  * **Note**, *Don't ever **modify / add / remove** the actual file/folder of whatever you're re-uploading*
  * `python3 auto_upload.py -t ABC -nfo "/home/user/Downloads/file.nfo"`
 
 
* `-mkt` or `--use_mktorrent`
  * Provide this flag in case if you want to create the .torrent file using mktorrent instead of torf


* `-fpm` or `--force_pymediainfo`
  * Provide this flag to Force use PyMediaInfo to extract video codec over regex extraction from file name
***

### Optional Flags:
* `-anon` **(flag)**
  * This is used to upload **anonymously**
  * `python3 auto_upload.py -t ABC -anon`
  

* `-batch` **(flag)**
  * This is related to the `--path` arg in the way that this will systematically & **<u>individually</u>** upload all the files in a specified folder
  * The requirements for this to work are:
    * Pass the path to a **folder** (<u>not an individual file</u>) with `--path`
    * Need to have **more than 1** file / folder in the specified directory
  * `python3 auto_upload.py -t ABC -p /home/user/Videos/partial_airing_tv_show/ -batch`

  
* `-disc` **(flag)**
  * You **must** pass this arg if you're uploading a Raw Bluray disc
  * `*.iso` bluray files are not currently supported, only `/BDMV/STREAM/` *"structured"* directories are. 
  * `python3 auto_upload.py -t ABC -p /home/user/Videos/bluray_folder/ -disc`
  

* `-reupload` **(flag)**
  * **Used by autodl-irssi during automated re-uploads**
  * This is only used by the **[automatic re-uploading](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/autodl-irssi-automatic-re-uploading)** function. Don't pass unless you know what you're doing.
  
***

### Optional Flags (Internals only):
* This is only applicable if your account is already in a **Internal** class
* If you are in a **internal** class on a **[UNIT3D](https://github.com/HDInnovations/UNIT3D-Community-Edition)** tracker, you have some extra options when uploading
* `python3 auto_upload.py -t ABC -p /home/user/Videos/file.mkv -internal -doubleup`

| Arg         | Description                             |
| :---------- | :-------------------------------------- |
| `-internal` | Mark a new upload as **Internal**       |
| `-freeleech`| Mark a new upload as **Freeleech**      |
| `-featured` | **Feature** a new upload                |
| `-doubleup` | Gives a new upload **Double Up** status |
| `-sticky`   | Pins the new upload                     |
