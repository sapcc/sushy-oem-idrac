# Copyright (c) 2020-2021 Dell Inc. or its subsidiaries.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging

from sushy.resources import base
from sushy.resources import common

LOG = logging.getLogger(__name__)


class ActionsField(base.CompositeField):
    remote_service_api_status = common.ActionField(
        "#DellLCService.GetRemoteServicesAPIStatus")


class DellLCService(base.ResourceBase):

    _actions = ActionsField('Actions')
    _IDRAC_READY_STATUS_CODE = 200
    _IDRAC_READY_STATUS = 'Ready'
    identity = base.Field('Id', required=True)

    def __init__(self, connector, identity, redfish_version=None,
                 registries=None):
        """A class representing a DellLCService.

        :param connector: A Connector instance
        :param identity: The identity of the DellLCService resource
        :param redfish_version: The version of Redfish. Used to construct
            the object according to schema of the given version.
        :param registries: Dict of Redfish Message Registry objects to be
            used in any resource that needs registries to parse messages.
        """
        super(DellLCService, self).__init__(
            connector, identity, redfish_version, registries)

    def is_idrac_ready(self):
        """Indicates if the iDRAC is ready to accept commands.

        :returns: A boolean value True/False based on remote service api status
            response.
        """
        target_uri = self._actions.remote_service_api_status.target_uri
        LOG.debug('Checking to see if the iDRAC is ready...')
        idrac_ready_response = self._conn.post(target_uri, data={})
        if idrac_ready_response.status_code != self._IDRAC_READY_STATUS_CODE:
            return False
        data = idrac_ready_response.json()
        lc_status = data['LCStatus']
        return lc_status == self._IDRAC_READY_STATUS
