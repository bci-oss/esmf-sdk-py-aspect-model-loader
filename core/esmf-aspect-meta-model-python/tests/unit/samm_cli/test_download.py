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


class TestArchiveFileDownload:
    @mock.patch(f"{BASE_SCRIPT_PATH}.requests.get")
    @mock.patch(f"{BASE_SCRIPT_PATH}.print")
    @mock.patch(f"{BASE_SCRIPT_PATH}.open")
    def test_download_archive_file_no_content(self, open_mock, print_mock, requests_get_mock):
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
    def test_download_archive_file(self, open_mock, print_mock, requests_get_mock, sys_stdout_mock):
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
    def test_download_samm_cli_error(self, get_samm_cli_file_name_mock, print_mock):
        test_error = NotImplementedError("exception_message")
        get_samm_cli_file_name_mock.side_effect = test_error

        result = download_samm_cli()

        assert result is None
        get_samm_cli_file_name_mock.assert_called_once()
        print_mock.assert_called_once_with(test_error)

    @mock.patch(f"{BASE_SCRIPT_PATH}.zipfile")
    @mock.patch(f"{BASE_SCRIPT_PATH}.download_archive_file")
    @mock.patch(f"{BASE_SCRIPT_PATH}.os")
    @mock.patch(f"{BASE_SCRIPT_PATH}.Path")
    @mock.patch(f"{BASE_SCRIPT_PATH}.print")
    @mock.patch(f"{BASE_SCRIPT_PATH}.get_samm_cli_file_name")
    def test_download_samm_cli(
        self,
        get_samm_cli_file_name_mock,
        print_mock,
        path_mock,
        os_mock,
        download_archive_file_mock,
        zipfile_mock,
    ):
        get_samm_cli_file_name_mock.return_value = "samm_cli_file_name"
        path_mock.return_value = path_mock
        path_mock.resolve.return_value = path_mock
        path_mock.parents = ["parent_dir"]
        os_mock.path.join.side_effect = ("archive_file", "extracted_files_path")
        archive_mock = mock.MagicMock(name="archive_mock")
        archive_mock.namelist.return_value = ["file_1", "file_2"]
        zipfile_mock.ZipFile.return_value = archive_mock
        result = download_samm_cli()

        assert result is None
        get_samm_cli_file_name_mock.assert_called_once()
        print_mock.assert_has_calls(
            [
                mock.call("Start downloading SAMM CLI samm_cli_file_name"),
                mock.call("\nSAMM CLI archive file downloaded"),
                mock.call("Start extracting files"),
                mock.call("Done extracting files"),
                mock.call("Deleting SAMM CLI archive file"),
            ]
        )
        path_mock.assert_called_once_with(download_module.__file__)
        path_mock.resolve.assert_called_once()
        os_mock.path.join.assert_has_calls(
            [mock.call("parent_dir", "samm_cli_file_name"), mock.call("parent_dir", "samm-cli")]
        )
        os_mock.remove.assert_called_once()
        download_archive_file_mock.assert_called_once_with(
            Const.BASE_PATH.substitute(version_number=Const.JAVA_CLI_VERSION, file_name="samm_cli_file_name"),
            "archive_file",
        )
        zipfile_mock.ZipFile.assert_called_once_with("archive_file")
        archive_mock.namelist.assert_called_once()
        archive_mock.extract.has_calls(
            [
                mock.call("file_1", "extracted_files_path"),
                mock.call("file_2", "extracted_files_path"),
            ]
        )
        archive_mock.close.assert_called_once()
