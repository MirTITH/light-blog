#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argparse, argcomplete
import os
from colorama import Fore, init
import subprocess
from tqdm import tqdm
import shutil
from enum import Enum

init(autoreset=True)  # For colorama: reset color after each print


def ask_user_to_continue(prompt: str = "Continue?") -> bool:
    """Ask the user if they want to continue

    Returns:
        bool: True if the user wants to continue
    """

    print(prompt + " [Y/n] ", end="")
    return input().lower() in ["y", ""]


def get_temp_file_name(file_path: str, postfix: str = "_temp") -> str:
    name, ext = os.path.splitext(file_path)
    return name + postfix + ext


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


def remix_copy(src: str, dst: str, ffmpeg_path: str = "ffmpeg") -> bool:
    """Remix video in src to dst

    Args:
        src (str): Source file
        dst (str): Destination file

    Returns:
        bool: True if successful
    """
    result = False

    # Use temp file to avoid overwriting dst file
    temp_dst = get_temp_file_name(dst, "_copy")

    cmd = [ffmpeg_path, "-i", src, "-c:v", "copy", "-c:a", "copy", temp_dst]
    print(" ".join(cmd))

    run_result = subprocess.run(cmd)
    result = run_result.returncode == 0

    # Rename temp file to dst
    if result:
        os.rename(temp_dst, dst)

    return result


def copy_or_remix_video(src: str, dst: str, ffmpeg_path: str = "ffmpeg") -> dict:
    """Copy video if the source and destination have the same extension. Otherwise, remix the video.

    Args:
        src (str): Source file
        dst (str): Destination file

    Returns:
        bool: True if successful
    """

    result = {"success": False, "remix": False}

    src_ext = os.path.splitext(src)[1]
    dst_ext = os.path.splitext(dst)[1]

    if src_ext.lower() == dst_ext.lower():
        print(f"Copying {Fore.BLUE}{src}{Fore.RESET} to {Fore.GREEN}{dst}")
        shutil.copyfile(src, dst)
        result["success"] = True
        result["remix"] = False
    else:
        print(f"Remixing {Fore.BLUE}{src}{Fore.RESET} to {Fore.GREEN}{dst}")
        remix_result = remix_copy(src, dst, ffmpeg_path)
        if remix_result:
            result["success"] = True
            result["remix"] = True

    return result


class VideoConvertResult(Enum):
    FAILED = 0
    CONVERTED = 1
    COPIED = 2
    REMIXED = 3


def convert_video(src: str, dst: str, args: list, ffmpeg_path: str = "ffmpeg", copy_if_larger: bool = False) -> VideoConvertResult:
    """Convert video in src to dst

    Args:
        src (str): Source file
        dst (str): Destination file
        args (list, optional): Arguments for ffmpeg. Defaults to None.

    Returns:
        dict: Result of the conversion
    """

    # Use temp file to avoid overwriting dst file
    temp_dst = get_temp_file_name(dst)

    cmd = [ffmpeg_path, "-i", src, *args, temp_dst]
    print(" ".join(cmd))

    convert_result = subprocess.run(cmd).returncode == 0

    if not convert_result:
        return VideoConvertResult.FAILED

    if copy_if_larger:
        src_size = os.path.getsize(src)
        output_size = os.path.getsize(temp_dst)
        print(f"Source size: {src_size} bytes, Output size: {output_size} bytes")
        if output_size > src_size:
            print(f"{Fore.RED}Output size is larger than source size.")
            copy_result = copy_or_remix_video(src, dst)
            if copy_result["success"]:
                os.remove(temp_dst)
                if copy_result["remix"]:
                    return VideoConvertResult.REMIXED
                else:
                    return VideoConvertResult.COPIED
            else:
                print(f"{Fore.RED}Failed to copy file. Use converted file even if it is larger.")

    # Rename temp file to dst
    os.rename(temp_dst, dst)

    return VideoConvertResult.CONVERTED


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
    parser.add_argument("--format", help="Output format. If you don't want to change the format, specify 'copy'.", default="copy")
    parser.add_argument("-s", "--scale", help="Output scale")
    parser.add_argument("--copy-if-larger", help="Delete output file if it is larger than the source file", action="store_true")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    video_ext = {".mp4", ".mkv", ".avi", ".mov"}

    # Video arguments
    # ultrafast, superfast, veryfast, faster, medium, slow, slower, veryslow
    ffmpeg_video_args = ["-c:v", "libx265", "-crf", "23", "-preset", "veryslow"]

    # Audio arguments
    ffmpeg_audio_args = ["-c:a", "copy"]
    # ffmpeg_audio_args = ["-c:a", "libfdk_aac", "-vbr", "4"]
    # ffmpeg_audio_args = ["-c:a", "aac", "-b:a", "256k"]
    # ffmpeg_audio_args = ["-c:a", "aac", "-q:a", "2"]

    ffmpeg_args = ffmpeg_video_args + ffmpeg_audio_args

    # Print arguments
    print("Arguments:")
    for arg in vars(args):
        print(f"{arg}: {getattr(args, arg)}")

    if getattr(args, "scale", None) is not None:
        ffmpeg_args.extend(["-vf", f"scale={args.scale}"])

    print("FFmpeg arguments: " + " ".join(ffmpeg_args))

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
        print(f"{Fore.BLUE}{src_file}{Fore.RESET} -> {Fore.GREEN}{dst_file}")

        temp_file = get_temp_file_name(dst_file)
        if os.path.exists(temp_file):
            if ask_user_to_continue(f"Temp file '{temp_file}' already exists. Delete?"):
                os.remove(temp_file)

        copy_file = get_temp_file_name(dst_file, "_copy")
        if os.path.exists(copy_file):
            if ask_user_to_continue(f"Copy file '{copy_file}' already exists. Delete?"):
                os.remove(copy_file)

    if not ask_user_to_continue(f"Convert {len(src_rfiles)} videos?"):
        return

    success_files = []
    converted_files = []
    copied_files = []
    remixed_files = []
    for src_rfile, dst_file in tqdm(zip(src_rfiles, dst_files), total=len(src_rfiles)):
        src_file = os.path.join(src_wd, src_rfile)
        if os.path.exists(dst_file):
            print(f"{Fore.YELLOW}'{dst_file}' already exists. Skipping")
            continue
        dst_dir = os.path.dirname(dst_file)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        convert_result = convert_video(
            src_file,
            dst_file,
            ffmpeg_args,
            # ffmpeg_path="/home/nros/.local/ffmpeg_build/bin/ffmpeg",
            copy_if_larger=args.copy_if_larger,
        )
        if convert_result != VideoConvertResult.FAILED:
            success_files.append(src_file)
            if convert_result == VideoConvertResult.CONVERTED:
                converted_files.append(src_file)
            elif convert_result == VideoConvertResult.COPIED:
                copied_files.append(src_file)
            elif convert_result == VideoConvertResult.REMIXED:
                remixed_files.append(src_file)

    print(f"Successfully processed {len(success_files)} files:")
    print(f"  Converted {len(converted_files)} files.")
    if len(copied_files) > 0:
        print(f"  Copied {len(copied_files)} files:")
        for file in copied_files:
            print(f"    {file}")

    if len(remixed_files) > 0:
        print(f"  Remixed {len(remixed_files)} files:")
        for file in remixed_files:
            print(f"    {file}")


if __name__ == "__main__":
    main()
