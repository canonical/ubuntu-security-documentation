What kind of updates are not provided by Livepatch
##################################################

The livepatch service provides patches exclusively for
Canonical-released kernels, addressing security issues that have been
assigned a CVE and are rated as high or critical priority.

Livepatches are intended to address significant security issues in the
kernel, and provide customers with protection from serious
vulnerabilities until they can schedule a reboot. All CVEs that are
rated as either a high or critical issue will always be livepatched if
possible, and, if it is not possible, a notification that a reboot is
required will be issued by the Livepatch client.

There are frequently patches included in `kernel
updates <https://wiki.ubuntu.com/KernelTeam/KernelUpdates>`__ that are
not included in the Livepatch service, such as: \* bug fixes that are
not security issues \* performance improvements \* driver updates \* new
features

To receive these updates, it is necessary to upgrade the kernel package
using the package manager for the system (apt for Ubuntu desktop or
server, or snapd if running on Ubuntu Core) and then reboot into the
upgraded kernel.
