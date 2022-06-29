
## 1. API Keys, Tracker Settings, and URLs:

Tracker API keys and announce urls are optional unless you plan on uploading torrents to them. For example if you don't intent to upload torrents to Asiancinema, then there is no need to provide its api key and announce url.

<details>
<summary>Tracker API and Announce Url Properties</summary>

| **Property**             | **Required/Optional** | **Description**                         |
| ------------------------ | --------------------- | --------------------------------------- |
| **ACM_API_KEY**          | Optional              | Asiancinema API Key                     |
| **ACM_ANNOUNCE_URL**     | Optional              | Asiancinema private announce url        |
|                          |                       |                                         |
| **BHD_API_KEY**          | Optional              | Beyond-HD API Key                       |
| **BHD_ANNOUNCE_URL**     | Optional              | Beyond-HD private announce url          |
|                          |                       |                                         |
| **BLU_API_KEY**          | Optional              | Blutopia API Key                        |
| **BLU_ANNOUNCE_URL**     | Optional              | Blutopia private announce url           |
|                          |                       |                                         |
| **R4E_API_KEY**          | Optional              | Racing4Everyone API Key                 |
| **R4E_ANNOUNCE_URL**     | Optional              | Racing4Everyone private announce url    |
|                          |                       |                                         |
| **ATH_API_KEY**          | Optional              | Aither API Key                          |
| **ATH_ANNOUNCE_URL**     | Optional              | Aither private announce url             |
|                          |                       |                                         |
| **NTELOGO_API_KEY**      | Optional              | Ntelogo API Key                         |
| **NTELOGO_ANNOUNCE_URL** | Optional              | Ntelogo private announce url            |
|                          |                       |                                         |
| **TSP_API_KEY**          | Optional              | TheScenePlace API Key                   |
| **TSP_ANNOUNCE_URL**     | Optional              | TheScenePlace private announce url      |
|                          |                       |                                         |
| **DT_API_KEY**           | Optional              | Desitorrents API Key                    |
| **DT_ANNOUNCE_URL**      | Optional              | Desitorrents private announce url       |
|                          |                       |                                         |
| **STT_API_KEY**          | Optional              | SkipTheTrailers API Key                 |
| **STT_ANNOUNCE_URL**     | Optional              | SkipTheTrailers private announce url    |
|                          |                       |                                         |
| **STC_API_KEY**          | Optional              | SkipTheCommericals API Key              |
| **STC_ANNOUNCE_URL**     | Optional              | SkipTheCommericals private announce url |
|                          |                       |                                         |
| **SPD_API_KEY**          | Optional              | SpeedApp API Key                        |
| **SPD_ANNOUNCE_URL**     | Optional              | SpeedApp private announce url           |
|                          |                       |                                         |
| **TDB_API_KEY**          | Optional              | TorrentDB API Key                       |
| **TDB_ANNOUNCE_URL**     | Optional              | TorrentDB private announce url          |
|                          |                       |                                         |
| **BHDTV_API_KEY**        | Optional              | BIT-HDTV API Key                        |
| **BHDTV_ANNOUNCE_URL**   | Optional              | BIT-HDTV private announce url           |
|                          |                       |                                         |
| **NBL_API_KEY**          | Optional              | Nebulance API Key                       |
| **NBL_ANNOUNCE_URL**     | Optional              | Nebulance private announce url          |
|                          |                       |                                         |
| **ANT_API_KEY**          | Optional              | Anthelion API Key                       |
| **ANT_ANNOUNCE_URL**     | Optional              | Anthelion private announce url          |
|                          |                       |                                         |
| **RF_API_KEY**           | Optional              | ReelFliX API Key                        |
| **RF_ANNOUNCE_URL**      | Optional              | ReelFliX private announce url           |


</details>The metadata fetching is performed by the upload assistant with the help of [TheMovieDB](https://www.themoviedb.org/). The API Key to interact with TMDB needs to be provided and the operations done by the upload assistant can be notified to a text channel in a discord service with the help of discord webhook.

<table>
<tr>
<th>

Property

</th>
<th>

Required/Optional

</th>
<th>

Description

</th>
</tr>
<tr>
<td>

**TMDB_API_KEY**

</td>
<td>Required</td>
<td>

The API key to communicate with TMDB ([TheMovieDB](https://www.themoviedb.org/))<br><br>To get an API Key:

- Create an account at [TheMovieDB](https://www.themoviedb.org/)
- Navigate to settings
- Choose the API section and copy the API Key (v3 auth)

Refer to [API Documentation](https://www.themoviedb.org/documentation/api) for more details

</td>
</tr>

<tr>
<td>

**tmdb_result_auto_select_threshold**

</td>
<td>Required</td>
<td>

This property determines whether or not the tmdb id will be automatically decided by the uploader or not. Be default this is set as 1, which is the safest configuration (although not fool proof).
<br>
<br>
1 => This indicates that if the TMDB search returns only 1 result, then auto select that and proceed.
if this below property is set to say 3, then the uploader will auto select the 1st result as long as the tmdb search gave maximum of 3 entries for detailed explanation see wiki pages.
<br>
<br>
> ⚠️If you want to ignore this config just set it to 0. (the first result will always be selected !!!DANGEROUS!!! ) ⚠️
<br>
Example: ``` tmdb_result_auto_select_threshold=2 ```
</td>
</tr>
</table>

<br>

## 2. Screenshots and Image Uploads

GG-BOT Upload Assistant take frame accurate screenshots automatically and can upload them to the image hosting site of users choice.
| **Property** | **Required/Optional** | **Description** |
|--------------|-----------------------|-----------------|
| **num_of_screenshots** | Optional | The property denotes the number of screenshots to be taken. The screenshots taken are evenly spaced depending on the length of the video file.<br>If the number of screenshot is set as 0, then the screenshot taking and upload process will be skipped |
| **thumb_size** | Optional | Denotes the size of the thumbnail to be used while generating the thumbnail linked image bbcode. For trackers where full image urls are provided this property has no particular significance. |
| **no_spoilers** | Optional | Flag is used to avoid spoiler in screenshots. By default the property is **disabled (False)**. When enabled, screenshots will be taken from the first half of the input video only. If disabled screenshots will be taken at regular intervals from the full length of the video. |

Once a screenshot has been created it'll be uploaded to one of the image host configured by the user.

> A total of 6 Image Hosts are currently supported. imgbox | imgbb | freeimage | ptpimg | imgfi | imgur

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
img_host_4=imgur
img_host_5=
img_host_6=
# imgbox and Imgfi are disabled in this configuration
```

</td>
<td>

Indicates the priority of an image host with lower number having higher priority. <br>Screenshots will be uploaded to the hosts based on the priority. If an upload fails to a particular host, then the uploader fallbacks to the next host specified. <br>If not image hosts are provided then screenshots will not be uploaded. <br>Keys available for configuration

- img_host_1
- img_host_2
- img_host_3
- img_host_4
- img_host_5
- img_host_6
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
<tr>
<td>

**imgur_api_key**

</td>
<td>Optional</td>
<td>XXXXXXXXXXXXXXX</td>
<td>Image Host: [imgur](https://imgur.com/) <br> This is the client secret for your imgur applicaton <br>
You need to register your application [here](https://api.imgur.com/oauth2/addclient) with `Anonymous usage without user authorization` to get client id and secret</td>
</tr>
<tr>
<td>

**imgur_client_id**

</td>
<td>Optional</td>
<td>XXXXXXXXXXXXXXX</td>
<td>Image Host: [imgur](https://imgur.com/) <br> This is the client id for your imgur applicaton <br>
You need to register your application [here](https://api.imgur.com/oauth2/addclient) with `Anonymous usage without user authorization` to get client id and secret</td>
</tr>
</table>

<br>

## 3. Post Processing:
Once a torrent has been uploaded the upload assistant can perform various operations. GG-BOT Uploader is capable of 2 kinds of post processing steps.
1. Immediate seeding via torrent client
> Once a torrent has been uploaded, the uploader can add the dot torrent to a torrent client for immediate seeding.
2. Move media and torrents to watch folders
> You can specify a "Watch Directory" in some torrent clients that will automatically add new .torrent files to its download queue. This could be used to automatically start seeding an upload using AutoTools (rtorrent)

> Post-processing steps can be enabled or disabled based on the flag `enable_post_processing`. By default post processing steps are disabled.

| Property | Required/Optional | Description | Possible Values |
| ------ | ------ | ------ | ------ |
| **enable_post_processing** | Optional | This acts as a flag to tell the upload assistant whether or not to perform post processing steps. By default post processing steps are disabled. | True/False |
| **post_processing_mode** | Optional | This property tells the upload assistant which kind of post processing needs to be done. The two supported types are immediate cross-seeding via a torrent client and media and torrent movement to watch folders | CROSS_SEED/WATCH_FOLDER |

### 3.1 Post Processing: Watch Folders
GG-BOT Upload assistant can move the generate torrent files and the original media file to specified locations which are configured as watch folder for torrent clients.
> Please ensure that the below two paths (if configured) are available and writable. Uploader will **NOT** create these paths.

<table>
    <tbody>
        <tr>
            <th><strong>Property</strong></th>
            <th><strong>Description</strong></th>
        </tr>
        <tr>
            <td><strong>dot_torrent_move_location</strong></td>
            <td>
Once the uploads have been completed the torrent files will be moved to this particular location
</td>
        </tr>
<tr>
            <td><strong>media_move_location</strong></td>
            <td>
The mediafile which was provided as input the uploader will be moved to this particular location
</td>
        </tr>
<tr>
            <td><strong>enable_type_base_move</strong></td>
            <td>
This property tells the upload assistant to create subfolders and move contents to those subfolders.

When type based move is enabled...
- Torrents will be moved to sub folders within the dot_torrent_move_location
    - Movies dot torrent will be moved to `{dot_torrent_move_location}/movie/...torrent`
    - Epsiodes / Season Packs dot torrent  will be moved to `{dot_torrent_move_location}/epsiode/...torrent`
- Media will be moved to sub folders within the media_move_location
    - Movies file will be moved to `{media_move_location}/movie/...file`
    - Epsiodes / Season Packs file will be moved to `{media_move_location}/epsiode/...file`
</td>
        </tr>
</tbody>
</table>

<details><summary>Torrent client & watch directories</summary>

1. Transmission: open `settings.json` & append the following lines

```plaintext
"watch-dir": "/path/to/folder/to/watch/",
"watch-dir-enabled": true
```

2. rtorrent/ruTorrent: open `rtorrent.rc` and add the following line (might already exist)

```plaintext
schedule = watch_directory,5,5,"load.start=/path/to/folder/to/watch/*.torrent,d.delete_tied="
```
</details>

### 3.2 Post Processing: Immediate Cross Seeding
Once upload has been completed, upload assistant can be configured to upload the torrents of successful uploads to a torrent client for immediate cross-seeding. This feature requires a torrent client to the configured with the upload assistant. GG-BOT Upload Assistant supports the following torrent clients

- Qbittorrent
- RuTorrent

<table>
    <tbody>
        <tr>
            <th><strong>Property</strong></th>
            <th><strong>Description</strong></th>
        </tr>
        <tr>
            <td><strong>client</strong></td>
            <td>
Specifies the client to which torrents needs to be uploaded. The possible options for this property are

- `Qbittorrent`
- `Rutorrent`
</td>
        </tr>
<tr>
            <td><strong>client_host</strong></td>
            <td>
This is the domain / ipaddress where the torrent client is location and accessible
</td>
        </tr>
<tr>
            <td><strong>client_port</strong></td>
            <td>
The port using which upload assistant can communicate with the torrent client
</td>
        </tr>
<tr>
            <td><strong>client_username</strong></td>
            <td>
Username to be user for authentication with the torrent client. <br> Leave this as empty in case the torrent client doesn't have any authentication.
</td>
        </tr>
<tr>
            <td><strong>client_password</strong></td>
            <td>
Password to be user for authentication with the torrent client. <br> Leave this as empty in case the torrent client doesn't have any authentication.
</td>
        </tr>
<tr>
            <td><strong>client_path</strong></td>
            <td>

This property specifies the path (URL Path) at which the torrent client is located. <br> For example, if you access your torrent client at `http://ggbot.com/rutorrent`, then the `client_path` will be `/rutorrent`

</td>
        </tr>
<tr>
            <td><strong>cross_seed_label</strong></td>
            <td>

The label or category under which the cross-seeded torrents needs to be uploaded as. If you don't provide any value, uploader will set `GGBotCrossSeed` as the default value for this field.
</td>
        </tr>
</tbody>
</table>

If you are running the torrent client / uploader in a docker containers there is a high chance that the paths accessible inside the containers will be different. For such cases, path translations can be used for propper seeding. If you're running the client / uploader in a docker container you will need to map the containers download path to its system path.
> If you are using Sonarr/Radarr then you've already probably done this under "Remote Path Mappings" in the "Download Clients" section

| Property | Description |
| ------ | ------ |
| **translation_needed** | Flag to indicate whether uploader should perform path translations |
| **client_accessible_path** | The path that is accessible to the torrent client |
| **uploader_accessible_path** | The path that is accessible to the upload assistant|

For Example:
```
Uploader container / system path: /mnt/local/downloads/torrents/rutorrent/completed/file.mkv
Client container / system path:   /media/torrents/rutorrent/completed/file.mkv
```
Using those paths ^^ you would set the mappings like this:
```
uploader_accessible_path=/mnt/local/downloads/
client_accessible_path=/media/
```
That way the file with path `/mnt/local/downloads/torrents/rutorrent/completed/file.mkv` will be uploaded to client with path `/media/torrents/rutorrent/completed/file.mkv`

<br>

## 4. Dupe check:
The upload assistant uses `fuzzywuzzy` to compare a stripped down version of the title it generated to the results obtained from the site search API. The title, year, resolution are removed before comparing similarity (the upload assistant filter out results that don't match the resolution of the local file).
| Property | Required/Optional | Default value| Description |
| ------ | ------ | ------ | ------ |
| **check_dupes** | Required | true | This flag determines whether or not dupe check needs to be done on a tracker site before uploading torrents to that tracker.|
| **acceptable_similarity_percentage** | Required | 70 | Set a maximum similarity percentage. If torrents obtained from tracker site is greater than this threshold user will be prompted a choice to stop or continue the upload. Please note that this flag has significance only when `check_dupes=true`|

<details><summary>Examples of filename & percentage similarities</summary>

```
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

<br>

## 4. Auto Mode:
> Note that you are responsible for following **all** tracker rules and should manually double check all automatic uploads

<table>
    <tbody>
        <tr>
            <th><strong>Property</strong></th>
            <th><strong>Required/Optional</strong></th>
            <th><strong>Default Value</strong></th>
            <th><strong>Description</strong></th>
        </tr>
        <tr>
            <td><strong>auto_mode</strong></td>
            <td>Optional</td>
            <td>False </td>
            <td>

- Set this to `true` to run without any human interaction
    - This will parse the filename & auto select the _right_ TMDB ID
    - If minor issues are found (e.g. the filename year is off by 1) it will deal with it and upload anyways
    - Note that you are responsible for following **all** tracker rules and should manually double check all automatic uploads
- Set this to `false` to have a more interactive & hands on experience **(recommended)**
    - If issues are found (e.g. source can't be auto-detected) you'll be prompted for user input that we can use
    - You'll be shown status updates continually & will have a chance to review/approve the final upload data
    - You'll be shown the exact POST data/file payload before its uploaded for your review/approval
</td>
        </tr>
        <tr>
            <td><strong>force_auto_upload </strong></td>
            <td>Required </td>
            <td>False </td>
            <td>This works in tandem with **auto_mode**, if `auto_mode=False` then this won't work. <br> If your torrent has minor issues like we can't auto-detect the `audio_channels`, this will force the upload without that info.

<br>

```
Eg. If pymediainfo / ffprobe / regex can not detect the `audio_codec` this will simply omit the `audio_codec` from the torrent
```
</td>
        </tr>
    </tbody>
</table>

<br>

## 4. Miscellaneous Properties:
<table>
    <tbody>
        <tr>
            <th><strong>Property</strong></th>
            <th><strong>Required/Optional</strong></th>
            <th><strong>Default Value</strong></th>
            <th><strong>Description</strong></th>
        </tr>
        <tr>
            <td><strong>live</strong></td>
            <td>Optional </td>
            <td>False </td>
            <td>Property to determine whether or not to mark uploads as Live/Draft
<br>

- This only applies to **BHD** since they are the only supported site that has a **Drafts** page
- It's recommended to set this to `False` for your first few uploads, so you can verify everything is to your liking
- Setting this to `True` will result in **BHD** uploads being posted _live_ for everyone to see

</td>
        </tr>
        <tr>
            <td><strong>bdinfo_script</strong></td>
            <td>Optional</td>
            <td></td>
            <td>

```
Please note that this property is not applicable when using docker images for torrent uploads.
```

- If you plan on uploading a "Raw Bluray Disc" you need to fill out this option
- You need to supply it with the path of the **BDInfoCLI-ng** docker wrapper script
- Process:
    - Download & install Docker
    - Clone this project [BDInfoCLI-ng](https://github.com/zoffline/BDInfoCLI-ng) & `cd` into it
    - In the folder `/BDInfoCLI-ng-UHD_Support_CLI/scripts/` you'll find a file called `bdinfo`
    - Copy the entire path to that `bdinfo` file into `config.env`

</td>
        </tr>
<tr>
            <td><strong>uploader_signature</strong></td>
            <td>Optional </td>
            <td></td>
            <td>

Uploader signature is added at the bottom of the torrent description. By default if no signature is provided the upload assistant will add ``` Uploaded with ❤ using GG-BOT Upload Assistant ``` as the uploader signature.  With this property you can add your own custom signature to torrent uploads.
PS:
- The signature provided has to be plain text or must be a valid bbcode
- The signature will automatically be wrapped inside [center][/center] tag by the upload assistant

``` Sample: uploader_signature=[url=https://ibb.co/VH6n8tC][img]https://i.ibb.co/VH6n8tC/Manchester-United-Logo11.jpg[/img][/url] ```
</td>
        </tr>

<tr>
            <td><strong>readable_temp_data</strong></td>
            <td>Optional </td>
            <td>False</td>
            <td>

This property decided whether or not the sub_folders in `temp_upload` containing screnshots, mediainfo, urls etc needs to be in a human readable format or not. By default a unique hash will be generated for the input path and it'll be used. If this property is enabled then the sub_folder will be created using the file name.

</td>
        </tr>
    </tbody>
</table>