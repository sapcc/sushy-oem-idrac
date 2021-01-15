# Copyright 2017 Red Hat, Inc.
# All Rights Reserved.
# Copyright (c) 2020-2021 Dell Inc. or its subsidiaries.
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
from unittest import mock

from oslotest.base import BaseTestCase
import sushy
from sushy.resources.manager import manager

from sushy_oem_idrac.resources.manager import constants as mgr_cons
from sushy_oem_idrac.resources.manager import idrac_card_service as idrac_card
from sushy_oem_idrac.resources.manager import job_collection as jc
from sushy_oem_idrac.resources.manager import job_service as job
from sushy_oem_idrac.resources.manager import lifecycle_service as lifecycle


class ManagerTestCase(BaseTestCase):

    def setUp(self):
        super(ManagerTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('sushy_oem_idrac/tests/unit/json_samples/'
                  'manager.json') as f:
            mock_response = self.conn.get.return_value
            mock_response.json.return_value = json.load(f)
            mock_response.status_code = 200

        mock_response = self.conn.post.return_value
        mock_response.status_code = 202
        mock_response.headers.get.return_value = '1'

        self.manager = manager.Manager(self.conn, '/redfish/v1/Managers/BMC',
                                       redfish_version='1.0.2')

    @mock.patch('sushy.resources.oem.common._global_extn_mgrs_by_resource', {})
    def test_import_system_configuration_uri(self):
        oem = self.manager.get_oem_extension('Dell')

        self.assertEqual(
            '/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager'
            '.ImportSystemConfiguration',
            oem.import_system_configuration_uri)

    @mock.patch('sushy.resources.oem.common._global_extn_mgrs_by_resource', {})
    def test_set_virtual_boot_device_cd(self):
        oem = self.manager.get_oem_extension('Dell')

        oem.set_virtual_boot_device(
            sushy.VIRTUAL_MEDIA_CD, manager=self.manager)

        self.conn.post.assert_called_once_with(
            '/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager'
            '.ImportSystemConfiguration', data=mock.ANY)

    @mock.patch('sushy.resources.oem.common._global_extn_mgrs_by_resource', {})
    def test_get_allowed_export_target_values(self):
        oem = self.manager.get_oem_extension('Dell')
        expected_values = {mgr_cons.EXPORT_TARGET_IDRAC,
                           mgr_cons.EXPORT_TARGET_RAID,
                           mgr_cons.EXPORT_TARGET_ALL,
                           mgr_cons.EXPORT_TARGET_BIOS,
                           mgr_cons.EXPORT_TARGET_NIC}
        allowed_values = oem.get_allowed_export_target_values()
        self.assertEqual(expected_values, allowed_values)

    @mock.patch('sushy.resources.oem.common._global_extn_mgrs_by_resource', {})
    def test_export_system_configuration_uri(self):
        oem = self.manager.get_oem_extension('Dell')

        self.assertEqual(
            '/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager'
            '.ExportSystemConfiguration',
            oem.export_system_configuration_uri)

    @mock.patch('sushy.resources.oem.common._global_extn_mgrs_by_resource', {})
    def test__export_system_configuration(self):
        oem = self.manager.get_oem_extension('Dell')
        oem._export_system_configuration(
            target=mgr_cons.EXPORT_TARGET_ALL)

        self.conn.post.assert_called_once_with(
            '/redfish/v1/Managers/iDRAC.Embedded.1/Actions/Oem/EID_674_Manager'
            '.ExportSystemConfiguration', data={'ShareParameters':
                                                {'Target': 'ALL'},
                                                'ExportFormat': 'JSON'})

    @mock.patch('sushy.resources.oem.common._global_extn_mgrs_by_resource', {})
    def test__export_system_configuration_invalid_target(self):
        oem = self.manager.get_oem_extension('Dell')
        target = "xyz"
        self.assertRaises(sushy.exceptions.InvalidParameterValueError,
                          oem._export_system_configuration, target)

    @mock.patch('sushy.resources.oem.common._global_extn_mgrs_by_resource', {})
    def test_get_pxe_port_macs_bios(self):
        oem = self.manager.get_oem_extension('Dell')
        oem._export_system_configuration = mock.Mock()
        with open('sushy_oem_idrac/tests/unit/json_samples/'
                  'export_configuration_nic_bios.json') as f:
            mock_response = oem._export_system_configuration.return_value
            mock_response.json.return_value = json.load(f)
            mock_response.status_code = 200
        ethernet_interfaces_mac = {'NIC.Integrated.1-4-1': '68:05:CA:AF:AA:C9',
                                   'NIC.Slot.7-2-1': '3C:FD:FE:CD:67:31',
                                   'NIC.Slot.7-1-1': '3C:FD:FE:CD:67:30',
                                   'NIC.Integrated.1-2-1': '68:05:CA:AF:AA:C7',
                                   'NIC.Integrated.1-3-1': '68:05:CA:AF:AA:C8',
                                   'NIC.Integrated.1-1-1': '68:05:CA:AF:AA:C6'}

        self.assertEqual(["68:05:CA:AF:AA:C8"],
                         oem.get_pxe_port_macs_bios(ethernet_interfaces_mac))

    @mock.patch('sushy.resources.oem.common._global_extn_mgrs_by_resource', {})
    def test_get_pxe_port_macs_bios_invalid_system_config_tag(self):
        oem = self.manager.get_oem_extension('Dell')
        oem._export_system_configuration = mock.Mock()
        mock_response = oem._export_system_configuration.return_value
        mock_response.json.return_value = {'Model': 'PowerEdge R7525'}
        mock_response.status_code = 200
        ethernet_interfaces_mac = {'NIC.Integrated.1-4-1': '68:05:CA:AF:AA:C9',
                                   'NIC.Slot.7-2-1': '3C:FD:FE:CD:67:31',
                                   'NIC.Slot.7-1-1': '3C:FD:FE:CD:67:30',
                                   'NIC.Integrated.1-2-1': '68:05:CA:AF:AA:C7',
                                   'NIC.Integrated.1-3-1': '68:05:CA:AF:AA:C8',
                                   'NIC.Integrated.1-1-1': '68:05:CA:AF:AA:C6'}

        self.assertRaises(sushy.exceptions.ExtensionError,
                          oem.get_pxe_port_macs_bios, ethernet_interfaces_mac)

    @mock.patch('sushy.resources.oem.common._global_extn_mgrs_by_resource', {})
    def test_get_pxe_port_macs_bios_invalid_response(self):
        oem = self.manager.get_oem_extension('Dell')
        oem._export_system_configuration = mock.Mock()
        mock_response = oem._export_system_configuration.return_value
        mock_response.status_code = 204
        ethernet_interfaces_mac = {'NIC.Integrated.1-4-1': '68:05:CA:AF:AA:C9',
                                   'NIC.Slot.7-2-1': '3C:FD:FE:CD:67:31',
                                   'NIC.Slot.7-1-1': '3C:FD:FE:CD:67:30',
                                   'NIC.Integrated.1-2-1': '68:05:CA:AF:AA:C7',
                                   'NIC.Integrated.1-3-1': '68:05:CA:AF:AA:C8',
                                   'NIC.Integrated.1-1-1': '68:05:CA:AF:AA:C6'}

        self.assertRaises(sushy.exceptions.ExtensionError,
                          oem.get_pxe_port_macs_bios, ethernet_interfaces_mac)

    def test_idrac_card_service(self):
        oem = self.manager.get_oem_extension('Dell')
        with open('sushy_oem_idrac/tests/unit/json_samples/'
                  'idrac_card_service.json') as f:
            mock_response = self.conn.get.return_value
            mock_response.json.return_value = json.load(f)
            mock_response.status_code = 200
        idrac_card_service = oem.idrac_card_service
        self.assertEqual(
            '/redfish/v1/Dell/Managers/iDRAC.Embedded.1/DelliDRACCardService',
            idrac_card_service.path)
        self.assertIsInstance(idrac_card_service,
                              idrac_card.DelliDRACCardService)

    @mock.patch('sushy.resources.oem.common._global_extn_mgrs_by_resource', {})
    def test_lifecycle_service(self):
        oem = self.manager.get_oem_extension('Dell')
        with open('sushy_oem_idrac/tests/unit/json_samples/'
                  'lifecycle_service.json') as f:
            mock_response = self.conn.get.return_value
            mock_response.json.return_value = json.load(f)
            mock_response.status_code = 200
        lifecycle_service = oem.lifecycle_service
        self.assertEqual(
            '/redfish/v1/Dell/Managers/iDRAC.Embedded.1/DellLCService',
            lifecycle_service.path)
        self.assertIsInstance(lifecycle_service,
                              lifecycle.DellLCService)

    @mock.patch('sushy.resources.oem.common._global_extn_mgrs_by_resource', {})
    def test_job_service(self):
        oem = self.manager.get_oem_extension('Dell')
        with open('sushy_oem_idrac/tests/unit/json_samples/'
                  'job_service.json') as f:
            mock_response = self.conn.get.return_value
            mock_response.json.return_value = json.load(f)
            mock_response.status_code = 200
        job_service = oem.job_service
        self.assertEqual(
            '/redfish/v1/Dell/Managers/iDRAC.Embedded.1/DellJobService',
            job_service.path)
        self.assertIsInstance(job_service,
                              job.DellJobService)

    @mock.patch('sushy.resources.oem.common._global_extn_mgrs_by_resource', {})
    def test_job_collection(self):
        oem = self.manager.get_oem_extension('Dell')
        with open('sushy_oem_idrac/tests/unit/json_samples/'
                  'job_collection_expanded.json') as f:
            mock_response = self.conn.get.return_value
            mock_response.json.return_value = json.load(f)
            mock_response.status_code = 200
        job_collection = oem.job_collection
        self.assertEqual(
            '/redfish/v1/Managers/iDRAC.Embedded.1/Jobs',
            job_collection.path)
        self.assertIsInstance(job_collection,
                              jc.DellJobCollection)
