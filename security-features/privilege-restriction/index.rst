Privilege restriction
#####################

Ubuntu provides a set of security features that allow you to restrict the
privileges available to processes. :ref:`AppArmor` provides Mandatory Access
Control (MAC) by default. Other MAC solutions, implemented through Linux
Security Module (LSM) hooks, are available but not supported.

AppArmor
========

.. toctree::
   :maxdepth: 1

   apparmor

Cgroups (control groups)
========================

.. toctree::
   :maxdepth: 1

   cgroups

Filesystem capabilities
=======================

You can reduce the need for setuid applications via the application of
`filesystem 
capabilities <https://manpages.ubuntu.com/manpages/resolute/en/man7/capabilities.7.html>`_
using the ``xattrs`` available to most modern filesystems. This reduces the possible
misuse of vulnerable setuid applications. The kernel provides support, and the
user-space tools are in the Ubuntu Main component (``libcap2-bin``).

Regression tests: `test-kernel-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_.

PR_SET_SECCOMP
==============

Setting ``SECCOMP`` for a process confines it to a small subsystem of system
calls, used for specialized processing-only programs.

See `test-kernel-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_
for regression tests.

Seccomp filtering
=================

Programs can filter out the availability of kernel syscalls by using the
``seccomp_filter`` interface, which allows for fine-grained control. Containers
or sandboxes use this to further limit exposure to kernel interfaces when
potentially running untrusted software.

See `test-kernel-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_
for regression tests.

SELinux
=======

`SELinux <https://selinuxproject.org/page/Main_Page>`_ is an inode-based MAC.
Targeted policies are available for Ubuntu in ``universe``. Installing the
``selinux`` package applies the necessary boot-time adjustments.

Regression tests: `test-kernel-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_.

SMACK
=====

SMACK is a flexible inode-based MAC.

Regression tests: `test-kernel-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_.

Snap Confinement

.. toctree::
   :maxdepth: 1

   snap-confinement
