# ROS Humble Docker

## Build image

```shell
./build_image.sh
```

## Create container
Use the python script `create_container.py` in the parent directory.

```shell
cd ..

# Show help
./create_container.py -h

# An example, do not use directly
./create_container.py my-ros-humble my-project-name --rc-file common_rc -v ~/Documents/:Documents -v ~/Downloads/:Downloads --user-data /path/to/project
```

## Attach vecode to the container

Use Dev Container and attach to the container: `my-project-name`

## Test if GUI apps work

In your host:

```shell
xhost +local:docker
```

In docker:

```shell
rviz2
```

## Customize

### Use zsh

Change the default console to zsh in vscode

### Change Qt app style

#### This can:

- Change the look of rviz2 etc  
- Fix icon missing problem in some apps

#### Method: 

Run the GUI tool:

```shell
qt5ct
```

My recommendation:  
- In `Appearence` tab, change the style to `Breeze`  
- In `Icon Theme` tab, choose Breeze then click on OK  
