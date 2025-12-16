Process and memory protections
##############################

Ubuntu provides a set of security features that protect userspace processes at
runtime.


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

The kernel and the ELF loader implement ASLR by randomizing the location of
memory allocations (stack, heap, shared libraries, and so on). This makes
memory addresses harder to predict when an attacker attempts a
memory-corruption exploit. ASLR is controlled system-wide by the value of
``/proc/sys/kernel/randomize_va_space``. Prior to Ubuntu 8.10 (Intrepid
Ibex), this defaulted to "1" (on). In later releases that included ``brk``
ASLR, it defaults to "2" (on, with ``brk`` ASLR).

See `test-kernel-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_
for regression tests for all the different types of ASLR.

Stack ASLR
----------

Each execution of a program results in a different stack memory space layout.
This makes it harder to locate where to attack or deliver an executable attack
payload in memory. This has been available in the mainline kernel since 2.6.15
(Ubuntu 6.06 LTS (Dapper Drake)).

vDSO ASLR
---------

Each execution of a program results in a random vDSO location. While this has
existed in the mainline kernel since 2.6.18 (x86, PPC) and 2.6.22 (x86_64), it
wasn't enabled in Ubuntu 6.10 due to ``COMPAT_VDSO`` being enabled, which was
removed in Ubuntu 8.04 LTS (Hardy Heron). This protects against
jump-into-syscall attacks. Only x86 (maybe ppc?) is supported by glibc 2.6.
glibc 2.7 (Ubuntu 8.04 LTS) supports x86_64 ASLR vDSO. If you need ancient
pre-libc6 static high vDSO mappings, you can use "vdso=2" on the kernel boot
command line to gain ``COMPAT_VDSO`` again.

* https://lwn.net/Articles/184734/
* https://articles.manugarg.com/systemcallinlinux2_6.html

Libs/mmap ASLR
--------------

Each execution of a program results in a different ``mmap`` memory space layout
(which causes the dynamically loaded libraries to load into different locations
each time). This makes it harder to locate where to jump to in memory for
"return to libc" or similar attacks. This has been available in the mainline
kernel since 2.6.15 (Ubuntu 6.06 LTS).

Exec ASLR
---------

Each execution of a program built with ``-fPIE -pie`` loads into a different
memory location. This makes it harder to locate where to attack or jump to in
memory when performing memory-corruption-based attacks. This has been available
in the mainline kernel since 2.6.25 (and was backported to Ubuntu 8.04 LTS).

brk ASLR
--------

Similar to exec ASLR, ``brk`` ASLR adjusts the memory locations relative
between the exec memory area and the ``brk`` memory area (for small mallocs).
The randomization of the ``brk`` offset from exec memory was added in 2.6.26
(Ubuntu 8.10), though some effects of ``brk`` ASLR can be seen for PIE programs
in Ubuntu 8.04 LTS since exec was ASLR, and ``brk`` is allocated immediately
after the exec region (so it was technically randomized, but not randomized
with respect to the text region until 8.10).


0-address protection
====================

Since the kernel and userspace share virtual memory addresses, the "NULL"
memory space needs protection so that userspace ``mmap``'d memory cannot start
at address 0. This stops "NULL dereference" kernel attacks. This became
possible with 2.6.22 kernels and was implemented with the ``mmap_min_addr``
sysctl setting. Since Ubuntu 9.04 (Jaunty Jackalope), the ``mmap_min_addr``
setting is built into the kernel (64k for x86, 32k for ARM).

See ``test-kernel-security.py`` for regression tests.


/dev/mem protection
===================

Some applications (Xorg) need direct access to physical memory from user-space.
The special file ``/dev/mem`` exists to provide this access. In the past, an
attacker with root access could view and change kernel memory from this file.
The ``CONFIG_STRICT_DEVMEM`` kernel option was introduced to block non-device
memory access (originally named ``CONFIG_NONPROMISC_DEVMEM``).

See `test-kernel-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_
for regression tests.


/proc/$pid/maps protection
==========================

With ASLR, a process's memory space layout becomes valuable to attackers. The
``maps`` file is read-only except to the process itself or the owner of the
process. This went into the mainline kernel with a sysctl toggle in 2.6.22. The
toggle became non-optional in 2.6.27, forcing the privacy to be enabled
regardless of sysctl settings.

See `test-kernel-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_
for regression tests.


ptrace scope
============

A weakness of the Linux process interfaces is that a single user can examine
the memory and running state of any of their processes. For example, if one
application is compromised, an attacker could attach to other running processes
(such as SSH sessions, GPG agent) to extract additional credentials and
immediately expand the scope of their attack without resorting to user-assisted
phishing or trojans.

In Ubuntu 10.10 (Maverick Meerkat) and later, users cannot ptrace processes
that aren't a descendant of the debugger. You can control this behavior through
the ``/proc/sys/kernel/yama/ptrace_scope`` sysctl, available via Yama.

In the case of automatic crash handlers, a crashing process can specifically
allow an existing crash handler process to attach on a process-by-process basis
using ``prctl(PR_SET_PTRACER, debugger_pid, 0, 0, 0)``.

See `test-kernel-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_
for regression tests.


Non-executable memory
=====================

Most modern CPUs protect against executing non-executable memory regions (heap,
stack, and so on). This is known either as Non-eXecute (NX) or eXecute-Disable
(XD). Some BIOS manufacturers disable it by default, so check your BIOS
settings. This protection reduces the areas an attacker can use to perform
arbitrary code execution. It requires that the kernel use "PAE" addressing
(which also allows addressing of physical addresses above 3GB). The 64-bit and
32-bit ``-server`` and ``-generic-pae`` kernels are compiled with PAE
addressing. Starting in Ubuntu 9.10 (Karmic Koala), this protection is
partially emulated for processors lacking NX when running on a 32-bit kernel
(built with or without PAE). After booting, you can see what NX protection is
in effect:

* Hardware-based (via PAE mode):

  .. code-block:: text

     [    0.000000] NX (Execute Disable) protection: active

* Partial Emulation (via segment limits):

  .. code-block:: text

     [    0.000000] Using x86 segment limits to approximate NX protection

If you see neither, you don't have any NX protections enabled. Check your BIOS
settings and CPU capabilities. If "nx" shows up in each of the "flags" lines in
``/proc/cpuinfo``, it is enabled/supported by your hardware (and a PAE kernel
is needed to actually use it).

Starting in Ubuntu 11.04 (Natty Narwhal), the kernel ignores BIOS NX settings.


Pointer obfuscation
===================

Some pointers stored in glibc are obfuscated via ``PTR_MANGLE``/``PTR_UNMANGLE``
macros internally in glibc, preventing libc function pointers from being
overwritten during runtime.

See `test-glibc-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-glibc-security.py>`_
for regression tests.


Heap protector
==============

The GNU C Library heap protector (both automatic via ``ptmalloc`` and manual)
provides corrupted-list/unlink/double-free/overflow protections to the glibc
heap memory manager (first introduced in glibc 2.3.4). This stops the ability
to perform arbitrary code execution via heap memory overflows that try to
corrupt the control structures of the malloc heap memory areas.

This protection has evolved over time, adding more protections as additional
corner cases were researched. As it currently stands, glibc 2.10 and later
successfully resists even these hard-to-hit conditions.

See `test-glibc-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-glibc-security.py>`_
for regression tests.
