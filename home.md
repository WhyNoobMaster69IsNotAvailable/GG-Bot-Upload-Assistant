## GG-Bot-Uploader Wiki

### [Video usage examples](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Usage:-Video-Examples)

### [Arguments and User Inputs](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Arguments-and-User-Inputs)

### [Environment Configuration File (config.env breakdown)](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Environment-Configuration-File)

### [/site_templates/*.json guide](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Tracker-Templates)

### [Automatic re-uploading (autodl)](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/autodl-irssi-automatic-re-uploading)

### [Docker Run Command Examples](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Docker-Run-Command-Examples)
## Supported Sites:
  * `BHD` `BLU` `ACM` `R4E` `ATH` `TSP` `DT` `Telly` `Ntelogo`


## Usage Examples Bare Metal / VMs

1. Upload to BHD drafts with manually selected TMDB ID
     * See [video example](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Usage:-Video-Examples)
2. Upload to **Beyond-HD** & **Blutopia** with movie file in **/home/user/Videos/movie.title.year.bluray.1080p.etc.mkv**
    * ```python3 auto_upload.py -t BHD BLU -path /home/user/Videos/movie.title.year.bluray.1080p.etc.mkv```
3. Upload movie **anonymously** to **AsianCinema** with manually specified **TMDB** & **IMDB** IDs
    * ```python3 auto_upload.py -t acm -p /home/user/Videos/movie.title.year.bluray.1080p.etc.mkv -imdb tt0111161 -tmdb 278 -anon```

## Usage Examples Docker
1. Upload to BHD drafts with manually selected TMDB ID
     * See [video example](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Usage:-Video-Examples)
2. Upload to **Beyond-HD** & **Blutopia** with movie file in **/home/user/Videos/movie.title.year.bluray.1080p.etc.mkv**
    * 
```
     docker run --rm -it \
    -v <PATH_TO_YOUR_MEDIA>:/data \
    --env-file config.env \
    noobmaster669/gg-bot-uploader -t BHD BLU -path /home/user/Videos/movie.title.year.bluray.1080p.etc.mkv
```
3. Upload movie **anonymously** to **AsianCinema** with manually specified **TMDB** & **IMDB** IDs
    * 
```
    docker run --rm -it \
    -v <PATH_TO_YOUR_MEDIA>:/data \
    --env-file config.env \
    noobmaster669/gg-bot-uploader -t acm -p /home/user/Videos/movie.title.year.bluray.1080p.etc.mkv -imdb tt0111161 -tmdb 278 -anon
```