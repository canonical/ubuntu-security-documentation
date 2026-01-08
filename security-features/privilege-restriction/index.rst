Privilege restriction
#####################

Ubuntu provides a set of security features that allow restricting the privileges available to processes. Mandatory Access Control (MAC) is, by default, provided by :ref:`AppArmor`; other MAC solutions, implemented through Linux Security Module (LSM) hooks, are available, but not supported.

AppArmor
========

.. toctree::
   :maxdepth: 1

   apparmor

Cgroups (Control Groups)
========================

.. toctree::
   :maxdepth: 1

   cgroups

Filesystem Capabilities
=======================

The need for setuid applications can be reduced via the application of `filesystem capabilities <http://www.olafdietsche.de/linux/capability/>`_ using the `xattrs` available to most modern filesystems. This reduces the possible misuse of vulnerable setuid applications. The kernel provides the support, and the user-space tools are in the Ubuntu Main component (`libcap2-bin`).

Regression tests: `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_.


PR_SET_SECCOMP
==============

Setting `SECCOMP` for a process is meant to confine it to a small subsystem of system calls, used for specialized processing-only programs.

See `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_ for regression tests. 


Seccomp Filtering
=================

Programs can filter out the availability of kernel syscalls by using the `seccomp_filter` interface, which allows for fine-grained control. This is done in containers or sandboxes that want to further limit the exposure to kernel interfaces when potentially running untrusted software.

See `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_ for regression tests. 


SELinux
=======

`SELinux <https://selinuxproject.org/page/Main_Page>`_ (Security-Enhanced Linux) is a Linux Security Module (LSM) that implements Mandatory Access Control (MAC) through a flexible, policy-driven framework maintained as an open-source project. SELinux provides fine-grained access controls by assigning security contexts (labels) to all system objects including files, processes, network ports and devices. These labels are used by a centralized policy engine to make access control decisions based on predefined security policies.

SELinux operates through three main components: security contexts (labels in the format ``user:role:type:level``), a fine-grained policy language for defining rules and enforcement modes (enforcing, permissive, or disabled). This architecture enables sophisticated security models including Multi-Level Security (MLS) and Multi-Category Security (MCS).

Ubuntu uses `AppArmor <https://documentation.ubuntu.com/server/how-to/security/apparmor/index.html>`_ as its default MAC system instead of SELinux. While both provide mandatory access controls, AppArmor uses a path-based approach that is generally simpler to configure and maintain, whereas SELinux uses an inode-based labeling system that offers fine-grained coverage but with significantly greater complexity. AppArmor's focus on application confinement through pathname-based rules makes it well-suited for Ubuntu's desktop and server use cases, while SELinux's label-based model provides comprehensive system-wide policy enforcement.

Kernel support
--------------

SELinux support is compiled into Ubuntu's default kernels as a loadable security module, meaning the underlying kernel infrastructure is present and functional. However, SELinux is not the active LSM by default, AppArmor takes precedence as the enabled security module at boot time.

Userspace packages
------------------

SELinux userspace tools and policies are available through Ubuntu's ``universe`` repository, including packages such as ``selinux-basics``, ``policycoreutils`` and the ``selinux`` metapackage. These packages provide the essential tools for policy management, system labeling and SELinux administration, but they require manual configuration and are not pre-tuned for Ubuntu's specific package ecosystem.

Support level
-------------

SELinux on Ubuntu is community-supported rather than officially supported by Canonical. The SELinux packages in universe are maintained by community contributors and lack the extensive integration testing, policy tuning and commercial support that Ubuntu provides for AppArmor. Users choosing SELinux on Ubuntu should expect to handle policy development, troubleshooting and maintenance themselves, as most Ubuntu documentation, tools and support resources assume AppArmor is in use. For production Ubuntu deployments, `AppArmor <https://documentation.ubuntu.com/server/how-to/security/apparmor/index.html>`_ remains the recommended and fully supported MAC solution.


SMACK
=====

SMACK is a flexible inode-based MAC.

Regression tests: `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_.

Snap Confinement
================

.. toctree::
   :maxdepth: 1

   snap-confinement
