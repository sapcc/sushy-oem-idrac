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

from sushy import utils

from sushy_oem_idrac.resources.manager import constants as mgr_cons

EXPORT_CONFIG_VALUE_MAP = {
    'ALL': mgr_cons.EXPORT_TARGET_ALL,
    'BIOS': mgr_cons.EXPORT_TARGET_BIOS,
    'IDRAC': mgr_cons.EXPORT_TARGET_IDRAC,
    'NIC': mgr_cons.EXPORT_TARGET_NIC,
    'RAID': mgr_cons.EXPORT_TARGET_RAID
}

EXPORT_CONFIG_VALUE_MAP_REV = utils.revert_dictionary(EXPORT_CONFIG_VALUE_MAP)

RESET_IDRAC_VALUE_MAP = {
    'Graceful': mgr_cons.RESET_IDRAC_GRACEFUL_RESTART,
    'Force': mgr_cons.RESET_IDRAC_FORCE_RESTART,
}

RESET_IDRAC_VALUE_MAP_REV = utils.revert_dictionary(RESET_IDRAC_VALUE_MAP)

IMPORT_SHUTDOWN_VALUE_MAP = {
    'Graceful': mgr_cons.IMPORT_SHUTDOWN_GRACEFUL,
    'Forced': mgr_cons.IMPORT_SHUTDOWN_FORCED,
    'NoReboot': mgr_cons.IMPORT_SHUTDOWN_NO_REBOOT
}

IMPORT_SHUTDOWN_VALUE_MAP_REV =\
    utils.revert_dictionary(IMPORT_SHUTDOWN_VALUE_MAP)

EXPORT_USE_VALUE_MAP = {
    'Default': mgr_cons.EXPORT_USE_DEFAULT,
    'Clone': mgr_cons.EXPORT_USE_CLONE,
    'Replace': mgr_cons.EXPORT_USE_REPLACE
}

EXPORT_USE_VALUE_MAP_REV = utils.revert_dictionary(EXPORT_USE_VALUE_MAP)

INCLUDE_EXPORT_VALUE_MAP = {
    'Default': mgr_cons.INCLUDE_EXPORT_DEFAULT,
    'IncludeReadOnly': mgr_cons.INCLUDE_EXPORT_READ_ONLY,
    'IncludePasswordHashValues':
        mgr_cons.INCLUDE_EXPORT_PASSWORD_HASHES,
    'IncludeReadOnly,IncludePasswordHashValues':
        mgr_cons.INCLUDE_EXPORT_READ_ONLY_PASSWORD_HASHES
}

INCLUDE_EXPORT_VALUE_MAP_REV =\
    utils.revert_dictionary(INCLUDE_EXPORT_VALUE_MAP)
