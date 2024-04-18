# Learning Docker

 ## Commands

```shell
# Image
docker image ls # == docker images
docker image pull ros:humble # == docker pull
docker image rm # == docker rmi
docker image rm -f # Delete image even there is a container related to the image

# container
docker container run <image> # == docker run <image>. Create a new container from image
docker run -it ros:humble # -i: interactive -t:TTY
docker run --rm --name <container_name> <image> # --rm: Remove container after it stopped. --name: Give the new container a name.
docker container start -i <container> # Start a stopped container
docker container exec <container> <COMMAND> # == docker exec -it <container>. Run another command in the container.
docker exec -it <container> bash # Run another bash shell in t container
docker container ls -a # == docker ps -a
docker container stop
docker container rm # == docker rm
docker container prune # Remove all stopped container
```

