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
# Recommended example:
docker run -it --user ros --network=host --ipc=host -v $PWD/source:/my_source_code my_image
```

| switches                              | description                                                                        |
| ------------------------------------- | ---------------------------------------------------------------------------------- |
| -it                                   | -i: interactive -t: TTY                                                            |
| --rm                                  | Remove container after it stopped.                                                 |
| --name <container_name>               | Give the new container a name.                                                     |
| -v <path_on_host>:<path_in_container> | Mount path_on_host to path_in_container. Note: these path should be absolute path. |
| --user <user>                         | Run as a user. <user> can be user name or uid which is in docker environment.      |
| --network=host                        |                                                                                    |
| --ipc=host                            |                                                                                    |

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

See subfolders

## GUI and GPU

```shell
docker run -it --network=host --ipc=host \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    --env DISPLAY \
    --gpus all \
    --env NVIDIA_DRIVER_CAPABILITIES=all \
    <IMAGE_NAME>
```

## Network problem when building image

```shell
docker build -t <IMAGE_NAME> . \
    --build-arg "http_proxy=http://localhost:1081" \
    --build-arg "https_proxy=http://localhost:1081" \
    --network host
```
