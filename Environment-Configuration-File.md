
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
| **TELLY_API_KEY**        | Optional              | Telly API Key                           |
| **TELLY_ANNOUNCE_URL**   | Optional              | Telly private announce url              |
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
| **ACM_API_KEY**          | Optional              | Asiancinema API Key                     |
| **ACM_ANNOUNCE_URL**     | Optional              | Asiancinema private announce url        |

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

**auto_select_tmdb_result**

</td>
<td>Required</td>
<td>

When enabled the show will be automatically selected from the tmdb search result. [well there is only one to choose anyway]
Notes: This attribute has no particular significance
- when the `auto_mode` is enabled.
- If the search results from tmdb has multiple results

Refer to [API Documentation](https://www.themoviedb.org/documentation/api) for more details

</td>
</tr>

<tr>
<td>

**tmdb_result_auto_select_threshold**

</td>
<td>Required</td>
<td>

This property determines whether or not the tmdb id will be automatically decided by the uploader or not. By default this is set as 0, which disables this property altogether. This property is applicable only when auto_mode is enabled. This property is mainly supposed to be used along with GG-BOT Auto ReUploader.
- when its set to 1, if the TMDB search returns only 1 result, then auto select that and proceed.
- if this below property is set to say 3, then the uploader will auto select the 1st result as long as the tmdb search gave maximum of 3 entries
</td>
</tr>

<tr>
<td>

**DISCORD_WEBHOOK**

</td>
<td>Optional</td>
<td>

Discord webhook where torrent upload messages and status are to be sent to. <br><br>To create a Webhook:

- Open your Server Settings and head into the Integrations tab
- Click the "Create Webhook" button to create a new webhook!

Refer to [Intro To Webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) for more details See the image below for an example of the notifications you would receive ![discord_notification](https://user-images.githubusercontent.com/80369373/111088206-68cfb580-84fc-11eb-853a-66b968f90a75.png)

</td>
</tr>
<tr>
<td>

**default_trackers_list**

</td>
<td>Optional</td>
<td>

Comma separated list of trackers which should be considered as default or fallback trackers in case `--trackers or -t`  flag is not provided.
<br>
<br>
Sample: `default_trackers_list=NBL,BLU,BHDTV `
<br>
This will by default uploads the torrent to NBL, BLU and BHDTV if `--trackers or -t` is not provided as runtime argument.

Notes:
- The runtime argument `--trackers or -t` has higher priority and overrides `default_trackers_list` property
- The trackers provided in `default_trackers_list` must have a valid configuration. The trackers without valid configurations will be ignored.  

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
Once a torrent has been uploaded the upload assistant can move the .torrent file and the actual media file/folder to configured folder.
> Leave these properties blank to disable any post processing

| Property | Required/Optional | Description |
| ------ | ------ | ------ |
| **dot_torrent_move_location** | Optional | Specify the full path to where you want the .torrent file moved after uploading. (_This could be used with an AutoWatch directory to automatically start seeding_) |
| **media_move_location** | Optional | Path to location where you want media file/folder moved to after uploading (_Again this could be used with AutoTools to automatically start seeding after uploading_) |
| **enable_type_base_move** | Optional | when type based move is enabled, torrents will be moved to sub folders within the `dot_torrent_move_location`|

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
            <td><strong>translation_needed</strong></td>
            <td>Optional </td>
            <td></td>
            <td>

```
This key is not required & are used if you are auto re-uploading torrents & are using docker containers
```
- See this page for more info [xpbot/wiki/autodl-irssi-automatic-re-uploading](https://github.com/ryelogheat/xpbot/wiki/autodl-irssi-automatic-re-uploading)
</td>
        </tr>
        <tr>
            <td><strong>host_path</strong></td>
            <td>Optional </td>
            <td></td>
            <td>

```
This key is not required & are used if you are auto re-uploading torrents & are using docker containers
```
- See this page for more info [xpbot/wiki/autodl-irssi-automatic-re-uploading](https://github.com/ryelogheat/xpbot/wiki/autodl-irssi-automatic-re-uploading)
</td>
        </tr>
        <tr>
            <td><strong>remote_path</strong></td>
            <td>Optional </td>
            <td></td>
            <td>

```
This key is not required & are used if you are auto re-uploading torrents & are using docker containers
```
- See this page for more info [xpbot/wiki/autodl-irssi-automatic-re-uploading](https://github.com/ryelogheat/xpbot/wiki/autodl-irssi-automatic-re-uploading)
</td>
        </tr>
    </tbody>
</table>