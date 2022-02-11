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

## Basic steps in setting up GG-BOT Upload Assistant
- Install docker
- Setup your configuration file
- Start container and beginning uploading


### Install Docker
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

### Setup your configuration file
There are various aspects of the upload assistant that can be configured as per the users requirement and convenience. These properties are accepted as environment variables. If you wish to have a different set of properties in a different system/environment, all you need to do is change the environment variables. When using docker the environment variables can be set with the `-e` flag or the `--env-file`. More on this in upcoming sections. 

### References
[1] https://www.linux.com/topic/desktop/how-install-and-use-docker-linux/