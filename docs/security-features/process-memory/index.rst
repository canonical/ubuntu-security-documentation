Process and memory integrity
============================

Stack Protector
---------------

gcc's -fstack-protector provides a randomized stack canary that protects against stack overflows, and reduces the chances of arbitrary code execution via controlling return address destinations. Enabled at compile-time. (A small number of applications do not play well with it, and have it disabled.) The routines used for stack checking are actually part of glibc, but gcc is patched to enable linking against those routines by default.

See test-gcc-security.py for regression tests. 

Heap Protector
--------------

The GNU C Library heap protector (both automatic via ptmalloc and manual) provides corrupted-list/unlink/double-free/overflow protections to the glibc heap memory manager (first introduced in glibc 2.3.4). This stops the ability to perform arbitrary code execution via heap memory overflows that try to corrupt the control structures of the malloc heap memory areas.

This protection has evolved over time, adding more and more protections as additional corner-cases were researched. As it currently stands, glibc 2.10 and later appears to successfully resist even these hard-to-hit conditions.

See test-glibc-security.py for regression tests. 

Pointer Obfuscation
-------------------

Some pointers stored in glibc are obfuscated via PTR_MANGLE/PTR_UNMANGLE macros internally in glibc, preventing libc function pointers from being overwritten during runtime.

See test-glibc-security.py for regression tests. 

Address Space Layout Randomisation (ASLR)
-----------------------------------------

ASLR is implemented by the kernel and the ELF loader by randomising the location of memory allocations (stack, heap, shared libraries, etc). This makes memory addresses harder to predict when an attacker is attempting a memory-corruption exploit. ASLR is controlled system-wide by the value of /proc/sys/kernel/randomize_va_space. Prior to Ubuntu 8.10, this defaulted to "1" (on). In later releases that included brk ASLR, it defaults to "2" (on, with brk ASLR).

See test-kernel-security.py for regression tests for all the different types of ASLR. 

Stack ASLR
~~~~~~~~~~

Each execution of a program results in a different stack memory space layout. This makes it harder to locate in memory where to attack or deliver an executable attack payload. This was available in the mainline kernel since 2.6.15 (Ubuntu 6.06).

Libs/mmap ASLR
~~~~~~~~~~~~~~

Each execution of a program results in a different mmap memory space layout (which causes the dynamically loaded libraries to get loaded into different locations each time). This makes it harder to locate in memory where to jump to for "return to libc" to similar attacks. This was available in the mainline kernel since 2.6.15 (Ubuntu 6.06).

Exec ASLR
~~~~~~~~~

Each execution of a program that has been built with "-fPIE -pie" will get loaded into a different memory location. This makes it harder to locate in memory where to attack or jump to when performing memory-corruption-based attacks. This was available in the mainline kernel since 2.6.25 (and was backported to Ubuntu 8.04 LTS).

brk ASLR
~~~~~~~~

Similar to exec ASLR, brk ASLR adjusts the memory locations relative between the exec memory area and the brk memory area (for small mallocs). The randomization of brk offset from exec memory was added in 2.6.26 (Ubuntu 8.10), though some of the effects of brk ASLR can be seen for PIE programs in Ubuntu 8.04 LTS since exec was ASLR, and brk is allocated immediately after the exec region (so it was technically randomized, but not randomized with respect to the text region until 8.10).

VDSO ASLR
~~~~~~~~~

Each execution of a program results in a random vdso location. While this has existed in the mainline kernel since 2.6.18 (x86, PPC) and 2.6.22 (x86_64), it hadn't been enabled in Ubuntu 6.10 due to COMPAT_VDSO being enabled, which was removed in Ubuntu 8.04 LTS. This protects against jump-into-syscall attacks. Only x86 (maybe ppc?) is supported by glibc 2.6. glibc 2.7 (Ubuntu 8.04 LTS) supports x86_64 ASLR vdso. People needing ancient pre-libc6 static high vdso mappings can use "vdso=2" on the kernel boot command line to gain COMPAT_VDSO again. 

* https://lwn.net/Articles/184734/

* https://articles.manugarg.com/systemcallinlinux2_6.html

Built as PIE
------------

All programs built as Position Independent Executables (PIE) with "-fPIE -pie" can take advantage of the exec ASLR. This protects against "return-to-text" and generally frustrates memory corruption attacks. This requires centralized changes to the compiler options when building the entire archive. PIE has a large (5-10%) performance penalty on architectures with small numbers of general registers (e.g. x86), so it initially was only used for a select number of security-critical packages (some upstreams natively support building with PIE, other require the use of "hardening-wrapper" to force on the correct compiler and linker flags). PIE on 64-bit architectures do not have the same penalties, and it was made the default (as of 16.10, it is the default on amd64, ppc64el and s390x). As of 17.10, it was decided that the security benefits are significant enough that PIE is now enabled across all architectures in the Ubuntu archive by default.

See test-built-binaries.py for regression tests. 

Built with Fortify Source
-------------------------

Programs built with "-D_FORTIFY_SOURCE=2" (and -O1 or higher), enable several compile-time and run-time protections in glibc:

* expand unbounded calls to "sprintf", "strcpy" into their "n" length-limited cousins when the size of a destination buffer is known (protects against memory overflows).
* stop format string "%n" attacks when the format string is in a writable memory segment.
* require checking various important function return codes and arguments (e.g. system, write, open).
* require explicit file mask when creating new files. 

See test-gcc-security.py for regression tests. 

Built with RELRO
----------------

Hardens ELF programs against loader memory area overwrites by having the loader mark any areas of the relocation table as read-only for any symbols resolved at load-time ("read-only relocations"). This reduces the area of possible GOT-overwrite-style memory corruption attacks.

See test-gcc-security.py for regression tests. 

Built with BIND_NOW
-------------------

Marks ELF programs to resolve all dynamic symbols at start-up (instead of on-demand, also known as "immediate binding") so that the GOT can be made entirely read-only (when combined with RELRO above).

See test-built-binaries.py for regression tests. 

Built with -fstack-clash-protection
-----------------------------------

Adds extra instructions around variable length stack memory allocations (via alloca() or gcc variable length arrays etc) to probe each page of memory at allocation time. This mitigates stack-clash attacks by ensuring all stack memory allocations are valid (or by raising a segmentation fault if they are not, and turning a possible code-execution attack into a denial of service).

See test-built-binaries.py for regression tests. 

Built with -fcf-protection
--------------------------

Instructs the compiler to generate instructions to support Intel's Control-flow Enforcement Technology (CET).

See test-built-binaries.py for regression tests. 

Non-Executable Memory
---------------------

Most modern CPUs protect against executing non-executable memory regions (heap, stack, etc). This is known either as Non-eXecute (NX) or eXecute-Disable (XD), and some BIOS manufacturers needlessly disable it by default, so check your BIOS Settings. This protection reduces the areas an attacker can use to perform arbitrary code execution. It requires that the kernel use "PAE" addressing (which also allows addressing of physical addresses above 3GB). The 64bit and 32bit -server and -generic-pae kernels are compiled with PAE addressing. Starting in Ubuntu 9.10, this protection is partially emulated for processors lacking NX when running on a 32bit kernel (built with or without PAE). After booting, you can see what NX protection is in effect:

* Hardware-based (via PAE mode):

    [    0.000000] NX (Execute Disable) protection: active

* Partial Emulation (via segment limits):

    [    0.000000] Using x86 segment limits to approximate NX protection

If neither are seen, you do not have any NX protections enabled. Check your BIOS settings and CPU capabilities. If "nx" shows up in each of the "flags" lines in /proc/cpuinfo, it is enabled/supported by your hardware (and a PAE kernel is needed to actually use it).

Starting in Ubuntu 11.04, BIOS NX settings are ignored by the kernel. 

/proc/$pid/maps protection
--------------------------

With ASLR, a process's memory space layout suddenly becomes valuable to attackers. The "maps" file is made read-only except to the process itself or the owner of the process. Went into mainline kernel with sysctl toggle in 2.6.22. The toggle was made non-optional in 2.6.27, forcing the privacy to be enabled regardless of sysctl settings (this is a good thing).

See test-kernel-security.py for regression tests. 

ptrace scope
------------

A troubling weakness of the Linux process interfaces is that a single user is able to examine the memory and running state of any of their processes. For example, if one application was compromised, it would be possible for an attacker to attach to other running processes (e.g. SSH sessions, GPG agent, etc) to extract additional credentials and continue to immediately expand the scope of their attack without resorting to user-assisted phishing or trojans.

In Ubuntu 10.10 and later, users cannot ptrace processes that are not a descendant of the debugger. The behavior is controllable through the /proc/sys/kernel/yama/ptrace_scope sysctl, available via Yama.

In the case of automatic crash handlers, a crashing process can specficially allow an existing crash handler process to attach on a process-by-process basis using prctl(PR_SET_PTRACER, debugger_pid, 0, 0, 0).

See test-kernel-security.py for regression tests. 

0-address protection
--------------------

Since the kernel and userspace share virtual memory addresses, the "NULL" memory space needs to be protected so that userspace mmap'd memory cannot start at address 0, stopping "NULL dereference" kernel attacks. This is possible with 2.6.22 kernels, and was implemented with the "mmap_min_addr" sysctl setting. Since Ubuntu 9.04, the mmap_min_addr setting is built into the kernel. (64k for x86, 32k for ARM.)

See test-kernel-security.py for regression tests. 

/dev/mem protection
-------------------

Some applications (Xorg) need direct access to the physical memory from user-space. The special file /dev/mem exists to provide this access. In the past, it was possible to view and change kernel memory from this file if an attacker had root access. The CONFIG_STRICT_DEVMEM kernel option was introduced to block non-device memory access (originally named CONFIG_NONPROMISC_DEVMEM).

See test-kernel-security.py for regression tests. 

/dev/kmem disabled
-------------------

There is no modern user of /dev/kmem any more beyond attackers using it to load kernel rootkits. CONFIG_DEVKMEM is set to "n". While the /dev/kmem device node still exists in Ubuntu 8.04 LTS through Ubuntu 9.04, it is not actually attached to anything in the kernel.

See test-kernel-security.py for regression tests. 

Block module loading
---------------------

In Ubuntu 8.04 LTS and earlier, it was possible to remove CAP_SYS_MODULES from the system-wide capability bounding set, which would stop any new kernel modules from being loaded. This was another layer of protection to stop kernel rootkits from being installed. The 2.6.25 Linux kernel (Ubuntu 8.10) changed how bounding sets worked, and this functionality disappeared. Starting with Ubuntu 9.10, it is now possible to block module loading again by setting "1" in /proc/sys/kernel/modules_disabled.

See test-kernel-security.py for regression tests. 

Read-only data sections
-----------------------

This makes sure that certain kernel data sections are marked to block modification. This helps protect against some classes of kernel rootkits. Enabled via the CONFIG_DEBUG_RODATA option.

See test-kernel-security.py for configuration regression tests.

Stack protector
---------------

Similar to the stack protector used for ELF programs in userspace, the kernel can protect its internal stacks as well. Enabled via the CONFIG_CC_STACKPROTECTOR option.

See test-kernel-security.py for configuration regression tests. 

Module RO/NX
------------

This feature extends CONFIG_DEBUG_RODATA to include similar restrictions for loaded modules in the kernel. This can help resist future kernel exploits that depend on various memory regions in loaded modules. Enabled via the CONFIG_DEBUG_MODULE_RONX option.

See test-kernel-security.py for configuration regression tests. 

Kernel Address Display Restriction
----------------------------------

When attackers try to develop "run anywhere" exploits for kernel vulnerabilities, they frequently need to know the location of internal kernel structures. By treating kernel addresses as sensitive information, those locations are not visible to regular local users. Starting with Ubuntu 11.04, /proc/sys/kernel/kptr_restrict is set to "1" to block the reporting of known kernel address leaks. Additionally, various files and directories were made readable only by the root user: /boot/vmlinuz*, /boot/System.map*, /sys/kernel/debug/, /proc/slabinfo

See test-kernel-security.py for regression tests. 

Kernel Address Space Layout Randomisation
-----------------------------------------

Kernel Address Space Layout Randomisation (kASLR) aims to make some kernel exploits more difficult to implement by randomizing the base address value of the kernel. Exploits that rely on the locations of internal kernel symbols must discover the randomized base address.

kASLR is available starting with Ubuntu 14.10 and is enabled by default in 16.10 and later.

Before 16.10, you can specify the "kaslr" option on the kernel command line to use kASLR.

Note: Before 16.10, enabling kASLR will disable the ability to enter hibernation mode. 

Denylist Rare Protocols
-----------------------

Normally the kernel allows all network protocols to be autoloaded on demand via the MODULE_ALIAS_NETPROTO(PF_...) macros. Since many of these protocols are old, rare, or generally of little use to the average Ubuntu user and may contain undiscovered exploitable vulnerabilities, they have been denylisted since Ubuntu 11.04. These include: ax25, netrom, x25, rose, decnet, econet, rds, and af_802154. If any of the protocols are needed, they can speficially loaded via modprobe, or the /etc/modprobe.d/blacklist-rare-network.conf file can be updated to remove the denylist entry.

See test-kernel-security.py for regression tests. 

Syscall Filtering
-----------------

Programs can filter out the availability of kernel syscalls by using the seccomp_filter interface. This is done in containers or sandboxes that want to further limit the exposure to kernel interfaces when potentially running untrusted software.

See test-kernel-security.py for regression tests. 

dmesg restrictions
------------------

When attackers try to develop "run anywhere" exploits for vulnerabilties, they frequently will use dmesg output. By treating dmesg output as sensitive information, this output is not available to the attacker. Starting with Ubuntu 12.04 LTS, /proc/sys/kernel/dmesg_restrict can be set to "1" to treat dmesg output as sensitive. Starting with 20.10, this is enabled by default. 

Block kexec
-----------

Starting with Ubuntu 14.04 LTS, it is now possible to disable kexec via sysctl. CONFIG_KEXEC is enabled in Ubuntu so end users are able to use kexec as desired and the new sysctl allows administrators to disable kexec_load. This is desired in environments where CONFIG_STRICT_DEVMEM and modules_disabled are set, for example. When Secure Boot is in use, kexec is restricted by default to only load appropriately signed and trusted kernels. 

UEFI Secure Boot (amd64)
-------------------------

Starting with Ubuntu 12.04 LTS, UEFI Secure Boot was implemented in enforcing mode for the bootloader and non-enforcing mode for the kernel. With this configuration, a kernel that fails to verify will boot without UEFI quirks enabled. The Ubuntu 18.04.2 release of Ubuntu 18.04 LTS enabled enforcing mode for the bootloader and the kernel, so that kernels which fail to verify will not be booted, and kernel modules which fail to verify will not be loaded. This is planned to be backported for Ubuntu 16.04 LTS and Ubuntu 14.04 LTS (however only with kernel signature enforcement for Ubuntu 14.04 LTS, not kernel module signature enforcement). 

usbguard
--------

Starting with Ubuntu 16.10, the usbguard package has been available in universe to provide a tool for using the Linux kernel's USB authorization support, to control device IDs and device classes that will be recognized.

usbauth
-------

Starting with Ubuntu 18.04, the usbauth package has been available in universe to provide a tool for using the Linux kernel's USB authorization support, to control device IDs and device classes that will be recognized.

bolt
----

Starting with Ubuntu 18.04, the bolt package has been available in main to provide a desktop-oriented tool for using the Linux kernel's Thunderbolt authorization support. 

thunderbolt-tools
-----------------

Starting with Ubuntu 18.04, the thunderbolt-tools package has been available in universe to provide a server-oriented tool for using the Linux kernel's Thunderbolt authorization support. 

Kernel Lockdown
---------------

Starting with Ubuntu 20.04, the Linux kernel's lockdown mode is enabled in integrity mode. This prevents the root account from loading arbitrary modules or BPF programs that can manipulate kernel datastructures. Lockdown enforcement is tied to UEFI secure boot.



.. toctree::
   :maxdepth: 2
   
   secure-boot