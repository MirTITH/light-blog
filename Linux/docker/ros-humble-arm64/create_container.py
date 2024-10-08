#!/usr/bin/python3

import os
import sys
import subprocess
import argparse
from typing import List


def ask_user_to_continue(prompt: str = "Continue?") -> bool:
    """Ask the user if they want to continue

    Returns:
        bool: True if the user wants to continue
    """

    print(prompt + " [Y/n] ", end="")
    return input().lower() in ["y", ""]


class DockerCmdGenerator:
    def __init__(self, args):
        self.image_name: str = getattr(args, "image-name")
        self.container_name: str = getattr(args, "container-name")
        self.container_user_name: str = getattr(args, "user_name")
        self.user_data_dir: str = getattr(args, "user_data", None)
        self.no_nv: bool = getattr(args, "no_nv", False)

        self.volumes: List[str] = getattr(args, "volume")
        if not self.volumes:
            self.volumes = []

        self.cmd_prefix = ["docker", "run", "-d", "--name", self.container_name, "--user", self.container_user_name]
        self.cmd_postfix = [self.image_name, "sleep", "infinity"]

    def generate_cmd(self) -> List[str]:
        cmd_args = self.__get_cmd_args()
        cmd = self.cmd_prefix + cmd_args + self.cmd_postfix
        return cmd

    def run_cmd(self):
        cmd = self.generate_cmd()
        print(f"Running command: {' '.join(cmd)}")

        if ask_user_to_continue():
            print("Creating container...")
            result = subprocess.run(cmd)
            if result.returncode != 0:
                print("Failed to create container")
                sys.exit(1)
            print("Done.\n\nYou can attach to the container using vscode or by running the following command:")
            print(f"    docker exec -it {self.container_name} /bin/bash\n")
            print("To remove the container, run the following command:")
            print(f"    docker rm -f {self.container_name}")
        else:
            print("Aborted")

    def __get_home_dir(self, user_name):
        if user_name == "root":
            return "/root"
        else:
            return f"/home/{user_name}"

    def __to_host_abs_path(self, path):
        return os.path.abspath(os.path.expanduser(path))

    def __to_container_abs_path(self, path):
        if os.path.isabs(path):
            return path
        else:
            return os.path.join(self.__get_home_dir(self.container_user_name), path)

    def __check_and_create_directory(self, dir_path, ask=True):
        if not os.path.exists(dir_path):
            if ask:
                if not ask_user_to_continue(f"Directory '{dir_path}' does not exist. Create? "):
                    return

            print(f"Creating directory '{dir_path}'")
            os.makedirs(dir_path)

    def __check_and_create_file(self, file_path, ask=True):
        if not os.path.exists(file_path):
            if ask:
                if not ask_user_to_continue(f"File '{file_path}' does not exist. Create? "):
                    return

            print(f"Creating file '{file_path}'")
            with open(file_path, "w") as f:
                f.write("")

    def __get_mount_args(self, host_path: str, container_path: str, path_type: str = "", options: str = "") -> List[str]:
        """Get the arguments to mount a directory or file from the host to the container

        Args:
            host_path (str): Host path
            container_path (str): Container path
            path_type (str, optional): "dir" or "file". If not specified, the function will deduce the type by checking if the path ends with "/"
            options (str, optional): Mount options

        Returns:
            List[str]: List of arguments to mount the directory or file
        """

        if not path_type:
            if host_path.endswith("/"):
                path_type = "dir"
            else:
                path_type = "file"

        host_abs_path = self.__to_host_abs_path(host_path)
        container_abs_path = self.__to_container_abs_path(container_path)

        # Create the directory or file if it does not exist
        if path_type == "dir":
            self.__check_and_create_directory(host_abs_path)
        elif path_type == "file":
            self.__check_and_create_file(host_abs_path)
        else:
            if not os.path.exists(host_abs_path):
                print(f"Warning: {host_abs_path} does not exist")

        if options:
            print(f"Mounting {host_abs_path} to {container_abs_path} with options: {options}")
            return ["-v", f"{host_abs_path}:{container_abs_path}:{options}"]
        else:
            print(f"Mounting {host_abs_path} to {container_abs_path}")
            return ["-v", f"{host_abs_path}:{container_abs_path}"]

    def __get_volumes_mount_args(self) -> List[str]:
        result = []
        for volume in self.volumes:
            paths = volume.split(":")
            if len(paths) <= 1:
                raise ValueError(f"Invalid volume: {volume}")
            options = paths[2] if len(paths) > 2 else ""
            result.extend(self.__get_mount_args(paths[0], paths[1], options=options))
        return result

    def __get_cmd_args(self):
        CONTAINER_HOME = self.__get_home_dir(self.container_user_name)

        XDG_RUNTIME_DIR = os.getenv("XDG_RUNTIME_DIR")
        HOME = os.getenv("HOME")
        SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

        cmd_args = []

        cmd_args.extend(["--network=host", "--ipc=host"])  # Enable host networking
        cmd_args.extend(["--privileged"])  # Allow access to all devices

        # Enable X11 GUI
        cmd_args.extend(self.__get_mount_args("/tmp/.X11-unix", "/tmp/.X11-unix", path_type="dir", options="rw"))
        cmd_args.extend(["--env", "DISPLAY"])

        # Enable NVIDIA GPU
        if not self.no_nv:
            cmd_args.extend(["--runtime=nvidia", "--gpus", "all", "--env", "NVIDIA_DRIVER_CAPABILITIES=all"])

        # Enable sound
        cmd_args.extend(self.__get_mount_args(f"{XDG_RUNTIME_DIR}/pulse", "/tmp/pulse", "dir"))
        cmd_args.extend(self.__get_mount_args(f"{HOME}/.config/pulse/cookie", f"{CONTAINER_HOME}/.config/pulse/cookie", "file"))
        cmd_args.extend(["--env", "PULSE_SERVER=unix:/tmp/pulse/native"])

        # Mount .ssh directory
        cmd_args.extend(self.__get_mount_args(f"{HOME}/.ssh", f"{CONTAINER_HOME}/.ssh", "dir"))

        # Mount .gitconfig
        cmd_args.extend(self.__get_mount_args(f"{HOME}/.gitconfig", f"{CONTAINER_HOME}/.gitconfig", "file"))

        # Mount some files in SCRIPT_DIR
        cmd_args.extend(self.__get_mount_args(f"{SCRIPT_DIR}/common_rc", f"{CONTAINER_HOME}/.local/common_rc", "file"))

        # Mount user data directory
        if self.user_data_dir:
            USER_DATA_DIR = self.__to_host_abs_path(self.user_data_dir)
            print(f"User data directory: {USER_DATA_DIR}")
            cmd_args.extend(self.__get_mount_args(USER_DATA_DIR, f"{CONTAINER_HOME}/user_data", "dir"))

        # Mount volumes
        cmd_args.extend(self.__get_volumes_mount_args())

        return cmd_args


def main():
    parser = argparse.ArgumentParser(description="Create a container")
    parser.add_argument("image-name", help="The name of the image to create the container from")
    parser.add_argument("container-name", help="The name of the container to create")
    parser.add_argument("--user-name", help="The user to run the container as.", default="docker_user")
    parser.add_argument("--user-data", help="The directory to store user data. Will be mounted to /home/<user_name>/user_data")
    parser.add_argument("--no-nv", help="Do not enable NVIDIA GPU", action="store_true")
    parser.add_argument("--volume", "-v", help="Mount a volume from the host to the container", action="append")
    args = parser.parse_args()

    # Print arguments
    for arg in vars(args):
        print(f"{arg}: {getattr(args, arg)}")

    docker_cmd_generator = DockerCmdGenerator(args)
    docker_cmd_generator.run_cmd()


if __name__ == "__main__":
    main()
