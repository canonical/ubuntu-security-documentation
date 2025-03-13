\__NOTOC\_\_

Features
========

.. _configuration:

Configuration
-------------


.. _ports:

No Open Ports
~~~~~~~~~~~~~

<<Include(`SecurityTeam <SecurityTeam>`__/Policies, , from="== No Open
Ports ==", to="==")>>

Testing for this can be done with \`netstat -an --inet \| grep LISTEN \|
grep -v 127.0.0.1:\` on a fresh install.


.. _hashing:

Password hashing
~~~~~~~~~~~~~~~~

The system password used for logging into Ubuntu is stored in
/etc/shadow. Very old style password hashes were based on DES and
visible in /etc/passwd. Modern Linux has long since moved to
/etc/shadow, and for some time now has used salted MD5-based hashes for
password verification (crypt id 1). Since MD5 is considered "broken" for
some uses and as computational power available to perform brute-forcing
of MD5 increases, Ubuntu 8.10 and later proactively moved to using
salted SHA-512 based password hashes (crypt id 6), which are orders of
magnitude more difficult to brute-force. Ubuntu 22.04 LTS and later then
moved to yescrypt to provide increased protection against offline
password cracking. See the `crypt <Manpage:crypt>`__ manpage for
additional details.

See
`test-glibc-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-glibc-security.py>`__
for regression tests.


.. _syn-cookies:

SYN cookies
~~~~~~~~~~~

When a system is overwhelmed by new network connections, SYN cookie use
is activated, which helps mitigate a SYN-flood attack.

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for configuration regression tests.


.. _unattended-upgrades:

Automatic security updates
~~~~~~~~~~~~~~~~~~~~~~~~~~

Starting with Ubuntu 16.04 LTS, unattended-upgrades is configured to
automatically apply security updates daily. Earlier Ubuntu releases can
be
`configured <https://help.ubuntu.com/14.04/serverguide/automatic-updates.html>`__
to automatically apply security updates.


.. _kernel-livepatches:

Kernel Livepatches
~~~~~~~~~~~~~~~~~~

The `Canonical Livepatch
service <https://www.ubuntu.com/server/livepatch>`__ provides security
fixes for most major kernel security issues without requiring a reboot.
Ubuntu users can take advantage of the service on up to three nodes for
free. All machines covered by an Ubuntu Advantage support subscription
are able to receive livepatches.


.. _disable-legacy-tls:

Disable legacy TLS
~~~~~~~~~~~~~~~~~~

Legacy versions of the Transport Layer Security protocol including SSL
3.0, TLS 1.0 and TLS 1.1, have several inherent vulnerabilities and
cannot provide the advertised level of security. For that Ubuntu 20.04
and later proactively disable these versions setting the bar of secure
communication to protocols that are considered secure today.

To communicate with legacy systems it is possible to re-enable the
protocols. See `this discourse
article <https://discourse.ubuntu.com/t/default-to-tls-v1-2-in-all-tls-libraries-in-20-04-lts/12464/8>`__
for more information.

.. _subsystems:

Subsystems
----------


.. _fscaps:

Filesystem Capabilities
~~~~~~~~~~~~~~~~~~~~~~~

The need for setuid applications can be reduced via the application of
`filesystem
capabilities <http://www.olafdietsche.de/linux/capability/>`__ using the
xattrs available to most modern filesystems. This reduces the possible
misuse of vulnerable setuid applications. The kernel provides the
support, and the user-space tools are in main ("libcap2-bin").

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for configuration regression tests.


.. _firewall:

Configurable Firewall
~~~~~~~~~~~~~~~~~~~~~

`ufw <UbuntuFirewall>`__ is a frontend for iptables, and is installed by
default in Ubuntu (users must explicitly enable it). Particularly
well-suited for host-based firewalls, ufw provides a framework for
managing a netfilter firewall, as well as a command-line interface for
manipulating the firewall. ufw aims to provide an easy to use interface
for people unfamiliar with firewall concepts, while at the same time
simplifies complicated iptables commands to help an administrator who
knows what he or she is doing. ufw is an upstream for other
distributions and graphical frontends.

See `ufw
tests <https://bazaar.launchpad.net/~jdstrand/ufw/trunk/files>`__ for
regression tests.


.. _prng-cloud:

Cloud PRNG seed
~~~~~~~~~~~~~~~

`Pollinate <https://bazaar.launchpad.net/~kirkland/pollen/trunk/view/head:/README>`__
is a client application that retrieves entropy from one or more Pollen
servers and seeds the local Pseudo Random Number Generator (PRNG).
Pollinate is designed to adequately and securely seed the PRNG through
communications with a Pollen server which is particularly important for
systems operating in cloud environments. Starting with Ubuntu 14.04 LTS,
Ubuntu cloud images include the Pollinate client, which will try to seed
the PRNG with input from https://entropy.ubuntu.com for up to 3 seconds
on first boot.

See
`pollen_test.go <https://bazaar.launchpad.net/~kirkland/pollen/trunk/view/head:/pollen_test.go>`__
for regression tests

.. _seccomp:

PR_SET_SECCOMP
~~~~~~~~~~~~~~

Setting `SECCOMP <https://lwn.net/Articles/332974/>`__ for a process is
meant to confine it to a small subsystem of system calls, used for
specialized processing-only programs.

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for regression tests.


.. _mac:

Mandatory Access Control (MAC)
------------------------------

Mandatory Access Controls are handled via the kernel LSM hooks.


.. _apparmor:

`AppArmor <AppArmor>`__
~~~~~~~~~~~~~~~~~~~~~~~

`AppArmor <https://help.ubuntu.com/community/AppArmor>`__ is a
path-based MAC. It can mediate:

-  file access (read, write, link, lock)
-  library loading
-  execution of applications
-  coarse-grained network (protocol, type, domain)
-  capabilities
-  coarse owner checks (task must have the same euid/fsuid as the object
   being checked) starting with Ubuntu 9.10
-  mount starting with Ubuntu 12.04 LTS
-  unix(7) named sockets starting with Ubuntu 13.10
-  DBus API (path, interface, method) starting with Ubuntu 13.10
-  signal(7) starting with Ubuntu 14.04 LTS
-  ptrace(2) starting with Ubuntu 14.04 LTS
-  unix(7) abstract and anonymous sockets starting with Ubuntu 14.10

`AppArmor <AppArmor>`__ is a core technology for application confinement
for `Ubuntu
Touch <https://wiki.ubuntu.com/SecurityTeam/Specifications/ApplicationConfinement>`__
and `Snappy for Ubuntu Core and
Personal <https://developer.ubuntu.com/en/snappy/guides/security-policy/>`__.

Example profiles are found in the apparmor-profiles package from
universe, and by-default shipped `enforcing
profiles <SecurityTeam/KnowledgeBase/AppArmorProfiles>`__ are being
built up:

<<Include(`SecurityTeam/KnowledgeBase/AppArmorProfiles <SecurityTeam/KnowledgeBase/AppArmorProfiles>`__,
, from="=== Supported profiles in main ===", to="===")>>

Starting with Ubuntu 16.10, `AppArmor <AppArmor>`__ can "stack" profiles
so that the mediation decisions are made using the intersection of
multiple profiles. This feature, combined with `AppArmor <AppArmor>`__
profile namespaces, allows `LXD <https://linuxcontainers.org/lxd/>`__ to
define a profile that an entire container will be confined with while
still allowing individual, containerized processes to be further
confined with profiles loaded inside of the container environment.

See
`test-apparmor.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-apparmor.py>`__
and
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for regression tests.


.. _apparmor-unprivileged-userns-restrictions:

`AppArmor <AppArmor>`__ unprivileged user namespace restrictions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Starting with Ubuntu 23.10, `AppArmor <AppArmor>`__ provides support for
denying unprivileged applications the use of user namespaces. This
prevents an unprivileged application from making use of a user namespace
to gain access to additional capabilities and various kernel subsystems
which present an additional attack surface. Applications which do
require legitimate unprivileged access to user namespaces are designated
by an appropriate `AppArmor <AppArmor>`__ profile. Starting with Ubuntu
24.04 this is enabled by default.

See
`test-apparmor.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-apparmor.py>`__
for regression tests.

.. _selinux:

SELinux
~~~~~~~

`SELinux <SELinux>`__ is an inode-based MAC. Targeted policies are
available for Ubuntu in universe. Installing the "selinux" package will
make the boot-time adjustments that are needed.

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for configuration regression tests.


.. _smack:

SMACK
~~~~~

SMACK is a flexible inode-based MAC.

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for configuration regression tests.


.. _encryption:

Storage Encryption
------------------


.. _encrypted-lvm:

Encrypted LVM
~~~~~~~~~~~~~

Ubuntu 12.10 and newer include the ability to install Ubuntu onto an
encrypted LVM, which allows all partitions in the logical volume,
including swap, to be encrypted. Between 6.06 LTS and 12.04 LTS the
alternate installer can install to an encrypted LVM.


.. _encrypted-files:

File Encryption
~~~~~~~~~~~~~~~

Encrypted Private Directories were implemented, utilizing
`eCryptfs <https://ecryptfs.org/>`__, in Ubuntu 8.10 as a secure
location for users to store sensitive information. The server and
alternate installers had the option to setup an encrypted private
directory for the first user. In Ubuntu 9.04, support for encrypted home
and filename encryption was added. Encrypted Home allowed users to
encrypt all files in their home directory and was supported in the
Alternate Installer and also in the Desktop Installer via the preseed
option \`user-setup/encrypt-home=true\`.

Official support for Encrypted Private and Encrypted Home directories
was dropped in Ubuntu 18.04 LTS. It is still possible to configure an
encrypted private or home directory, after Ubuntu is installed, with the
\`ecryptfs-setup-private\` utility provided by the \`ecryptfs-utils\`
package.

Starting in Ubuntu 18.04 LTS, it is also possible to install and use
`fscrypt <https://github.com/google/fscrypt>`__ to encrypt directories
on ext4 filesystems. Note that fscrypt is not officially supported but
is available via the fscrypt package in universe.


.. _TPM:

Trusted Platform Module
-----------------------

TPM 1.2 support was added in Ubuntu 7.10. "tpm-tools" and related
libraries are available in Ubuntu universe. For TPM 2.0, tpm2-tools is
available in Ubuntu universe.


.. _userspace-hardening:

Userspace Hardening
-------------------

Many security features are available through the default `compiler
flags <CompilerFlags>`__ used to build packages and through the kernel
in Ubuntu. **Note:** Ubuntu's compiler hardening applies not only to its
official builds but also anything built on Ubuntu using its compiler.


.. _stack-protector:

Stack Protector
~~~~~~~~~~~~~~~

gcc's -fstack-protector provides a randomized stack canary that protects
against stack overflows, and reduces the chances of arbitrary code
execution via controlling return address destinations. Enabled at
compile-time. (A small number of applications do not play well with it,
and have it disabled.) The routines used for stack checking are actually
part of glibc, but gcc is patched to enable linking against those
routines by default.

See
`test-gcc-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-gcc-security.py>`__
for regression tests.


.. _heap-protector:

Heap Protector
~~~~~~~~~~~~~~

The GNU C Library heap protector (both automatic via
`ptmalloc <http://www.malloc.de/en/>`__ and
`manual <https://www.gnu.org/s/libc/manual/html_node/Heap-Consistency-Checking.html>`__)
provides corrupted-list/unlink/double-free/overflow protections to the
glibc heap memory manager (first introduced in glibc 2.3.4). This stops
the ability to perform arbitrary code execution via heap memory
overflows that try to corrupt the control structures of the malloc heap
memory areas.

This protection has evolved over time, adding more and more protections
as additional `corner-cases were
researched <http://www.phrack.com/issues.html?issue=66&id=10#article>`__.
As it currently stands, glibc 2.10 and later appears to successfully
resist even these hard-to-hit conditions.

See
`test-glibc-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-glibc-security.py>`__
for regression tests.


.. _pointer-obfuscation:

Pointer Obfuscation
~~~~~~~~~~~~~~~~~~~

Some `pointers stored in glibc are
obfuscated <https://udrepper.livejournal.com/13393.html>`__ via
PTR_MANGLE/PTR_UNMANGLE macros internally in glibc, preventing libc
function pointers from being overwritten during runtime.

See
`test-glibc-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-glibc-security.py>`__
for regression tests.


.. _aslr:

Address Space Layout Randomisation (ASLR)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ASLR is implemented by the kernel and the ELF loader by randomising the
location of memory allocations (stack, heap, shared libraries, etc).
This makes memory addresses harder to predict when an attacker is
attempting a memory-corruption exploit. ASLR is controlled system-wide
by the value of ``/proc/sys/kernel/randomize_va_space``. Prior to Ubuntu
8.10, this defaulted to "1" (on). In later releases that included brk
ASLR, it defaults to "2" (on, with brk ASLR).

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for regression tests for all the different types of ASLR.


.. _stack-aslr:

Stack ASLR
^^^^^^^^^^

Each execution of a program results in a different stack memory space
layout. This makes it harder to locate in memory where to attack or
deliver an executable attack payload. This was available in the mainline
kernel since 2.6.15 (Ubuntu 6.06).


.. _mmap-aslr:

Libs/mmap ASLR
^^^^^^^^^^^^^^

Each execution of a program results in a different mmap memory space
layout (which causes the dynamically loaded libraries to get loaded into
different locations each time). This makes it harder to locate in memory
where to jump to for "return to libc" to similar attacks. This was
available in the mainline kernel since 2.6.15 (Ubuntu 6.06).


.. _exec-aslr:

Exec ASLR
^^^^^^^^^

Each execution of a program that has been built with "-fPIE -pie" will
get loaded into a different memory location. This makes it harder to
locate in memory where to attack or jump to when performing
memory-corruption-based attacks. This was available in the mainline
kernel since 2.6.25 (and was backported to Ubuntu 8.04 LTS).


.. _brk-aslr:

brk ASLR
^^^^^^^^

Similar to exec ASLR, brk ASLR adjusts the memory locations relative
between the exec memory area and the brk memory area (for small
mallocs). The randomization of brk offset from exec memory was added in
2.6.26 (Ubuntu 8.10), though some of the effects of brk ASLR can be seen
for PIE programs in Ubuntu 8.04 LTS since exec was ASLR, and brk is
allocated immediately after the exec region (so it was technically
randomized, but not randomized with respect to the text region until
8.10).


.. _vdso-aslr:

VDSO ASLR
^^^^^^^^^

Each execution of a program results in a random vdso location. While
this has existed in the mainline kernel since 2.6.18 (x86, PPC) and
2.6.22 (x86_64), it hadn't been enabled in Ubuntu 6.10 due to
COMPAT_VDSO being enabled, which was removed in Ubuntu 8.04 LTS. This
protects against jump-into-syscall attacks. Only x86 (maybe ppc?) is
supported by glibc 2.6. glibc 2.7 (Ubuntu 8.04 LTS) supports x86_64 ASLR
vdso. People needing ancient pre-libc6 static high vdso mappings can use
"vdso=2" on the kernel boot command line to gain COMPAT_VDSO again.

-  https://lwn.net/Articles/184734/
-  https://articles.manugarg.com/systemcallinlinux2_6.html


.. _pie:

Built as PIE
~~~~~~~~~~~~

All programs built as Position Independent Executables (PIE) with "-fPIE
-pie" can take advantage of the exec ASLR. This protects against
"return-to-text" and generally frustrates memory corruption attacks.
This requires centralized changes to the compiler options when building
the entire archive. PIE has a large (5-10%) performance penalty on
architectures with small numbers of general registers (e.g. x86), so it
initially was only used for a `select number of security-critical
packages <SecurityTeam/KnowledgeBase/BuiltPIE>`__ (some upstreams
natively support building with PIE, other require the use of
"hardening-wrapper" to force on the correct compiler and linker flags).
PIE on 64-bit architectures do not have the same penalties, and it was
made the default (as of 16.10, it is the default on amd64, ppc64el and
s390x). As of 17.10, it was decided that the security benefits are
significant enough that PIE is now enabled across all architectures in
the Ubuntu archive by default.

See
`test-built-binaries.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-built-binaries.py>`__
for regression tests.


.. _fortify-source:

Built with Fortify Source
~~~~~~~~~~~~~~~~~~~~~~~~~

Programs built with "-D_FORTIFY_SOURCE=2" (and -O1 or higher), enable
several compile-time and run-time protections in glibc:

-  expand unbounded calls to "sprintf", "strcpy" into their "n"
   length-limited cousins when the size of a destination buffer is known
   (protects against memory overflows).
-  stop format string "%n" attacks when the format string is in a
   writable memory segment.
-  require checking various important function return codes and
   arguments (e.g. system, write, open).
-  require explicit file mask when creating new files.

See
`test-gcc-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-gcc-security.py>`__
for regression tests.


.. _relro:

Built with RELRO
~~~~~~~~~~~~~~~~

Hardens ELF programs against loader memory area overwrites by having the
loader mark any areas of the relocation table as read-only for any
symbols resolved at load-time ("read-only relocations"). This reduces
the area of possible GOT-overwrite-style memory corruption attacks.

See
`test-gcc-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-gcc-security.py>`__
for regression tests.


.. _bindnow:

Built with BIND_NOW
~~~~~~~~~~~~~~~~~~~

Marks ELF programs to resolve all dynamic symbols at start-up (instead
of on-demand, also known as "immediate binding") so that the GOT can be
made entirely read-only (when combined with RELRO above).

See
`test-built-binaries.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-built-binaries.py>`__
for regression tests.


.. _stack-clash-protection:

Built with -fstack-clash-protection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adds extra instructions around variable length stack memory allocations
(via alloca() or gcc variable length arrays etc) to probe each page of
memory at allocation time. This mitigates stack-clash attacks by
ensuring all stack memory allocations are valid (or by raising a
segmentation fault if they are not, and turning a possible
code-execution attack into a denial of service).

See
`test-built-binaries.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-built-binaries.py>`__
for regression tests.


.. _cf-protection:

Built with -fcf-protection
~~~~~~~~~~~~~~~~~~~~~~~~~~

Instructs the compiler to generate instructions to support Intel's
Control-flow Enforcement Technology (CET).

See
`test-built-binaries.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-built-binaries.py>`__
for regression tests.


.. _nx:

Non-Executable Memory
~~~~~~~~~~~~~~~~~~~~~

Most modern CPUs protect against executing non-executable memory regions
(heap, stack, etc). This is known either as Non-eXecute (NX) or
eXecute-Disable (XD), and some BIOS manufacturers needlessly disable it
by default, so check your `BIOS Settings <Security/CPUFeatures>`__. This
protection reduces the areas an attacker can use to perform arbitrary
code execution. It requires that the kernel use "PAE" addressing (which
also allows addressing of physical addresses above 3GB). The 64bit and
32bit ``-server`` and ``-generic-pae`` kernels are compiled with PAE
addressing. Starting in Ubuntu 9.10, this protection is partially
emulated for processors lacking NX when running on a 32bit kernel (built
with or without PAE). After booting, you can see what NX protection is
in effect:

-  Hardware-based (via PAE mode):

::

   <nowiki>
   [    0.000000] NX (Execute Disable) protection: active</nowiki>

-  Partial Emulation (via segment limits):

::

   <nowiki>
   [    0.000000] Using x86 segment limits to approximate NX protection</nowiki>

If neither are seen, you do not have any NX protections enabled. Check
your BIOS settings and CPU capabilities. If "nx" shows up in each of the
"flags" lines in ``/proc/cpuinfo``, it is enabled/supported by your
hardware (and a PAE kernel is needed to actually use it).

Starting in Ubuntu 11.04, BIOS NX settings are `ignored by the
kernel <https://git.kernel.org/?p=linux/kernel/git/torvalds/linux-2.6.git;a=commitdiff;h=ae84739c27b6b3725993202fe02ff35ab86468e1>`__.

===== ========================================
\     
\     
i386  ``|-386``, ``-generic`` kernel (non-PAE)
\     ``|-server`` kernel (PAE)
amd64 any kernel (PAE)
===== ========================================

===== ===========================================
\     
\     
i386  ``|-386``, ``-generic`` kernel (non-PAE)
\     ``|-server``, ``-generic-pae`` kernel (PAE)
amd64 any kernel (PAE)
===== ===========================================

===== ===========================================
\     
i386  ``|-386``, ``-generic`` kernel (non-PAE)
\     ``|-server``, ``-generic-pae`` kernel (PAE)
amd64 any kernel (PAE)
===== ===========================================

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for regression tests.


.. _proc-maps:

/proc/$pid/maps protection
~~~~~~~~~~~~~~~~~~~~~~~~~~

With ASLR, a process's memory space layout suddenly becomes valuable to
attackers. The "maps" file is `made
read-only <https://lkml.org/lkml/2007/3/10/250>`__ except to the process
itself or the owner of the process. Went into mainline kernel with
sysctl toggle in 2.6.22. The toggle was made non-optional in 2.6.27,
forcing the privacy to be enabled regardless of sysctl settings (this is
a good thing).

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for regression tests.


.. _symlink:

Symlink restrictions
~~~~~~~~~~~~~~~~~~~~

A long-standing class of security issues is the symlink-based
`ToCToU <https://en.wikipedia.org/wiki/Time-of-check-to-time-of-use>`__
race, most commonly seen in world-writable directories like \`/tmp/\`.
The common method of exploitation of `this
flaw <https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=tmp+symlink>`__
is crossing privilege boundaries when following a given symlink (i.e. a
\`root\` user follows a symlink belonging to another user).

In Ubuntu 10.10 and later, symlinks in world-writable sticky directories
(e.g. \`/tmp\`) cannot be followed if the follower and directory owner
do not match the symlink owner. The behavior is controllable through the
\`/proc/sys/kernel/yama/protected_sticky_symlinks\` sysctl, available
via
`Yama <https://www.kernel.org/doc/html/latest/admin-guide/LSM/Yama.html>`__.

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for regression tests.


.. _hardlink:

Hardlink restrictions
~~~~~~~~~~~~~~~~~~~~~

Hardlinks can be abused in a `similar
fashion <https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=hardlink>`__
to symlinks above, but they are not limited to world-writable
directories. If \`/etc/\` and \`/home/\` are on the same partition, a
regular user can create a hardlink to \`/etc/shadow\` in their home
directory. While it retains the original owner and permissions, it is
possible for privileged programs that are otherwise symlink-safe to
mistakenly access the file through its hardlink. Additionally, a very
minor untraceable quota-bypassing local denial of service is possible by
an attacker exhausting disk space by filling a world-writable directory
with hardlinks.

In Ubuntu 10.10 and later, hardlinks cannot be created to files that the
user would be unable to read and write originally, or are otherwise
sensitive. The behavior is controllable through the
\`/proc/sys/kernel/yama/protected_nonaccess_hardlinks\` sysctl,
available via
`Yama <https://www.kernel.org/doc/html/latest/admin-guide/LSM/Yama.html>`__.

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for regression tests.


.. _protected-fifos:

FIFO restrictions
~~~~~~~~~~~~~~~~~

Processes may not check that the files being created are actually
created as the desired type. This global control forbids some
potentially unsafe configurations from working.

See the `kernel
admin-guide <https://www.kernel.org/doc/html/latest/admin-guide/sysctl/fs.html#protected-fifos>`__
for documentation.


.. _protected-regular:

Regular file restrictions
~~~~~~~~~~~~~~~~~~~~~~~~~

Processes may not check that the files being created are actually
created as desired. This global control forbids some potentially unsafe
configurations from working.

See the `kernel
admin-guide <https://www.kernel.org/doc/html/latest/admin-guide/sysctl/fs.html#protected-regular>`__
for documentation.


.. _ptrace:

ptrace scope
~~~~~~~~~~~~

A troubling weakness of the Linux process interfaces is that a single
user is able to examine the memory and running state of any of their
processes. For example, if one application was compromised, it would be
possible for an attacker to attach to other running processes (e.g. SSH
sessions, GPG agent, etc) to extract additional credentials and continue
to immediately expand the scope of their attack without resorting to
user-assisted phishing or trojans.

In Ubuntu 10.10 and later, users cannot ptrace processes that are not a
descendant of the debugger. The behavior is controllable through the
\`/proc/sys/kernel/yama/ptrace_scope\` sysctl, available via
`Yama <https://www.kernel.org/doc/html/latest/admin-guide/LSM/Yama.html>`__.

In the case of automatic crash handlers, a crashing process can
specficially allow an existing crash handler process to attach on a
process-by-process basis using \`prctl(PR_SET_PTRACER, debugger_pid, 0,
0, 0)\`.

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for regression tests.


.. _kernel-hardening:

Kernel Hardening
----------------

The kernel itself has protections enabled to make it more difficult to
become compromised.


.. _null-mmap:

0-address protection
~~~~~~~~~~~~~~~~~~~~

Since the kernel and userspace share virtual memory addresses, the
"NULL" memory space needs to be protected so that userspace mmap'd
memory cannot start at address 0, stopping "NULL dereference" kernel
attacks. This is possible with 2.6.22 kernels, and was implemented with
the "mmap_min_addr" sysctl setting. Since Ubuntu 9.04, the mmap_min_addr
setting is built into the kernel. (64k for x86, 32k for ARM.)

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for regression tests.


.. _dev-mem:

/dev/mem protection
~~~~~~~~~~~~~~~~~~~

Some applications (Xorg) need direct access to the physical memory from
user-space. The special file \`/dev/mem\` exists to provide this access.
In the past, it was possible to view and change kernel memory from this
file if an attacker had root access. The `CONFIG_STRICT_DEVMEM kernel
option <https://lwn.net/Articles/267427/>`__ was introduced to block
non-device memory access (originally named CONFIG_NONPROMISC_DEVMEM).

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for regression tests.


.. _dev-kmem:

/dev/kmem disabled
~~~~~~~~~~~~~~~~~~

There is no modern user of \`/dev/kmem\` any more beyond attackers using
it to load kernel rootkits.
`CONFIG_DEVKMEM <https://lkml.org/lkml/2008/2/10/328>`__ is set to "n".
While the \`/dev/kmem\` device node still exists in Ubuntu 8.04 LTS
through Ubuntu 9.04, it is not actually attached to anything in the
kernel.

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for regression tests.


.. _block-modules:

Block module loading
~~~~~~~~~~~~~~~~~~~~

In Ubuntu 8.04 LTS and earlier, it was possible to `remove
CAP_SYS_MODULES from the system-wide capability bounding
set <https://www.debian.org/doc/manuals/securing-debian-howto/ch10.en.html#s-proactive>`__,
which would stop any new kernel modules from being loaded. This was
another layer of protection to stop kernel rootkits from being
installed. The 2.6.25 Linux kernel (Ubuntu 8.10) changed how bounding
sets worked, and this functionality disappeared. Starting with Ubuntu
9.10, it is now `possible to block module
loading <https://git.kernel.org/?p=linux/kernel/git/torvalds/linux-2.6.git;a=commitdiff;h=3d43321b7015387cfebbe26436d0e9d299162ea1>`__
again by setting "1" in ``/proc/sys/kernel/modules_disabled``.

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for regression tests.


.. _rodata:

Read-only data sections
~~~~~~~~~~~~~~~~~~~~~~~

This makes sure that certain kernel data sections are marked to block
modification. This helps protect against some classes of kernel
rootkits. Enabled via the CONFIG_DEBUG_RODATA option.

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for configuration regression tests.


.. _kernel-stack-protector:

Stack protector
~~~~~~~~~~~~~~~

Similar to the stack protector used for ELF programs in userspace, the
kernel can protect its internal stacks as well. Enabled via the
CONFIG_CC_STACKPROTECTOR option.

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for configuration regression tests.


.. _module-ronx:

Module RO/NX
~~~~~~~~~~~~

This feature extends CONFIG_DEBUG_RODATA to include similar restrictions
for loaded modules in the kernel. This can help resist future kernel
exploits that depend on various memory regions in loaded modules.
Enabled via the CONFIG_DEBUG_MODULE_RONX option.

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for configuration regression tests.


.. _kptr-restrict:

Kernel Address Display Restriction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When attackers try to develop "run anywhere" exploits for kernel
vulnerabilities, they frequently need to know the location of internal
kernel structures. By treating kernel addresses as sensitive
information, those locations are not visible to regular local users.
Starting with Ubuntu 11.04, ``/proc/sys/kernel/kptr_restrict`` is set to
"1" to block the reporting of known kernel address leaks. Additionally,
various files and directories were made readable only by the root user:
\`/boot/vmlinuz*\`, \`/boot/System.map*\`, \`/sys/kernel/debug/\`,
\`/proc/slabinfo\`

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for regression tests.


.. _kASLR:

Kernel Address Space Layout Randomisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kernel Address Space Layout Randomisation (kASLR) aims to make some
kernel exploits more difficult to implement by randomizing the base
address value of the kernel. Exploits that rely on the locations of
internal kernel symbols must discover the randomized base address.

kASLR is available starting with Ubuntu 14.10 and is enabled by default
in 16.10 and later.

Before 16.10, you can specify the "kaslr" option on the kernel command
line to use kASLR.

**Note:** Before 16.10, enabling kASLR will disable the ability to enter
hibernation mode.


.. _denylist-rare-net:

Denylist Rare Protocols
~~~~~~~~~~~~~~~~~~~~~~~

Normally the kernel allows all network protocols to be autoloaded on
demand via the ``MODULE_ALIAS_NETPROTO(PF_...)`` macros. Since many of
these protocols are old, rare, or generally of little use to the average
Ubuntu user and may contain undiscovered exploitable vulnerabilities,
they have been denylisted since Ubuntu 11.04. These include: ax25,
netrom, x25, rose, decnet, econet, rds, and af_802154. If any of the
protocols are needed, they can speficially loaded via modprobe, or the
``/etc/modprobe.d/blacklist-rare-network.conf`` file can be updated to
remove the denylist entry.

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for regression tests.


.. _seccomp-filter:

Syscall Filtering
~~~~~~~~~~~~~~~~~

Programs can filter out the availability of kernel syscalls by using the
`seccomp_filter interface <https://lkml.org/lkml/2011/6/23/784>`__. This
is done in containers or sandboxes that want to further limit the
exposure to kernel interfaces when potentially running untrusted
software.

See
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for regression tests.


.. _dmesg-restrict:

dmesg restrictions
~~~~~~~~~~~~~~~~~~

When attackers try to develop "run anywhere" exploits for
vulnerabilties, they frequently will use dmesg output. By treating dmesg
output as sensitive information, this output is not available to the
attacker. Starting with Ubuntu 12.04 LTS,
``/proc/sys/kernel/dmesg_restrict`` can be set to "1" to treat dmesg
output as sensitive. Starting with 20.10, this is enabled by default.


.. _kexec:

Block kexec
~~~~~~~~~~~

Starting with Ubuntu 14.04 LTS, it is now `possible to disable
kexec <https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/commit/?id=7984754b99b6c89054edc405e9d9d35810a91d36>`__
via sysctl. CONFIG_KEXEC is enabled in Ubuntu so end users are able to
use kexec as desired and the new sysctl allows administrators to disable
kexec_load. This is desired in environments where CONFIG_STRICT_DEVMEM
and modules_disabled are set, for example. When Secure Boot is in use,
kexec is restricted by default to only load appropriately signed and
trusted kernels.


.. _secure-boot:

UEFI Secure Boot (amd64)
~~~~~~~~~~~~~~~~~~~~~~~~

Starting with Ubuntu 12.04 LTS, UEFI Secure Boot was implemented in
enforcing mode for the bootloader and non-enforcing mode for the kernel.
With this configuration, a kernel that fails to verify will boot without
UEFI quirks enabled. The Ubuntu 18.04.2 release of Ubuntu 18.04 LTS
enabled enforcing mode for the bootloader and the kernel, so that
kernels which fail to verify will not be booted, and kernel modules
which fail to verify will not be loaded. This is planned to be
backported for Ubuntu 16.04 LTS and Ubuntu 14.04 LTS (however only with
kernel signature enforcement for Ubuntu 14.04 LTS, not kernel module
signature enforcement).


.. _usbguard:

usbguard
~~~~~~~~

Starting with Ubuntu 16.10, the usbguard package has been available in
universe to provide a tool for using the Linux kernel's USB
authorization support, to control device IDs and device classes that
will be recognized.


.. _usbauth:

usbauth
~~~~~~~

Starting with Ubuntu 18.04, the usbauth package has been available in
universe to provide a tool for using the Linux kernel's USB
authorization support, to control device IDs and device classes that
will be recognized.


.. _bolt:

bolt
~~~~

Starting with Ubuntu 18.04, the bolt package has been available in main
to provide a desktop-oriented tool for using the Linux kernel's
Thunderbolt authorization support.


.. _thunderbolt-tools:

thunderbolt-tools
~~~~~~~~~~~~~~~~~

Starting with Ubuntu 18.04, the thunderbolt-tools package has been
available in universe to provide a server-oriented tool for using the
Linux kernel's Thunderbolt authorization support.


.. _kernel-lockdown:

Kernel Lockdown
~~~~~~~~~~~~~~~

Starting with Ubuntu 20.04, the Linux kernel's lockdown mode is enabled
in integrity mode. This prevents the root account from loading arbitrary
modules or BPF programs that can manipulate kernel datastructures.
Lockdown enforcement is tied to UEFI secure boot.


.. _additional_documentation:

Additional Documentation
========================

-  Coordination with Debian: https://wiki.debian.org/Hardening
-  Gentoo's Hardening project:
   https://www.gentoo.org/proj/en/hardened/hardened-toolchain.xml
-  `Ubuntu Security Features for all releases </Historical>`__

If you have questions or comments on these features, please `contact the
security team <SecurityTeam/FAQ#Contact>`__.

`Category:SecurityTeam <Category:SecurityTeam>`__
