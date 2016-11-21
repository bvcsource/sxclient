# Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
# License: Apache 2.0, see LICENSE for more details.

from __future__ import unicode_literals


class TestUser(object):
    # NOTE: create and delete user is already tested in conftest.

    def test_list(self, sx_controller, sx_uname, sx_test_uname):
        response = sx_controller.listUsers.json_call()
        assert response[sx_uname]['admin']
        assert not response[sx_test_uname]['admin']

    def test_who_am_i(self, sx_controller, sx_uname):
        response = sx_controller.whoAmI.json_call()
        assert response[sx_uname]['admin']

    def test_modify(
        self, request, sx_controller, sx_test_uname, random_hex_string
    ):
        def finalizer():
            sx_controller.modifyUser.json_call(
                sx_test_uname, desc=''
            )
        request.addfinalizer(finalizer)

        sx_controller.modifyUser.json_call(
            sx_test_uname, desc=random_hex_string
        )
        response = sx_controller.listUsers.json_call()
        assert response[sx_test_uname]['userDesc'] == random_hex_string
