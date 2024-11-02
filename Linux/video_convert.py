#!/usr/bin/python3

import argparse
import os
from colorama import Fore, init
import subprocess
from tqdm import tqdm

init(autoreset=True)


def ask_user_to_continue(prompt: str = "Continue?") -> bool:
    """Ask the user if they want to continue

    Returns:
        bool: True if the user wants to continue
    """

    print(prompt + " [Y/n] ", end="")
    return input().lower() in ["y", ""]


def get_temp_file_name(file_path: str) -> str:
    name, ext = os.path.splitext(file_path)
    return name + "_temp" + ext


def get_all_files_in_dir(dir_path: str, extenstion: set = None) -> list:
    """Get all files in a directory

    Args:
        dir_path (str): Directory path
        extenstion (set, optional): File extension. Defaults to None.

    Returns:
        list: List of files (relative path)
    """
    result = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_path = os.path.relpath(file_path, dir_path)
            if extenstion:
                if file_path.lower().endswith(tuple(extenstion)):
                    result.append(file_path)
            else:
                result.append(file_path)

    return result


def convert_video(src: str, dst: str, args: list = None, ffmpeg_path: str = "ffmpeg"):
    """Convert video in src to dst

    Args:
        src (str): Source file
        dst (str): Destination file
        args (list, optional): Arguments for ffmpeg. Defaults to None.
    """
    if not args:
        args = ["-c:v", "libx264", "-crf", "23", "-c:a", "copy"]

    # Use temp file to avoid overwriting dst file
    temp_dst = get_temp_file_name(dst)

    cmd = [ffmpeg_path, "-i", src, *args, temp_dst]
    print(" ".join(cmd))

    run_result = subprocess.run(cmd)

    # Rename temp file to dst
    if run_result.returncode == 0:
        os.rename(temp_dst, dst)


def make_dst_path(src_path: str, dst_folder: str, extenstion: str = None) -> str:
    """Make destination path

    Args:
        src_path (str): Source
        dst_folder (str): Destination folder
        extenstion (str, optional): File extension. Defaults to None.

    Returns:
        str: Destination path
    """
    if extenstion:
        if not extenstion.startswith("."):
            extenstion = "." + extenstion
        dst_name, _ = os.path.splitext(src_path)
        result = os.path.join(dst_folder, dst_name + extenstion)
    else:
        result = os.path.join(dst_folder, src_path)

    return result


def main():
    parser = argparse.ArgumentParser(description="Convert video in src to dst")
    parser.add_argument("src", help="Src folder or file")
    parser.add_argument("dst", help="Dst folder or file")
    parser.add_argument("--format", help="Output format. If you don't want to change the format, specify 'copy'.", default="mp4")
    parser.add_argument("-s", "--size", help="Output size")
    args = parser.parse_args()

    video_ext = {".mp4", ".mkv", ".avi", ".mov"}

    # ultrafast, superfast, veryfast, faster, medium, slow, slower, veryslow
    # ffmpeg_args = ["-c:v", "copy", "-c:a", "copy"]
    ffmpeg_args = ["-c:v", "libx265", "-crf", "20", "-preset", "medium", "-c:a", "copy"]
    # ffmpeg_args = ["-c:v", "libx265", "-crf", "23", "-preset", "veryslow", "-c:a", "aac", "-b:a", "256k"]
    # ffmpeg_args = ["-c:v", "libx265", "-crf", "23", "-preset", "veryslow", "-c:a", "libfdk_aac", "-vbr", "5"]

    # Print arguments
    for arg in vars(args):
        print(f"{arg}: {getattr(args, arg)}")

    if getattr(args, "size", None) is not None:
        ffmpeg_args.extend(["-vf", f"scale={args.size}"])

    src = args.src
    dst = args.dst
    target_format = getattr(args, "format")

    # Create destination directory if it does not exist
    if not os.path.exists(dst):
        if not ask_user_to_continue(f"Directory '{dst}' does not exist. Create?"):
            return

        print(f"Creating directory '{dst}'")
        os.makedirs(dst)

    # Get all files in src
    if os.path.isdir(src):
        src_wd = src
        # Source files relative to src_wd
        src_rfiles = get_all_files_in_dir(src_wd, video_ext)
    else:
        src_wd = os.path.dirname(src)
        # Source files relative to src_wd
        src_rfiles = [os.path.relpath(src, src_wd)]

    dst_files = []
    for src_rfile in src_rfiles:
        if target_format == "copy":
            dst_file = make_dst_path(src_rfile, dst)
        else:
            dst_file = make_dst_path(src_rfile, dst, target_format)
        dst_files.append(dst_file)

    # Check if destination files already exist
    print("Files to convert:")
    for src_rfile, dst_file in zip(src_rfiles, dst_files):
        src_file = os.path.join(src_wd, src_rfile)
        print(f"{Fore.BLUE}{src_file} -> {Fore.GREEN}{dst_file}")
        temp_file = get_temp_file_name(dst_file)
        if os.path.exists(temp_file):
            if ask_user_to_continue(f"Temp file '{temp_file}' already exists. Delete?"):
                os.remove(temp_file)

    if not ask_user_to_continue(f"Convert {len(src_rfiles)} videos?"):
        return

    for src_rfile, dst_file in tqdm(zip(src_rfiles, dst_files), total=len(src_rfiles)):
        src_file = os.path.join(src_wd, src_rfile)
        if os.path.exists(dst_file):
            print(f"{Fore.YELLOW}'{dst_file}' already exists. Skipping")
            continue
        dst_dir = os.path.dirname(dst_file)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        convert_video(
            src_file,
            dst_file,
            ffmpeg_args,
            # ffmpeg_path="/home/nros/.local/ffmpeg_build/bin/ffmpeg",
        )


if __name__ == "__main__":
    main()
