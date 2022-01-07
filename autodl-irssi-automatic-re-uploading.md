# Prerequisites
1. [autodl](https://autodl-community.github.io/autodl-irssi/)
(you need to have at least one trackers irc server configured)

2. [rtorrent](https://github.com/rakshasa/rtorrent/wiki) 
(need access to **rtorrent.rc** & permissions to edit it)

3. [rtorrent_on_complete_reupload.sh](https://github.com/ryelogheat/xpbot/blob/master/rtorrent_on_complete_reupload.sh.sample)
(rtorrent triggers this .sh script which in turn triggers [auto_upload.py](https://github.com/ryelogheat/xpbot/blob/master/auto_upload.py))

***

# Things to note
1. Other auto upload bots exist & the **search_for_dupes.py** script needs to be heavily improved so the possibility of uploading dupes is real
   * Follow all site rules & consider only uploading to BHD drafts until you are comfortable with the scripts reliability/dupe checking  
2. If you have the system package `unrar` installed & its available at `/usr/bin/unrar` we can auto extract from rar archives when uploading
   * This can be used in "Manual mode" if rar files are detected in a folder you are trying to upload
   * Its original purpose though was to extract new Scene releases when being used with this autodl-irssi re-upload 
3. Currently pretty early in the *automatic re-uploading* script development so be aware it might break at any time & the design of the *automatic re-uploading* function will likely change heavily in the near future

***

# Configuration
### autodl
1. Set the filters `Action` to `rtorrent`

2. An IMDB ID must be provided (as a label) for each filter
   * This means you need to have a specific TV Show or Movie in mind for each filter
![IMDB Example](https://ptpimg.me/0l5b09.png)

3. Under the `Action` tab you need to specify which tracker(s) you want to *upload to*
   * In the `Commands` input box paste the following line (**Replace ABC_XYZ with the actual trackers you want to upload to**)
   * `d.custom.set=upload_to_tracker,ABC_XYZ`
   * `ABC_XYZ` can be replaced with any of the trackers that are currently supported e.g. `BHD, BLU, R4E, etc`
   * If uploading to multiple sites, separate each one with an underscore

4. The actual *matching* of releases is left up to you, just keep in mind that each filter needs to be tied to a unique IMDB ID

### rtorrent.rc
1. Locate your `rtorrent.rc` file & append the following lines
   * `method.insert = d.data_path, simple, "if=(d.is_multi_file), (cat,(d.directory),/), (cat,(d.directory),/,(d.name))"`
   * **(Next line) Replace `/PATH/TO/rtorrent_on_complete_reupload.sh` with your actual path to `rtorrent_on_complete_reupload.sh`**
   * `method.set_key = event.download.finished,complete,"execute=/PATH/TO/rtorrent_on_complete_reupload.sh,$d.name=,$d.data_path=,$d.custom1=,$d.custom=upload_to_tracker"`
2. save, exit, and restart rtorrent

### rtorrent_on_complete_reupload.sh
1. Locate & make this file executable `chmod +x rtorrent_on_complete_reupload.sh`
2. Open this file, then make the following changes
   * set `log_location_for_autodl_matches` to a specific .log file you want logs written to 
   * set `location_of_auto_upload_py` to the full path to `auto_upload.py`
3. If you are using rtorrent in Docker!
   * Verify that you can actually access the location of `auto_upload.py` from your container
   * Whatever that path is ^^ set that for `location_of_auto_upload_py`

***

# Execution
### How it works & its (current) limitations

(Fill in later)
