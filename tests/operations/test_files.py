# Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
# License: Apache 2.0, see LICENSE for more details.

from __future__ import unicode_literals

import io
import random
import string

import pytest
import six
from six.moves import range

from sxclient import SXClusterNotFound
from sxclient.tools import SXFileUploader, SXFileDownloader, SXFileCat


@pytest.fixture(scope='session')
def uploader(sx_controller):
    # We lower MAX_BATCH_SIZE so that we don't use too much memory.
    # Plus that way it is faster (smaller HTTP requests).
    uploader = SXFileUploader(sx_controller)
    uploader.MAX_BATCH_SIZE = 2**15
    return uploader


# Note that these sizes are taken in such a way that one is < MAX_BATCH_SIZE
# and the other is > MAX_BATCH_SIZE. This makes uploader to either not use or
# use multiple HTTP requests (i.e. "add chunk" request is used or not)
@pytest.fixture(params=[0, 2**13+357, 2**16+115, 2**20*4])
def stream(request):
    size = request.param
    data = ''.join(
        random.choice(string.ascii_letters) for _ in range(size)
    ).encode('utf-8')
    stream = io.BytesIO(data)
    stream.size = size
    return stream


@pytest.fixture
def fname():
    return 'test/file.' + ''.join(
        random.choice(string.ascii_letters) for _ in range(20)
    )


class TestFiles(object):
    def test_file_cat(
        self, sx_controller, uploader, sx_volume, stream, fname,
        random_hex_string
    ):
        fmeta = {'TestMeta': random_hex_string}
        uploader.upload_stream(
            sx_volume, stream.size, fname, stream, meta=fmeta
        )

        stream.seek(0)
        local_data = stream.read()

        with SXFileCat(sx_controller) as downloader:
            remote_data = downloader.get_file_content(sx_volume, fname)

        assert remote_data == local_data

        response = sx_controller.listFiles.json_call(sx_volume, recursive=True)
        assert '/' + fname in response['fileList']

        sx_controller.deleteFile.json_call(sx_volume, fname)
        with pytest.raises(SXClusterNotFound):
            sx_controller.getFile.call(sx_volume, fname)

    def test_file_upload_download(
        self, sx_controller, uploader, sx_volume, stream, fname,
        random_hex_string
    ):
        fmeta = {'TestMeta': random_hex_string}
        uploader.upload_stream(
            sx_volume, stream.size, fname, stream, meta=fmeta
        )

        stream.seek(0)
        local_data = stream.read()

        with SXFileDownloader(sx_controller) as downloader:
            remote_data = downloader.get_file_content(sx_volume, fname)
            stats = downloader.clean_cached_files(
                volume=sx_volume,
                file_name=fname
            )
            assert stats['found'] == stats['deleted']

        assert remote_data == local_data

        response = sx_controller.listFiles.json_call(sx_volume, recursive=True)
        assert '/' + fname in response['fileList']

        sx_controller.deleteFile.json_call(sx_volume, fname)
        with pytest.raises(SXClusterNotFound):
            sx_controller.getFile.call(sx_volume, fname)

    def test_revisions(
        self, sx_volume, uploader, sx_controller, fname
    ):
        first_content = b'version 1'
        stream = io.BytesIO(first_content)
        uploader.upload_stream(sx_volume, len(first_content), fname, stream)

        second_content = b'version 2'
        stream = io.BytesIO(second_content)
        uploader.upload_stream(sx_volume, len(second_content), fname, stream)

        response = sx_controller.listFileRevisions.json_call(sx_volume, fname)
        revisions = sorted(
            six.iteritems(response['fileRevisions']),
            key=lambda x: x[0]
        )

        with SXFileDownloader(sx_controller) as downloader:
            first_file = downloader.get_file_content(
                sx_volume, fname, revision=revisions[0][0]
            )
            assert first_file == first_content

            second_file = downloader.get_file_content(
                sx_volume, fname, revision=revisions[1][0]
            )
            assert second_file == second_content
            downloader.clean_cached_files(
                volume=sx_volume,
                file_name=fname
            )
