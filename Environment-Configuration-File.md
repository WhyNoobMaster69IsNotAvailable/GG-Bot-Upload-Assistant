## API Keys and URLs:

Tracker API keys and announce urls are optional unless you plan on uploading torrents to them. For example if you don't intent to upload torrents to Asiancinema, then there is no need to provide its api key and announce url.

<details>
<summary>Tracker API and Announce Url Properties</summary>

| **Property** | **Required/Optional** | **Description** |
|--------------|-----------------------|-----------------|
| **ACM_API_KEY** | Optional | Asiancinema API Key |
| **ACM_ANNOUNCE_URL** | Optional | Asiancinema private announce url |
|  |  |  |
| **BHD_API_KEY** | Optional | Beyond-HD API Key |
| **BHD_ANNOUNCE_URL** | Optional | Beyond-HD private announce url |
|  |  |  |
| **BLU_API_KEY** | Optional | Blutopia API Key |
| **BLU_ANNOUNCE_URL** | Optional | Blutopia private announce url |
|  |  |  |
| **R4E_API_KEY** | Optional | Racing4Everyone API Key |
| **R4E_ANNOUNCE_URL** | Optional | Racing4Everyone private announce url |
|  |  |  |
| **ATH_API_KEY** | Optional | Aither API Key |
| **ATH_ANNOUNCE_URL** | Optional | Aither private announce url |
|  |  |  |
| **TELLY_API_KEY** | Optional | Telly API Key |
| **TELLY_ANNOUNCE_URL** | Optional | Telly private announce url |
|  |  |  |
| **NTELOGO_API_KEY** | Optional | Ntelogo API Key |
| **NTELOGO_ANNOUNCE_URL** | Optional | Ntelogo private announce url |
|  |  |  |
| **TSP_API_KEY** | Optional | TheScenePlace API Key |
| **TSP_ANNOUNCE_URL** | Optional | TheScenePlace private announce url |
|  |  |  |
| **DT_API_KEY** | Optional | Desitorrents API Key |
| **DT_ANNOUNCE_URL** | Optional | Desitorrents private announce url |
|  |  |  |
| **UHDHVN_API_KEY** | Optional | UHD-Heaven API Key |
| **UHDHVN_ANNOUNCE_URL** | Optional | UHD-Heaven private announce url |
|  |  |  |
| **STC_API_KEY** | Optional | SkipTheCommericals API Key |
| **STC_ANNOUNCE_URL** | Optional | SkipTheCommericals private announce url |
|  |  |  |
| **SPD_API_KEY** | Optional | SpeedApp API Key |
| **SPD_ANNOUNCE_URL** | Optional | SpeedApp private announce url |
|  |  |  |
| **TDB_API_KEY** | Optional | TorrentDB API Key |
| **TDB_ANNOUNCE_URL** | Optional | TorrentDB private announce url |
|  |  |  |
| **ACM_API_KEY** | Optional | Asiancinema API Key |
| **ACM_ANNOUNCE_URL** | Optional | Asiancinema private announce url |

</details>The metadata fetching is performed by the upload assistant with the help of [TheMovieDB](https://www.themoviedb.org/). The API Key to interact with TMDB needs to be provided and the operations done by the upload assistant can be notified to a text channel in a discord service with the help of discord webhook.

<table>
<tr>
<th>

**Property**
</th>
<th>

**Required/Optional**
</th>
<th>

**Description**
</th>
</tr>
<tr>
<td>

**TMDB_API_KEY**
</td>
<td>Required</td>
<td>

The API key to communicate with TMDB ([TheMovieDB](https://www.themoviedb.org/))<br><br>To get an API Key:

* Create an account at [TheMovieDB](https://www.themoviedb.org/)
* Navigate to settings
* Choose the API section and copy the API Key (v3 auth)

Refer to [API Documentation](https://www.themoviedb.org/documentation/api) for more details
</td>
</tr>
<tr>
<td>

**DISCORD_WEBHOOK**
</td>
<td>Optional</td>
<td>

Discord webhook where torrent upload messages and status are to be sent to. <br><br>To create a Webhook:

* Open your Server Settings and head into the Integrations tab
* Click the "Create Webhook" button to create a new webhook!

Refer to [Intro To Webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) for more details See the image below for an example of the notifications you would receive ![discord_notification](https://user-images.githubusercontent.com/80369373/111088206-68cfb580-84fc-11eb-853a-66b968f90a75.png)
</td>
</tr>
</table>

## Screenshots and Image Uploads

GG-BOT Upload Assistant take frame accurate screenshots automatically and can upload them to the image hosting site of users choice.
| **Property** | **Required/Optional** | **Description** |
|--------------|-----------------------|-----------------|
| **num_of_screenshots** | Optional | The property denotes the number of screenshots to be taken. The screenshots taken are evenly spaced depending on the length of the video file.<br>If the number of screenshot is set as 0, then the screenshot taking and upload process will be skipped |
| **thumb_size** | Optional | Denotes the size of the thumbnail to be used while generating the thumbnail linked image bbcode. For trackers where full image urls are provided this property has no particular significance. |
| **no_spoilers** | Optional | Flag is used to avoid spoiler in screenshots. By default the property is **disabled (False)**. When enabled, screenshots will be taken from the first half of the input video only. If disabled screenshots will be taken at regular intervals from the full length of the video. |

Once a screenshot has been created it'll be uploaded to one of the image host configured by the user.

> A total of 5 Image Hosts are currently supported. imgbox | imgbb | freeimage | ptpimg | imgfi

The properties associated with Image Hosting sites are described below.

<table>
<tr>
<th>

**Property**
</th>
<th>

**Required/Optional**
</th>
<th>

**Sample Configuration**
</th>
<th>

**Description**
</th>
</tr>
<tr>
<td>

**img_host_X**
</td>
<td>Optional</td>
<td>

```markdown
img_host_1=freeimage
img_host_2=imgbb
img_host_3=ptpimg
img_host_4=
img_host_5=
# imgbox and Imgfi are disabled in this configuration
```

</td>
<td>

Indicates the priority of an image host with lower number having higher priority. <br>Screenshots will be uploaded to the hosts based on the priority. If an upload fails to a particular host, then the uploader fallbacks to the next host specified. <br>If not image hosts are provided then screenshots will not be uploaded. <br>Keys available for configuration

* img_host_1
* img_host_2
* img_host_3
* img_host_4
* img_host_5
</td>
</tr>
<tr>
<td>

**imgbox_api_key**
</td>
<td>Do Not Change</td>
<td>leave_blank</td>
<td>
Image Host: [imgbb](https://api.imgbb.com/) <br>
No api key is needed. The default value seen in the config file **SHOULD NOT BE MODIFIED.** <br>
[Documentation](https://github.com/plotski/pyimgbox)
</td>
</tr>
<tr>
<td>

**ptpimg_api_key**
</td>
<td>Optional</td>
<td>XXXXXXXXXXXXXXX</td>
<td>
Image Host: [ptpimg](https://ptpimg.me/) <br>
The API Key for ptpimg. <br>Follow the guide [here](https://github.com/theirix/ptpimg-uploader#api-key) to get api key for ptpimg. <br>

</td>
</tr>
<tr>
<td>

**imgbb_api_key**
</td>
<td>Optional</td>
<td>XXXXXXXXXXXXXXX</td>
<td>Image Host: [imgbb](https://api.imgbb.com/) <br> The API key for ImgBB</td>
</tr>
<tr>
<td>

**freeimage_api_key**
</td>
<td>Optional</td>
<td>XXXXXXXXXXXXXXX</td>
<td>Image Host: [freeimage](https://freeimage.host/page/api) <br> The API key for FreeImage.</td>
</tr>
<tr>
<td>

**imgfi_api_key**
</td>
<td>Optional</td>
<td>XXXXXXXXXXXXXXX</td>
<td>Image Host: [imgfi](https://imgfi.com/) <br> The API key for ImgFi</td>
</tr>
</table>

 4. **Selecting media for uploading**
    * You can either set a **upload_dir_path** or use the **-path** argument
    1. **upload_dir_path:** set the full path to a folder which contains a single file or folder (e.g. season pack), and it will be uploaded automatically upon script execution
       * `upload_dir_path=/home/user/videos/upload_me/`
    2. **-path argument:** If you leave **upload_dir_path** blank then you have to supply the **-path** argument followed by the path to the media you want to upload (video file or folder)
       * `python3 auto_upload.py -t ABC -path /home/user/videos/upload_me/test.mkv`
 5. **Post Processing**
    * After a successful upload we can move the .torrent file & actual media file/folder to a location you specify
    * **Leave blank to disable any movement**

    1\. **dot_torrent_move_location:** specify the full path to where you want the .torrent file moved after uploading \* this could be used with an AutoWatch directory to automatically start seeding

    2\. **media_move_location:** path to location where you want media file/folder moved to after uploading \* again this could be used with AutoTools to automatically start seeding after uploading

    **Torrent client & watch directories:**
    1. **Transmission**: open **settings.json** & append the following lines

       ```plaintext
       "watch-dir": "/path/to/folder/to/watch/",
       "watch-dir-enabled": true
       ```
    2. **rtorrent/ruTorrent**: open **rtorrent.rc** and add the following line (might already exist)

       ```plaintext
       schedule = watch_directory,5,5,"load.start=/path/to/folder/to/watch/*.torrent,d.delete_tied="
       ```
    3. **Deluge**: TODO

       ```plaintext
       fill me out later
       ```
 6. **Dupe check**
    * _Use at your own risk_
    * Set `check_dupes=` to `true` if you want to use this
      * Using fuzzywuzzy we compare a stripped down version of the title we generate to the results we get from the site search API
      * We remove the title, year, resolution before comparing similarity (we filter out results that don't match the resolution of the local file)
    * Set a maximum similarity percentage (don't include percentage symbol) at `acceptable_similarity_percentage=`
      * `acceptable_similarity_percentage` only works if `check_dupes=true`
      * **100% dupe matches** will always cancel the upload no matter what `acceptable_similarity_percentage` is set to
      * (Higher = Riskier)

    <details>
    <summary>examples of filename & percent differences</summary>

    ```plaintext
     Ex Machina 2015 1080p UHD Bluray DTS 5.1 HDR x265-D-Z0N3
     Ex Machina 2014 1080p UHD BluRay DTS HDR x265 D-Z0N3
     100%
     -----
     Atomic Blonde 2017 1080p UHD Bluray DD+ 7.1 HDR x265-NCmt
     Atomic Blonde 2017 1080p UHD BluRay DD+7.1 HDR x265 - HQMUX
     84%
     -----
     Get Him to the Greek 2010 1080p Bluray DTS-HD MA 5.1 AVC Remux-EPSiLON
     Get Him to the Greek 2010 Unrated BluRay 1080p DTS-HD MA 5.1 AVC REMUX-FraMeSToR
     88%
     -----
     Knives Out 2019 1080p UHD Bluray DD+ 7.1 HDR x265-D-Z0N3
     Knives Out 2019 REPACK 1080p UHD BluRay DDP 7.1 HDR x265-SA89
     89%
    ```

    </details>
 7. **Auto Mode (silent mode)**
    * Set this to `true` to run without any human interaction
      * This will parse the filename & auto select the _right_ TMDB ID
      * If minor issues are found (e.g. the filename year is off by 1) it will deal with it and upload anyways
      * Note that you are responsible for following **all** tracker rules and should manually double check all automatic uploads
    * Set this to `false` to have a more interactive & hands on experience **(recommended)**
      * If issues are found (e.g. source can't be auto-detected) you'll be prompted for user input that we can use
      * You'll be shown status updates continually & will have a chance to review/approve the final upload data
      * You'll be shown the exact POST data/file payload before its uploaded for your review/approval
 8. **auto_mode_force**
    * This works in tandem with **auto_mode**, if `auto_mode=false` then this won't work
    * If your torrent has minor issues like we can't auto-detect the _audio_channels_, this will force the upload without that info
      * e.g. If **pymediainfo** / **ffprobe** / **regex** can not detect the audio_codec this will simply omit the _audio_codec_ from the torrent title and finish the upload
    * **If missing, these can be skipped:**
      * `audio_codec` `audio_channels` `video_codec (maybe)`
 9. **Live / Draft**
    * This only applies to **BHD** since they are the only supported site that has a **Drafts** page
    * It's recommended to set this to `False` for your first few uploads, so you can verify everything is to your liking
    * Setting this to `True` will result in **BHD** uploads being posted _live_ for everyone to see
10. **BDInfo script**
    * If you plan on uploading a "Raw Bluray Disc" you need to fill out this option
    * You need to supply it with the path of the **BDInfoCLI-ng** docker wrapper script
    * Process:
      * Download & install Docker
      * Clone this project [BDInfoCLI-ng](https://github.com/zoffline/BDInfoCLI-ng) & `cd` into it
      * In the folder `/BDInfoCLI-ng-UHD_Support_CLI/scripts/` you'll find a file called `bdinfo`
      * Copy the entire path to that `bdinfo` file into `config.env`
11. **Auto re-upload**
    * these keys are not required & are used if you are auto re-uploading torrents & are using docker containers

      ```plaintext
      translation_needed=
      host_path=
      remote_path=
      ```
    * See this page for more info [xpbot/wiki/autodl-irssi-automatic-re-uploading](https://github.com/ryelogheat/xpbot/wiki/autodl-irssi-automatic-re-uploading)
```
</td>
<td>

</td>
</tr>
</table>

