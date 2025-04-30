Default compiler and linker flags
#################################

Built as PIE
============

All programs built as Position Independent Executables (PIE) with "-fPIE -pie" can take advantage of the exec ASLR. This protects against "return-to-text" and generally frustrates memory corruption attacks. This requires centralized changes to the compiler options when building the entire archive. PIE has a large (5-10%) performance penalty on architectures with small numbers of general registers (e.g. x86), so it initially was only used for a select number of security-critical packages (some upstreams natively support building with PIE, other require the use of "hardening-wrapper" to force on the correct compiler and linker flags). PIE on 64-bit architectures do not have the same penalties, and it was made the default (as of 16.10, it is the default on amd64, ppc64el and s390x). As of 17.10, it was decided that the security benefits are significant enough that PIE is now enabled across all architectures in the Ubuntu archive by default.

See test-built-binaries.py for regression tests. 
See `test-built-binaries.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-built-binaries.py>`_ for regression tests. 


Built with BIND_NOW
===================

Marks ELF programs to resolve all dynamic symbols at start-up (instead of on-demand, also known as "immediate binding") so that the GOT can be made entirely read-only (when combined with RELRO above).

See `test-built-binaries.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-built-binaries.py>`_ for regression tests. 


Built with -fcf-protection
==========================

Instructs the compiler to generate instructions to support Intel's Control-flow Enforcement Technology (CET).

See `test-built-binaries.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-built-binaries.py>`_ for regression tests. 


Built with Fortify Source
=========================

Programs built with "-D_FORTIFY_SOURCE=2" (and -O1 or higher), enable several compile-time and run-time protections in glibc:

* expand unbounded calls to "sprintf", "strcpy" into their "n" length-limited cousins when the size of a destination buffer is known (protects against memory overflows).
* stop format string "%n" attacks when the format string is in a writable memory segment.
* require checking various important function return codes and arguments (e.g. system, write, open).
* require explicit file mask when creating new files. 

See `test-gcc-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-gcc-security.py>`_ for regression tests. 


Built with -fstack-clash-protection
===================================

Adds extra instructions around variable length stack memory allocations (via alloca() or gcc variable length arrays etc) to probe each page of memory at allocation time. This mitigates stack-clash attacks by ensuring all stack memory allocations are valid (or by raising a segmentation fault if they are not, and turning a possible code-execution attack into a denial of service).

See `test-built-binaries.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-built-binaries.py>`_ for regression tests. 


Built with RELRO
================

Hardens ELF programs against loader memory area overwrites by having the loader mark any areas of the relocation table as read-only for any symbols resolved at load-time ("read-only relocations"). This reduces the area of possible GOT-overwrite-style memory corruption attacks.

See `test-gcc-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-gcc-security.py>`_ for regression tests. 


Stack Protector
===============

gcc's -fstack-protector provides a randomized stack canary that protects against stack overflows, and reduces the chances of arbitrary code execution via controlling return address destinations. Enabled at compile-time. (A small number of applications do not play well with it, and have it disabled.) The routines used for stack checking are actually part of glibc, but gcc is patched to enable linking against those routines by default.

See `test-gcc-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-gcc-security.py>`_ for regression tests. 


