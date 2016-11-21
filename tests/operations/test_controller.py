# Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
# License: Apache 2.0, see LICENSE for more details.

from __future__ import unicode_literals

import pytest

from sxclient.operations import OPERATION_CLASSES


@pytest.mark.parametrize('op_name, op_class', OPERATION_CLASSES.items())
def test_operations_on_controller(sx_controller, op_name, op_class):
    attr_name = op_name[:1].lower() + op_name[1:]
    op_inst = getattr(sx_controller, attr_name)
    assert isinstance(op_inst, op_class)
