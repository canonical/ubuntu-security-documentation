Check-client-status
###################

Once ``canonical-livepatch``, the livepatch client, is running on a
machine, it will periodically (every hour by default) check for new
patches.

To show the current state of the client, run:

::


   $ canonical-livepatch status

This will produce output similar to:

::


   last check: 5 minutes ago
   kernel: 5.4.0-146.163-generic
   server check-in: succeeded
   kernel state: ✓ kernel is supported by Canonical until 2024-04-25
   patch state: ✓ no livepatches needed for this kernel yet
   tier: updates (Free usage; This machine beta tests new patches.)
   machine id: {alpha-numeric-string}

The ``kernel state`` line can have one of several values:

-  **✓ kernel is supported by Canonical until {date}** This kernel is
   actively supported by Canonical until the specified date. Please
   upgrade and reboot before this date to continue receiving patches.
   Note, this message means that this kernel series (e.g. 5.4) is still
   supported but the specific release will eventually stop receiving
   patches.

-  **✗ kernel not supported by Canonical** This kernel is not currently
   supported by Canonical.

-  **✗ kernel is no longer supported by Canonical** This kernel has been
   marked “end of life” for Canonical support and is no longer
   supported. To continue receiving patches please consider switching to
   the `HWE <https://wiki.ubuntu.com/Kernel/LTSEnablementStack>`__
   kernel or upgrade to a newer Ubuntu release.

-  **✗ Canonical kernel support ended {date}; please upgrade and
   reboot** This release of the kernel has reached the end of its
   support window. It is strongly recommended to upgrade and reboot, as
   the kernel will no longer receive any patches.

-  **✗ unable to determine kernel support status; please contact
   Canonical support** Something unexpected has happened. Please
   `contact
   us <https://bugs.launchpad.net/canonical-livepatch-client/+filebug>`__
   for support.

The ``patch state`` line can also have one of several values:

-  **⧗ livepatches are installed, but the module is not yet applied** A
   new patch has been downloaded and is going to be applied.

-  **⧗ patching the kernel** A patch is currently being applied.

-  **✓ no livepatches needed for this kernel yet** No livepatch modules
   exist yet for this kernel.

-  **✓ all applicable livepatch modules inserted** The current kernel is
   up-to-date with the current patches released by Canonical.

-  **✗ module inserted but kernel bug detected** the kernel reported an
   error after applying the patch.

-  **✗ the application caused a crash last time it was applied, check
   system logs with ``journalctl -f -t canonical-livepatch``** An
   attempt to apply the patch has failed and caused the client to crash.

-  **✗ patches are no longer available for this version of the kernel,
   please upgrade** The kernel the machine is currently running will no
   longer receive new patches, it is recommended to upgrade to a new
   kernel and reboot. This is normally caused by a CVE that cannot be
   livepatched and is a separate issue compared to the ``kernel state``
   requesting an upgrade.

-  **✗ failed to verify the signature of the livepatch kernel module**
   It has been detected that this patch is not from Canonical.
