# Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
# License: Apache 2.0, see LICENSE for more details.

from __future__ import absolute_import, unicode_literals

from sxclient.operations.volume import ChangeVolumeReplica, ModifyVolume


class TestVolume(object):
    # NOTE: create and delete volume is already tested in conftest

    def test_locate(self, sx_controller, sx_volume, sx_host):
        nodelist_response = sx_controller.listNodes.json_call()
        locate_response = sx_controller.locateVolume.json_call(
            sx_volume, includeMeta=True
        )
        cluster_nodes = set(nodelist_response['nodeList'])
        locate_nodes = set(locate_response['nodeList'])
        assert locate_nodes.issubset(cluster_nodes)
        assert locate_response['volumeMeta'] == {'MyMeta': '00aa00'}

    def test_list(self, sx_controller, sx_volume, sx_uname):
        response = sx_controller.listVolumes.json_call()
        volume = response['volumeList'][sx_volume]

        assert volume['maxRevisions'] == 2
        assert volume['owner'] == sx_uname
        assert volume['replicaCount'] == 1
        assert volume['sizeBytes'] == 10*(2**20)
        assert 'usedSize' in volume

    def test_change_replica(self):
        operation = ChangeVolumeReplica(None, None)
        vol_name = 'foo'
        next_replica = 3

        body = operation._generate_body(vol_name, next_replica)
        query = operation._generate_query_params(vol_name, next_replica)

        assert body == {'next_replica': next_replica}
        assert query.sx_verb == 'JOB_PUT'
        assert query.path_items == [vol_name]
        assert query.dict_params == {'o': 'replica'}
        assert not query.bool_params


class TestModifyVolume(object):
    def test_modify_meta(self, sx_controller, sx_volume, random_hex_string):
        response = sx_controller.modifyVolume.json_call(
            sx_volume, customVolumeMeta={'ModifyTest': random_hex_string}
        )
        assert response['requestStatus'] == 'OK'

        response = sx_controller.locateVolume.json_call(
            sx_volume, includeMeta=True, includeCustomMeta=True
        )
        assert response['customVolumeMeta']['ModifyTest'] == random_hex_string

    def test_modify_rename(self):
        modifyVolume = ModifyVolume(None, None)
        vol_name = 'foo'
        new_name = 'bar'

        body = modifyVolume._generate_body(vol_name, newName=new_name)

        modifyVolume._generate_query_params(vol_name, newName=new_name)
        assert body == {'name': new_name}
