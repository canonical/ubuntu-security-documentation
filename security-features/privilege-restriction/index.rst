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

`SELinux <https://selinuxproject.org/page/Main_Page>`_ is an inode-based MAC. Targeted policies are available for Ubuntu in universe. Installing the "selinux" package applies the necessary boot-time adjustments.

Regression tests: `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_.

SMACK
=====

SMACK (Simplified Mandatory Access Control Kernel) is a Linux Security Module (LSM) that implements a label-based Mandatory Access Control (MAC) framework designed for simplicity and minimal administrative overhead. Unlike complex policy-driven systems, SMACK uses straightforward text labels assigned to subjects (processes) and objects (files, sockets, etc.) with access decisions made through simple rule comparisons. This architecture makes SMACK particularly well-suited for embedded systems, IoT devices and environments where security policies need to be easily understood and maintained without extensive expertise.

Access rules are expressed as::

    <subject-label> <object-label> <access>

where access describes the access permitted using the traditional Linux read (R or r) access, write (W or w) access, execute (X or x) access, or append (A or a) access. A dash (-) can be used as a place holder or to express that no access be permitted if used by itself.

SMACK uses several special system labels:

- ``_`` pronounced "floor"
- ``*`` pronounced "star"
- ``^`` pronounced "hat"

There are a limited number of pre-defined rules:

+---------------+---------------+---------+
| Subject Label | Object Label  | Access  |
+===============+===============+=========+
| \*            | any           | (None)  |
+---------------+---------------+---------+
| any           | \*            | rwxa    |
+---------------+---------------+---------+
| ordinary      | ordinary      | rwxa    |
+---------------+---------------+---------+
| any           | \_            | rx      |
+---------------+---------------+---------+
| ^             | any           | rx      |
+---------------+---------------+---------+

The third rule uses "ordinary" to refer to any label except ``*`` and describes the case where the subject label and the object label are the same. For example, if a process labeled ``user`` accesses a file also labeled ``user``, the access is allowed with ``rwxa`` permissions. If the same process accesses a file labeled ``_`` (floor), the access is restricted to ``rx``, regardless of the subject label.

Compared to `AppArmor <https://documentation.ubuntu.com/server/how-to/security/apparmor/index.html>`_, Ubuntu's default MAC system, SMACK serves a different architectural philosophy. AppArmor uses path-based mandatory access controls focused on confining specific applications through profiles that restrict file access, network usage and capabilities. SMACK provides system-wide label-based access control that is more suitable for creating isolated security domains and enforcing consistent policies across all system components. AppArmor excels at application-specific confinement and is easier to deploy incrementally, while SMACK is better suited for environments requiring comprehensive labeling schemes, such as multi-tenant systems or devices where all processes and data need clear security classifications.

SMACK support is available in Ubuntu kernels (**2.6.25** or newer) starting with Ubuntu 8.10 (Intrepid Ibex) but is not enabled by default, as AppArmor serves as Ubuntu's primary LSM. To enable SMACK you need to add ``security=smack`` to the kernel line in ``/boot/grub/menu.lst``

Create the directories ``/smack`` and ``/etc/smack``. Add this line to the ``/etc/fstab`` file::

    smackfs /smack smackfs defaults 0 0 

to get the SMACK control interface mounted at boot.

SMACK will create the init process with the floor label and will use the floor label as the default for all filesystems unless instructed otherwise using mount options. Because processes inherit the label of their parent all processes will run with the floor label unless explicitly set otherwise. Because all processes will have the floor label and all files will have the floor label, SMACK will never fail an access check in this configuration. 

Snap Confinement
================

.. toctree::
   :maxdepth: 1

   snap-confinement
