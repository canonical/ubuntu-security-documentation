Do I need to reboot
###################

To upgrade (not just patch) your kernel to the newest version
livepatching is not sufficient, and you need to reboot. Note that
livepatches include only high and critical kernel vulnerabilities. The
service provides protection from serious security issues, but this is
just one aspect of keeping your system secure and well maintained. There
are a number of other software components that can require you to reboot
your system, including, but not limited to:

-  CPU firmware and microcode updates

-  Updates to shared libraries and low-level dependencies (glibc, for
   example)

-  System BIOS and EFI updates

**Enabling the Livepatch service does not turn on automatic installation
of security updates in APT.**

For best security, you should `enable security updates using
APT <https://help.ubuntu.com/community/AutomaticSecurityUpdates>`__,
subscribe to the `security announcement mailing
list <https://lists.ubuntu.com/mailman/listinfo/ubuntu-security-announce>`__,
follow all advised security updates, and reboot your system at your
earliest convenience when any software component requires it.

Additionally, kernel SRU updates include non-security bugfixes and
lower-priority security fixes that may be important to your specific
circumstances, and these fixes are only available by rebooting into an
updated kernel.
