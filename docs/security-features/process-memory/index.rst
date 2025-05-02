Process and memory protections
##############################

Ubuntu provides a set of security features that protect userspace processes at runtime.

Default compiler flags
======================

.. toctree::
   :maxdepth: 2
   :glob:

   compiler-flags


File handling protections
=========================

.. toctree::
   :maxdepth: 2
   :glob:

   file-handling


Address Space Layout Randomisation (ASLR)
=========================================

ASLR is implemented by the kernel and the ELF loader by randomising the location of memory allocations (stack, heap, shared libraries, etc). This makes memory addresses harder to predict when an attacker is attempting a memory-corruption exploit. ASLR is controlled system-wide by the value of /proc/sys/kernel/randomize_va_space. Prior to Ubuntu 8.10, this defaulted to "1" (on). In later releases that included brk ASLR, it defaults to "2" (on, with brk ASLR).

See `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_ for regression tests for all the different types of ASLR. 

Stack ASLR
~~~~~~~~~~

Each execution of a program results in a different stack memory space layout. This makes it harder to locate in memory where to attack or deliver an executable attack payload. This was available in the mainline kernel since 2.6.15 (Ubuntu 6.06).

VDSO ASLR
~~~~~~~~~

Each execution of a program results in a random vdso location. While this has existed in the mainline kernel since 2.6.18 (x86, PPC) and 2.6.22 (x86_64), it hadn't been enabled in Ubuntu 6.10 due to COMPAT_VDSO being enabled, which was removed in Ubuntu 8.04 LTS. This protects against jump-into-syscall attacks. Only x86 (maybe ppc?) is supported by glibc 2.6. glibc 2.7 (Ubuntu 8.04 LTS) supports x86_64 ASLR vdso. People needing ancient pre-libc6 static high vdso mappings can use "vdso=2" on the kernel boot command line to gain COMPAT_VDSO again. 

* https://lwn.net/Articles/184734/

* https://articles.manugarg.com/systemcallinlinux2_6.html

Libs/mmap ASLR
~~~~~~~~~~~~~~

Each execution of a program results in a different mmap memory space layout (which causes the dynamically loaded libraries to get loaded into different locations each time). This makes it harder to locate in memory where to jump to for "return to libc" to similar attacks. This was available in the mainline kernel since 2.6.15 (Ubuntu 6.06).

Exec ASLR
~~~~~~~~~

Each execution of a program that has been built with "-fPIE -pie" will get loaded into a different memory location. This makes it harder to locate in memory where to attack or jump to when performing memory-corruption-based attacks. This was available in the mainline kernel since 2.6.25 (and was backported to Ubuntu 8.04 LTS).

brk ASLR
~~~~~~~~

Similar to exec ASLR, brk ASLR adjusts the memory locations relative between the exec memory area and the brk memory area (for small mallocs). The randomization of brk offset from exec memory was added in 2.6.26 (Ubuntu 8.10), though some of the effects of brk ASLR can be seen for PIE programs in Ubuntu 8.04 LTS since exec was ASLR, and brk is allocated immediately after the exec region (so it was technically randomized, but not randomized with respect to the text region until 8.10).


0-address protection
====================

Since the kernel and userspace share virtual memory addresses, the "NULL" memory space needs to be protected so that userspace mmap'd memory cannot start at address 0, stopping "NULL dereference" kernel attacks. This is possible with 2.6.22 kernels, and was implemented with the "mmap_min_addr" sysctl setting. Since Ubuntu 9.04, the mmap_min_addr setting is built into the kernel. (64k for x86, 32k for ARM.)

See test-kernel-security.py for regression tests. 


/dev/mem protection
===================

Some applications (Xorg) need direct access to the physical memory from user-space. The special file /dev/mem exists to provide this access. In the past, it was possible to view and change kernel memory from this file if an attacker had root access. The CONFIG_STRICT_DEVMEM kernel option was introduced to block non-device memory access (originally named CONFIG_NONPROMISC_DEVMEM).

See `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_ for regression tests. 


/proc/$pid/maps protection
==========================

With ASLR, a process's memory space layout suddenly becomes valuable to attackers. The "maps" file is made read-only except to the process itself or the owner of the process. Went into mainline kernel with sysctl toggle in 2.6.22. The toggle was made non-optional in 2.6.27, forcing the privacy to be enabled regardless of sysctl settings (this is a good thing).

See `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_ for regression tests. 


ptrace scope
============

A troubling weakness of the Linux process interfaces is that a single user is able to examine the memory and running state of any of their processes. For example, if one application was compromised, it would be possible for an attacker to attach to other running processes (e.g. SSH sessions, GPG agent, etc) to extract additional credentials and continue to immediately expand the scope of their attack without resorting to user-assisted phishing or trojans.

In Ubuntu 10.10 and later, users cannot ptrace processes that are not a descendant of the debugger. The behavior is controllable through the /proc/sys/kernel/yama/ptrace_scope sysctl, available via Yama.

In the case of automatic crash handlers, a crashing process can specficially allow an existing crash handler process to attach on a process-by-process basis using prctl(PR_SET_PTRACER, debugger_pid, 0, 0, 0).

See `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_ for regression tests. 


Non-Executable Memory
=====================

Most modern CPUs protect against executing non-executable memory regions (heap, stack, etc). This is known either as Non-eXecute (NX) or eXecute-Disable (XD), and some BIOS manufacturers needlessly disable it by default, so check your BIOS Settings. This protection reduces the areas an attacker can use to perform arbitrary code execution. It requires that the kernel use "PAE" addressing (which also allows addressing of physical addresses above 3GB). The 64bit and 32bit -server and -generic-pae kernels are compiled with PAE addressing. Starting in Ubuntu 9.10, this protection is partially emulated for processors lacking NX when running on a 32bit kernel (built with or without PAE). After booting, you can see what NX protection is in effect:

* Hardware-based (via PAE mode):

    [    0.000000] NX (Execute Disable) protection: active

* Partial Emulation (via segment limits):

    [    0.000000] Using x86 segment limits to approximate NX protection

If neither are seen, you do not have any NX protections enabled. Check your BIOS settings and CPU capabilities. If "nx" shows up in each of the "flags" lines in /proc/cpuinfo, it is enabled/supported by your hardware (and a PAE kernel is needed to actually use it).

Starting in Ubuntu 11.04, BIOS NX settings are ignored by the kernel. 


Pointer Obfuscation
===================

Some pointers stored in glibc are obfuscated via PTR_MANGLE/PTR_UNMANGLE macros internally in glibc, preventing libc function pointers from being overwritten during runtime.

See `test-glibc-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-glibc-security.py>`_ for regression tests. 


Heap Protector
==============

The GNU C Library heap protector (both automatic via ptmalloc and manual) provides corrupted-list/unlink/double-free/overflow protections to the glibc heap memory manager (first introduced in glibc 2.3.4). This stops the ability to perform arbitrary code execution via heap memory overflows that try to corrupt the control structures of the malloc heap memory areas.

This protection has evolved over time, adding more and more protections as additional corner-cases were researched. As it currently stands, glibc 2.10 and later appears to successfully resist even these hard-to-hit conditions.

See `test-glibc-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-glibc-security.py>`_ for regression tests. 

