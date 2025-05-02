Overview of security features
##############################

This page provides a high-level overview of the security features in Ubuntu, their default configurations and rationale for having them enabled or disabled.

.. csv-table:: 
   :header: area, feature, 20.04 LTS, 22.04 LTS, 24.04 LTS, 24.10, 25.04
   :widths: auto

   :ref:`Privilege restriction`, :ref:`AppArmor`, 2.13.3, 3.0.4, 3.0.7, 3.0.7, 3.0.7 
   :ref:`Privilege restriction`, :ref:`AppArmor unprivileged user namespace restrictions`, --, --, kernel & userspace, kernel & userspace, kernel & userspace
   :ref:`Privilege restriction`, :ref:`SELinux`, universe, universe, universe, universe, universe 
   :ref:`Privilege restriction`, :ref:`SMACK`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Privilege restriction`, :ref:`PR_SET_SECCOMP`, kernel, kernel, kernel, kernel, kernel
   :ref:`Privilege restriction`, :ref:`Seccomp Filtering`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Privilege restriction`, :ref:`Filesystem Capabilities`, kernel & userspace (default on server), kernel & userspace (default on server), kernel & userspace (default on server), kernel & userspace (default on server), kernel & userspace (default on server) 
   :ref:`Storage and filesystem`, :ref:`Full disk encryption (FDE)`, LUKS + TPM, LUKS + TPM, LUKS + TPM, LUKS + TPM, LUKS + TPM
   :ref:`Storage and filesystem`, :ref:`Encrypted LVM`, main installer, main installer, main installer, main installer, main installer 
   :ref:`Storage and filesystem`, :ref:`File Encryption`, "ZFS dataset encryption available, encrypted Home (eCryptfs) and ext4 encryption (fscrypt) available in universe", "ZFS dataset 
   encryption available, encrypted Home (eCryptfs) and ext4 encryption (fscrypt) available in universe", "ZFS dataset encryption available, encrypted Home (eCryptfs) and ext4 encryption (fscrypt) available in universe", "ZFS dataset encryption available, encrypted Home (eCryptfs) and ext4 encryption (fscrypt) available in universe", "ZFS dataset encryption available, encrypted Home (eCryptfs) and ext4 encryption (fscrypt) available in universe"
   :ref:`Network and firewalls`, :ref:`No Open Ports`, policy, policy, policy, policy, policy 
   :ref:`Network and firewalls`, :ref:`SYN cookies`, kernel & sysctl, kernel & sysctl, kernel & sysctl, kernel & sysctl, kernel & sysctl 
   :ref:`Network and firewalls`, :ref:`Firewall`, ufw, ufw, ufw, ufw, ufw 
   :ref:`Cryptography`, :ref:`Password hashing`, sha512, yescrypt, yescrypt, yescrypt, yescrypt 
   :ref:`Cryptography`, :ref:`Cloud PRNG seed`, pollinate, pollinate, pollinate, pollinate, pollinate
   :ref:`Cryptography`, :ref:`Disable legacy TLS`, policy, policy, policy, policy, policy 
   :ref:`Process and memory protections`, :ref:`Symlink restrictions`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Process and memory protections`, :ref:`Hardlink restrictions`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Process and memory protections`, :ref:`FIFO restrictions`, kernel & sysctl, kernel & sysctl, kernel & sysctl, kernel & sysctl, kernel & sysctl
   :ref:`Process and memory protections`, :ref:`Regular file restrictions`, kernel & sysctl, kernel & sysctl, kernel & sysctl, kernel & sysctl, kernel & sysctl
   :ref:`Process and memory protections`, :ref:`Stack Protector`, gcc patch, gcc patch, gcc patch, gcc patch, gcc patch 
   :ref:`Process and memory protections`, :ref:`Heap Protector`, glibc, glibc, glibc, glibc, glibc 
   :ref:`Process and memory protections`, :ref:`Pointer Obfuscation`, glibc, glibc, glibc, glibc, glibc 
   :ref:`Process and memory protections`, :ref:`Stack ASLR`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Process and memory protections`, :ref:`Libs/mmap ASLR`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Process and memory protections`, :ref:`Exec ASLR`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Process and memory protections`, :ref:`brk ASLR`, kernel, kernel, kernel, kernel, kernel
   :ref:`Process and memory protections`, :ref:`vDSO ASLR`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Process and memory protections`, :ref:`Built as PIE`, "gcc patch (amd64, ppc64el, s390x), package list for others", "gcc patch (amd64, ppc64el, s390x), package list for others", "gcc patch (amd64, ppc64el, s390x), package list for others", "gcc patch (amd64, ppc64el, s390x), package list for others", "gcc patch (amd64, ppc64el, s390x), package list for others"
   :ref:`Process and memory protections`, :ref:`Built with Fortify Source`, gcc patch, gcc patch, gcc patch, gcc patch, gcc patch
   :ref:`Process and memory protections`, :ref:`Built with RELRO`, gcc patch, gcc patch, gcc patch, gcc patch, gcc patch
   :ref:`Process and memory protections`, :ref:`Built with BIND_NOW`, "gcc patch (amd64, ppc64el, s390x), package list for others", "gcc patch (amd64, ppc64el, s390x), package list for others", "gcc patch (amd64, ppc64el, s390x), package list for others", "gcc patch (amd64, ppc64el, s390x), package list for others", "gcc patch (amd64, ppc64el, s390x), package list for others"
   :ref:`Process and memory protections`, :ref:`Built with -fstack-clash-protection`, "gcc patch (i386, amd64, ppc64el, s390x)", "gcc patch (i386, amd64, ppc64el, s390x)", "gcc patch (i386, amd64, ppc64el, s390x)", "gcc patch (i386, amd64, ppc64el, s390x)", "gcc patch (i386, amd64, ppc64el, s390x)"
   :ref:`Process and memory protections`, :ref:`Built with -fcf-protection`, "gcc patch (i386, amd64)", "gcc patch (i386, amd64)", "gcc patch (i386, amd64)", "gcc patch (i386, amd64)", "gcc patch (i386, amd64)"
   :ref:`Process and memory protections`, :ref:`Non-Executable Memory`, "PAE, ia32 partial-NX-emulation", "PAE, ia32 partial-NX-emulation", "PAE, ia32 partial-NX-emulation", "PAE, ia32 partial-NX-emulation", "PAE, ia32 partial-NX-emulation"
   :ref:`Process and memory protections`, :ref:`/proc/$pid/maps protection`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Process and memory protections`, :ref:`ptrace scope`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Process and memory protections`, :ref:`0-address protection`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Process and memory protections`, :ref:`/dev/mem protection`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Kernel protections`, :ref:`Kernel Lockdown`, "integrity only, no confidentiality", "integrity only, no confidentiality", "integrity only, no confidentiality", "integrity only, no confidentiality", "integrity only, no confidentiality"
   :ref:`Kernel protections`, :ref:`/dev/kmem disabled`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Kernel protections`, :ref:`Block module loading`, sysctl, sysctl, sysctl, sysctl, sysctl
   :ref:`Kernel protections`, :ref:`Read-only data sections`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Kernel protections`, :ref:`Kernel Stack protector`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Kernel protections`, :ref:`Module RO/NX`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Kernel protections`, :ref:`Kernel Address Display Restriction`, kernel, kernel, kernel, kernel, kernel
   :ref:`Kernel protections`, :ref:`Kernel Address Space Layout Randomisation`, "kernel (i386, amd64, arm64, and s390 only)", "kernel (i386, amd64, arm64, and s390 only)", "kernel (i386, amd64, arm64, and s390 only)", "kernel (i386, amd64, arm64, and s390 only)", "kernel (i386, amd64, arm64, and s390 only)"
   :ref:`Kernel protections`, :ref:`Denylist Rare Protocols`, kernel, kernel, kernel, kernel, kernel 
   :ref:`Kernel protections`, :ref:`dmesg restrictions`, sysctl, kernel, kernel, kernel, kernel
   :ref:`Kernel protections`, :ref:`Block kexec`, sysctl, sysctl, sysctl, sysctl, sysctl
   :ref:`Platform protections`, :ref:`UEFI Secure Boot`, "amd64, kernel signature enforcement", "amd64, kernel signature enforcement", "amd64, kernel signature enforcement", "amd64, kernel signature enforcement", "amd64, kernel signature enforcement"
   :ref:`Platform protections`, :ref:`usbguard`, "kernel & userspace", "kernel & userspace", "kernel & userspace", "kernel & userspace", "kernel & userspace"
   :ref:`Platform protections`, :ref:`usbauth`, "kernel & userspace", "kernel & userspace", "kernel & userspace", "kernel & userspace", "kernel & userspace"
   :ref:`Platform protections`, :ref:`bolt`, "kernel & userspace", "kernel & userspace", "kernel & userspace", "kernel & userspace", "kernel & userspace"
   :ref:`Platform protections`, :ref:`thunderbolt-tools`, "kernel & userspace", "kernel & userspace", "kernel & userspace", "kernel & userspace", "kernel & userspace"
   :ref:`Security updates`, :ref:`Livepatch`, "20.04 LTS Kernel", "22.04 LTS Kernel", "24.04 LTS Kernel", "--", "--" 

Additional Documentation
========================

- `Coordination with Debian <https://wiki.debian.org/Hardening>`_
- `Gentoo's Hardening project <https://www.gentoo.org/proj/en/hardened/hardened-toolchain.xml>`_
- `Ubuntu Security Features for all releases <https://wiki.ubuntu.com/Security/Features>`_





