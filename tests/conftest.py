# Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
# License: Apache 2.0, see LICENSE for more details.

from __future__ import unicode_literals

import codecs
import random
import string

import pytest
from six.moves import range

import sxclient

MB = 2**20
MAX_VOLUME_SIZE = 10*MB


def pytest_addoption(parser):
    parser.addoption(
        '--sxcl-domain',
        dest='cluster_domain',
        required=True,
        help='Domain of the cluster'
    )
    parser.addoption(
        '--sxkey-path',
        required=True,
        dest='key_path',
        help='Path to the file with user\'s authentication key'
    )


@pytest.fixture(scope='session')
def sx_host(request):
    return request.config.getoption('cluster_domain')


@pytest.fixture(scope='session')
def sx_cluster(sx_host):
    return sxclient.Cluster(sx_host, verify_ssl_cert=False, is_secure=False)


@pytest.fixture(scope='session')
def sx_user_data(request):
    path = request.config.getoption('key_path')
    user_name = 'admin'
    user_data = sxclient.UserData.from_key_path(path)
    user_data.user_name = user_name
    return user_data


@pytest.fixture(scope='session')
def sx_uname(sx_user_data):
    return sx_user_data.user_name


@pytest.fixture(scope='session')
def sx_controller(request, sx_cluster, sx_user_data, sx_volume):
    controller = sxclient.SXController(sx_cluster, sx_user_data)

    def create_volume():
        controller.createVolume.call(
            sx_volume, MAX_VOLUME_SIZE, sx_user_data.user_name, 1,
            maxRevisions=2, volumeMeta={'MyMeta': '00aa00'}
        )

    def delete_volume():
        controller.deleteVolume.call(sx_volume, force=True)
    request.addfinalizer(delete_volume)

    try:
        create_volume()
    except sxclient.SXClientException:
        delete_volume()
        create_volume()

    return controller


@pytest.fixture(scope='session')
def sx_test_uname():
    return '__test_user__'


@pytest.fixture(scope='session', autouse=True)
def sx_test_user(request, sx_controller, sx_test_uname):

    def finalizer():
        sx_controller.removeUser.json_call(userName=sx_test_uname)
    request.addfinalizer(finalizer)

    sx_controller.createUser.json_call(
        sx_test_uname, 'normal', '00112233445566778899aabbccddeeff00112233',
        desc=''
    )


@pytest.fixture(scope='session')
def sx_volume():
    return '__volume_for_test__'


ALPHABET = string.ascii_letters + string.digits


@pytest.fixture
def random_hex_string():
    size = random.randint(10, 30)
    string = ''.join(random.choice(ALPHABET) for _ in range(size))
    return codecs.encode(string.encode('utf-8'), 'hex').decode('utf-8')
