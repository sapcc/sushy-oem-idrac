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

# export system config action constants

EXPORT_TARGET_ALL = 'all'
"""Export entire system configuration"""

EXPORT_TARGET_BIOS = 'BIOS'
"""Export BIOS related configuration"""

EXPORT_TARGET_IDRAC = 'iDRAC'
"""Export IDRAC related configuration"""

EXPORT_TARGET_NIC = 'NIC'
"""Export NIC related configuration"""

EXPORT_TARGET_RAID = 'RAID'
"""Export RAID related configuration"""

# iDRAC Reset action constants


RESET_IDRAC_GRACEFUL_RESTART = 'graceful restart'
"""Perform a graceful shutdown followed by a restart of the system"""

RESET_IDRAC_FORCE_RESTART = 'force restart'
"""Perform an immediate (non-graceful) shutdown, followed by a restart"""

# ImportSystemConfiguration ShutdownType values
IMPORT_SHUTDOWN_GRACEFUL = 'graceful shutdown'
"""Graceful shutdown for Import System Configuration

Will wait for the host up to 5 minutes to shut down before timing out. The
operating system can potentially deny or ignore the graceful shutdown request.
"""

IMPORT_SHUTDOWN_FORCED = 'forced shutdown'
"""Forced shutdown for Import System Configuration

The host server will be powered off immediately. Should be used when it is safe
to power down the host.
"""

IMPORT_SHUTDOWN_NO_REBOOT = 'no shutdown'
"""No reboot for Import System Configuration

No shutdown performed. Explicit reboot is necessary to apply changes.
"""

# ExportUse in ExportSystemConfiguration
EXPORT_USE_DEFAULT = 'Default'
"""Default export type

Leaves some attributes commented out and requires user to enable them before
they can be applied during import.
"""

EXPORT_USE_CLONE = 'Clone'
"""Clone export type suitable for cloning a 'golden' configuration.

Compared to Default export type, more attributes are enabled and
storage settings adjusted to aid in cloning process.
"""

EXPORT_USE_REPLACE = 'Replace'
"""Replace export type suited for retiring or replacing complete configuration.

Compared to Clone export type, most attributes are enabled and storage settings
adjusted to aid in the replace process.
"""

# IncludeInExport in ExportSystemConfiguration
INCLUDE_EXPORT_DEFAULT = 'Default'
"""Default for what to include in export.

Does not include read-only attributes, and depending on Export Use, passwords
are marked as ****** (for Default) or are set to default password values (for
Clone and Replace).
"""

INCLUDE_EXPORT_READ_ONLY = 'Include read only attributes'
"""Includes read-only attributes.

In addition to values included by Default option, this also includes read-only
attributes that cannot be changed via Import and are provided for informational
purposes only.
"""

INCLUDE_EXPORT_PASSWORD_HASHES = 'Include password hash values'
"""Include password hashes.

When using Clone or Replace, include password hashes, instead of default
password. Can be used to replicate passwords across systems.
"""

INCLUDE_EXPORT_READ_ONLY_PASSWORD_HASHES = ('Include read only attributes and '
                                            'password hash values')
"""Includes both read-only attributes and password hashes.

INCLUDE_EXPORT_READ_ONLY and INCLUDE_EXPORT_PASSWORD_HASHES combined
"""
