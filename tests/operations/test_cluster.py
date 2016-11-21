# Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
# License: Apache 2.0, see LICENSE for more details.

from __future__ import unicode_literals


class TestCluster(object):
    def test_get_status(self, sx_controller):
        expected_keys = {
            'clusterAuth', 'distributionModels', 'distributionVersion',
            'distributionChecksum', 'operatingMode', 'distributionUUID'
        }
        response = sx_controller.getClusterStatus.json_call()

        assert expected_keys.issubset(response['clusterStatus'])

    def test_set_get_meta(self, sx_controller, random_hex_string):
        key = '__test_meta__'
        sx_controller.setClusterMetadata.json_call(
            {key: random_hex_string}
        )

        response = sx_controller.getClusterMetadata.json_call()
        assert response['clusterMeta'][key] == random_hex_string
