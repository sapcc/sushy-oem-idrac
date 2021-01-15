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
import time

import sushy
from sushy.resources import base
from sushy.resources import common
from sushy.resources.oem import base as oem_base
from sushy import utils as sushy_utils

from sushy_oem_idrac import asynchronous
from sushy_oem_idrac import constants
from sushy_oem_idrac.resources.manager import constants as mgr_cons
from sushy_oem_idrac.resources.manager import idrac_card_service
from sushy_oem_idrac.resources.manager import job_collection
from sushy_oem_idrac.resources.manager import job_service
from sushy_oem_idrac.resources.manager import lifecycle_service
from sushy_oem_idrac.resources.manager import mappings as mgr_maps
from sushy_oem_idrac import utils

LOG = logging.getLogger(__name__)

# System Configuration Tag Constant
_SYSTEM_CONFIG_TAG = "SystemConfiguration"

# Response Code Constant
_RESPONSE_OK_CODE = 200


class SharedParameters(base.CompositeField):
    allowed_target_values = base.Field('Target@Redfish.AllowableValues')


class ExportActionField(common.ActionField):
    shared_parameters = SharedParameters('ShareParameters')


class DellManagerActionsField(base.CompositeField):
    import_system_configuration = common.ActionField(
        lambda key, **kwargs: key.endswith(
            '#OemManager.ImportSystemConfiguration'))

    export_system_configuration = ExportActionField(
        lambda key, **kwargs: key.endswith(
            '#OemManager.ExportSystemConfiguration'))


class DellManagerExtension(oem_base.OEMResourceBase):

    _actions = DellManagerActionsField('Actions')

    ACTION_DATA = {
        'ShareParameters': {
            'Target': 'ALL'
        },
        'ImportBuffer': None
    }

    # NOTE(etingof): iDRAC job would fail if this XML has
    # insignificant whitespaces

    IDRAC_CONFIG_CD = """\
<SystemConfiguration>\
<Component FQDD="%s">\
<Attribute Name="ServerBoot.1#BootOnce">\
%s\
</Attribute>\
<Attribute Name="ServerBoot.1#FirstBootDevice">\
VCD-DVD\
</Attribute>\
</Component>\
</SystemConfiguration>\
"""

    IDRAC_CONFIG_FLOPPY = """\
<SystemConfiguration>\
<Component FQDD="%s">\
<Attribute Name="ServerBoot.1#BootOnce">\
%s\
</Attribute>\
<Attribute Name="ServerBoot.1#FirstBootDevice">\
VFDD\
</Attribute>\
</Component>\
</SystemConfiguration>\
"""

    IDRAC_MEDIA_TYPES = {
        sushy.VIRTUAL_MEDIA_FLOPPY: IDRAC_CONFIG_FLOPPY,
        sushy.VIRTUAL_MEDIA_CD: IDRAC_CONFIG_CD
    }

    RETRY_COUNT = 10
    RETRY_DELAY = 15

    @property
    def import_system_configuration_uri(self):
        return self._actions.import_system_configuration.target_uri

    @property
    def export_system_configuration_uri(self):
        return self._actions.export_system_configuration.target_uri

    @property
    @sushy_utils.cache_it
    def idrac_card_service(self):
        """Property to reference `DelliDRACCardService` instance of this manager.

        """
        path = sushy_utils.get_sub_resource_path_by(
            self, ["Links", "Oem", "Dell", "DelliDRACCardService"],
            is_collection=False)

        return idrac_card_service.DelliDRACCardService(
            self._conn, path, self.redfish_version, self.registries)

    @property
    @sushy_utils.cache_it
    def lifecycle_service(self):
        """Property to reference `DellLCService` instance of this manager.

        """
        path = sushy_utils.get_sub_resource_path_by(
            self, ["Links", "Oem", "Dell", "DellLCService"],
            is_collection=False)

        return lifecycle_service.DellLCService(
            self._conn, path, self.redfish_version, self.registries)

    @property
    @sushy_utils.cache_it
    def job_service(self):
        """Property to reference `DellJobService` instance of this manager.

        """
        path = sushy_utils.get_sub_resource_path_by(
            self, ["Links", "Oem", "Dell", "DellJobService"],
            is_collection=False)

        return job_service.DellJobService(
            self._conn, path, self.redfish_version, self.registries)

    @property
    @sushy_utils.cache_it
    def job_collection(self):
        """Property to reference `DellJobService` instance of this manager.

        """
        path = sushy_utils.get_sub_resource_path_by(
            self, ["Links", "Oem", "Dell", "Jobs"], is_collection=False)

        return job_collection.DellJobCollection(
            self._conn, path, self.redfish_version, self.registries)

    def set_virtual_boot_device(self, device, persistent=False,
                                manager=None, system=None):
        """Set boot device for a node.

        Dell iDRAC Redfish implementation does not support setting
        boot device to virtual media via standard Redfish means.
        However, this still can be done via an OEM extension.

        :param device: Boot device. Values are vendor-specific.
        :param persistent: Whether to set next-boot, or make the change
            permanent. Default: False.
        :raises: InvalidParameterValue if Dell OEM extension can't
            be used.
        :raises: ExtensionError on failure to perform requested
            operation.
        """
        try:
            idrac_media = self.IDRAC_MEDIA_TYPES[device]

        except KeyError:
            raise sushy.exceptions.InvalidParameterValue(
                error='Unknown or unsupported device %s' % device)

        idrac_media = idrac_media % (
            manager.identity, 'Disabled' if persistent else 'Enabled')

        action_data = dict(self.ACTION_DATA, ImportBuffer=idrac_media)

        # TODO(etingof): figure out if on-time or persistent boot can at
        # all be implemented via this OEM call

        attempts = self.RETRY_COUNT
        rebooted = False

        while True:
            try:
                response = asynchronous.http_call(
                    self._conn, 'post',
                    self.import_system_configuration_uri,
                    data=action_data,
                    sushy_task_poll_period=1)

                LOG.info("Set boot device to %(device)s via "
                         "Dell OEM magic spell (%(retries)d "
                         "retries)", {'device': device,
                                      'retries': self.RETRY_COUNT - attempts})

                return response

            except (sushy.exceptions.ServerSideError,
                    sushy.exceptions.BadRequestError) as exc:
                LOG.warning(
                    'Dell OEM set boot device failed (attempts left '
                    '%d): %s', attempts, exc)

                errors = exc.body and exc.body.get(
                    '@Message.ExtendedInfo') or []

                for error in errors:
                    message_id = error.get('MessageId')

                    LOG.warning('iDRAC error: %s',
                                error.get('Message', 'Unknown error'))

                    if message_id == constants.IDRAC_CONFIG_PENDING:
                        if not rebooted:
                            LOG.warning(
                                'Let\'s try to turn it off and on again... '
                                'This may consume one-time boot settings if '
                                'set previously!')
                            utils.reboot_system(system)
                            rebooted = True
                            break

                    elif message_id == constants.IDRAC_JOB_RUNNING:
                        pass

                else:
                    time.sleep(self.RETRY_DELAY)

                if not attempts:
                    LOG.error('Too many (%d) retries, bailing '
                              'out.', self.RETRY_COUNT)
                    raise

                attempts -= 1

    def get_allowed_export_target_values(self):
        """Get the allowed targets of export system configuration.

        :returns: A set of allowed values.
        """
        export_action = self._actions.export_system_configuration
        allowed_values = export_action.shared_parameters.allowed_target_values

        return set([mgr_maps.EXPORT_CONFIG_VALUE_MAP[value] for value in
                    set(mgr_maps.EXPORT_CONFIG_VALUE_MAP).
                    intersection(allowed_values)])

    def _export_system_configuration(self, target):
        """Export system configuration.

        It exports system configuration for specified target
        like NIC, BIOS, RAID.

        :param target: Component of the system to export the
            configuration from. Can be the entire system.
            Valid values can be gotten from
            `get_allowed_export_target_values`.
        :returns: a response object containing configuration details for
            the specified target.
        :raises: InvalidParameterValueError on invalid target.
        :raises: ExtensionError on failure to perform requested
            operation
        """
        valid_allowed_targets = self.get_allowed_export_target_values()
        if target not in valid_allowed_targets:
            raise sushy.exceptions.InvalidParameterValueError(
                parameter='target', value=target,
                valid_values=valid_allowed_targets)

        target = mgr_maps.EXPORT_CONFIG_VALUE_MAP_REV[target]

        action_data = {
            'ShareParameters': {
                'Target': target
            },
            'ExportFormat': "JSON"
        }

        try:
            response = asynchronous.http_call(
                self._conn,
                'post',
                self.export_system_configuration_uri,
                data=action_data)

            LOG.info("Successfully exported system configuration "
                     "for %(target)s", {'target': target})

            return response

        except (sushy.exceptions.ExtensionError,
                sushy.exceptions.InvalidParameterValueError) as exc:
            LOG.error('Dell OEM export system configuration failed : %s', exc)
            raise

    def get_pxe_port_macs_bios(self, ethernet_interfaces_mac):
        """Get a list of pxe port MAC addresses for BIOS.

        :param ethernet_interfaces_mac: Dictionary of ethernet interfaces.
        :returns: List of pxe port MAC addresses.
        :raises: ExtensionError on failure to perform requested operation.
        """
        pxe_port_macs = []
        # Get NIC configuration
        nic_settings = self._export_system_configuration(
            target=mgr_cons.EXPORT_TARGET_NIC)

        if nic_settings.status_code != _RESPONSE_OK_CODE:
            error = (('An error occurred when attempting to export '
                     'the system configuration. Status code: %(code), '
                      'Error details: %(err)'),
                     {'code': nic_settings.status_code,
                      'err': nic_settings.__dict__})
            LOG.error(error)
            raise sushy.exceptions.ExtensionError(error=error)
        # Parse the exported system configuration for the NIC
        # ports that are set to PXE boot
        json_data = nic_settings.json()
        if _SYSTEM_CONFIG_TAG in json_data.keys():
            for root in json_data[_SYSTEM_CONFIG_TAG]['Components']:
                nic_id = root['FQDD']
                for child in root['Attributes']:
                    if child.get('Name') == "LegacyBootProto":
                        if child['Value'] == "PXE":
                            mac_address = ethernet_interfaces_mac[nic_id]
                            pxe_port_macs.append(mac_address)
            return pxe_port_macs

        else:
            error = (('Failed to get system configuration from response'))
            LOG.error(error)
            raise sushy.exceptions.ExtensionError(error=error)


def get_extension(*args, **kwargs):
    return DellManagerExtension
