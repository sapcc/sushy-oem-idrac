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

# Job state constants
JOB_STATE_COMPLETED = "Completed"
"""A job is in completed state"""

JOB_STATE_COMPLETED_ERRORS = "Completed with errors"
"""A job is in completed state with errors"""

JOB_STATE_DOWNLOADED = "Downloaded"
"""A job is in downloaded state"""

JOB_STATE_DOWNLOADING = "Downloading"
"""A job is in downloading state"""

JOB_STATE_FAILED = "Failed"
"""A job is in failed state"""

JOB_STATE_NEW = "New"
"""A job is in newly created state"""

JOB_STATE_PAUSED = "Paused"
"""A job is in paused state"""

JOB_STATE_PENDING_ACTIVATION = "Pending activation"
"""A job is in pending activation state"""

JOB_STATE_READY_EXECUTION = "Ready for execution"
"""A job is in ready for execution state"""

JOB_STATE_REBOOT_COMPLETED = "Reboot completed"
"""A job is in reboot completed state"""

JOB_STATE_REBOOT_FAILED = "Reboot failed"
"""A job is in reboot failed state"""

JOB_STATE_REBOOT_PENDING = "Reboot pending"
"""A job is in pending state for reboot"""

JOB_STATE_RUNNING = "Running"
"""A job is in running state"""

JOB_STATE_SCHEDULED = "Scheduled"
"""A job is in scheduled state"""

JOB_STATE_SCHEDULING = "Scheduling"
"""A job is in scheduling state"""

JOB_STATE_UNKNOWN = "Unknown"
"""A job is in unknown state"""

JOB_STATE_WAITING = "Waiting"
"""A job is in waiting state"""

# Job type constants
JOB_TYPE_BIOS_CONF = "BIOS configuration"
"""A BIOS configuration job"""

JOB_TYPE_EXPORT_CONF = "Export configuration"
"""A server configuration profile export job"""

JOB_TYPE_FC_CONF = "Fibre Channel configuration"
"""A Fibre Channel configuration job"""

JOB_TYPE_FACTORY_CONF_EXPORT = "Factory configuration export"
"""A factory configuration export job"""

JOB_TYPE_FIRMWARE_ROLLBACK = "Firmware rollback"
"""A firmware rollback job"""

JOB_TYPE_FIRMWARE_UPDATE = "Firmware update"
"""A firmware update job"""

JOB_TYPE_HW_INVENTORY_EXPORT = "Hardware inventory export"
"""A hardware inventory export job"""

JOB_TYPE_IMPORT_CONF = "Import configuration"
"""A server configuration profile import job"""

JOB_TYPE_INBAND_BIOS_CONF = "Inband BIOS configuration"
"""An inband BIOS configuration job"""

JOB_TYPE_LC_CONF = "LC configuration"
"""A lifecycle controller attribute configuration job"""

JOB_TYPE_LC_EXPORT = "LC export"
"""A lifecycle controller export job"""

JOB_TYPE_LC_LOG_EXPORT = "LC log export"
"""A lifecycle controller log export job"""

JOB_TYPE_LICENSE_EXPORT = "License export"
"""A license export job"""

JOB_TYPE_LICENSE_IMPORT = "License import"
"""A license import job"""

JOB_TYPE_MSG_REG_EXPORT = "Message registry export"
"""Export message registry report job"""

JOB_TYPE_NIC_CONF = "NIC configuration"
"""A NIC configuration job"""

JOB_TYPE_OS_DEPLOY = "OS deploy"
"""Operating System deploy job"""

JOB_TYPE_RAID_CONF = "RAID configuration"
"""A RAID configuration job"""

JOB_TYPE_RT_NO_REBOOT_CONF = "Real-time no reboot configuration"
"""A real time configuration job without reboot"""

JOB_TYPE_REBOOT_FORCE = "Reboot force"
"""A reboot job with forced shutdown"""

JOB_TYPE_REBOOT_NO_FORCE = "Reboot no force"
"""A graceful reboot job without forced shutdown"""

JOB_TYPE_REBOOT_POWER_CYCLE = "Reboot power cycle"
"""A power cycle job"""

JOB_TYPE_REMOTE_DIAG = "Remote diagnostics"
"""A remote diagnostics job"""

JOB_TYPE_REPO_UPDATE = "Repository update"
"""An update job from a repository"""

JOB_TYPE_SA_COL_EXP_HEALTH_DATA = "SA collect and export health data"
"""Support Assist collect and export health data job"""

JOB_TYPE_SA_COL_HEALTH_DATA = "SA collect health data"
"""Support Assist collect health data job"""

JOB_TYPE_SA_EXP_HEALTH_DATA = "SA export health data"
"""Support Assist export health data job"""

JOB_TYPE_SA_ISM = "SA expose iSM"
"""Support Assist expose iDRAC Service Module installer package to host job"""

JOB_TYPE_SA_REG = "SA registration"
"""Support Assist register iDRAC to Dell backend server job"""

JOB_TYPE_SEKM_REKEY = "SEKM rekey"
"""A Secure Enterprise Key Manager rekey job"""

JOB_TYPE_SEKM_STATUS_SET = "SEKM status set"
"""A Secure Enterprise Key Manager status set job"""

JOB_TYPE_SHUTDOWN = "Shutdown"
"""A shutdown job"""

JOB_TYPE_SYS_ERASE = "System erase"
"""A selective system erase job"""

JOB_TYPE_SYS_INFO_CONF = "System info configuration"
"""A system info configuration job"""

JOB_TYPE_THERMAL_HIST_EXP = "Thermal history export"
"""A thermal history export job"""

JOB_TYPE_UNKNOWN = "Unknown"
"""An unknown job"""

JOB_TYPE_IDRAC_CONF = "iDRAC configuration"
"""An iDRAC configuration job"""
