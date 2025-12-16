File handling
#############

FIFO restrictions
=================

Processes might not check that files are created as the desired type. This
global control prevents some potentially unsafe configurations from working.

See the `kernel admin-guide
<https://www.kernel.org/doc/html/latest/admin-guide/sysctl/fs.html#protected-fifos>`_
for documentation.


Regular file restrictions
=========================

Processes might not check that files are created as desired. This global
control prevents some potentially unsafe configurations from working.

See the `kernel admin-guide
<https://www.kernel.org/doc/html/latest/admin-guide/sysctl/fs.html#protected-regular>`_
for documentation.


Hardlink restrictions
=====================

Attackers can abuse hardlinks similarly to symlinks, but they aren't limited to
world-writable directories. If ``/etc/`` and ``/home/`` are on the same
partition, a regular user can create a hardlink to ``/etc/shadow`` in their
home directory. While it retains the original owner and permissions, privileged
programs that are otherwise symlink-safe might mistakenly access the file
through its hardlink. Additionally, an attacker can cause a minor, untraceable
quota-bypassing local denial of service by exhausting disk space by filling a
world-writable directory with hardlinks.

In Ubuntu 10.10 (Maverick Meerkat) and later, users cannot create hardlinks to
files they cannot read and write originally, or that are otherwise sensitive.
You can control this behavior through the
``/proc/sys/fs/protected_hardlinks`` sysctl.

See `test-kernel-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_
for regression tests.


Symlink restrictions
====================

The symlink-based Time-of-Check-Time-of-Use (ToCToU) race is a long-standing
class of security issues, most commonly seen in world-writable directories like
``/tmp/``. The common exploitation method involves crossing privilege
boundaries when following a given symlink (for example, a root user follows a
symlink belonging to another user).

In Ubuntu 10.10 (Maverick Meerkat) and later, the system prevents following
symlinks in world-writable sticky directories (such as ``/tmp``) if the
follower and directory owner don't match the symlink owner. You can control
this behavior through the ``/proc/sys/kernel/yama/protected_sticky_symlinks``
sysctl, available via Yama.

See `test-kernel-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_
for regression tests.
