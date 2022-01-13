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

from sushy import exceptions
from sushy.resources import base

from sushy_oem_idrac.resources.manager import constants as mgr_cons

LOG = logging.getLogger(__name__)


class ForceActionField(base.CompositeField):
    target_uri = base.Field('target', required=True)
    allowed_values = base.Field('Force@Redfish.AllowableValues',
                                adapter=list)


class ActionsField(base.CompositeField):
    reset_idrac = ForceActionField('#DelliDRACCardService.iDRACReset')


class DelliDRACCardService(base.ResourceBase):

    _actions = ActionsField('Actions')
    identity = base.Field('Id', required=True)

    def __init__(self, connector, identity, redfish_version=None,
                 registries=None):
        """A class representing a DelliDRACCardService.

        :param connector: A Connector instance
        :param identity: The identity of the DelliDRACCardService resource
        :param redfish_version: The version of Redfish. Used to construct
            the object according to schema of the given version.
        :param registries: Dict of Redfish Message Registry objects to be
            used in any resource that needs registries to parse messages.
        """
        super(DelliDRACCardService, self).__init__(
            connector, identity, redfish_version, registries)

    def get_allowed_reset_idrac_values(self):
        """Get the allowed values for resetting the idrac.

        :returns: A set of allowed values.
        """
        reset_action = self._actions.reset_idrac

        if not reset_action.allowed_values:
            LOG.warning('Could not figure out the allowed values for the '
                        'reset idrac action for %s', self.identity)
            return set(mgr_cons.ResetType)

        return {v for v in mgr_cons.ResetType
                if v.value in reset_action.allowed_values}

    def reset_idrac(self):
        """Reset the iDRAC.

        """
        reset_type = mgr_cons.ResetType.GRACEFUL
        valid_resets = self.get_allowed_reset_idrac_values()
        if reset_type not in valid_resets:
            raise exceptions.InvalidParameterValueError(
                parameter='value', value=reset_type, valid_values=valid_resets)
        target_uri = self._actions.reset_idrac.target_uri
        payload = {"Force": reset_type.value}
        LOG.debug('Resetting the iDRAC %s ...', self.identity)
        self._conn.post(target_uri, data=payload)
        LOG.info('The iDRAC %s is being reset', self.identity)
