# ROS Humble Docker

## 1-2

```shell
# 1. Build image
./build_image.sh

# 2. Create container
./create_container.sh
```

## 3. Attach vecode to the container

Use Dev Container and attach to the container: `my-ros-humble`

### 4. Test if GUI apps work

In your host:

```shell
xhost +local:docker
```

In docker:

```shell
rviz2
```

You 

## Customize

### Use zsh

Change the default console to zsh in vscode

### Change Qt app style

This can change the look of rviz2 etc.

Run the GUI tool:

```shell
qt5ct
```

I recommend breeze theme