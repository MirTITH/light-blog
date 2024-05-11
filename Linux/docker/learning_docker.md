# Learning Docker

 ## Commands

### Image

```shell

docker image ls # == docker images
docker image pull ros:humble # == docker pull
docker image rm # == docker rmi
docker image rm -f # Delete image even there is a container related to the image
docker image build -t <new_image_name> <Dockerfile_folder>
```

### Container

#### docker container run

`docker container run` == `docker run`

```shell
docker run [switches] <image>
```

| switches                              | description                                                                        |
| ------------------------------------- | ---------------------------------------------------------------------------------- |
| -it                                   | -i: interactive -t: TTY                                                            |
| --rm                                  | Remove container after it stopped.                                                 |
| --name <container_name>               | Give the new container a name.                                                     |
| -v <path_on_host>:<path_in_container> | Mount path_on_host to path_in_container. Note: these path should be absolute path. |
| --user <user>                         | Run as a user. <user> can be user name or uid which is in docker environment.      |

#### Other commands

```shell
docker container start -i <container> # Start a stopped container

docker container exec <container> <COMMAND> # == docker exec -it <container>. Run another command in the container.
docker exec -it <container> bash # Run another bash shell in t container

docker container ls -a # == docker ps -a
docker container stop
docker container rm # == docker rm
docker container prune # Remove all stopped container
```

## Example docker files

### ROS2 humble with GUI

```dockerfile
# This is not the official docker image. But it contains GUI support.
FROM osrf/ros:humble-desktop-full


# Example of installing programs
RUN apt-get update \
    && apt-get install -y \
    nano \
    vim \
    && rm -rf /var/lib/apt/lists/*


# Example of copying a file
COPY config/ /site_config/


# Create a non-root user
ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  && mkdir /home/$USERNAME/.config && chown $USER_UID:$USER_GID /home/$USERNAME/.config


# Set up sudo
RUN apt-get update \
  && apt-get install -y sudo \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
  && chmod 0440 /etc/sudoers.d/$USERNAME \
  && rm -rf /var/lib/apt/lists/*


# Copy the entrypoint and bashrc scripts so we have 
# our container's environment set up correctly
COPY entrypoint.sh /entrypoint.sh
COPY bashrc /home/${USERNAME}/.bashrc


# Set up entrypoint and default command
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
CMD ["bash"]
```

