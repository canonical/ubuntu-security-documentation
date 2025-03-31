Patch installation
##################

This document acts as a reference on how patch installation takes place.

How are patches installed?
--------------------------

Once the Livepatch client downloads a patch, it is stored on the
machine’s filesystem. The patch contains a Linux kernel module
responsible for patching the running kernel.

The Livepatch client inserts the kernel module by making the appropriate
syscall. The kernel module only affects the kernel as it is in-memory,
without modifying the installed kernel.

What if my system crashes or the patch is buggy after a Livepatch module is inserted?
-------------------------------------------------------------------------------------

If a module crashes a system, it will not be loaded on reboot. Livepatch
will make a best-effort attempt to not re-insert and reload the patch,
given it detects a system crash within 10 seconds of loading the module.

In a scenario where a patch contains a bug, Livepatch will do a best
effort match against the kernel logs to locate bug messages after
insertion. In case a bug is found the Livepatch client will report that
the module was inserted but caused a bug and the patch will not be
reapplied on reboot

Additionally, in both cases a “lockfile” is created, containing the bug
trace.

On the next reboot of the machine, if the lockfile is present, the patch
will not be inserted again. After Canonical becomes aware that the patch
is faulty, it will be blocked from delivery.

Are the Livepatch modules inserted on system boot?
--------------------------------------------------

No, we do not insert the modules at boot, instead patches are inserted
when the Livepatch client daemon service starts. This helps to prevent
placing a system into a crash loop.

How do I know if the patch is designed for my system?
-----------------------------------------------------

Each patch payload designed for Livepatch contains the kernel version in
the format “ABI.BUILDNO-FLAVOUR” which is matched against the currently
running kernel.
