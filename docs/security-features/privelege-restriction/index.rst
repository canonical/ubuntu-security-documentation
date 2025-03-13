Privilige restriction
#####################

MAC is handled via kernel LSM hooks.

AppArmor
--------

`AppArmor <https://help.ubuntu.com/community/AppArmor>`_ is a path-based MAC that mediates:

- File access (read, write, link, lock)
- Library loading
- Application execution
- Coarse-grained network access (protocol, type, domain)
- Capabilities
- Coarse owner checks (starting with Ubuntu 9.10)
- Mount operations (starting with Ubuntu 12.04 LTS)
- Unix(7) named sockets (starting with Ubuntu 13.10)
- DBus API (starting with Ubuntu 13.10)
- Signal(7) (starting with Ubuntu 14.04 LTS)
- Ptrace(2) (starting with Ubuntu 14.04 LTS)
- Unix(7) abstract and anonymous sockets (starting with Ubuntu 14.10)

AppArmor is a core technology for `Ubuntu Touch <https://wiki.ubuntu.com/SecurityTeam/Specifications/ApplicationConfinement>`_ and `Snappy for Ubuntu Core <https://developer.ubuntu.com/en/snappy/guides/security-policy/>`_.

Example profiles are included in the `apparmor-profiles` package.

Regression tests: 
- `test-apparmor.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-apparmor.py>`_
- `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_

AppArmor Unprivileged User Namespace Restrictions
-------------------------------------------------
Starting with Ubuntu 23.10, AppArmor can deny unprivileged applications the use of user namespaces, preventing them from gaining additional capabilities and reducing kernel attack surface. Applications requiring unprivileged namespaces must be explicitly allowed by their AppArmor profile. 

From Ubuntu 24.04 onward, this restriction is enabled by default.

Regression tests: `test-apparmor.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-apparmor.py>`_.

SELinux
-------
`SELinux <https://selinuxproject.org/page/Main_Page>`_ is an inode-based MAC. Targeted policies are available for Ubuntu in universe. Installing the "selinux" package applies the necessary boot-time adjustments.

Regression tests: `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_.

SMACK
-----
SMACK is a flexible inode-based MAC.

Regression tests: `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_.

PR_SET_SECCOMP
--------------

Setting SECCOMP for a process is meant to confine it to a small subsystem of system calls, used for specialized processing-only programs.

See test-kernel-security.py for regression tests. 

.. toctree::
   :maxdepth: 2
   
   apparmor