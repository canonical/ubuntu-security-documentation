What kind of updates are provided by Livepatch
##############################################

The Livepatch Service intends to address high and critical severity
Linux kernel security vulnerabilities, as identified by `Ubuntu Security
Notices <https://ubuntu.com/security/notices>`__ and the `CVE
tracker <https://ubuntu.com/security/cve>`__. Since there are
limitations to the `kernel livepatch
technology <https://github.com/torvalds/linux/blob/master/Documentation/livepatch/livepatch.rst>`__,
some Linux kernel code paths cannot be safely patched while running.
There may be occasions when the traditional kernel upgrade and reboot
might still be necessary.

Livepatches are developed and released based on kernel SRU releases, and
contain a subset of the CVEs fixed by that kernel SRU. Livepatches are
cumulative, so when a new livepatch is released, it contains both the
new CVE fixes, as well as all of the CVE fixes from the previous release
of that livepatch.
