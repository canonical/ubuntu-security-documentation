Privilege restriction
#####################

MAC is handled via kernel LSM hooks.

.. toctree::
   :maxdepth: 1
   :glob:

   *

Filesystem Capabilities
=======================

The need for setuid applications can be reduced via the application of `filesystem capabilities <http://www.olafdietsche.de/linux/capability/>`_ using the xattrs available to most modern filesystems. This reduces the possible misuse of vulnerable setuid applications. The kernel provides the support, and the user-space tools are in main ("libcap2-bin").

Regression tests: `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_.


PR_SET_SECCOMP
==============

Setting SECCOMP for a process is meant to confine it to a small subsystem of system calls, used for specialized processing-only programs.

See `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_ for regression tests. 


Seccomp Filtering
=================

Programs can filter out the availability of kernel syscalls by using the seccomp_filter interface. This is done in containers or sandboxes that want to further limit the exposure to kernel interfaces when potentially running untrusted software.

See test-kernel-security.py for regression tests. 


SELinux
=======

`SELinux <https://selinuxproject.org/page/Main_Page>`_ is an inode-based MAC. Targeted policies are available for Ubuntu in universe. Installing the "selinux" package applies the necessary boot-time adjustments.

Regression tests: `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_.

SMACK
=====

SMACK is a flexible inode-based MAC.

Regression tests: `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_.
