Dangerous sysctls
#################

Sysctls are Linux kernel parameters which can be manipulated from userspace to
alter the behaviour or tune certain limits of the kernel. They are exposed
through the ``proc`` filesystem (usually mounted on ``/proc``) and commonly
managed through the `sysctl
<https://manpages.ubuntu.com/manpages/resolute/man8/sysctl.8.html>`_ utility.

This page provides a non-exhaustive list of sysctls which have important
security implications and require dilligence before changing. They are referred
to be their qualified sysctl name, but they can be managed through multiple
means.

The ``kernel.core_pattern`` sysctl can be ephemerally modified through the
sysctl utility or through writing to the ``proc`` filesystem:

.. code-block:: console

    sudo sysctl kernel.core_pattern='|/bin/false'
    echo '|/bin/false' | sudo tee /proc/sys/kernel/core_pattern

For a persistent configuration, drop-in files in ``/etc/sysctl.d/`` are
recommended, along with immediately loading their contents using the ``sysctl``
utility:

.. code-block:: console

    echo 'kernel.core_pattern = |/bin/false' | sudo tee /etc/sysctl.d/90coredump.conf
    sudo sysctl -p /etc/sysctl.d/90coredump.conf

fs.protected_fifos
^^^^^^^^^^^^^^^^^^

Unintentional writes to an attacker-controlled FIFO could pose security risk.
This parameter can restrict unsafe operations and is documented :doc:`here
<../security-features/process-memory/file-handling#fifo-restrictions>`.

Ubuntu recommends setting this parameter to ``1``, which enables the
restrictions.

fs.protected_hardlinks
^^^^^^^^^^^^^^^^^^^^^^

A race-condition-prone use of hardlinks could pose security risks for
applications. This parameter restricts certain unsafe operations and is
documented :doc:`here
<../security-features/process-memory/file-handling#hardlink-restrictions>`.

Ubuntu recommends setting this parameter to ``1``, which enables the
restrictions.

fs.protected_symlinks
^^^^^^^^^^^^^^^^^^^^^

A race-conditoin-prone use of sysmlinks, commonly in world-writable directories
(such as ``/tmp``), could pose security risks. This parameter restricts certain
unsafe operations and is documented :doc:`here
<../security-features/process-memory/file-handling#symlink-restrictions>`.

Ubuntu recommends setting this parameter to ``1``, which enables the
restrictions.

fs.suid_dumpable
^^^^^^^^^^^^^^^^

A setuid executable will be run with elevated privileges when invoked by a
regular user. If the process crashes, the regular user must not be able to
obtain access to the crash data (the core dump), as it would leak sensitive
data. This parameter works in conjunction with the ``kernel.core_pattern``
sysctl.

Ubuntu recommends never setting this parameter to ``0``, which allows
unrestricted core dumping of setuid executables.

kernel.core_pattern
^^^^^^^^^^^^^^^^^^^

This parameter configures a filename for writing `core
<https://manpages.ubuntu.com/manpages/resolute/man5/core.5.html>`_ files to when
a process crashes or using a coredump handler for the automatic processing of
the crash data. This parameter is sensitive because the core files contain the
memory contents of processes, which could be privileged or belonging to other
users.

You should never install a coredump handler you do not trust. Ubuntu recommends
`apport <https://manpages.ubuntu.com/manpages/resolute/man1/apport-bug.1.html>`_
or `systemd-coredump
<https://manpages.ubuntu.com/manpages/resolute/man8/systemd-coredump.8.html>`_.

kernel.dmesg_restrict
^^^^^^^^^^^^^^^^^^^^^

This parameters controls whether the `dmesg
<https://manpages.ubuntu.com/manpages/resolute/man1/dmesg.1.html>`_ log buffer
is accessible to unprivileged users, as documented :doc:`here
<../security-features/kernel-protections#dmesg-restrictions>`

Ubuntu recommends setting this parameter to ``1``, which restricts access to
privileged users.

kernel.kexec_load_disabled
^^^^^^^^^^^^^^^^^^^^^^^^^^

The `kexec <https://manpages.ubuntu.com/manpages/resolute/man8/kexec.8.html>`_
system call allows loading another kernel from the currently running one. This
parameter can disable the functionality and is documented :doc:`here
<../security-features/kernel-protections#block-kexec>`.

Ubuntu recommends only enabling this restriction when the kexec function
functionality is not needed. By default, the restriction is not enabled and the
parameter is set to ``0``.

kernel.kptr_restrict
^^^^^^^^^^^^^^^^^^^^

The ability to know in-use kernel addresses can help defeat :doc:`kASLR
<../security-features/kernel-protections#kernel-address-space-layout-randomization>`
protections. This parameter can restrict users' access to logs containing kernel
addresses, as documented :doc:`here
<../security-features/kernel-protections#kernel-address-display-restriction>`.

Ubuntu recommends setting this parameter to ``1`` or ``2``, which enables the
restrictions.

kernel.modules_disabled
^^^^^^^^^^^^^^^^^^^^^^^

Loaded kernel modules are, by definition, highly privileged as they form part of
the running kernel. This parameter can reduce the risk of an attacker loading a
malicious module or a legitimate one that has exploitable vulnerabilities and is
documented :doc:`here
<../security-features/kernel-protections#block-module-loading>`.

Enabling this restriction will stop modules from being dynamically loaded when
their functionality is required, a feature that systems often rely on. The
necessary modules would have to be preloaded at boot time. Ubuntu only
recommends setting this parameter to ``1`` and enabling the restriction if the
implications are fully accounted for.

kernel.randomize_va_space
^^^^^^^^^^^^^^^^^^^^^^^^^

This parameter controls :doc:`kASLR <../security-features/process-memory/aslr>`,
a feature that can reduce the risk of exploiting code execution and memory
access kernel vulnerabilities.

Ubuntu recommends setting this parameter to ``2``, which enable randomization of
both address bases and the kernel heap.

kernel.yama.ptrace_scope
^^^^^^^^^^^^^^^^^^^^^^^^

The powerful `ptrace
<https://manpages.ubuntu.com/manpages/resolute/man2/ptrace.2.html>` system call
can be used to inspect and manage a running process. This parameter can restrict
which processes can use ``ptrace`` on a running process and is documented
:doc:`here <../security-features/process-memory/ptrace-scope>`.

Ubuntu recommends not setting this parameter to ``0``, which would disable the
protections provided by this feature.

net.ipv4.conf.*.accept_redirects and net.ipv6.conf.*.accept_redirects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ICMP and ICMPv6 redirects can be used by local networks for more efficient
routing, especially when multiple Layer-3 routers are deployed on the same
segment. However, they can also be abused by network-adjacent attackers to
redirect traffic from a victim to an attacker-controlled host. While modern
protocols are often designed to be resistant to such MitM attacks, applications
can still be susceptible.

Ubuntu recommends only setting this parameter to ``0``, which disables the
processing of received ICMP/ICMPv6 redirects, if the implications are understood
and are appropriate for the local network configuration.

net.ipv4.conf.*.rp_filter
^^^^^^^^^^^^^^^^^^^^^^^^^

Hosts connected to multiple network segments often expect to receive packets on
the same interface which would be used for sending packets out (that is, in the
reverse direction). Reverse-path filtering ensures that packets with a
particular source address arrive on the expected interface. However, this
restriction does not hold for complex routing setups, such as asymmetric
routing.

The default value of ``2`` provides a loose, but widely-compatible
configuration. Ubuntu recommends only setting the value to ``0``, which disables
the restriction altogether, if the implications are understood or if other types
of reverse-path filtering are enabled. Nftables supports a much more flexible
:doc:`reverse-path filtering
<../security-features/network/firewall/nftables#fib-lookup-and-reverse-path-filtering>`
configuration.

net.ipv4.tcp_syncookies
^^^^^^^^^^^^^^^^^^^^^^^

TCP SYN cookies are used as a protective measure in case TCP SYN DoS attacks.
This parameter controls the feature and are documented :doc:`here
<../security-features/network/syn-cookies>`.

Ubuntu recommends setting this parameter to ``1``, which enables the
protection.

net.ipv4.tcp_timestamps
^^^^^^^^^^^^^^^^^^^^^^^

TCP timestamps are an extension of the TCP protocol which can help with
estimating round-trip time. The behaviour on Ubuntu prior to Bionic Beaver
(18.04) could leak information about the local time on a system and this
parameter was often recommended for hardening (by setting it to ``0``). On newer
systems, the default behaviour is to introduce a random offset, negating an
attacker's ability to obtain information about the victim's local time.

Ubuntu recommends setting this parameter to ``1`` and only changing it if the
implications are understood.

vm.mmap_min_addr
^^^^^^^^^^^^^^^^

NULL-dereference attacks could have implications beyond crashes if memory at
low-addresses is valid. This parameter controls the minimum address at which
pages are mapped in a process' address space and is documented :doc:`here
<../security-features/process-memory#address-protection>`.

vm.mmap_rnd_bits and vm.mmap_rnd_compat_bits
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:doc:`ASLR <../security-features/process-memory/aslr>` is a protective measure
that reduces the risk of code execution or memory manipulation vulnerabilities.
These parameters control the amount of randomness introduced in the processes'
address bases.

Ubuntu recommends not reducing these values below their defaults.
