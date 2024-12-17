What happens when a problem cannot be patched
##############################################

When an un-patchable security issue occurs, users *must* upgrade to a
version of the kernel that is fixed, and reboot. Problems of this type
are announced on the mailing list via LSN. Kernels prior to the levels
named in that announcement will no longer be livepatched.

The Livepatch client will report a state of “kernel-upgrade-required” if
you are running a kernel that is no longer livepatched due to an earlier
un-patchable kernel security issue. This notice will appear in the
user’s desktop notifications, and in the text-based message of the day
(MOTD) if logged into a terminal.
