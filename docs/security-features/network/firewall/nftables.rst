nftables
========

`nftables <https://www.nftables.org/projects/nftables/index.html>`_ is a
component in the Linux Netfilter subsystem that provides the most modern
framework for defining packet classification and filtering functionality. As
such, it is a successor to the ``xtables`` kernel component and its associated
``iptables`` / ``ip6tables`` / ``arptables`` / ``ebtables`` userspace utilities.

This documentation uses the term ``nftables`` when referring to the Linux kernel
component and ``nft`` when referring to userspace utility. Please note that the
Ubuntu package that provides the userspace utility is called ``nftables`` and
this documentation will refer to it as the ``nftables`` Ubuntu package.

Advantages
----------

There are several advantages to using ``nftables`` over the older alternatives:

  * The expressions forming the packet classification rules are compiled in
    userspace to bytecode and executed by the kernel using a purpose-built
    virtual machine; this allows for far more flexibility.
  * High-performance can be achieved through maps and concatenations: instead of
    linear rule processing (O(n)), constant time (O(1)) can be achieved.
  * The syntax used by the userspace ``nft`` utility is declarative, instead of
    the procedural format required for ``ip/ip6/arp/ebtables``, simplifying
    management of firewall configuration
  * Tables and chains are not predefined and the structure allows registering
    an arbitrary number of them: this facilitates the independent management of
    rules by multiple applications.
  * Packet forwarding can be accelerated by using the ``flowtables``
    functionality, which also integrates with selected hardware.
  * Common rules for IPv4 and IPv6 can be defined, unlike with the older
    ``iptables`` and ``ip6tables``.
  * Tracing of the rules' evaluation for specific packets can be easily enabled.

Compatibility
-------------

In general, all the rules that can be defined using ``iptables``,
``ip6tables``, ``arptables`` and ``ebtables`` can also be defined using
``nftables``, but not the other way around. It is strongly recommended that you
only use one of two appraoches to managing firewall rules.

Starting with Ubuntu 16.04 Xenial Xerus, the ``iptables`` package has provided
versions of the ``iptables``, ``ip6tables``, ``arptables`` and ``ebtables``
tools that work with ``nftables`` API and provide a compatible interface to the
legacy implementation. The ``nftables`` backend has been the default since
Ubuntu 20.10 Groovy Gorilla. These are managed through the alternatives system
and the current configuration can be displayed with the following commands:

.. code-block:: console

    $ update-alternatives --display iptables
    $ update-alternatives --display ip6tables
    $ update-alternatives --display arptables
    $ update-alternatives --display ebtables


``ufw`` works by invoking the legacy ``iptables`` and ``ip6tables`` utilities.
As such, it should not be used concurrently with native ``nftables`` firewall
rules.

Usage
-----

``nftables`` rules can be configured by using the userspace ``nft`` utility,
which is provided by the ``nftables`` Ubuntu package. Communication with
Netfilter is done over `AF_NETLINK
<https://manpages.ubuntu.com/manpages/en/man7/netlink.7.html>`_ sockets,
allowing applications to alternatively use this low-level interface. This
documentation will only cover the use of the ``nft`` utility.

Starting with Ubuntu 15.04 Vivid Vervet, the ``nftables`` package provides a
systemd service unit file that is disabled by default. If enabled, the service
unit file will automatically load ``nftables`` configuration from the
``/etc/nftables.conf`` file (a mock file that does not perform any filtering is
provided in the ``nftables`` package). You can enable this and load the
configuration using the following commands:

.. code-block:: console

    $ sudo systemctl enable nftables.service
    $ sudo systemctl start nftables.service

Command-line usage
~~~~~~~~~~~~~~~~~~

The ``nft`` can accept one or more commands as arguments to manage any of the
objects (tables, rules, sets, etc.) supported. For example, the following
command will list all of the firewall rules:

.. code-block:: console

    $ sudo nft list ruleset

All operations are performed atomically: the processing of a packet will either
see the firewall rules defined prior to the invocation of the utility or the
firewall rules with all of the requested changes applied. The following command
will create two tables that process both IPv4 and IPv6 packets:

.. code-block:: console

    $ sudo nft "add table inet foo; add table inet bar"

Alternatively, a filename can be passed as an argument using the ``-f`` flag.
The file can contain both commands, as well as object definitions using a
declarative syntax, which are implied to be created. As with the command-line
usage, all of the operations are performed atomically. The default
``/etc/nftables.conf`` file contains a command to delete all of the configured
rules (``flush ruleset``) and a declarative definition of a table named
``filter`` that processes both IPv4 and IPv6 packets in three empty chains:

.. code-block::

    #!/usr/sbin/nft -f

    flush ruleset

    table inet filter {
        chain input {
            type filter hook input priority filter;
        }
        chain forward {
            type filter hook forward priority filter;
        }
        chain output {
            type filter hook output priority filter;
        }
    }

The ``-f`` option allows the ``nft`` utility to be used as an interpreter, as
demonstrated in the shebang line above. Given that the file is marked as
executable by default, the rules can be atomically reloaded by simply executing
the file:

.. code-block:: console

    $ sudo /etc/nftables.conf

Alternatively, the systemd unit file supports the ``reload`` command to achieve
the same objective:

.. code-block:: console

    $ sudo systemctl reload nftables.service

Configuration file format
~~~~~~~~~~~~~~~~~~~~~~~~~

The configuration file is line-oriented. Multiple commands can be combined on
the same line by separating them with semicolons (``;``). Comments can be
included by using the hash sign (``#``) and span until the end of the line.
Commands can be split across multiple lines by escaping the end-of-line with a
backslash (``\\``). Whitespace (and hence, indentation) does not matter.

Even though the declarative syntax uses braces (``{`` and ``}``) to define
blocks containing an object's definition, the line-oriented processing is still
enforced and must be taken into account (e.g. the opening brace (``{``) must be
on the same line as the object type and name. The following example establishes
a base for a host firewall configuration file, which will be expanded upon
throughout this documentation:

.. code-block::

    #!/usr/sbin/nft -f

    # This empty definition is needed to allow the flush command to work if the
    # table is not already defined.
    table inet host-firewall; flush table inet host-firewall

    table inet host-firewall {
        chain input {
            # Process packets destined for this host.
            type filter hook input priority filter;
            # Use a default-deny policy for packets.
            policy drop;
        }
    }

The include directive
^^^^^^^^^^^^^^^^^^^^^

Files can be included by using the ``include`` directive. These are interpreted
in the context in which the directive is used. For example, the following allows
drop-in files to be add rules to the defined ``input`` chain (if wildcards are
used, the files need not exist):

.. code-block::

    #!/usr/sbin/nft -f

    # This empty definition is needed to allow the flush command to work if the
    # table is not already defined.
    table inet host-firewall; flush table inet host-firewall

    table inet host-firewall {
        chain input {
            # Process packets destined for this host.
            type filter hook input priority filter;
            # Use a default-deny policy for packets.
            policy drop;

            # Drop-in files can add rules here.
            include "/etc/nftables/input-rules.d/*.conf"
        }
    }

Symbolic variables
^^^^^^^^^^^^^^^^^^

Symbolic variables increase the maintainability of the firewall rules by
associating names to arbitrary expressions, which can then be reused throughout
the configuration. Associating the name ``IF_LOOPBACK`` to the interface name
``lo`` (the standard Linux loopback interface) allows defining a rule that
references it:

.. code-block::

    #!/usr/sbin/nft -f

    define IF_LOOPBACK = lo

    # This empty definition is needed to allow the flush command to work if the
    # table is not already defined.
    table inet host-firewall; flush table inet host-firewall

    table inet host-firewall {

        chain input {
            # Process packets destined for this host.
            type filter hook input priority filter;
            # Use a default-deny policy for packets.
            policy drop;

            # Allow traffic on the loopback interface(s).
            iif $IF_LOOPBACK accept

            # Drop-in files can add rules here.
            include "/etc/nftables/input-rules.d/*.conf"
        }
    }

If, at a later date, a new loopback interface is created, the set notation can
be taken advantage of to only modify the symbolic variable:

.. code-block::

    define IF_LOOPBACK = { lo, lo1 }

The scope of the symbolic variables is the file interpreted by the ``nft``
utility (and any included files), but restricted to the block in which it is
defined and all inner blocks, in order to reduce clashes. The symbolic variable
is only interpreted in userspace. Any other configuration file passed to ``nft``
would not be able to reference it. Similarly, retrieving the ruleset installed
in ``nftables`` (such as by using the ``nft list ruleset`` command) would
reconstruct the rules, but without any references to any symbolic variables.

Debugging
^^^^^^^^^

Netfilter integration
---------------------

The ``nftables`` component is integrated into the existing Netfilter subsystem
and uses the same hooks, stateful processing for connection tracking or NAT, and
functionality for userspace packet queueing and processing as the ``xtables``
subsystem.

A high-level understanding of the Netfilter framework is important for managing
firewall rules.  This section provides the necessary information and references
additional documentation.

Packet flow
~~~~~~~~~~~

A packet starts being handled by the Linux networking subsystem (and, by
extension, by Netfilter) through one of three options:

  * it is received by a network interface driver (whether for physical NIC or a
    virtual one);
  * it is generated by an application process on the system (via a socket);
  * it is generated by the kernel.

Netfilter is integrated into the wider Linux network subsystem. Packet
processing will go through multiple decision points, potentially modifying the
packet, such as:

  * fragment reassembly;
  * connection tracking;
  * routing decisions;
  * source and destination NAT (including port translation).

Netfilter provides hooks that allow Netfilter components to process a packet at
various stages. These are used by both ``nftables`` and ``xtables`` to execute
user-defined rules. In particular, the names of the predefined chains in the
legacy ``iptables`` / ``ip6tables`` / ``ebtables`` / ``arptables`` utilities are
derived from names of the Netfilter hooks:

  * ``ingress`` (only available for ``nftables``)
  * ``prerouting`` (for bridge and IP)
  * ``input`` (for ARP, bridge and IP)
  * ``forward`` (for bridge and IP)
  * ``postrouting`` (for bridge and IP)
  * ``output`` (for ARP, bridge and IP)
  * ``egress`` (only available for ``nftables``)

Packets will not traverse all hook points: this depends on the some of the
decisions made during the processing. This is represented graphically in the
diagram on the `Netfilter hooks nftables wiki page
<https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks>`_. In
particular, the use of bridges will result in a different packet flow, but one
which partially overlaps with the flow taken by non-bridged packets.

It should be noted that some of the standard packet processing is performed at
some of the hook points (fragment reassembly, connection tracking lookup, NAT),
while others are in-between hook points (routing decision). At each hook point,
the order of operations is defined by a priority. For example, these are some of
the standard operations executed at the IP layer ``prerouting`` hook:

.. csv-table::
    :header: Netfilter priority value, Operation
    :widths: auto

    -400, fragment reassembly
    -200, connection tracking lookup and association
    -100, destination NAT

If you register rules to be executed at priority value lower than ``-400`` (e.g.
``-500``), these will be executed before IP datagram fragments are reassembled.
As such the rules may see IP datagram fragments for which the transport header
may not be available, because they are not the first fragment. On the other
hand, rules registered at priority value higher than ``-400`` (e.g. ``-300``)
would not be able to make decisions based on fragmentation information (the
packet would look as if the entire IP datagram was received).

The priority values themselves do not hold any intrinsic meaning, other than the
fact that some standard operations are executed at well-known priority values.
For example, in absence of other context, registering rules at priority ``1000``
is no different from using priority ``1500``. The `nftables documentation
<https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks#Priority_within_hook>`_
lists the well-known priority values.

A packet stops being handled by the Linux networking subsystem, implying that no
more Netfilter hooks would be invoked, when one of these conditions occur:

  * the packet is dropped, either through a firewall rule or some other
    condition in the standard processing (e.g. blackhole route);
  * the packet is passed to an application process on the system (via a socket);
  * the packet is handled by the kernel (e.g. ICMP echo request - a ping);
  * the packet is sent out a network interface (whether for a physical NIC or a
    virtual one).

It should be noted that a particular packet can traverse the Netfilter hooks
several times, if one of the following conditions occur (FIXME: this is probably
not exhaustive, maybe leave as examples?):

  * the packet is sent out a virtual interface that loops the packet back to the
    same Linux kernel (e.g. `veth
    <https://manpages.ubuntu.com/manpages/en/man4/veth.4.html>`_ interfaces),
    although the list of hooks are not going to overlap completely;
  * Virtual Routing and Forwarding (VRF) is in use - a packet will traverse the
    L3 prerouting hook twice, once with the input interface set to the L3
    interface and once with the input interface set to the VRF interface.
  * the packet is processed and reinjected by the kernel into the networking
    stack (e.g. after IPsec encryption/decryption and ESP
    encapsulation/decapsulation - although the packet is admittedly modified,
    some of the state is maintained across this operation).

The Netfilter hooks and, hence, the ``nftables`` rules are managed independently
per `network namespace
<https://manpages.ubuntu.com/manpages/en/man7/network_namespaces.7.html>`_. As
such, different firewall rules are configured in each network namespace,
facilitating functionality such containers. This also means that if the two ends
of a veth pair are associated with different namespaces, they will be processed
by independent firewall rules.

Structure
---------

Rule composition
~~~~~~~~~~~~~~~~

Sets
~~~~

Maps
~~~~

Stateful objects
~~~~~~~~~~~~~~~~

Flowtables
~~~~~~~~~~
