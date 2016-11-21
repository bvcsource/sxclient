# Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
# License: Apache 2.0, see LICENSE for more details.

from __future__ import unicode_literals

import pytest

from sxclient.tools.filters import list_filters, generate_poll_times
from sxclient.defaults import FILTER_NAME_TO_UUID


def test_list_filters():
    filters = list_filters()
    assert filters == sorted(FILTER_NAME_TO_UUID)
    assert 'aes256' in filters


def test_generate_poll_times():
    start, end, steps =  0.5, 2.5, 5
    gen = generate_poll_times(start, end, steps)

    times = [next(gen) for _ in range(10)]
    assert times == sorted(times)
    assert times[0] == start
    assert times[-1] == end
    assert next(gen) == end


@pytest.mark.parametrize('start, end', [
    (1, -1), (-1, 1),
])
def test_generate_poll_times_invalid(start, end):
    with pytest.raises(ValueError):
        list(generate_poll_times(start, end, 2))
