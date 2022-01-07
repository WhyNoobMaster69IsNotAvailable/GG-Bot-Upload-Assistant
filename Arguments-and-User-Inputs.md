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
  * This is only used by the **[automatic re-uploading](https://github.com/ryelogheat/xpbot/wiki/autodl-irssi-automatic-re-uploading)** function. Don't pass unless you know what you're doing.
  
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
