import os
from http.client import HTTPException
from os import path

import pytest

from loader.core.client import run_requests, check_status
from loader.core.files import file_to_url, write_to_file, \
    convert_page, save_page_data

TEST_URL = 'https://hexlet.io/courses'
TEST_PATH = '/var/tmp'
TEST_PATH_HTML = '/var/tmp/hexlet-io-courses.html'


def test_url_status():
    response = run_requests(TEST_URL)
    assert response.status_code == 200, 'web site is not ok'


def test_match_file_path():
    response = run_requests(TEST_URL)
    file_name = file_to_url(TEST_URL)
    file_path = write_to_file(response.text, file_name=file_name,
                              file_dir=TEST_PATH)
    assert file_path == TEST_PATH_HTML, 'paths do not match'


def test_save_html_file():
    file_name = file_to_url(TEST_URL)
    response = run_requests(TEST_URL)
    path_to_file = path.join(TEST_PATH, file_name)
    edited_html, page_data = convert_page(response.text, path_to_file,
                                          TEST_URL)
    save_page_data(page_data)
    path_to_resource_file = f'{path_to_file}_files'
    created_files = os.listdir(path_to_resource_file)
    assert len(created_files) >= 1, 'folder is empty'


def test_cant_create_dir():
    with pytest.raises(OSError):
        response = run_requests(TEST_URL)
        write_to_file(response.text, file_name='test',
                      file_dir='/../foo')


def test_cant_create_file():
    with pytest.raises(OSError):
        response = run_requests(TEST_URL)
        write_to_file(response.text, file_name='/../foo',
                      file_dir=TEST_PATH)


@pytest.mark.parametrize("status", ['400, 500, 404, 503'])
def test_error_status_code(status):
    with pytest.raises(HTTPException):
        check_status(404)


def test_no_error_status_code(status=200):
    assert status == check_status(status)
