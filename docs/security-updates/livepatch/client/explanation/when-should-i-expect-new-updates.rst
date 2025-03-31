When should I expect new updates
#################################

Livepatches are related to and are ‘’usually’’ derived from, but are not
the same as, the kernel SRU updates for CVEs. While the vulnerabilities
being addressed by both kernel SRU updates and livepatches are the same,
the process for development and testing are not. A livepatch for a
vulnerability can be significantly more complex than an ordinary kernel
patch, and due to the additional complexity, can take more time to
develop and test.

Canonical is committed to livepatching every high or critical rated CVE
possible as quickly as we can, and in ideal circumstances, a livepatch
will be available at the same time as the corresponding kernel SRU
update.

If we determine that we cannot livepatch a high or critical CVE, we will
inform our livepatch users at the same time an SRU kernel update that
does fix the issue becomes available, in two ways: \* The livepatch
client will indicate that the system must be rebooted by reporting a
state of “reboot required.” This will be accompanied by a notification
in the desktop, on desktop systems, and a notification in the MOTD on
the terminal. \* A LSN will be released containing instructions to
reboot into a new SRU kernel that contains a fix for the CVE. LSNs are
released on both the security website and via email.
