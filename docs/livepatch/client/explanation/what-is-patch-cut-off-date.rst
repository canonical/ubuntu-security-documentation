What is patch cut off date
##########################

*Patch cut-off date* is a feature that allows you to set a time in the
past, after which no patches will be applied to the system. This is
useful for ensuring that the state of the system is deterministic and
reproducible. It guarantees that no changes will be made after a certain
date.

The use of patch cut-off date is recommended only for systems that
require a high level of predictability, as using it might expose the
system to security vulnerabilities due to the lack of the latest
patches.

Availability
------------

This feature is available only for users with a paid Ubuntu Pro
subscription connected to Canonical’s hosted Livepatch service.

What if I already have a patch applied?
---------------------------------------

If you already have a patch applied and its release date is after the
cut-off date to fully remove the changes from your system, you will need
to reboot the machine.

If you set a cut-off date and the release date of the patch is before
the cut-off date, you are not required to take any action. The patch
will remain applied.
