Address Space Layout Randomization (ASLR)
#########################################

Address Space Layout Randomization (ASLR) is a security feature that randomizes
memory allocations. The randomization may be performed by the kernel or by the
ELF loader, depending on the type of ASLR. This makes it more difficult for
attackers to reliably predict or locate memory addresses when attempting to read
or corrupt memory.

It is one of the most widely deployed memory safety mitigations in modern
operating systems. On most modern Linux distributions, ASLR is enabled
by default.

Configuration
=============

ASLR is controlled system-wide by the value of ``/proc/sys/kernel/randomize_va_space``.

.. list-table:: ``/proc/sys/kernel/randomize_va_space`` values
   :widths: 15 85
   :header-rows: 1

   * - Value
     - Meaning
   * - 0
     - ASLR is off.
   * - 1
     - Partial ASLR. The addresses of stack, mmap base and vDSO page are randomized.
       This is the default if the ``CONFIG_COMPAT_BRK`` option is enabled.
   * - 2 (default for most systems)
     - Full ASLR. Additionally enable heap randomization.
       This is the default if ``CONFIG_COMPAT_BRK`` is disabled.

To temporarily change the value, it can be done via the ``proc`` file system::

   echo 1 > /proc/sys/kernel/randomize_va_space

Or via ``sysctl``::

   sysctl -w kernel.randomize_va_space=1

To make it persistent across reboots, add a line to a config file in ``/etc/sysctl.d/``. For example,::

   echo "kernel.randomize_va_space=1" | sudo tee /etc/sysctl.d/aslr.conf

.. _types-of-aslr:

Types of ASLR
=============

See `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__ for regression tests for all the different types of ASLR.

.. _stack-aslr:

Stack ASLR
~~~~~~~~~~

Each execution of a program results in a different stack memory space layout.

This makes it harder to locate in memory where to attack or deliver an
executable attack payload.

.. _mmap-aslr:

Libs/mmap ASLR
~~~~~~~~~~~~~~

Each execution of a program results in a different ``mmap`` memory space layout.

It causes the dynamically loaded libraries to get loaded into different
locations each time. This makes it harder to locate in memory where to jump to
for "return-to-libc" to similar attacks.

.. _exec-aslr:

Exec ASLR
~~~~~~~~~

Each execution of a program that has been built with "-fPIE -pie"
(see :ref:`Built as PIE <compiler-flags-pie>`) will get loaded into a different memory location.


This makes it harder to locate in memory where to attack or jump to when
performing memory-corruption-based attacks.

.. _brk-aslr:

``brk`` ASLR
~~~~~~~~~~~~

Small ``malloc`` allocations are served from the program break (``brk``)
segment. Randomizing the gap between the ``exec`` region and ``brk`` makes it
harder to locate in memory where to attack or jump to.

.. _vdso-aslr:

vDSO ASLR
~~~~~~~~~

Each execution of a program results in a random vDSO location.

The vDSO (Virtual Dynamic Shared Object) offers a selected set of kernel space
routines (e.g. ``gettimeofday``) to user space applications to improve
performance. Randomizing the address avoids "jump-into-syscall" attacks.

.. _further-reading-for-aslr:

Further reading for ASLR
========================

* `vdso: -V3 <https://lwn.net/Articles/184734/>`_
* `randomize_va_space in the Linux kernel documentation <https://docs.kernel.org/admin-guide/sysctl/kernel.html#randomize-va-space>`_
* `Address space randomization in 2.6 <https://lwn.net/Articles/121845/>`_
* `On vsyscalls and the vDSO <https://lwn.net/Articles/446528/>`_