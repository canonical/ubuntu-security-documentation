Default compiler and linker flags
#################################

.. _compiler-flags-pie:

Built as PIE
============

Programs built as Position Independent Executables (PIE) with ``-fPIE -pie``
take advantage of exec ASLR. This protects against "return-to-text" attacks and
generally frustrates memory corruption attacks. This required centralized
changes to the compiler options when building the entire archive.

PIE incurs a large (5-10%) performance penalty on architectures with small
numbers of general registers (such as x86), so we initially used it only for a
select number of security-critical packages. Some upstreams natively support
building with PIE, while others require the use of ``hardening-wrapper`` to
force the correct compiler and linker flags.

PIE on 64-bit architectures doesn't have the same penalties. We made it the
default on amd64, ppc64el, and s390x as of Ubuntu 16.10 (Yakkety Yak). As of
Ubuntu 17.10 (Artful Aardvark), we decided that the security benefits are
significant enough to enable PIE across all architectures in the Ubuntu archive
by default.

See `test-built-binaries.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-built-binaries.py>`_
for regression tests.


Built with BIND_NOW
===================

This marks ELF programs to resolve all dynamic symbols at start-up (instead of
on-demand, also known as "immediate binding"). This allows the Global Offset
Table (GOT) to be made entirely read-only (when combined with RELRO).

See `test-built-binaries.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-built-binaries.py>`_
for regression tests.


Built with -fcf-protection
==========================

This instructs the compiler to generate instructions to support Intel's
Control-flow Enforcement Technology (CET).

See `test-built-binaries.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-built-binaries.py>`_
for regression tests.


Built with Fortify Source
=========================

Building programs with ``-D_FORTIFY_SOURCE=2`` (and ``-O1`` or higher) enables
several compile-time and run-time protections in glibc:

* Expands unbounded calls to ``sprintf`` and ``strcpy`` into their "n"
  length-limited cousins when the size of a destination buffer is known
  (protects against memory overflows).
* Stops format string ``%n`` attacks when the format string is in a writable
  memory segment.
* Requires checking various important function return codes and arguments (for
  example, ``system``, ``write``, ``open``).
* Requires an explicit file mask when creating new files.

See `test-gcc-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-gcc-security.py>`_
for regression tests.


Built with -fstack-clash-protection
===================================

This adds extra instructions around variable-length stack memory allocations
(via ``alloca()`` or GCC variable-length arrays) to probe each page of memory
at allocation time. This mitigates stack-clash attacks by ensuring all stack
memory allocations are valid. If they aren't, it raises a segmentation fault,
turning a possible code-execution attack into a denial of service.

See `test-built-binaries.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-built-binaries.py>`_
for regression tests.


Built with RELRO
================

This hardens ELF programs against loader memory area overwrites. The loader
marks any areas of the relocation table as read-only for any symbols resolved
at load-time ("read-only relocations"). This reduces the area of possible
GOT-overwrite-style memory corruption attacks.

See `test-gcc-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-gcc-security.py>`_
for regression tests.


Stack protector
===============

GCC's ``-fstack-protector`` provides a randomized stack canary that protects
against stack overflows and reduces the chances of arbitrary code execution via
controlling return address destinations. This is enabled at compile-time. (A
small number of applications don't play well with it and have it disabled.) The
routines used for stack checking are part of glibc, but GCC is patched to
enable linking against those routines by default.

See `test-gcc-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-gcc-security.py>`_
for regression tests.
