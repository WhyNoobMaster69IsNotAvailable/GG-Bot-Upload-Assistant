### How exactly `/site_templates/*.json` works
1. Each site is going to have some small differences in the required API key/values as well as what info we can pass in
    * A simple example of this would be the *resolution / source*  sites have you select
    * BHD has `BD Remux` clumped in with other resolutions (??) while still leaving `Bluray` as a `source` option

2. So `site_templates/` purpose is to set our own standard and translate other sites to our style
    * The most obvious example of this is the `translation` dict which matches our info 'name/key' to each site, this can be seen below
    *
        ```
        "translation": {
            "dot_torrent": "file",
            "torrent_title" : "name",
            "description": "description",
            "mediainfo": "mediainfo",
            "type": "category_id",
            "source": "source",
            "resolution": "type",
            "tmdb": "tmdb_id",
            "imdb": "imdb_id",
            "anon": "anon",
            "live": "live",
            "sd": "sd",
            "tvdb": "tvdb",
            "mal": "mal",
            "igdb": "igdb",
            "optimized": "stream",
            "nfo_file": "nfo_file"
        },
        ```
    * In the example above ^^ we convert our `torrent_info` dict to fit into BHDs API parameters
        * e.g. in the script we assign `dot_torrent` to the path of the generated .torrent file 
            * BHD want it passed as `file`
            * BLU & ACM want it passed as `torrent`


3.  Next we split the **.json* file into **2** parts
    * **Part 1:** Required
        * All the *Keys* here **have** to be set a value and passed during the upload process
        * If the value is doesn't exist, we just the value to `0` but it still has to be passed
            * e.g. the TVDB ID for a movie doesn't exist, but we still pass it with the value `0`
    * **Part 2:** Optional
        * This currently only really applies to BHD (Could change in future)
        * BHD has optional fields that can be assigned to torrents such as:
            * `edition` `region` `pack` `special` `sd` etc
        * None of these are typically *required* when uploading but its good tracker etiquette to be as accurate & complete as possible when uploading

4. When `auto_upload.py` runs, one of the last things we do is format all the data we have into the required API parameters
    * **The Process:**
    * 1\. We start a loop for every item under `required` in the corresponding `/site_templates/*.json` file
    * 2\. Using the `translation` dict we reverse each required API param into the formatting we use
    * 3\. We try to match each API param (reversed) to key/values in the `torrent_info` dict
    * 4\. If we get match we assign the value of `torrent_info[API_PARAM_REVERSED]` into a new dict called `tracker_settings`
    * 5\. In the case of no match we just assign a value of `0` 
        * Remember these are **Required** keys so each one must have a value (e.g. `0`)


5. **Resolution** & **Source**:  
    **NOTE:** These *definitions* will be different for each site
    * These are a bit tricky since we need to define what a particular source is & what its requirements are
        * e.g. BHD source:`BD Remux` must have a *Bluray* source, Be a *Remux*, & be *1080p*
    * See the following example:
      ```
      # 0 = optional
      # 1 = required
      # 2 = one of these items must 'match'

      
      "UHD Remux": {
        "bluray_remux": 1,
        "2160p": 1
      },
      
      "2160p": {
        "2160p": 1,
        "bluray_encode": 2,
        "webdl": 2,
        "webrip" : 2
      },
      ```
    * In this example ^^ 
      * `UHD Remux` requires that both `bluray_remux` & `2160p` be in the `torrent_info` dict
        * if either `bluray_remux` or `2160p` is missing then it's not considered a match and we try the next *definition*
      * `2160p` requires that `2160p` be in the `torrent_info` dict & **1** of the following:
        * `bluray_encode`, `webdl`, or `webrip`
