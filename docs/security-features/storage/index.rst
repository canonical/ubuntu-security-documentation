Storage and filesystem
======================

Symlink restrictions
-----------------------

A long-standing class of security issues is the symlink-based ToCToU race, most commonly seen in world-writable directories like /tmp/. The common method of exploitation of this flaw is crossing privilege boundaries when following a given symlink (i.e. a root user follows a symlink belonging to another user).

In Ubuntu 10.10 and later, symlinks in world-writable sticky directories (e.g. /tmp) cannot be followed if the follower and directory owner do not match the symlink owner. The behavior is controllable through the /proc/sys/kernel/yama/protected_sticky_symlinks sysctl, available via Yama.

See `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_ for regression tests.

Hardlink restrictions
-----------------------
Hardlinks can be abused in a similar fashion to symlinks above, but they are not limited to world-writable directories. If /etc/ and /home/ are on the same partition, a regular user can create a hardlink to /etc/shadow in their home directory. While it retains the original owner and permissions, it is possible for privileged programs that are otherwise symlink-safe to mistakenly access the file through its hardlink. Additionally, a very minor untraceable quota-bypassing local denial of service is possible by an attacker exhausting disk space by filling a world-writable directory with hardlinks.

In Ubuntu 10.10 and later, hardlinks cannot be created to files that the user would be unable to read and write originally, or are otherwise sensitive. The behavior is controllable through the /proc/sys/kernel/yama/protected_nonaccess_hardlinks sysctl, available via Yama.

See `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_        for regression tests.

FIFO restrictions
-----------------------

Processes may not check that the files being created are actually created as the desired type. This global control forbids some potentially unsafe configurations from working.

See the kernel admin-guide for documentation. 

Filesystem Capabilities
-----------------------

The need for setuid applications can be reduced via the application of `filesystem capabilities <http://www.olafdietsche.de/linux/capability/>`_ using the xattrs available to most modern filesystems. This reduces the possible misuse of vulnerable setuid applications. The kernel provides the support, and the user-space tools are in main ("libcap2-bin").

Regression tests: `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_.

Full disk encryption
--------------------

https://ubuntu.com/core/docs/full-disk-encryption

Encrypted LVM
-------------
Ubuntu 12.10 and later support installation onto an encrypted LVM, encrypting all partitions, including swap. Earlier versions (6.06 LTS to 12.04 LTS) provided this option via the alternate installer.

File Encryption
---------------
Encrypted Private Directories were introduced in Ubuntu 8.10 using `eCryptfs <https://ecryptfs.org/>`_, allowing users to store sensitive data securely. 

- Ubuntu 9.04 introduced encrypted home directories.
- Support for Encrypted Private and Encrypted Home directories was dropped in Ubuntu 18.04 LTS.
- Encrypted directories can still be set up manually using `ecryptfs-setup-private`.

Since Ubuntu 18.04 LTS, `fscrypt <https://github.com/google/fscrypt>`_ is also available for encrypting directories on ext4 filesystems, though it is not officially supported.

Regular file restrictions
-------------------------

Processes may not check that the files being created are actually created as desired. This global control forbids some potentially unsafe configurations from working.

See the kernel admin-guide for documentation. 

.. toctree::
   :maxdepth: 2
   
   disk-encryption
   file-integrity-monitoring