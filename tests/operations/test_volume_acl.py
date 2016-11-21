# Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
# License: Apache 2.0, see LICENSE for more details.

from __future__ import unicode_literals


class TestVolumeACL(object):
    def test_get(self, sx_controller, sx_volume, sx_uname):
        response = sx_controller.getVolumeACL.json_call(sx_volume)
        assert response[sx_uname] == ['read', 'write', 'manager', 'owner']

    def test_update(self, request, sx_controller, sx_volume, sx_test_uname):
        def finalizer():
            try:
                sx_controller.updateVolumeACL.json_call(
                    sx_volume, {'revoke-read': [sx_test_uname]}
                )
            except Exception:
                pass
        request.addfinalizer(finalizer)

        response = sx_controller.updateVolumeACL.json_call(
            sx_volume, {'grant-read': [sx_test_uname]}
        )
        assert response['requestStatus'] == 'OK'

        response = sx_controller.getVolumeACL.json_call(sx_volume)
        assert response[sx_test_uname] == ['read']

    def test_set(self, request, sx_controller, sx_volume, sx_test_uname):
        def finalizer():
            try:
                sx_controller.updateVolumeACL.json_call(
                    sx_volume, {'revoke-write': [sx_test_uname]}
                )
            except Exception:
                pass
        request.addfinalizer(finalizer)

        response = sx_controller.setVolumeACL.json_call(
            sx_volume, {sx_test_uname: ['write']}
        )
        assert response['requestStatus'] == 'OK'

        response = sx_controller.getVolumeACL.json_call(sx_volume)
        assert response[sx_test_uname] == ['write']
