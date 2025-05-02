Kernel protections
##################

Block kexec
===========

Starting with Ubuntu 14.04 LTS, it is now possible to disable kexec via sysctl. CONFIG_KEXEC is enabled in Ubuntu so end users are able to use kexec as desired and the new sysctl allows administrators to disable kexec_load. This is desired in environments where CONFIG_STRICT_DEVMEM and modules_disabled are set, for example. When Secure Boot is in use, kexec is restricted by default to only load appropriately signed and trusted kernels. 


Block module loading
=====================

In Ubuntu 8.04 LTS and earlier, it was possible to remove CAP_SYS_MODULES from the system-wide capability bounding set, which would stop any new kernel modules from being loaded. This was another layer of protection to stop kernel rootkits from being installed. The 2.6.25 Linux kernel (Ubuntu 8.10) changed how bounding sets worked, and this functionality disappeared. Starting with Ubuntu 9.10, it is now possible to block module loading again by setting "1" in /proc/sys/kernel/modules_disabled.

See test-kernel-security.py for regression tests. 


Denylist Rare Protocols
=======================

Normally the kernel allows all network protocols to be autoloaded on demand via the MODULE_ALIAS_NETPROTO(PF_...) macros. Since many of these protocols are old, rare, or generally of little use to the average Ubuntu user and may contain undiscovered exploitable vulnerabilities, they have been denylisted since Ubuntu 11.04. These include: ax25, netrom, x25, rose, decnet, econet, rds, and af_802154. If any of the protocols are needed, they can speficially loaded via modprobe, or the /etc/modprobe.d/blacklist-rare-network.conf file can be updated to remove the denylist entry.

See test-kernel-security.py for regression tests. 


dmesg restrictions
==================

When attackers try to develop "run anywhere" exploits for vulnerabilties, they frequently will use dmesg output. By treating dmesg output as sensitive information, this output is not available to the attacker. Starting with Ubuntu 12.04 LTS, /proc/sys/kernel/dmesg_restrict can be set to "1" to treat dmesg output as sensitive. Starting with 20.10, this is enabled by default. 


Kernel Address Display Restriction
==================================

When attackers try to develop "run anywhere" exploits for kernel vulnerabilities, they frequently need to know the location of internal kernel structures. By treating kernel addresses as sensitive information, those locations are not visible to regular local users. Starting with Ubuntu 11.04, /proc/sys/kernel/kptr_restrict is set to "1" to block the reporting of known kernel address leaks. Additionally, various files and directories were made readable only by the root user: /boot/vmlinuz*, /boot/System.map*, /sys/kernel/debug/, /proc/slabinfo

See test-kernel-security.py for regression tests. 


Kernel Address Space Layout Randomisation
=========================================

Kernel Address Space Layout Randomisation (kASLR) aims to make some kernel exploits more difficult to implement by randomizing the base address value of the kernel. Exploits that rely on the locations of internal kernel symbols must discover the randomized base address.

kASLR is available starting with Ubuntu 14.10 and is enabled by default in 16.10 and later.

Before 16.10, you can specify the "kaslr" option on the kernel command line to use kASLR.

Note: Before 16.10, enabling kASLR will disable the ability to enter hibernation mode. 


/dev/kmem disabled
===================

There is no modern user of /dev/kmem any more beyond attackers using it to load kernel rootkits. CONFIG_DEVKMEM is set to "n". While the /dev/kmem device node still exists in Ubuntu 8.04 LTS through Ubuntu 9.04, it is not actually attached to anything in the kernel.

See test-kernel-security.py for regression tests. 


Kernel Lockdown
===============

Starting with Ubuntu 20.04, the Linux kernel's lockdown mode is enabled in integrity mode. This prevents the root account from loading arbitrary modules or BPF programs that can manipulate kernel datastructures. Lockdown enforcement is tied to UEFI secure boot.


Kernel Stack protector
======================

Similar to the stack protector used for ELF programs in userspace, the kernel can protect its internal stacks as well. Enabled via the CONFIG_CC_STACKPROTECTOR option.

See test-kernel-security.py for configuration regression tests. 


Module RO/NX
============

This feature extends CONFIG_DEBUG_RODATA to include similar restrictions for loaded modules in the kernel. This can help resist future kernel exploits that depend on various memory regions in loaded modules. Enabled via the CONFIG_DEBUG_MODULE_RONX option.

See test-kernel-security.py for configuration regression tests. 


Read-only data sections
=======================

This makes sure that certain kernel data sections are marked to block modification. This helps protect against some classes of kernel rootkits. Enabled via the CONFIG_DEBUG_RODATA option.

See test-kernel-security.py for configuration regression tests.


