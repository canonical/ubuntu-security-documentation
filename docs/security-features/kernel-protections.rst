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

The kernel configuration option ``CONFIG_SECURITY_DMESG_RESTRICT`` is used to set the default value of the sysctl key ``kernel.dmesg_restrict``:

.. code-block:: shell

    sysctl kernel.dmesg_restrict

When that configuration is set to ``1`` it restricts access to information from ``dmesg`` to privileged users with ``CAP_SYSLOG`` capability.

Starting with Ubuntu 20.10, the configuration is enabled by default.

For older releases, starting with Ubuntu 12.04 LTS, the configuration is available and can be set to ``1`` with the following command on a running system (not persisting after a reboot):

.. code-block:: shell

    sudo sysctl -w kernel.dmesg_restrict=1


Kernel Address Display Restriction
==================================

Kernel addresses can be exposed via ``/proc`` and other interfaces. They are sensitive information as it reveals the locations of internal kernel structures and end up being frequently used by attackers developing exploits.
Many files and interfaces contain these addresses (e.g. ``/proc/kallsyms``, ``/proc/modules``, etc)

The sysctl key ``kernel.kptr_restrict`` controls the restriction on exposing kernel addresses in such interfaces:

.. code-block:: shell

    sysctl kernel.kptr_restrict


When this key is set to ``1`` it restricts reporting kernel address to privileged users with ``CAP_SYSLOG`` capability replacing the actual address with 0s. Additionally, various files and directories that also expose kernel addresses were made readable only by the root user: ``/boot/vmlinuz*``, ``/boot/System.map*``, ``/sys/kernel/debug/``, ``/proc/slabinfo``.

Starting with Ubuntu 11.04, ``kernel.kptr_restrict`` is set to ``1`` by default.

Regression tests for this are included in `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_


Kernel Address Space Layout Randomisation
=========================================

Kernel Address Space Layout Randomization (kASLR) is a security feature that randomizes the kernel's base address in memory every time the system boots. This process ensures the location is unique for each startup, meaning two machines or even subsequent reboots of the same device are unlikely to share the same base address. Consequently, kASLR complicates exploits that depend on predictable memory locations, forcing them to first discover this randomized base address before they can target internal kernel symbols.

Kernel Address Space Layout Randomization (kASLR) and the userspace Address Space Layout Randomization (ASLR) shares the same concept to invalidate attacks that rely on static, predetermined addresses for code and data structures, forcing an exploit to first overcome the challenge of discovering these randomized locations. The fundamental distinction between them lies in their scope and application. Userspace ASLR is applied on a granular, per-process basis each time an application is launched to protect individual programs. In contrast, kASLR is applied monolithically to the entire operating system kernel once at system boot time to protect the core of the system as a whole.

Starting with Ubuntu 16.10, kASLR is enabled by default.

For older releases, starting with Ubuntu 14.10, the feature is available and can be enabled by specifying the ``kaslr`` option on the kernel command line parameters. It is important to note that doing that in such releases will disable the ability to enter hibernation mode.


/dev/kmem disabled
===================

``/dev/kmem`` used to provide access to the kernel's address space, but there is no modern use any more beyond attackers using it to load kernel rootkits.

The kernel configuration option ``CONFIG_DEVKMEM`` was used to set the existence of this special file.

The configuration and the interface were removed from the Kernel upstream source code since version 5.13. In Ubuntu that is reflected starting from Ubuntu 21.10.

For older releases with kernel versions supporting this special file, the kernel configuration ``CONFIG_DEVKMEM`` option is set to ``n`` to have it disabled by default.

Regression tests for this are included in `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_


Kernel Lockdown
===============

Starting with Ubuntu 20.04, the Linux kernel's lockdown mode is enabled in integrity mode. This prevents the root account from loading arbitrary modules or BPF programs that can manipulate kernel datastructures. Lockdown enforcement is tied to UEFI secure boot.


Kernel Stack protector
======================

The kernel stack protector is a security feature that detects memory corruption on the kernel stack before a function returns. It works by placing a small, random value known as a stack canary (or guard) on the stack between the local variables and the stored return address when a function is called. An usual stack smashing attack overwrites a function's local variables and continues writing past them to overwrite the return address, aiming to redirect program execution to malicious code. Before the function returns, the stack protector checks if the canary value has been altered. If an overflow has occurred and overwritten the canary, the check will fail. If that is the case, the kernel immediately panics or halts the system to prevent the attacker from gaining control, effectively mitigating exploits that rely on corrupting the return address to achieve arbitrary code execution or privilege escalation.

The kernel configuration option ``CONFIG_CC_STACKPROTECTOR`` is used to enable this feature.

This configuration is enabled by default in all supported Ubuntu releases for most of the supported architectures, not available on RISC-V and System z (S390X).

Regression tests for this are included in `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_


Read-only data sections
=======================

This feature is a kernel hardening mechanism that protects static kernel data from unauthorized modification by enforcing strict read-only permissions after system initialization is complete. During boot, critical data sections like ``.rodata`` are necessarily writable to allow for setup and configuration. Once this phase ends, the feature alters the underlying memory page permissions to be read-only, a rule enforced by the hardware's Memory Management Unit (MMU). This directly mitigates a common class of attacks used by kernel rootkits, which often attempt to overwrite static data such as function pointers or configuration tables to hijack system behavior. With this protection enabled, any illicit write attempt to these memory regions is blocked by the MMU, which triggers a hardware exception known as a page fault resulting in the kernel triggering a kernel panic. This immediate and total system halt is a "fail-secure" response designed to instantly stop the undesired operation and prevent a silent, malicious compromise of the kernel.

The kernel configuration option ``CONFIG_STRICT_KERNEL_RWX`` is used to enable this feature.
(Before Ubuntu 17.10 the configuration option was called ``CONFIG_DEBUG_RODATA``)

This configuration is enabled by default in all supported Ubuntu releases.

Regression tests for this are included in `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_


Module RO/NX
============

Read-Only (RO) and No-eXecute (NX) feature extends kernel configuration option ``CONFIG_STRICT_KERNEL_RWX`` to include similar restrictions for loaded modules in the kernel. The feature maps a module's executable code into read-only, executable pages while mapping its data into read-write, non-executable pages. This separation directly prevents attacks that rely on memory corruption, as it prevents an attacker from executing injected shellcode from a data section or from modifying the module's existing code at runtime. The Memory Management Unit (MMU) checks the permissions on each memory access. Any attempt to violate these rules is immediately blocked by the hardware, which triggers a page fault exception resulting in the kernel triggering a kernel panic.

The kernel configuration option ``CONFIG_STRICT_MODULE_RWX`` is used to enable this feature.
(Before Ubuntu 17.10 the configuration option was called ``CONFIG_DEBUG_SET_MODULE_RONX``)

This configuration is enabled by default in all supported Ubuntu releases.

Regression tests for this are included in `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_


