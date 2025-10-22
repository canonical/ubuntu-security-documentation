File Handing
############


FIFO restrictions
=================

Processes may not check that the files being created are actually created as the desired type. This global control forbids some potentially unsafe configurations from working.

See the `kernel admin-guide <https://www.kernel.org/doc/html/latest/admin-guide/sysctl/fs.html#protected-fifos>`_ for documentation. 


Regular file restrictions
=========================

Processes may not check that the files being created are actually created as desired. This global control forbids some potentially unsafe configurations from working.

See the `kernel admin-guide <https://www.kernel.org/doc/html/latest/admin-guide/sysctl/fs.html#protected-regular>`_ for documentation. 


Hardlink restrictions
=======================

Hardlinks can be abused in a similar fashion to symlinks above, but they are not limited to world-writable directories. If /etc/ and /home/ are on the same partition, a regular user can create a hardlink to /etc/shadow in their home directory. While it retains the original owner and permissions, it is possible for privileged programs that are otherwise symlink-safe to mistakenly access the file through its hardlink. Additionally, a very minor untraceable quota-bypassing local denial of service is possible by an attacker exhausting disk space by filling a world-writable directory with hardlinks.

In Ubuntu 10.10 and later, hardlinks cannot be created to files that the user would be unable to read and write originally, or are otherwise sensitive. The behavior is controllable through the `/proc/sys/fs/protected_hardlinks` sysctl.

See `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_ for regression tests.


Symlink restrictions
=======================

A long-standing class of security issues is the symlink-based ToCToU race, most commonly seen in world-writable directories like /tmp/. The common method of exploitation of this flaw is crossing privilege boundaries when following a given symlink (i.e. a root user follows a symlink belonging to another user).

In Ubuntu 10.10 and later, symlinks in world-writable sticky directories (e.g. /tmp) cannot be followed if the follower and directory owner do not match the symlink owner. The behavior is controllable through the /proc/sys/kernel/yama/protected_sticky_symlinks sysctl, available via Yama.

See `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_ for regression tests.


