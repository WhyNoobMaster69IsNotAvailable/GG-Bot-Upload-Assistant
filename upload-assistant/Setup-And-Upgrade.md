## Docker Setup
#### First Time Setup
1. Install docker
2. Setup folders and config
3. Start Uploading

**Install docker**

If you are on Windows, Mac, or Linux you can install the [Docker Desktop](https://www.docker.com/products/docker-desktop/) application and get started immediately.
If you are on linux headless, then you can run the `install_docker.sh` shell file available in `dev_scripts` folder of this repo.

**Setup folders and config**
1. Create a new folder named, `GGBOTUploadAssistant`
2. Download and place the `config.env` file from `samples/assistant` in this folder.
3. Fill in the necessary values. You can refer to the Upload Assistant Environment Configuration File wiki for more details regarding each property.

**Start Uploading**

You can now start uploading using GG-BOT Upload Assistant. The docker run commands must be executed from the `GGBOTUploadAssistant` folder. Advanced docker users know how to get around this 😉. You can also refer to the Noob Friendly Docker Guide and Run Command Examples for more information and examples on the various docker run command possibilitites.
<br>

##### Upgrading To Newer Versions
When running docker version of GG-BOT Upload Assistant, you have two possible options.
- Use the `:latest` tag
- Use a particular release tag `:2.0.6`

##### Upgrading when using :latest tag
```bash
docker pull noobmaster669/gg-bot-uploader:latest
```

**Automatic Updates**
When using the `:latest` tag, there is an option to download and use the latest versions automatically when they are released. To enable automatic updates, add `--pull=always` to the docker run command.
```
docker run --rm --pull=always -it \
    -v /home/user/media:/home/user/media \
    --env-file config.env \
    noobmaster669/gg-bot-uploader:latest -t BHDTV BHD NBL -p "/home/user/mediaYOUR_FILE_OR_FOLDER" OPTIONAL_ARGUMENTS
```

#### Upgrading when using a release tag
When you are using release tags, upgrading is just a matter of changing to new tag.
For example, if you were using `v2.0.1` and wants to use the `v2.0.5`, just change the tag in docker run command.

```
docker run --rm -it \
    -v /home/user/media:/home/user/media \
    --env-file config.env \
    noobmaster669/gg-bot-uploader:**2.0.5** -t BHDTV BHD NBL -p "/home/user/mediaYOUR_FILE_OR_FOLDER" OPTIONAL_ARGUMENTS
```

<br>

## Bare Metal / VM Setup
### First Time Setup
1. Install all dependencies
2. Clone the repository / tag you wish to use
3. Install required libraries
4. Setup folders and config
5. Start Uploading

### Upgrading To Newer Versions
Upgrading when using the master branch is the easiest option when running on bare metal. Just run the command below and you should have the latest changes.
```
git pull
```

When you are using a tag (recommended for bare metal), upgrading to new tag involes one more step.
```
git pull
git checkout -b <TAG>
```