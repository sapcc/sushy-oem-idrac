# Copyright (c) 2021 Dell Inc. or its subsidiaries.
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

from sushy_oem_idrac.resources.taskservice import constants as ts_cons

JOB_STATE_VALUE_MAP = {
    "New": ts_cons.JOB_STATE_NEW,
    "Scheduled": ts_cons.JOB_STATE_SCHEDULED,
    "Running": ts_cons.JOB_STATE_RUNNING,
    "Completed": ts_cons.JOB_STATE_COMPLETED,
    "Downloading": ts_cons.JOB_STATE_DOWNLOADING,
    "Downloaded": ts_cons.JOB_STATE_DOWNLOADED,
    "Scheduling": ts_cons.JOB_STATE_SCHEDULING,
    "ReadyForExecution": ts_cons.JOB_STATE_READY_EXECUTION,
    "Waiting": ts_cons.JOB_STATE_WAITING,
    "Paused": ts_cons.JOB_STATE_PAUSED,
    "Failed": ts_cons.JOB_STATE_FAILED,
    "CompletedWithErrors": ts_cons.JOB_STATE_COMPLETED_ERRORS,
    "RebootPending": ts_cons.JOB_STATE_REBOOT_PENDING,
    "RebootFailed": ts_cons.JOB_STATE_REBOOT_FAILED,
    "RebootCompleted": ts_cons.JOB_STATE_REBOOT_COMPLETED,
    "PendingActivation": ts_cons.JOB_STATE_PENDING_ACTIVATION,
    "Unknown": ts_cons.JOB_STATE_UNKNOWN
}

JOB_STATE_VALUE_MAP_REV = utils.revert_dictionary(JOB_STATE_VALUE_MAP)

JOB_TYPE_VALUE_MAP = {
    "FirmwareUpdate": ts_cons.JOB_TYPE_FIRMWARE_UPDATE,
    "FirmwareRollback": ts_cons.JOB_TYPE_FIRMWARE_ROLLBACK,
    "RepositoryUpdate": ts_cons.JOB_TYPE_REPO_UPDATE,
    "RebootPowerCycle": ts_cons.JOB_TYPE_REBOOT_POWER_CYCLE,
    "RebootForce": ts_cons.JOB_TYPE_REBOOT_FORCE,
    "RebootNoForce": ts_cons.JOB_TYPE_REBOOT_NO_FORCE,
    "Shutdown": ts_cons.JOB_TYPE_SHUTDOWN,
    "RAIDConfiguration": ts_cons.JOB_TYPE_RAID_CONF,
    "BIOSConfiguration": ts_cons.JOB_TYPE_BIOS_CONF,
    "NICConfiguration": ts_cons.JOB_TYPE_NIC_CONF,
    "FCConfiguration": ts_cons.JOB_TYPE_FC_CONF,
    "iDRACConfiguration": ts_cons.JOB_TYPE_IDRAC_CONF,
    "SystemInfoConfiguration": ts_cons.JOB_TYPE_SYS_INFO_CONF,
    "InbandBIOSConfiguration": ts_cons.JOB_TYPE_INBAND_BIOS_CONF,
    "ExportConfiguration": ts_cons.JOB_TYPE_EXPORT_CONF,
    "ImportConfiguration": ts_cons.JOB_TYPE_IMPORT_CONF,
    "RemoteDiagnostics": ts_cons.JOB_TYPE_REMOTE_DIAG,
    "RealTimeNoRebootConfiguration": ts_cons.JOB_TYPE_RT_NO_REBOOT_CONF,
    "LCLogExport": ts_cons.JOB_TYPE_LC_LOG_EXPORT,
    "HardwareInventoryExport": ts_cons.JOB_TYPE_HW_INVENTORY_EXPORT,
    "FactoryConfigurationExport": ts_cons.JOB_TYPE_FACTORY_CONF_EXPORT,
    "LicenseImport": ts_cons.JOB_TYPE_LICENSE_IMPORT,
    "LicenseExport": ts_cons.JOB_TYPE_LICENSE_EXPORT,
    "ThermalHistoryExport": ts_cons.JOB_TYPE_THERMAL_HIST_EXP,
    "LCConfig": ts_cons.JOB_TYPE_LC_CONF,
    "LCExport": ts_cons.JOB_TYPE_LC_EXPORT,
    "SACollectHealthData": ts_cons.JOB_TYPE_SA_COL_HEALTH_DATA,
    "SAExportHealthData": ts_cons.JOB_TYPE_SA_EXP_HEALTH_DATA,
    "SACollectExportHealthData": ts_cons.JOB_TYPE_SA_COL_EXP_HEALTH_DATA,
    "SAExposeISM": ts_cons.JOB_TYPE_SA_ISM,
    "SARegistration": ts_cons.JOB_TYPE_SA_REG,
    "SystemErase": ts_cons.JOB_TYPE_SYS_ERASE,
    "MessageRegistryExport": ts_cons.JOB_TYPE_MSG_REG_EXPORT,
    "OSDeploy": ts_cons.JOB_TYPE_OS_DEPLOY,
    "SEKMRekey": ts_cons.JOB_TYPE_SEKM_REKEY,
    "SEKMStatusSet": ts_cons.JOB_TYPE_SEKM_STATUS_SET,
    "Unknown": ts_cons.JOB_TYPE_UNKNOWN
}

JOB_TYPE_VALUE_MAP_REV = utils.revert_dictionary(JOB_TYPE_VALUE_MAP)
