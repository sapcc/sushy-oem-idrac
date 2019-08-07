# Copyright 2017 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import mock

from sushy.resources.manager import manager
from sushy.tests.unit import base


class MainTestCase(base.TestCase):

    def setUp(self):
        super(MainTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('sushy_oem_dellemc/tests/unit/json_samples/'
                  'manager.json') as f:
            self.conn.get.return_value.json.return_value = json.load(f)
        self.manager = manager.Manager(self.conn, '/redfish/v1/Managers/BMC',
                                       redfish_version='1.0.2')

    def test_oem_vendors(self):
        oem = self.manager.get_oem_extension('Dell')

        self.assertEqual(
            '/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager'
            '.ImportSystemConfiguration',
            oem.import_system_configuration_uri)
