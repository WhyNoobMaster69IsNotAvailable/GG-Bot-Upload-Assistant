
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
|                          |                       |                                         |
| **TELLY_API_KEY**        | Optional              | Telly API Key                           |
| **TELLY_ANNOUNCE_URL**   | Optional              | Telly private announce url              |
|                          |                       |                                         |
| **SZN_API_KEY**          | Optional              | Swarmazon API Key                       |
| **SZN_ANNOUNCE_URL**     | Optional              | Swarmazon private announce url          |
|                          |                       |                                         |
| **LST_API_KEY**          | Optional              | LST API Key                             |
| **LST_ANNOUNCE_URL**     | Optional              | LST private announce url                |
|                          |                       |                                         |
| **3EVILS_API_KEY**       | Optional              | 3Evils API Key                          |
| **3EVILS_ANNOUNCE_URL**  | Optional              | 3Evils private announce url             |


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

**IMDB_API_KEY**

</td>
<td>Optional</td>
<td>

The API key to communicate with IMDb ([IMDb](https://imdb.com/))<br><br>To get an API Key:

- Create an account at [IMDb API](https://imdb-api.com/api)
- Navigate to your profile
- Copy the API Key

Refer to [API Documentation](https://imdb-api.com/api) for more details

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

Example: `tmdb_result_auto_select_threshold=2`
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

> A total of 9 Image Hosts are currently supported. imgbox | imgbb | freeimage | ptpimg | imgfi | imgur 
| snappie | pixhost | lensdump

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
img_host_7=
img_host_8=
img_host_9=
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
- img_host_7
- img_host_8
- img_host_9
</td>
</tr>
<tr>
<td>

**imgbox_api_key**

</td>
<td>Do Not Change</td>
<td>leave_blank</td>
<td>
Image Host: [imgbox](https://api.imgbb.com/) <br>
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

<tr>
<td>

**snappie_api_key**

</td>
<td>Optional</td>
<td>XXXXXXXXXXXXXXX</td>
<td>Image Host: [Snappie](https://snappie.net/) <br> The API key for Snappie</td>
</tr>
<tr>

<tr>
<td>

**lensdump_api_key**

</td>
<td>Optional</td>
<td>XXXXXXXXXXXXXXX</td>
<td>Image Host: [lensdump](https://lensdump.com/) <br> The API key for Lensdump</td>
</tr>
<tr>

<tr>
<td>

**pixhost_api_key**

</td>
<td>Do Not Change</td>
<td>leave_blank</td>
<td>
Image Host: [pixhost](https://pixhost.to/) <br>
No api key is needed. The default value seen in the config file **SHOULD NOT BE MODIFIED.**
</td>
</tr>

</table>

<br>

## 3. Pre Processing:
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
That way the file with path `/media/torrents/rutorrent/completed/file.mkv` in torrent client, it'll read as `/mnt/local/downloads/torrents/rutorrent/completed/file.mkv` by the reuploader

<br>

## 4. Dupe Check:
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

## 5. Torrent Client Configurations:
GG-BOT Auto ReUploader needs to communicate with a torrent client to do pretty much anything. The ReUploader will listen to the torrents added to a torrent client and will upload them automatically to the configured trackers. As soon as an upload is completed, they will be cross-seeded automatically.

> Also see `dynamic_tracker_selection` in `Miscellaneous Properties`

The various torrent client configurations are listed below.

<table>
    <tbody>
        <tr>
            <th><strong>Property</strong></th>
            <th><strong>Description</strong></th>
        </tr>
        <tr>
            <td><strong>reupload_label</strong></td>
            <td>

Auto Reuploader will reupload torrents based on the labels assigned to them in the client.
<br>
- If `reupload_label` is set as `Movies`, then torrents with label `Movies` will be used for reupload
- If `reupload_label` is set as ``, then all the torrents in the client will be used for reupload (irrespective of labels and categories.)
- If `reupload_label` is set as `IGNORE_LABEL`, then torrents without any labels will be considered for reupload (ignore torrent labels)
            </td>
        </tr>
        <tr>
            <td><strong>cross_seed_label</strong></td>
            <td>

The seeds for reuploaded torrents will be labelled with the value of this property
> Default value for this property is `GGBotCrossSeed`
The original torrent (source torrent) which was used to create the seed torrents will be labelled as `{cross_seed_label}_source`
> If `cross_seed_label=SeedTorrents`, then the source torrent will be labelled as `SeedTorrents_source`.
Note that cross-seeded torrents will not be considered for reuploading (in case if this question popped into anyone's head).
            </td>
        </tr>
        <tr>
            <td><strong>client</strong></td>
            <td>

Specifies the client from which torrents needs to be reuploaded.
<br>
Possible Values are
- Qbittorrent
- Rutorrent

> See Setup and Upgrade Wiki page for samples configurations.

Based on the selected client, the values for further perperties will vary
            </td>
        </tr>
        <tr>
            <td><strong>client_host</strong></td>
            <td>
            The `hostname` / `domain name` / `ip address` with which reuploader can communicate with the cache
            </td>
        </tr>
        <tr>
            <td><strong>client_port</strong></td>
            <td>
            The `port` at which the cache is available for connections
            </td>
        </tr>
        <tr>
            <td><strong>client_username</strong></td>
            <td>
            The username to use to connect to the client if authentication is enabled for the cache
            </td>
        </tr>
        <tr>
            <td><strong>client_password</strong></td>
            <td>
            The password to use to connect to the client if authentication is enabled for the cache
            </td>
        </tr>
        <tr>
            <td><strong>client_path</strong></td>
            <td>
            The path to be added to the domain inorder to access the torrent client.
            <br>
            For example: To communicate with `http://somewhere.com/rutorrent`, you'll need to set `client_path` as `/rutorrent`
            </td>
        </tr>
    </tbody>
</table>

<br>

## 6. Cache Configuration:
GG-BOT Auto ReUploader caches some metadata about the torrent for keeping track of uploads, their status and search metadata. Currently reuploader supports the followings
applications as a cache
- MongoDB

These applications can be configured using the properties mentioned below.
> Cache configurations are MANDATORY for GG-BOT Auto ReUploader to work.

<table>
    <tbody>
        <tr>
            <th><strong>Property</strong></th>
            <th><strong>Description</strong></th>
        </tr>
        <tr>
            <td><strong>cache_type</strong></td>
            <td>

The type of the cache to be used by the reuploader.

Supported values are:
- `Mongo`
            </td>
        </tr>
        <tr>
            <td><strong>cache_host</strong></td>
            <td>

The `hostname` / `domain name` / `ip address` with which reuploader can communicate with the cache
            </td>
        </tr>
        <tr>
            <td><strong>cache_port</strong></td>
            <td>
                The `port` at which the cache is available for connections
            </td>
        </tr>
        <tr>
            <td><strong>cache_database</strong></td>
            <td>

The name of the database to be used by the reuploader. This is optional and its need is subjected to the type of cache being used.
- `Mongo`: Required
            </td>
        </tr>
        <tr>
            <td><strong>cache_username</strong></td>
            <td>
                The username to use to connect to the cache if authentication is enabled for the cache
            </td>
        </tr>
        <tr>
            <td><strong>cache_password</strong></td>
            <td>
                The password to use to connect to the cache if authentication is enabled for the cache
            </td>
        </tr>
    </tbody>
</table>

<br>

## 7. Miscellaneous Properties:
<table>
    <tbody>
        <tr>
            <th><strong>Property</strong></th>
            <th><strong>Required/Optional</strong></th>
            <th><strong>Default Value</strong></th>
            <th><strong>Description</strong></th>
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
        <tr>
            <td><strong>dynamic_tracker_selection</strong></td>
            <td>Optional </td>
            <td>False</td>
            <td>

When the dynamic tracker selction feature is enabled,
- Reuploader still needs some trackers to be provided via the `-t` or `--trackers` command line argument.
  These trackers will be considered as `fall_back_trackers`. (we'll get to this in more details later)
- The property `reupload_label` will be ignored.
  All torrents added to client must have label `GGBOT` or must start with `GGBOT`.

The trackers to which a particular tracker can be uploaded to can be added to the category/label as `::` separated entries. (dynamic trackers)
```
A torrent with label as GGBOT::TSP::SZN will be uploaded to TSP and SZN
A torrent with label as GGBOT::BHD::BLU::ATH::BHDTV will be uploaded to the following trackers BHD, BLU, ATH and BHDTV
```

- If the label is just GGBOT or GGBOT:: (user has not provided any dynamic trackers),
  then the reuploader will upload the torrent to the `fall_back_trackers` provided by the user via `-t` or `--trackers` argument at startup.

- If none of the dynamic trackers, are valid or not configured properly, then reuploader will attempt to upload to the `fall_back_trackers`.
</td>
        </tr>
    </tbody>
</table>