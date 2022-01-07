Please refer to the [Arguments and User Inputs](Arguments-and-User-Inputs) Wiki page to see list of arguments that can be supplied with the docker run command. All commands needs to provided in place of `ADDITIONAL_ARGUMENTS`

1. **Assumptions**
   * Your base path is `/home/ubuntu/`
   * A separate folder has been created for GG-Bot Upload Assistant `GGBotUploadAssistant`
   * All your media files are location in the folder `media`

<details>
<summary>Directory Structure</summary>

```plaintext
    /home/ubuntu/
    -----
    /home/ubuntu/GGBotUploadAssistant/
    -----
    /home/ubuntu/media/
    /home/ubuntu/media/movies/
    /home/ubuntu/media/tvshows/
```

</details>

2. **Files to Upload**
   * Movie File\
     `/home/ubuntu/media/movies/Movie.Name.2005.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-RELEASEGROUP.mkv`
   * TV Show Single Episode\
     `/home/ubuntu/media/tvshows/TV.Show.Name.S01E04.EpsiodeName.2160p.WEB-DL.DDP5.1.Atmos.DV.HEVC-RELEASEGROUP.mkv`
   * TV Show Season Pack\
     `/home/ubuntu/media/tvshows/TV.Show.Name.S02.2160p.HULU.WEB-DL.DDP5.1.DV.HEVC-RELEASEGROUP`

<details>
<summary>Final Directory Structure With All Files</summary>

```plaintext
    /home/ubuntu/
    -----
    /home/ubuntu/GGBotUploadAssistant/
    /home/ubuntu/GGBotUploadAssistant/config.env
    -----
    /home/ubuntu/media/
    -----
    /home/ubuntu/media/movies/
    /home/ubuntu/media/movies/Movie.Name.2005.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-RELEASEGROUP.mkv
    -----
    /home/ubuntu/media/tvshows/
    /home/ubuntu/media/tvshows/TV.Show.Name.S01E04.EpsiodeName.2160p.WEB-DL.DDP5.1.Atmos.DV.HEVC-RELEASEGROUP.mkv
    -----
    /home/ubuntu/media/tvshows/TV.Show.Name.S02.2160p.HULU.WEB-DL.DDP5.1.DV.HEVC-RELEASEGROUP/TV.Show.Name.S02E01.EpsiodeName.2160p.HULU.WEB-DL.DDP5.1.DV.HEVC-RELEASEGROUP.mkv
    /home/ubuntu/media/tvshows/TV.Show.Name.S02.2160p.HULU.WEB-DL.DDP5.1.DV.HEVC-RELEASEGROUP/TV.Show.Name.S02E02.EpsiodeName.2160p.HULU.WEB-DL.DDP5.1.DV.HEVC-RELEASEGROUP.mkv
    /home/ubuntu/media/tvshows/TV.Show.Name.S02.2160p.HULU.WEB-DL.DDP5.1.DV.HEVC-RELEASEGROUP/TV.Show.Name.S02E03.EpsiodeName.2160p.HULU.WEB-DL.DDP5.1.DV.HEVC-RELEASEGROUP.mkv
    /home/ubuntu/media/tvshows/TV.Show.Name.S02.2160p.HULU.WEB-DL.DDP5.1.DV.HEVC-RELEASEGROUP/TV.Show.Name.S02E04.EpsiodeName.2160p.HULU.WEB-DL.DDP5.1.DV.HEVC-RELEASEGROUP.mkv
    /home/ubuntu/media/tvshows/TV.Show.Name.S02.2160p.HULU.WEB-DL.DDP5.1.DV.HEVC-RELEASEGROUP/TV.Show.Name.S02E05.EpsiodeName.2160p.HULU.WEB-DL.DDP5.1.DV.HEVC-RELEASEGROUP.mkv
```

</details>

3. **Uploading a Single File**
* Reference Run Command

```plaintext
docker run -it 
        -v {YOUR_MEDIA_LOCATION}:/data 
        --env-file config.env 
        noobmaster669/gg-bot-uploader:latest -t TSP-p "/data/YOUR_FILE_OR_FOLDER" ADDITIONAL_ARGUMENTS
```

* Command to execute

```plaintext
docker run -it 
        -v /home/ubuntu/media:/data 
        --env-file config.env 
        noobmaster669/gg-bot-uploader:latest -t TSP-p "/data/movies/Movie.Name.2005.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-RELEASEGROUP.mkv" 
OR
docker run -it 
        -v /home/ubuntu/media:/data 
        --env-file config.env 
        noobmaster669/gg-bot-uploader:latest -t TSP-p "/data/tvshows/TV.Show.Name.S01E04.EpsiodeName.2160p.WEB-DL.DDP5.1.Atmos.DV.HEVC-RELEASEGROUP.mkv"
```

3. **Uploading a Folder**
* Reference Run Command

```plaintext
docker run -it 
        -v {YOUR_MEDIA_LOCATION}:/data 
        --env-file config.env 
        noobmaster669/gg-bot-uploader:latest -t TSP-p "/data/YOUR_FILE_OR_FOLDER" ADDITIONAL_ARGUMENTS
```

* Command to execute

```plaintext
docker run -it 
        -v /home/ubuntu/media:/data 
        --env-file config.env 
        noobmaster669/gg-bot-uploader:latest -t TSP-p "/data/tvshows/TV.Show.Name.S02.2160p.HULU.WEB-DL.DDP5.1.DV.HEVC-RELEASEGROUP"
```

3. **Uploading all files in a folder**
* By adding the flag `-batch` you can provide a folder and all the files inside the folder will be uploader. New .torrent file will be created for each file present in the provided folder.
* Reference Run Command

```plaintext
docker run -it 
        -v {YOUR_MEDIA_LOCATION}:/data 
        --env-file config.env 
        noobmaster669/gg-bot-uploader:latest -t TSP-p "/data/YOUR_FILE_OR_FOLDER" ADDITIONAL_ARGUMENTS
```

* Command to execute

```plaintext
docker run -it 
        -v /home/ubuntu/media:/data 
        --env-file config.env 
        noobmaster669/gg-bot-uploader:latest -t TSP-p "/data/tvshows/TV.Show.Name.S02.2160p.HULU.WEB-DL.DDP5.1.DV.HEVC-RELEASEGROUP" -batch
```