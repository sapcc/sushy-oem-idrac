
Dell EMC OEM extension for sushy
================================

**EARLY PROTOTYPE, WORK IS IN PROGRESS**

Sushy is a client [library](https://github.com/openstack/sushy) designed to
communicate with [Redfish](https://en.wikipedia.org/wiki/Redfish_(specification))
based BMC.

Redfish specification offers extensibility mechanism to let hardware vendors
introduce their own features with the common Redfish framework. At the same
time, `sushy` supports extending its data model by loading extensions found
within its "oem" namespace.

The `sushy-oem-dellemc` package is a sushy extension package that adds
high-level hardware management abstractions, that are specific to Dell EMC
BMC (which is known under the name of iDRAC), to the tree of sushy Redfish
resources.

Example use
-----------

Once installed, sushy user can access Dell EMC OEM resources:

```python

import sushy

root = sushy.Sushy('http://mydellemcbmc.example.com')
manager = root.get_manager('iDRAC.Embedded.1')

oem = manager.get_oem_extension('Dell')

print(oem.import_system_configuration_uri)

```
