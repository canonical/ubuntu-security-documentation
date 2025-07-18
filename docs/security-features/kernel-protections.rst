Kernel protections
##################

Block kexec
===========

Starting with Ubuntu 14.04 LTS, it is now possible to disable kexec via sysctl. CONFIG_KEXEC is enabled in Ubuntu so end users are able to use kexec as desired and the new sysctl allows administrators to disable kexec_load. This is desired in environments where CONFIG_STRICT_DEVMEM and modules_disabled are set, for example. When Secure Boot is in use, kexec is restricted by default to only load appropriately signed and trusted kernels.


Block module loading
=====================

In Ubuntu 8.04 LTS and earlier, it was possible to remove CAP_SYS_MODULES from the system-wide capability bounding set, which would stop any new kernel modules from being loaded. This was another layer of protection to stop kernel rootkits from being installed. The 2.6.25 Linux kernel (Ubuntu 8.10) changed how bounding sets worked, and this functionality disappeared. Starting with Ubuntu 9.10, it is now possible to block module loading again by setting "1" in /proc/sys/kernel/modules_disabled.

Regression tests for this are included in `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_


Denylist Rare Protocols
=======================

Normally the kernel allows all network protocols to be autoloaded on demand via the MODULE_ALIAS_NETPROTO(PF_...) macros. Since many of these protocols are old, rare, or generally of little use to the average Ubuntu user and may contain undiscovered exploitable vulnerabilities, they have been denylisted since Ubuntu 11.04. These include: ax25, netrom, x25, rose, decnet, econet, rds, and af_802154. If any of the protocols are needed, they can specifically loaded via modprobe, or the /etc/modprobe.d/blacklist-rare-network.conf file can be updated to remove the denylist entry.

Regression tests for this are included in `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_


dmesg restrictions
==================

``dmesg`` (diagnostic messages) is a well known command-line tool that displays the contents of kernel ring buffer, allowing users to analyze kernel operations related to software or hardware and can be treated as sensitive information. It is commonly used for troubleshooting issues in those layers and as it expose sensitive information it is frequently used by attackers developing exploits.

The kernel configuration option ``CONFIG_SECURITY_DMESG_RESTRICT`` is used to set the default value of the sysctl file ``/proc/sys/kernel/dmesg_restrict``, also available through the sysctl key ``kernel.dmesg_restrict``:

.. code-block:: shell

    sysctl kernel.dmesg_restrict

When that configuration is set to ``1`` it will restrict access to information from ``dmesg`` to privileged users.

Starting with Ubuntu 12.04 LTS, the configuration is available and can be set to ``1`` manually with:

.. code-block:: shell

    sudo sysctl -w kernel.dmesg_restrict=1

And starting with Ubuntu 20.10, it is enabled by default.


Kernel Address Display Restriction
==================================

Kernel addresses can be exposed via ``/proc`` and other interfaces. They are sensitive information as it reveals the locations of internal kernel structures and end up being frequently used by attackers developing exploits.

The syctl file ``/proc/sys/kernel/kptr_restrict`` controls the restriction on exposing kernel addresses, also available through the sysctl key ``kernel.kptr_restrict``:

.. code-block:: shell

    sysctl kernel.kptr_restrict

Starting with Ubuntu 11.04, ``/proc/sys/kernel/kptr_restrict`` is set to ``1`` to block the reporting of known kernel address leaks. Additionally, various files and directories that also expose kernel addresses were made readable only by the root user: ``/boot/vmlinuz*``, ``/boot/System.map*``, ``/sys/kernel/debug/``, ``/proc/slabinfo``.

Regression tests for this are included in `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_


Kernel Address Space Layout Randomisation
=========================================

Kernel Address Space Layout Randomisation (kASLR) randomizes the base address value of the kernel during load and it aims to make some kernel exploits more difficult to implement by. Exploits that rely on the locations of internal kernel symbols must discover the randomized base address.

kASLR is available starting with Ubuntu 14.10 and is enabled by default in Ubuntu 16.10 and later.

Before Ubuntu 16.10, you can specify the ``kaslr`` option on the kernel command line parameters to use kASLR.

Note: Before Ubuntu 16.10, enabling kASLR will disable the ability to enter hibernation mode.


/dev/kmem disabled
===================

``/dev/kmem`` used to provide access to the kernel's address space but there is no modern use any more beyond attackers using it to load kernel rootkits. In kernel versions supporting this special file, the kernel configuration ``CONFIG_DEVKMEM`` option is set to ``n`` to have it disabled.

While the ``/dev/kmem`` device node still exists in Ubuntu 8.04 LTS through Ubuntu 9.04, it is not actually attached to anything in the kernel.

Regression tests for this are included in `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_


Kernel Lockdown
===============

Starting with Ubuntu 20.04, the Linux kernel's lockdown mode is enabled in integrity mode. This prevents the root account from loading arbitrary modules or BPF programs that can manipulate kernel datastructures. Lockdown enforcement is tied to UEFI secure boot.


Kernel Stack protector
======================

Similar to the stack protector, which basically is a verification of the presence of a stack canary between the stack variables and the return address, used for ELF programs in userspace the kernel can protect its internal stacks as well.

It is enabled via the kernel configuration ``CONFIG_CC_STACKPROTECTOR`` option.

Starting with Ubuntu 9.10 it is enabled by default for most of the supported architectures.

Regression tests for this are included in `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_


Read-only data sections
=======================

This feature make sure that certain kernel data sections are marked to block modification. This helps protect against some classes of kernel rootkits.

It is enabled via the kernel configuration ``CONFIG_DEBUG_RODATA`` option.

Starting with Ubuntu 7.10 it is enabled by default.

Regression tests for this are included in `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_


Module RO/NX
============

Read-Only (RO) and No-eXecute (NX) feature extends kernel configuration option ``CONFIG_DEBUG_RODATA`` to include similar restrictions for loaded modules in the kernel. This can help resist future kernel exploits that depend on various memory regions in loaded modules.

It is enabled via the kernel configuration ``CONFIG_DEBUG_MODULE_RONX`` option.

Starting with Ubuntu 11.04 it is enabled by default.

Regression tests for this are included in `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_


