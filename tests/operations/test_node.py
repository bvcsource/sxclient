# Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
# License: Apache 2.0, see LICENSE for more details.

from __future__ import unicode_literals


class TestNode(object):
    def test_list(self, sx_controller):
        response = sx_controller.listNodes.json_call()
        host = sx_controller.cluster.host
        assert host in response['nodeList']

    def test_get_status(self, sx_controller):
        host = sx_controller.cluster.host
        response = sx_controller.getNodeStatus.json_call(host)
        expected_keys = {
            'osRelease', 'fsTotalBlocks', 'memTotal', 'UUID', 'nodeDir',
            'fsAvailBlocks', 'osEndianness', 'storageUsed', 'heal',
            'hashFSVersion', 'libsxclientVersion', 'osArch', 'utcTime',
            'storageAllocated', 'address', 'osType', 'cores', 'osVersion',
            'fsBlockSize', 'internalAddress', 'localTime'
        }
        assert expected_keys <= set(response.keys())
