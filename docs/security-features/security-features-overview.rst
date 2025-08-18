Overview of security features
##############################

This page provides a high-level overview of the security features in Ubuntu,
their default configurations and rationale for having them enabled or disabled.

.. tabs::

   .. tab:: Current Releases

      **Supported LTS and Interim Releases**

      .. list-table:: Security features
         :header-rows: 1

         * - Section
           - Feature
           - 22.04 LTS
           - 24.04 LTS
           - 25.04
           - 25.10
         * - :ref:`configuration`
           - :ref:`ports`
           - policy
           - policy
           - policy
           - policy
         * - :ref:`configuration`
           - :ref:`hashing`
           - yescrypt
           - yescrypt
           - yescrypt
           - yescrypt
         * - :ref:`configuration`
           - :ref:`syn-cookies`
           - kernel & sysctl
           - kernel & sysctl
           - kernel & sysctl
           - kernel & sysctl
         * - :ref:`configuration`
           - :ref:`unattended-upgrades`
           - enabled
           - enabled
           - enabled
           - enabled
         * - :ref:`configuration`
           - :ref:`kernel-livepatches`
           - 22.04 LTS Kernel
           - 22.04 LTS Kernel
           - 22.04 LTS Kernel
           - 22.04 LTS Kernel
         * - :ref:`configuration`
           - :ref:`disable-legacy-tls`
           - policy
           - policy
           - policy
           - policy
         * - :ref:`subsystems`
           - :ref:`fscaps`
           - kernel & userspace (default on server)
           - kernel & userspace (default on server)
           - kernel & userspace (default on server)
           - kernel & userspace (default on server)
         * - :ref:`subsystems`
           - :ref:`firewall`
           - ufw
           - ufw
           - ufw
           - ufw
         * - :ref:`subsystems`
           - :ref:`prng-cloud`
           - pollinate
           - pollinate
           - pollinate
           - pollinate
         * - :ref:`subsystems`
           - :ref:`seccomp`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`mac`
           - :ref:`apparmor`
           - 3.0.4
           - 3.0.4
           - 4.1.0
           - 4.1.0
         * - :ref:`mac`
           - :ref:`apparmor-unprivileged-userns-restrictions`
           - --
           - --
           - kernel & userspace
           - kernel & userspace
         * - :ref:`mac`
           - :ref:`selinux`
           - universe
           - universe
           - universe
           - universe
         * - :ref:`mac`
           - :ref:`smack`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`encryption`
           - :ref:`encrypted-lvm`
           - main installer
           - main installer
           - main installer
           - main installer
         * - :ref:`encryption`
           - :ref:`encrypted-files`
           - ZFS dataset encryption available, encrypted Home (eCryptfs) and ext4 encryption (fscrypt) available in universe
           - ZFS dataset encryption available, encrypted Home (eCryptfs) and ext4 encryption (fscrypt) available in universe
           - ZFS dataset encryption available, encrypted Home (eCryptfs) and ext4 encryption (fscrypt) available in universe
           - ZFS dataset encryption available, encrypted Home (eCryptfs) and ext4 encryption (fscrypt) available in universe
         * - :ref:`encryption`
           - :ref:`TPM`
           - kernel & userspace (tpm-tools)
           - kernel & userspace (tpm-tools)
           - kernel & userspace (tpm-tools)
           - kernel & userspace (tpm-tools)
         * - :ref:`userspace-hardening`
           - :ref:`stack-protector`
           - gcc patch
           - gcc patch
           - gcc patch
           - gcc patch
         * - :ref:`userspace-hardening`
           - :ref:`heap-protector`
           - glibc
           - glibc
           - glibc
           - glibc
         * - :ref:`userspace-hardening`
           - :ref:`pointer-obfuscation`
           - glibc
           - glibc
           - glibc
           - glibc
         * - :ref:`aslr`
           - :ref:`stack-aslr`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`aslr`
           - :ref:`mmap-aslr`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`aslr`
           - :ref:`exec-aslr`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`aslr`
           - :ref:`brk-aslr`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`aslr`
           - :ref:`vdso-aslr`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`aslr`
           - :ref:`pie`
           - gcc patch (amd64, ppc64el, s390x), package list for others
           - gcc patch (amd64, ppc64el, s390x), package list for others
           - gcc patch (amd64, ppc64el, s390x), package list for others
           - gcc patch (amd64, ppc64el, s390x), package list for others
         * - :ref:`aslr`
           - :ref:`fortify-source`
           - gcc patch
           - gcc patch
           - gcc patch
           - gcc patch
         * - :ref:`aslr`
           - :ref:`relro`
           - gcc patch
           - gcc patch
           - gcc patch
           - gcc patch
         * - :ref:`aslr`
           - :ref:`bindnow`
           - gcc patch (amd64, ppc64el, s390x), package list for others
           - gcc patch (amd64, ppc64el, s390x), package list for others
           - gcc patch (amd64, ppc64el, s390x), package list for others
           - gcc patch (amd64, ppc64el, s390x), package list for others
         * - :ref:`aslr`
           - :ref:`stack-clash-protection`
           - gcc patch (i386, amd64, ppc64el, s390x)
           - gcc patch (i386, amd64, ppc64el, s390x)
           - gcc patch (i386, amd64, ppc64el, s390x)
           - gcc patch (i386, amd64, ppc64el, s390x)
         * - :ref:`aslr`
           - :ref:`cf-protection`
           - gcc patch (i386, amd64)
           - gcc patch (i386, amd64)
           - gcc patch (i386, amd64)
           - gcc patch (i386, amd64)
         * - :ref:`aslr`
           - :ref:`nx`
           - PAE, ia32 partial-NX-emulation
           - PAE, ia32 partial-NX-emulation
           - PAE, ia32 partial-NX-emulation
           - PAE, ia32 partial-NX-emulation
         * - :ref:`aslr`
           - :ref:`proc-maps`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`aslr`
           - :ref:`symlink`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`aslr`
           - :ref:`hardlink`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`aslr`
           - :ref:`protected-fifos`
           - kernel & sysctl
           - kernel & sysctl
           - kernel & sysctl
           - kernel & sysctl
         * - :ref:`aslr`
           - :ref:`protected-regular`
           - kernel & sysctl
           - kernel & sysctl
           - kernel & sysctl
           - kernel & sysctl
         * - :ref:`aslr`
           - :ref:`ptrace`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`kernel-hardening`
           - :ref:`null-mmap`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`kernel-hardening`
           - :ref:`dev-mem`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`kernel-hardening`
           - :ref:`dev-kmem`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`kernel-hardening`
           - :ref:`block-modules`
           - sysctl
           - sysctl
           - sysctl
           - sysctl
         * - :ref:`kernel-hardening`
           - :ref:`rodata`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`kernel-hardening`
           - :ref:`kernel-stack-protector`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`kernel-hardening`
           - :ref:`module-ronx`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`kernel-hardening`
           - :ref:`kptr-restrict`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`kernel-hardening`
           - :ref:`kASLR`
           - kernel (i386, amd64, arm64, and s390 only)
           - kernel (i386, amd64, arm64, and s390 only)
           - kernel (i386, amd64, arm64, and s390 only)
           - kernel (i386, amd64, arm64, and s390 only)
         * - :ref:`kernel-hardening`
           - :ref:`denylist-rare-net`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`kernel-hardening`
           - :ref:`seccomp-filter`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`kernel-hardening`
           - :ref:`dmesg-restrict`
           - kernel
           - kernel
           - kernel
           - kernel
         * - :ref:`kernel-hardening`
           - :ref:`kexec`
           - sysctl
           - sysctl
           - sysctl
           - sysctl
         * - :ref:`kernel-hardening`
           - :ref:`secure-boot`
           - amd64, kernel signature enforcement
           - amd64, kernel signature enforcement
           - amd64, kernel signature enforcement
           - amd64, kernel signature enforcement
         * - :ref:`kernel-hardening`
           - :ref:`usbguard`
           - kernel & userspace
           - kernel & userspace
           - kernel & userspace
           - kernel & userspace
         * - :ref:`kernel-hardening`
           - :ref:`usbauth`
           - kernel & userspace
           - kernel & userspace
           - kernel & userspace
           - kernel & userspace
         * - :ref:`kernel-hardening`
           - :ref:`bolt`
           - kernel & userspace
           - kernel & userspace
           - kernel & userspace
           - kernel & userspace
         * - :ref:`kernel-hardening`
           - :ref:`thunderbolt-tools`
           - kernel & userspace
           - kernel & userspace
           - kernel & userspace
           - kernel & userspace
         * - :ref:`kernel-hardening`
           - :ref:`kernel-lockdown`
           - integrity only, no confidentiality
           - integrity only, no confidentiality
           - integrity only, no confidentiality
           - integrity only, no confidentiality

   .. tab:: ESM Releases

      **Extended Security Maintenance Releases**

      .. list-table:: Security features
         :header-rows: 1

         * - Section
           - Feature
           - 16.04 ESM
           - 18.04 ESM
           - 20.04 ESM
         * - :ref:`configuration`
           - :ref:`ports`
           - --
           - --
           - --
         * - :ref:`configuration`
           - :ref:`hashing`
           - --
           - --
           - --
         * - :ref:`configuration`
           - :ref:`syn-cookies`
           - --
           - --
           - --
         * - :ref:`configuration`
           - :ref:`unattended-upgrades`
           - enabled
           - enabled
           - enabled
         * - :ref:`configuration`
           - :ref:`kernel-livepatches`
           - 16.04 LTS Kernel
           - 18.04 LTS Kernel
           - 20.04 LTS Kernel
         * - :ref:`configuration`
           - :ref:`disable-legacy-tls`
           - --
           - --
           - policy
         * - :ref:`subsystems`
           - :ref:`fscaps`
           - --
           - --
           - --
         * - :ref:`subsystems`
           - :ref:`firewall`
           - --
           - --
           - --
         * - :ref:`subsystems`
           - :ref:`prng-cloud`
           - --
           - --
           - --
         * - :ref:`subsystems`
           - :ref:`seccomp`
           - --
           - --
           - --
         * - :ref:`mac`
           - :ref:`apparmor`
           - 2.10.95 (2.11 Beta 1)
           - 2.12.0
           - 2.13.3
         * - :ref:`mac`
           - :ref:`apparmor-unprivileged-userns-restrictions`
           - --
           - --
           - --
         * - :ref:`mac`
           - :ref:`selinux`
           - --
           - --
           - --
         * - :ref:`mac`
           - :ref:`smack`
           - --
           - --
           - --
         * - :ref:`encryption`
           - :ref:`encrypted-lvm`
           - --
           - --
           - --
         * - :ref:`encryption`
           - :ref:`encrypted-files`
           - --
           - Encrypted Home (eCryptfs) and ext4 encryption (fscrypt) available in universe
           - ZFS dataset encryption available, encrypted Home (eCryptfs) and ext4 encryption (fscrypt) available in universe
         * - :ref:`encryption`
           - :ref:`TPM`
           - --
           - --
           - --
         * - :ref:`userspace-hardening`
           - :ref:`stack-protector`
           - --
           - --
           - --
         * - :ref:`userspace-hardening`
           - :ref:`heap-protector`
           - --
           - --
           - --
         * - :ref:`userspace-hardening`
           - :ref:`pointer-obfuscation`
           - --
           - --
           - --
         * - :ref:`aslr`
           - :ref:`stack-aslr`
           - --
           - --
           - --
         * - :ref:`aslr`
           - :ref:`mmap-aslr`
           - --
           - --
           - --
         * - :ref:`aslr`
           - :ref:`exec-aslr`
           - --
           - --
           - --
         * - :ref:`aslr`
           - :ref:`brk-aslr`
           - --
           - --
           - --
         * - :ref:`aslr`
           - :ref:`vdso-aslr`
           - --
           - --
           - --
         * - :ref:`aslr`
           - :ref:`pie`
           - gcc patch (s390x), package list for others
           - gcc patch (s390x), package list for others
           - gcc patch (s390x), package list for others
         * - :ref:`aslr`
           - :ref:`fortify-source`
           - --
           - --
           - --
         * - :ref:`aslr`
           - :ref:`relro`
           - --
           - --
           - --
         * - :ref:`aslr`
           - :ref:`bindnow`
           - gcc patch (s390x), package list for others
           - gcc patch (s390x), package list for others
           - gcc patch (s390x), package list for others
         * - :ref:`aslr`
           - :ref:`stack-clash-protection`
           - --
           - --
           - --
         * - :ref:`aslr`
           - :ref:`cf-protection`
           - --
           - --
           - --
         * - :ref:`aslr`
           - :ref:`nx`
           - --
           - --
           - --
         * - :ref:`aslr`
           - :ref:`proc-maps`
           - --
           - --
           - --
         * - :ref:`aslr`
           - :ref:`symlink`
           - --
           - --
           - --
         * - :ref:`aslr`
           - :ref:`hardlink`
           - --
           - --
           - --
         * - :ref:`aslr`
           - :ref:`protected-fifos`
           - --
           - --
           - kernel & sysctl
         * - :ref:`aslr`
           - :ref:`protected-regular`
           - --
           - --
           - kernel & sysctl
         * - :ref:`aslr`
           - :ref:`ptrace`
           - --
           - --
           - --
         * - :ref:`kernel-hardening`
           - :ref:`null-mmap`
           - --
           - --
           - --
         * - :ref:`kernel-hardening`
           - :ref:`dev-mem`
           - --
           - --
           - --
         * - :ref:`kernel-hardening`
           - :ref:`dev-kmem`
           - --
           - --
           - --
         * - :ref:`kernel-hardening`
           - :ref:`block-modules`
           - --
           - --
           - --
         * - :ref:`kernel-hardening`
           - :ref:`rodata`
           - --
           - --
           - --
         * - :ref:`kernel-hardening`
           - :ref:`kernel-stack-protector`
           - --
           - --
           - --
         * - :ref:`kernel-hardening`
           - :ref:`module-ronx`
           - --
           - --
           - --
         * - :ref:`kernel-hardening`
           - :ref:`kptr-restrict`
           - --
           - --
           - --
         * - :ref:`kernel-hardening`
           - :ref:`kASLR`
           - --
           - --
           - --
         * - :ref:`kernel-hardening`
           - :ref:`denylist-rare-net`
           - --
           - --
           - --
         * - :ref:`kernel-hardening`
           - :ref:`seccomp-filter`
           - --
           - --
           - --
         * - :ref:`kernel-hardening`
           - :ref:`dmesg-restrict`
           - --
           - --
           - --
         * - :ref:`kernel-hardening`
           - :ref:`kexec`
           - --
           - --
           - --
         * - :ref:`kernel-hardening`
           - :ref:`secure-boot`
           - --
           - amd64, kernel signature enforcement
           - amd64, kernel signature enforcement
         * - :ref:`kernel-hardening`
           - :ref:`usbguard`
           - --
           - --
           - --
         * - :ref:`kernel-hardening`
           - :ref:`usbauth`
           - --
           - kernel & userspace
           - kernel & userspace
         * - :ref:`kernel-hardening`
           - :ref:`bolt`
           - --
           - kernel & userspace
           - kernel & userspace
         * - :ref:`kernel-hardening`
           - :ref:`thunderbolt-tools`
           - --
           - kernel & userspace
           - kernel & userspace
         * - :ref:`kernel-hardening`
           - :ref:`kernel-lockdown`
           - --
           - --
           - integrity only, no confidentiality


Additional Documentation
========================

- `Coordination with Debian <https://wiki.debian.org/Hardening>`_
- `Gentoo's Hardening project <https://www.gentoo.org/proj/en/hardened/hardened-toolchain.xml>`_
- `Ubuntu Security Features for all releases <https://wiki.ubuntu.com/Security/Features>`_
