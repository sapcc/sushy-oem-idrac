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

import sushy
from sushy.resources import base
from sushy.resources import common
from sushy.resources.oem import base as oem_base

LOG = logging.getLogger(__name__)


class DellManagerActionsField(base.CompositeField):
    import_system_configuration = common.ActionField(
        lambda key, **kwargs: key.endswith(
            '#OemManager.ImportSystemConfiguration'))


class DellManagerExtension(oem_base.OEMResourceBase):

    _actions = DellManagerActionsField('Actions')

    MAGIC_CD_SAUCE = """\
    <SystemConfiguration>\
      <Component FQDD="iDRAC.Embedded.1">\
        <Attribute Name="ServerBoot.1#BootOnce">\
          Enabled\
        </Attribute>\
        <Attribute Name="ServerBoot.1#FirstBootDevice">\
          VCD-DVD\
        </Attribute>\
      </Component>\
    </SystemConfiguration>\
    """

    MAGIC_FLOPPY_SAUCE = """\
        <SystemConfiguration>\
          <Component FQDD="iDRAC.Embedded.1">\
            <Attribute Name="ServerBoot.1#BootOnce">\
              Enabled\
            </Attribute>\
            <Attribute Name="ServerBoot.1#FirstBootDevice">\
              VFDD\
            </Attribute>\
          </Component>\
        </SystemConfiguration>\
    """

    MAGIC_SAUCER = {
        sushy.VIRTUAL_MEDIA_FLOPPY: MAGIC_FLOPPY_SAUCE,
        sushy.VIRTUAL_MEDIA_CD: MAGIC_CD_SAUCE
    }

    @property
    def import_system_configuration_uri(self):
        return self._actions.import_system_configuration.target_uri

    def set_virtual_boot_device(self, device, persistent=False):
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
            operation
        """
        try:
            magic_saucer = self.MAGIC_SAUCER[device]

        except KeyError:
            raise sushy.exceptions.InvalidParameterValue(
                error='Unknown or unsupported device %s' % device)

        # TODO (etingof): figure out if on-time or persistent boot can at
        # all be implemented via this OEM call

        response = self._conn.post(
            self.import_system_configuration_uri, data=magic_saucer)

        if response.status_code != 202:
            raise sushy.exceptions.ExtensionError(
                error='Dell OEM action ImportSystemConfiguration fails '
                      'with code %s' % response.status_code)

        LOG.info("Set boot device to %(device)s via "
                 "Dell OEM magic spell", {'device': device})

        # TODO(etingof): extract iDRAC task ID which looks like r"JID_.+?,"

        # TODO(etingof): poll Redfish TaskService to see when task is completed


def get_extension(*args, **kwargs):
    return DellManagerExtension
