"""SAMM client download script test suite."""

from unittest import mock

import pytest

import esmf_aspect_meta_model_python.samm_cli.download as download_module

from esmf_aspect_meta_model_python.samm_cli.constants import SAMMCliConstants as Const
from esmf_aspect_meta_model_python.samm_cli.download import (
    download_archive_file,
    download_samm_cli,
    get_samm_cli_file_name,
)

BASE_SCRIPT_PATH = "esmf_aspect_meta_model_python.samm_cli.download"


class TestGetSammCliFileNme:
    @mock.patch(f"{BASE_SCRIPT_PATH}.platform.system")
    def test_get_samm_cli_file_name_windows(self, system_mock):
        system_mock.return_value = "Windows"
        expected_file_name = Const.WIN_FILE_NAME.substitute(version_number=Const.JAVA_CLI_VERSION)

        result = get_samm_cli_file_name()

        assert result == expected_file_name

    @mock.patch(f"{BASE_SCRIPT_PATH}.platform.system")
    def test_get_samm_cli_file_name_linux(self, system_mock):
        system_mock.return_value = "Linux"
        expected_file_name = Const.LINUX_FILE_NAME.substitute(version_number=Const.JAVA_CLI_VERSION)

        result = get_samm_cli_file_name()

        assert result == expected_file_name

    @mock.patch(f"{BASE_SCRIPT_PATH}.platform.system")
    def test_get_samm_cli_file_name_raise_exception(self, system_mock):
        system_mock.return_value = "MacOS"

        with pytest.raises(NotImplementedError) as error:
            get_samm_cli_file_name()

        assert str(error.value) == (
            f"Please download a SAMM CLI manually for your operation system from '{Const.BASE_PATH}'"
        )


class TestDownloadArchiveFile:
    @mock.patch(f"{BASE_SCRIPT_PATH}.requests.get")
    @mock.patch(f"{BASE_SCRIPT_PATH}.print")
    @mock.patch(f"{BASE_SCRIPT_PATH}.open")
    def test_raise_http_error(self, open_mock, print_mock, requests_get_mock):
        f_mock = mock.MagicMock(name="file_mock")
        f_mock.__enter__.return_value = f_mock
        open_mock.return_value = f_mock
        response_mock = mock.MagicMock(name="response_mock")
        response_mock.raise_for_status.side_effect = Exception("HTTP error")
        requests_get_mock.return_value = response_mock

        with pytest.raises(Exception) as error:
            download_archive_file("http://example.com/archive.zip", "archive_file_path")

        assert str(error.value) == "HTTP error"
        open_mock.assert_called_once_with("archive_file_path", "wb")
        print_mock.assert_called_once_with("Downloading archive_file_path")
        requests_get_mock.assert_called_once_with("http://example.com/archive.zip", allow_redirects=True, stream=True)
        response_mock.raise_for_status.assert_called_once_with()
        f_mock.__enter__.assert_called_once()
        f_mock.write.assert_not_called()

    @mock.patch(f"{BASE_SCRIPT_PATH}.requests.get")
    @mock.patch(f"{BASE_SCRIPT_PATH}.print")
    @mock.patch(f"{BASE_SCRIPT_PATH}.open")
    def test_no_content(self, open_mock, print_mock, requests_get_mock):
        f_mock = mock.MagicMock(name="file_mock")
        f_mock.__enter__.return_value = f_mock
        open_mock.return_value = f_mock
        response_mock = mock.MagicMock(name="response_mock")
        response_mock.content = "response_content"
        response_mock.headers.get.return_value = None
        requests_get_mock.return_value = response_mock

        result = download_archive_file("http://example.com/archive.zip", "archive_file_path")

        assert result is None
        open_mock.assert_called_once_with("archive_file_path", "wb")
        print_mock.assert_called_once_with("Downloading archive_file_path")
        requests_get_mock.assert_called_once_with("http://example.com/archive.zip", allow_redirects=True, stream=True)
        response_mock.headers.get.assert_called_once_with("content-length")
        f_mock.__enter__.assert_called_once()
        f_mock.write.assert_called_once_with("response_content")

    @mock.patch(f"{BASE_SCRIPT_PATH}.sys.stdout")
    @mock.patch(f"{BASE_SCRIPT_PATH}.requests.get")
    @mock.patch(f"{BASE_SCRIPT_PATH}.print")
    @mock.patch(f"{BASE_SCRIPT_PATH}.open")
    def test_ok(self, open_mock, print_mock, requests_get_mock, sys_stdout_mock):
        f_mock = mock.MagicMock(name="file_mock")
        f_mock.__enter__.return_value = f_mock
        open_mock.return_value = f_mock
        response_mock = mock.MagicMock(name="response_mock")
        response_mock.content = "response_content"
        response_mock.headers.get.return_value = "42"
        response_mock.iter_content.return_value = ["content_data"]
        requests_get_mock.return_value = response_mock

        result = download_archive_file("http://example.com/archive.zip", "archive_file_path")

        assert result is None
        open_mock.assert_called_once_with("archive_file_path", "wb")
        print_mock.assert_called_once_with("Downloading archive_file_path")
        requests_get_mock.assert_called_once_with("http://example.com/archive.zip", allow_redirects=True, stream=True)
        response_mock.headers.get.assert_called_once_with("content-length")
        response_mock.iter_content.assert_called_once_with(chunk_size=4096)
        f_mock.__enter__.assert_called_once()
        f_mock.write.assert_called_once_with("content_data")
        sys_stdout_mock.write.assert_called_once_with(f"\r[{'*' * 14}{' ' * 36}]")
        sys_stdout_mock.flush.assert_called_once()


class TestDownloadSammCli:
    @mock.patch(f"{BASE_SCRIPT_PATH}.print")
    @mock.patch(f"{BASE_SCRIPT_PATH}.get_samm_cli_file_name")
    @mock.patch(f"{BASE_SCRIPT_PATH}.download_archive_file")
    def test_not_implemented(self, download_archive_file_mock, get_samm_cli_file_name_mock, print_mock):
        test_error = NotImplementedError("exception_message")
        get_samm_cli_file_name_mock.side_effect = test_error

        result = download_samm_cli()

        assert result is None
        get_samm_cli_file_name_mock.assert_called_once_with()
        print_mock.assert_called_once_with(test_error)
        download_archive_file_mock.assert_not_called()

    @mock.patch(f"{BASE_SCRIPT_PATH}.zipfile")
    @mock.patch(f"{BASE_SCRIPT_PATH}.download_archive_file")
    @mock.patch(f"{BASE_SCRIPT_PATH}.os")
    @mock.patch(f"{BASE_SCRIPT_PATH}.Path")
    @mock.patch(f"{BASE_SCRIPT_PATH}.print")
    @mock.patch(f"{BASE_SCRIPT_PATH}.get_samm_cli_file_name")
    @mock.patch(f"{BASE_SCRIPT_PATH}.extract_archive")
    def test_ok(
        self,
        extract_archive_mock,
        get_samm_cli_file_name_mock,
        print_mock,
        path_mock,
        os_mock,
        download_archive_file_mock,
        zipfile_mock,
    ):
        get_samm_cli_file_name_mock.return_value = "samm_cli_file_name.zip"
        path_mock.return_value = path_mock
        path_mock.resolve.return_value = path_mock
        path_mock.parents = ["parent_dir"]
        os_mock.path.join.side_effect = ("archive_file.zip", "extracted_files_path")
        archive_mock = mock.MagicMock(name="archive_mock")
        zipfile_mock.ZipFile.return_value = archive_mock

        result = download_samm_cli()

        assert result is None
        get_samm_cli_file_name_mock.assert_called_once_with()
        print_mock.assert_has_calls(
            [
                mock.call("Start downloading SAMM CLI samm_cli_file_name.zip"),
                mock.call("\nSAMM CLI archive file downloaded"),
                mock.call("Start extracting files"),
                mock.call("Done extracting files"),
                mock.call("Deleting SAMM CLI archive file"),
            ]
        )
        path_mock.assert_called_once_with(download_module.__file__)
        path_mock.resolve.assert_called_once_with()
        os_mock.path.join.assert_has_calls(
            [mock.call("parent_dir", "samm_cli_file_name.zip"), mock.call("parent_dir", "samm-cli")]
        )
        os_mock.remove.assert_called_once_with("archive_file.zip")
        download_archive_file_mock.assert_called_once_with(
            Const.BASE_PATH.substitute(version_number=Const.JAVA_CLI_VERSION, file_name="samm_cli_file_name.zip"),
            "archive_file.zip",
        )
        extract_archive_mock.assert_called_once_with("archive_file.zip", dest_dir="extracted_files_path")


class TestExtractArchive:
    @mock.patch(f"{BASE_SCRIPT_PATH}.zipfile.ZipFile")
    def test_zip(self, zipfile_zipfile_mock):
        archive_file = "archive.zip"
        dest_dir = "destination_directory"
        archive_mock = mock.MagicMock(name="archive_mock")
        zipfile_zipfile_mock.return_value = archive_mock

        download_module.extract_archive(archive_file, dest_dir)

        zipfile_zipfile_mock.assert_called_once_with(archive_file)
        archive_mock.__enter__.return_value.extractall.assert_called_once_with(dest_dir)

    @mock.patch(f"{BASE_SCRIPT_PATH}.tarfile.open")
    def test_tar_gz(self, tarfile_open_mock):
        archive_file = "archive.tar.gz"
        dest_dir = "destination_directory"
        archive_mock = mock.MagicMock(name="archive_mock")
        tarfile_open_mock.return_value = archive_mock

        download_module.extract_archive(archive_file, dest_dir)

        tarfile_open_mock.assert_called_once_with(archive_file, mode="r:gz")
        archive_mock.__enter__.return_value.extractall.assert_called_once_with(dest_dir)

    def test_extract_unsupported_format(self):
        archive_file = "archive.rar"
        dest_dir = "destination_directory"

        with pytest.raises(ValueError, match=f"Unsupported archive format: {archive_file}"):
            download_module.extract_archive(archive_file, dest_dir)
