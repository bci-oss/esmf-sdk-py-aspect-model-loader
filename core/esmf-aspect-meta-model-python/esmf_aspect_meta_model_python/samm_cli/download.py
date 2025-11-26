"""Download SAMM CLI.

Windows: https://github.com/eclipse-esmf/esmf-sdk/releases/download/v2.12.0/samm-cli-2.12.0-windows-x86_64.zip
  Linux: https://github.com/eclipse-esmf/esmf-sdk/releases/download/v2.12.0/samm-cli-2.12.0-linux-x86_64.tar.gz
    JAR: https://github.com/eclipse-esmf/esmf-sdk/releases/download/v2.12.0/samm-cli-2.12.0.jar
"""

import os
import platform
import sys
import tarfile
import zipfile

from pathlib import Path

import requests

from esmf_aspect_meta_model_python.samm_cli.constants import SAMMCliConstants as Const


def get_samm_cli_file_name():
    """Get a SAMM CLI file name for the current platform."""

    if platform.system() == "Windows":
        file_name = Const.WIN_FILE_NAME.substitute(version_number=Const.JAVA_CLI_VERSION)
    elif platform.system() == "Linux":
        file_name = Const.LINUX_FILE_NAME.substitute(version_number=Const.JAVA_CLI_VERSION)
    elif platform.system() == "Darwin":  # macOS
        file_name = Const.MAC_FILE_NAME.substitute(version_number=Const.JAVA_CLI_VERSION)
    else:
        raise NotImplementedError(
            f"Please download a SAMM CLI manually for your operation system from '{Const.BASE_PATH}'"
        )

    return file_name


def download_archive_file(url, archive_file):
    """Download an archive file."""
    with open(archive_file, "wb") as f:
        print("Downloading %s" % archive_file)
        response = requests.get(url, allow_redirects=True, stream=True)
        response.raise_for_status()  # Fail fast if HTTP error

        content_len = response.headers.get("content-length")

        if content_len is None:
            f.write(response.content)
        else:
            total_len = int(content_len)
            data_len = 0
            chunk = 4096
            progress_bar_len = 50

            for content_data in response.iter_content(chunk_size=chunk):
                data_len += len(content_data)

                f.write(content_data)

                curr_progress = int(50 * data_len / total_len)
                sys.stdout.write(f"\r[{'*' * curr_progress}{' ' * (progress_bar_len - curr_progress)}]")
                sys.stdout.flush()


def extract_archive(archive_file, dest_dir):
    """Extract archive depending on its file type."""
    if archive_file.endswith(".zip"):
        with zipfile.ZipFile(archive_file) as archive:
            archive.extractall(dest_dir)
    elif archive_file.endswith((".tar.gz", ".tgz")):
        with tarfile.open(archive_file, mode="r:gz") as archive:
            archive.extractall(dest_dir)
    else:
        raise ValueError(f"Unsupported archive format: {archive_file}")


def download_samm_cli():
    try:
        samm_cli_file_name = get_samm_cli_file_name()
    except NotImplementedError as error:
        print(error)
    else:
        print(f"Start downloading SAMM CLI {samm_cli_file_name}")
        url = Const.BASE_PATH.substitute(version_number=Const.JAVA_CLI_VERSION, file_name=samm_cli_file_name)
        dir_path = Path(__file__).resolve().parents[0]
        archive_file = os.path.join(dir_path, samm_cli_file_name)

        download_archive_file(url, archive_file)
        print("\nSAMM CLI archive file downloaded")

        print("Start extracting files")
        extract_archive(archive_file, dest_dir=os.path.join(dir_path, "samm-cli"))
        print("Done extracting files")

        print("Deleting SAMM CLI archive file")
        os.remove(archive_file)
