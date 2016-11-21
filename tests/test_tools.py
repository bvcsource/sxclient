# Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
# License: Apache 2.0, see LICENSE for more details.

# encoding: utf-8

from __future__ import unicode_literals

import pytest

from sxclient.tools import generate_blocks
from sxclient.tools.string_helpers import toutf8, tobytes


@pytest.mark.parametrize('size, uuid, content, result', [
    (
        10, b'xyz', b'ala',
        [('b8eaaa62670ba224f925d43e283e9cd311fa42d4', b'ala\0\0\0\0\0\0\0')]
    ),
    (
        3, b'xyz', b'ala',
        [('16be3533ed6b45db3a82ea24ced867e432d7415e', b'ala')]
    ),
    (
        3, b'xyz', b'ala ma kota',
        [
            ('16be3533ed6b45db3a82ea24ced867e432d7415e', b'ala'),
            ('f7e826fe267e2495bb6bb4dccce4ad64ae66ee4c', b' ma'),
            ('53688103333d804d733d6aec526611bbb086fe02', b' ko'),
            ('afdafa81896f7b380c5603ac07125e3108d6844a', b'ta\0')
        ]
    )
])
def test_generate_blocks(size, uuid, content, result):
    assert list(generate_blocks(size, uuid, content)) == result


def test_toutf8():
    assert toutf8('foo') == 'foo'
    assert toutf8(b'foo') == 'foo'
    assert toutf8('żółć') == 'żółć'
    assert toutf8('żółć'.encode('utf-8')) == 'żółć'
    with pytest.raises(TypeError):
        toutf8(42)


def test_tobytes():
    assert tobytes('foo') == b'foo'
    assert tobytes(b'foo') == b'foo'
    assert tobytes('żółć') == 'żółć'.encode('utf-8')
    assert tobytes('żółć'.encode('utf-8')) == 'żółć'.encode('utf-8')
    with pytest.raises(TypeError):
        tobytes(42)
