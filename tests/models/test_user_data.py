# Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
# License: Apache 2.0, see LICENSE for more details.

from __future__ import unicode_literals

import pytest

from sxclient import UserData


@pytest.mark.parametrize('credentials', [
    (u'foo', u'bar', u'baz'),
    (b'foo', b'bar', b'baz'),
    (b'foo', u'bar', b'baz'),
])
def test_from_userpass_pair(credentials):
    expected = (
        b'\x0b\xee\xc7\xb5\xea?\x0f\xdb\xc9]\r\xd4\x7f<[\xc2u\xda\x8a3' +
        b'|T8\xa2\xd5\xa6\xf1\x08\xb6%\x82\x15\x9d\xbc\xbd\xb7g\x17\xa0\xfc' +
        b'\x00\x00'
    )
    user_data = UserData.from_userpass_pair(*credentials)
    assert user_data.key == expected
