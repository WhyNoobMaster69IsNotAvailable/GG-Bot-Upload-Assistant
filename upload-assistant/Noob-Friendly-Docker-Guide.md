Before you start going any further it's important to understand why a docker based setup is recommended over the regular bare metal setup. The upload assistant is written in python and makes use of certain tool and utilities to automate the upload process. 
- Python 
- Python libraries and dependencies
- ffmpeg
- mediainfo
- mktorrent
- bdinfo
- mono

These programs and utilities needs to be installed manually on your system and configured properly. This itself is a painstaking task and debugging for errors will be a nightmare. In addition to these there are also chances of version mismatches to happen as well. If you want to upload from a different machine, you'll need to setup everything from the scratch again.

You will not encounter any of these issues when using the containerized approach with docker. A docker image is pre-built and is published to the certain docker registry. All the dependencies with the proper compatible versions are already packed inside container so that you can start using straight away.

<br>

## Basic steps in setting up GG-BOT Upload Assistant
- Install docker
- Setup your configuration file
- Start container and beginning uploading

<br>

### :diamond_shape_with_a_dot_inside: Install Docker
Docker Engine is available on a variety of Linux platforms, macOS and Windows 10 through Docker Desktop, and as a static binary installation. Detailed step on how to install docker is available here: [Install Docker Engine](https://docs.docker.com/engine/install/).

- You can install the `Docker Desktop` for Windows and Mac OS. 
- For Linux distributions you can install the .deb and .rpm packages.

<details><summary>Ubuntu, CentOS, Fedora Docker Installation[1]</summary>
Before you run the installation command, make sure to update apt and then run any necessary upgrades. Do note, if your server’s kernel upgrades, you’ll need to reboot the system. Thus, you might want to plan to do this during a time when a server reboot is acceptable.

To update apt, issue the command:
```
sudo apt update
```

Once that completes, upgrade with the command:
```
sudo apt upgrade
```

If the kernel upgrades, you’ll want to reboot the server with the command: (Optional)
```
sudo reboot
```

If the kernel doesn’t upgrade, you’re good to install Docker (without having to reboot). 
The Docker installation command for Ubuntu:
```
sudo apt install docker.io
```

The Docker installation command for Fedora:
```
sudo dnf install docker
```

The Docker installation command for CentOS:
```
curl -fsSL https://get.docker.com/ | sh
```

Out of the box, the docker command can only be run with admin privileges. Because of security issues, you won’t want to be working with Docker either from the root user or with the help of sudo. To get around this, you need to add your user to the docker group. This is done with the command:
```
sudo usermod -a -G docker $USER
```

Once you’ve taken care of that, log out and back in, and you should be good to go. That is, unless your platform is Fedora. When adding a user to the docker group to this distribution, you’ll find the group doesn’t exist. What do you do? You create it first. Here are the commands to take care of this:
```
sudo groupadd docker && sudo gpasswd -a ${USER} docker && sudo systemctl restart docker

newgrp docker
```

Log out and log back in. You should be ready to use Docker.
</details>

> Once docker has been installed, create a new folder, all the steps mentioned in the wiki sections below will be performed inside this folder.

```
Your present working directory should look like this if the new folder you created is ggbot
/home/user/ggbot
```

<br>

### :diamond_shape_with_a_dot_inside: Setup your configuration file
There are various aspects of the upload assistant that can be configured as per the users requirement and convenience. These properties are accepted as environment variables. If you wish to have a different set of properties in a different system/environment, all you need to do is change the environment variables. When using docker the environment variables can be set with the `-e` flag or the `--env-file`. More on this in upcoming sections. 

1. Get the `config.env`
    1.a If you are using the documentation repo, you'll see a `config.env` file. Download the file to the working folder.
    1.b If you are using the main repo, download the `config.env.sample` and rename it to `config.env`.
2. Refer to the [Environment Configuration File](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Environment-Configuration-File) Wiki and fill in the necessary details.

<br>

### :diamond_shape_with_a_dot_inside: Start container and beginning uploading
Now we are all ready to start the uploader inside the docker container and start uploading. The run command template that can be used to start the uploader inside a new docker container is given below
```
docker run --rm -it \
    -v /home/user/media:/home/user/media \
    --env-file config.env \
    noobmaster669/gg-bot-uploader:latest -t BHDTV BHD NBL -p "/home/user/mediaYOUR_FILE_OR_FOLDER" OPTIONAL_ARGUMENTS
```
If you are not familiar with docker going through the below section where each component of the run command is dissected and explained in detail.

#### Dissecting the run command

<br>

The different components in the run command are 

- **docker**
- **run**
- **--rm**
- **-it**
- **-v /home/user/media:/home/user/media**
- **--env-file config.env**
- **noobmaster669/gg-bot-uploader:latest**
- **-t BHDTV BHD NBL -p "/home/user/mediaYOUR_FILE_OR_FOLDER" OPTIONAL_ARGUMENTS**

#### :small_red_triangle: docker
Self explanatory. We're using the command `docker` to interact with the docker daemon.

#### :small_red_triangle: run
Telling docker that we want to `create` and `start` a new docker container with the details provided.

#### :small_red_triangle: --rm
Once the container is started, the GG-BOT upload assistant will also be started in the container. Once he uploader finishes uploading the process is killed and thus the container will be stopped by docker. Note that the container will only be stopped, it won't be removed. If you upload invoke the run command 5 times, you'll end up with 5 different containers that are all stopped. These containers are not needed any more and can be removed.

The `--rm` flag tells docker to remove the container when it stops. Thus once the uploader finishes uploading, the container will be stopped and removed.

#### :small_red_triangle: -it
By default docker containers will be started in the background and you'll not be able to interact with the uploader running inside the container. The `-it` flag instructs docker to run the container in **interactive mode**.

#### :small_red_triangle: -v /home/user/media:/home/user/media
Docker containers do not save the data they produce. As soon as the process is finished, the container stops and everything inside of it is removed. Similarly docker containers cannot access any data that is present in your file system of host machine. This is a major problem since the media files are present in our host machine, and they cannot be access from inside the docker container. One way to solve this problem would be to to share the host data with the container.

This is exactly what the `-v` flag does. You can learn more about Docker Volumes [here](https://docs.docker.com/storage/volumes/).

> A Docker bind mount is a high-performance connection from the container to a directory on the host machine. It allows the host to share its own file system with the container, which can be made read-only or read-write.[2]

`-v` or `--volume` consists of three fields, separated by colon characters (:). The fields must be in the correct order, and the meaning of each field is not immediately obvious.
- The first field is the path in the host machine which needs to be shared with the container.
- The second field is the path where the file or directory are mounted in the container.
- The third field is optional, and is a comma-separated list of options, such as ro. [2]

> Assume that all out media files are inside the folder /home/user/media. See [Docker Run Command Examples](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Docker-Run-Command-Examples) for more details and examples

**-v /home/user/media:/home/user/media**
Here we are mapping the folder /home/user/media from HOST to a path /home/user/media inside the CONTAINER.
A file `/home/user/media/movie.mkv` present in HOST machine can be accessed as `/home/user/media/movie.mkv` from within the CONTAINER.

If we provided the mapping like
**-v /home/user/media:/data**
then the same file `/home/user/media/movie.mkv` present in HOST machine can be accessed as `/data/movie.mkv` from within the CONTAINER.

> /home/user/media:/data  => /home/user/media in HOST == /data inside CONTAINER

#### :small_red_triangle: --env-file config.env
The configurable aspects of the uploader is controlled by environment variables. the `--env-file` flag can be used to read environment variables from a file and set them inside the docker container.

> Syntax: --env-file <ENVIRONMENT_FILE>

As mentioned before the `config.env` file is present inside the `/home/user/ggbot` folder and we are running the command from the same folder. Hence `--env-file config.env` is enough. If you are to run the docker run command from a different folder, then you'll need to provide the full path to the env file like `--env-file /home/user/ggbot/config.env`

#### :small_red_triangle: noobmaster669/gg-bot-uploader:latest
Every docker containers are created from a docker image. The docker image for GG-BOT upload assistant is noobmaster669/gg-bot-uploader.
The :latest is the tag for the docker image. Think of the tag like different versions of the image.

If you want to use the v1.0 of GG-BOT upload assistant then you can use the image
```
noobmaster669/gg-bot-uploader:1.0
```
If you want to use the v2.0 of GG-BOT upload assistant then you can use the image
```
noobmaster669/gg-bot-uploader:2.0
```
If you use the :latest tag, you'll get the latest version of the GG-BOT upload assistant automatically. When every a new version is available simply run the command, and you'll get the latest version ready to be used next time you run the `docker run` command. Please see the Upgrading To New Versions section below for more details
```
docker pull noobmaster669/gg-bot-uploader:latest
```

#### :small_red_triangle: -t BHDTV BHD NBL -p "/home/user/mediaYOUR_FILE_OR_FOLDER" OPTIONAL_ARGUMENTS
These are the Mandatory and Optional arguments for the GG-BOT Upload Assistant. Please refer to the [Arguments and User Inputs](https://gitlab.com/NoobMaster669/gg-bot-upload-assistant/-/wikis/Arguments-and-User-Inputs) Wiki for detailed explanation on each argument and its use.

<br>

## Additional Information
- Upgrading to newer versions
- Different image tags available

### :diamond_shape_with_a_dot_inside: Upgrading to newer versions
The first time you use the run command, the GG-BOT Upload Assistant docker image will be pulled automatically from the docker image registry([Docker Hub](https://hub.docker.com/r/noobmaster669/gg-bot-uploader))
```
docker run --rm -it \
    -v /home/user/media:/home/user/media \
    --env-file config.env \
    noobmaster669/gg-bot-uploader:latest -t BHDTV BHD NBL -p "/home/user/mediaYOUR_FILE_OR_FOLDER" OPTIONAL_ARGUMENTS
```

1. Using the `:latest` tags: When you are using the :latest tag or alternate tags with latest in them you'll need to run the below command when every a new version is available. The command will pull the latest version of the image again from docker hub. Once pulled any new containers created will be using the LATEST version of GG-BOT Upload Assistant
```
docker pull noobmaster669/gg-bot-uploader:latest
```

2. Other tags: If you are using release specific tags such as 1.0, 2.0, 2.0.1 etc, you just need to change the version tag in run command.
Suppose initially you were using 2.0 version 
```
docker run --rm -it \
    -v /home/user/media:/home/user/media \
    --env-file config.env \
    noobmaster669/gg-bot-uploader:2.0 -t BHDTV BHD NBL -p "/home/user/mediaYOUR_FILE_OR_FOLDER" OPTIONAL_ARGUMENTS
```
And now you wish to upgrade to version 2.0.3, then all you need to do is change `noobmaster669/gg-bot-uploader:2.0` to `noobmaster669/gg-bot-uploader:2.0.3`.
```
docker run --rm -it \
    -v /home/user/media:/home/user/media \
    --env-file config.env \
    noobmaster669/gg-bot-uploader:2.0.3 -t BHDTV BHD NBL -p "/home/user/mediaYOUR_FILE_OR_FOLDER" OPTIONAL_ARGUMENTS
```

### :diamond_shape_with_a_dot_inside: Different image tags available
GG-BOT Upload Assistant is released in different flavors.
1. Normal Images: Most of you will be using this flavor of the uploader. 
> Eg: noobmaster669/gg-bot-uploader:latest, noobmaster669/gg-bot-uploader:1.0 noobmaster669/gg-bot-uploader:1.1 etc
2. Full Disk Images: The normal image is not capable of uploading Full Bluray disks. If you wish to upload Full Bluray disks you need to use the Full Disk Image. This image is capable of doing everything the normal image is capable of doing plus Full Disk images. Look for `FullDisk-` prefix in tag section. 
> Eg: noobmaster669/gg-bot-uploader:FullDisk-latest, noobmaster669/gg-bot-uploader:FullDisk-2.0 etc
3. arm32v7 Images: This is image for machines using ARM architecture. Please note that full disk uploads are not possible here.
> noobmaster669/gg-bot-uploader:arm32v7-latest, noobmaster669/gg-bot-uploader:arm32v7-2.0 etc
3. aarch64 Images: This is image for machines using AARCH64 architecture. Please note that full disk uploads are not possible here.
> noobmaster669/gg-bot-uploader:aarch64-latest, noobmaster669/gg-bot-uploader:aarch64-2.0 etc

You can find the list of all available tags [here](https://hub.docker.com/r/noobmaster669/gg-bot-uploader/tags).

### References
[1] https://www.linux.com/topic/desktop/how-install-and-use-docker-linux

[2] https://www.baeldung.com/ops/docker-volumes