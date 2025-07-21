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

Table of contents
-----------------

.. toctree::
   :maxdepth: 2
   :glob:

   nftables

Advantages
----------

There are several advantages to using ``nftables`` over the older alternatives:

* The expressions forming the packet classification rules are compiled in
  userspace to bytecode and executed by the kernel using a purpose-built virtual
  machine; this allows for far more flexibility.
* High-performance can be achieved through maps and concatenations: instead of
  linear rule processing (O(n)), constant time (O(1)) can be achieved.
* The syntax used by the userspace ``nft`` utility is declarative, instead of
  the procedural format required for ``ip/ip6/arp/ebtables``, simplifying
  management of firewall configuration
* Tables and chains are not predefined and the structure allows registering an
  arbitrary number of them: this facilitates the independent management of rules
  by multiple applications.
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

Changes to the ``nftables`` performed via the utility are ephemeral and will be
lost upon a reboot (or, more specifically, upon the destruction of the `network
namespace
<https://manpages.ubuntu.com/manpages/en/man7/network_namespaces.7.html>`_ to
which they are associated). Persistence can be achieved through the
aforementioned systemd service unit or similar mechanisms.

As an alternative invocation, a filename can be passed to the ``nft`` utility as
an argument using the ``-f`` flag.  The file can contain both commands, as well
as object definitions using a declarative syntax, which are implied to be
created. As with the command-line usage, all of the operations are performed
atomically. The default ``/etc/nftables.conf`` file contains a command to delete
all of the configured rules (``flush ruleset``) and a declarative definition of
a table named ``filter`` that processes both IPv4 and IPv6 packets in three
empty chains:

.. code-block:: nft
    :caption: /etc/nftables.conf

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

.. code-block:: nft
    :caption: /etc/nftables.conf

    #!/usr/sbin/nft -f

    # This empty definition is needed to allow the flush command to work if the
    # table is not already defined.
    table inet host-firewall; flush table inet host-firewall

    # Note that the flush command does not destroy the table or the objects
    # contained within, only clearing the rules within all of the chains. Use the
    # following instead, if the object definitions need to be changed or chains
    # completely destroyed.
    #destroy table inet host-firewall

    table inet host-firewall {
        chain firewall-input {
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
drop-in files to be add rules to the defined ``firewall-input`` chain (if
wildcards are used, the files need not exist):

.. code-block:: nft
    :caption: /etc/nftables.conf

    #!/usr/sbin/nft -f

    # This empty definition is needed to allow the flush command to work if the
    # table is not already defined.
    table inet host-firewall; flush table inet host-firewall

    # Note that the flush command does not destroy the table or the objects
    # contained within, only clearing the rules within all of the chains. Use the
    # following instead, if the object definitions need to be changed or chains
    # completely destroyed.
    #destroy table inet host-firewall

    table inet host-firewall {
        chain firewall-input {
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

.. code-block:: nft
    :caption: /etc/nftables.conf

    #!/usr/sbin/nft -f

    define IF_LOOPBACK = lo

    # This empty definition is needed to allow the flush command to work if the
    # table is not already defined.
    table inet host-firewall; flush table inet host-firewall

    # Note that the flush command does not destroy the table or the objects
    # contained within, only clearing the rules within all of the chains. Use the
    # following instead, if the object definitions need to be changed or chains
    # completely destroyed.
    #destroy table inet host-firewall

    table inet host-firewall {
        chain firewall-input {
            # Process packets destined for this host.
            type filter hook input priority filter;
            # Use a default-deny policy for packets.
            policy drop;

            # Allow traffic on the loopback interface(s).
            meta iif $IF_LOOPBACK accept

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

``nftables`` provides several means to debug firewall rules:

* Using the ``log`` statement, which can be associated with any rule and will
  result in some packet information being logged, either to the kernel log
  (which can read via ``dmesg``) or to a userspace application. This is
  described in more detail in the `nftables documentation
  <https://wiki.nftables.org/wiki-nftables/index.php/Logging_traffic>`_ and in
  the `manual page
  <https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#statements>`_, under
  ``LOG STATEMENT``.
* Setting the ``nftrace`` flag on a packet, which allows tracing all of the
  rules, within all chains and all tables, which a packet matches, also
  identifying any actions taken. This is described in more detail in the
  `nftables documentation
  <https://wiki.nftables.org/wiki-nftables/index.php/Ruleset_debug/tracing>`_.

Log statement
.............

The following example demonstrates the use of the ``log`` statement to send any
packets coming in on the loopback interface to the kernel log, before accepting
them:

.. code-block:: nft
    :caption: /etc/nftables.conf

    #!/usr/sbin/nft -f

    define IF_LOOPBACK = lo

    # This empty definition is needed to allow the flush command to work if the
    # table is not already defined.
    table inet host-firewall; flush table inet host-firewall

    # Note that the flush command does not destroy the table or the objects
    # contained within, only clearing the rules within all of the chains. Use the
    # following instead, if the object definitions need to be changed or chains
    # completely destroyed.
    #destroy table inet host-firewall

    table inet host-firewall {
        chain firewall-input {
            # Process packets destined for this host.
            type filter hook input priority filter;
            # Use a default-deny policy for packets.
            policy drop;

            # Allow traffic on the loopback interface(s).
            meta iif $IF_LOOPBACK \
                # Log the packets...
                log prefix "loopback packet: " \
                # ...and accept them.
                accept


            # Drop-in files can add rules here.
            include "/etc/nftables/input-rules.d/*.conf"
        }
    }

Checking ``dmesg`` would show messages such as the following (assuming packets
are actually flowing through the loopback interface):

.. code-block::

    [694077.575927] loopback packet: IN=lo OUT= MAC=00:00:00:00:00:00:00:00:00:00:00:00:08:00 SRC=127.0.0.1 DST=127.0.0.53 LEN=73 TOS=0x00 PREC=0x00 TTL=64 ID=24453 DF PROTO=UDP SPT=37969 DPT=53 LEN=53

Rule tracing
............

The ``nftrace`` flag enables tracing of a packet's flow through ``nftables``
rules across chains and tables, from the moment the flag is set to the moment
the packet processing is completed or the flag is unset. This functionality
allows complex debugging of ``nftables`` firewall rules. The packet information,
along with references to the rules traversed is sent to a userspace application
through the netlink interface. The ``nft monitor trace`` command can be used to
receive this information.

The ``meta nftrace set 1`` statement can be combined with a match expression to
set the flag, while ``meta nftrace set 0`` will clear it. If all the rules
traversed are to be identified, the flag should be set as early as possible. The
following examples creates two chains attached to the ``prerouting`` and
``output`` hooks, running as early as feasible (even before other chains
registered at the ``raw`` priority):

.. code-block:: nft
    :caption: /etc/nftables.conf

    #!/usr/sbin/nft -f

    define IF_LOOPBACK = lo

    # This empty definition is needed to allow the flush command to work if the
    # table is not already defined.
    table inet host-firewall; flush table inet host-firewall

    # Note that the flush command does not destroy the table or the objects
    # contained within, only clearing the rules within all of the chains. Use the
    # following instead, if the object definitions need to be changed or chains
    # completely destroyed.
    #destroy table inet host-firewall

    table inet host-firewall {
        chain trace-inbound {
            # Process after reassembly and conntrack lookup, but before other
            # potential raw chains.
            type filter hook prerouting priority raw - 10; policy accept;

            meta l4proto udp meta nftrace set 1
        }

        chain trace-outbound {
            # Process after conntrack lookup, but before other potential raw chains.
            type filter hook output priority raw - 10; policy accept;

            meta l4proto udp meta nftrace set 1
        }

        chain firewall-input {
            # Process packets destined for this host.
            type filter hook input priority filter;
            # Use a default-deny policy for packets.
            policy drop;

            # Allow traffic on the loopback interface(s).
            meta iif $IF_LOOPBACK accept

            # Drop-in files can add rules here.
            include "/etc/nftables/input-rules.d/*.conf"
        }
    }

The two rules will only match UDP datagrams, but irrespective of whether they're
transported by Ipv4 or IPv6 (``meta l4proto udp``). Running the ``nft monitor
trace`` command will produce messages such as:

.. code-block::

    trace id 78653943 inet host-firewall trace-inbound packet: iif "lo" @ll,0,112 0x800 ip saddr 127.0.0.53 ip daddr 127.0.0.1 ip dscp cs0 ip ecn not-ect ip ttl 1 ip id 64669 ip protocol udp ip length 168 udp sport 53 udp dport 36520 udp length 148 @th,64,96 0x2e4881800001000100000004
    trace id 78653943 inet host-firewall trace-inbound rule meta l4proto udp meta nftrace set 1 (verdict continue)
    trace id 78653943 inet host-firewall trace-inbound policy accept
    trace id 78653943 inet host-firewall firewall-input packet: iif "lo" @ll,0,112 0x800 ip saddr 127.0.0.53 ip daddr 127.0.0.1 ip dscp cs0 ip ecn not-ect ip ttl 1 ip id 64669 ip protocol udp ip length 168 udp sport 53 udp dport 36520 udp length 148 @th,64,96 0x2e4881800001000100000004
    trace id 78653943 inet host-firewall firewall-input rule ct state established,related accept (verdict accept)

The ``trace id`` will be the same for the same packet across different tables
and chains, allowing correlation between different output lines. Whenever a
packet starts being handled by a chain, a ``packet`` line is output with
information about the contents of the packet.

It should be noted that the tracing notifications received by the ``nft monitor
trace`` utility only contain identifier references to the tables, chains and
rules. ``nft monitor trace`` reads all of the rules when it is first started.
The table and chain names and actual rule content are reconstructed from that
initial read for every logged packet. This means that if the rules are changed
after the ``nft monitor trace`` utility is started, the output will either be
incomplete or inaccurate (because rule identifiers (handles), in particular, can
be reused), so a printed rule may not be the actual rule that a packet matched.

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

The list of functions, including ``nftables`` chains and standard Netfilter
processing, that have been registered can be listed with the following command
(note that the numerical values are the priorities and that they are listed in
decimal format):

.. code-block:: console

    sudo nft list hooks

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

* the packet is dropped, either through a firewall rule or some other condition
  in the standard processing (e.g. blackhole route);
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
* Virtual Routing and Forwarding (VRF) is in use - a packet will traverse the L3
  prerouting hook twice, once with the input interface set to the L3 interface
  and once with the input interface set to the VRF interface.
* the packet is processed and reinjected by the kernel into the networking stack
  (e.g. after IPsec encryption/decryption and ESP encapsulation/decapsulation -
  although the packet is admittedly modified, some of the state is maintained
  across this operation).

The Netfilter hooks and, hence, the ``nftables`` rules are managed independently
per `network namespace
<https://manpages.ubuntu.com/manpages/en/man7/network_namespaces.7.html>`_. As
such, different firewall rules are configured in each network namespace,
facilitating functionality such containers. This also means that if the two ends
of a veth pair are associated with different namespaces, they will be processed
by independent firewall rules.

Structure
---------

``nftables`` structures objects for managing the firewall in a hiearchy. The
primary terminology used is:

* **Rulesets**: this refers to all of the objects defined in ``nftables``; the
  command ``nft list ruleset`` will output everything defined in ``nftables``
  (within a particular network namespace), while ``nft flush ruleset`` will
  destroy all of the objects: tables, :ref:`sets <Sets>`, :ref:`maps <Maps>`,
  etc. This includes elements defined in sets and maps, or the contents of
  stateful objects (e.g.  counter values). As such, a command such as the
  following is effectively a no-op: ``(echo "nft flush rulset"; nft list
  ruleset) | nft -f -``.
* **Tables**: unlike ``xtables``, any number of tables can be defined in
  ``nftables``. These are collections of chains, :ref:`sets <Sets>`, :ref:`maps
  <Maps>` and stateful objects (e.g. counters). The table name does not hold any
  intrinsic meaning and can be named by system administrators or applications as
  desired. Tables are associated with an address family, dictating limitations
  on chains and determining what Netfilter hooks the chains will be associated
  with. The address families are documented in the `manual page
  <https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#address%20families>`_.
  These are:

  * **ip**: for IPv4 packets, as what the legacy ``iptables`` utility would
    manage.
  * **ip6**: for IPv6 packets, as what the legacy ``ip6tables`` utility would
    manage.
  * **inet**: for both IPv4 and IPv6 packets, simplifying management of
    consistent rules across both network protocols.
  * **arp**: for IPv4 ARP packets, as what the legacy ``arptables`` utility
    would manage.
  * **bridge**: for Ethernet packets traversing bridges, as what the legacy
    ``ebtables`` utility would manage.
  * **netdev**: for very early (on ingress) or very late (on egress) packet
    processing. This is useful for efficient filtering or load balancing, but
    imposes limitations, such as only supporting the ``ingress`` and ``egress``
    hooks and requiring strict association of chains with a *single* network
    interface. Note that starting with Linux 5.10, the **inet** family also
    supports the ``ingress`` hook without the single network interface
    limitation, largely reducing the usefulness of the **netdev** address
    family; using a single table in the **inet** family would also facilitate
    the sharing of :ref:`sets <Sets>` and :ref:`maps <Maps>` with chains
    registered at other hooks.
* **Chains**: containers for firewall rules; similarly to ``xtables``, there is
  a distinction between base chains and regular chains. Unlike in ``xtables``,
  the base chains are not predefined and as many as necessary can be created,
  including multiple chains at the same hooks (with or without the same
  priority).

  * **base chains** have a ``type``, a ``policy`` and are registered with a
    Netfilter ``hook`` point at a specific ``priority``. They can also have
    additional attributes, as described in the `manual page
    <https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#chains>`_. Their
    rules are evaluated whenever packet processing traverses the specified
    Netfilter hook.
  * **regular chains** are simply called upon by rules in other chains and can
    be thought of as subprocedures. They are useful to simplify maintenance of
    rules or to optimize rule processing (e.g. by using :ref:`verdict maps
    <Verdict maps>`). Rules within a regular chain are not evaluated during the
    processing of a packet, unless called upon, directly or indirectly, from a
    base chain.

For base chains, the most important attributes are:

* **type**: dictates the conditions on which a packet gets processed by the
  chain and the available hooks. Some statements are only available in certain
  chain types. The possible values are:

  * **filter**: generic type, applicable to all address families and all hooks.
    Used for typical firewall actions, as well as arbitrary packet
    modifications.
  * **nat**: this is equivalent to the chains defined in the legacy ``iptables``
    / ``ip6tables`` ``nat`` table. Only the first packet of a connection is
    processed by chains of this type. NAT actions (``snat``, ``dnat``,
    ``masquerade``, ``redirect``) can only be taken in these chains.
  * **route**: this has no equivalent in ``xtables``, but allows the integration
    of the ``nftables`` rules with policy routing. Packets which are about to go
    through a routing decision traverse chains of this type; even though the
    only hook available is called ``output``, the rules are evaluated for both
    locally-generated packets and received packets (before both routing
    decisions, as documented in the `Netfilter flow diagram
    <https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks#Netfilter_hooks_into_Linux_networking_packet_flows>`_).
    As an example, such chains can be used with the expresive power of
    ``nftables`` to assign a Netfilter packet mark that is subsequently used to
    select a routing table (see the manual page for `ip rule
    <https://manpages.ubuntu.com/manpages/en/man8/ip-rule.8.html>`_). FIXME:
    double-check this statement.
* **hook**: the processing point at which rules are evaluated, as described in
  the :ref:`Packet flow` section. It should be noted that not all hooks are
  available for all address families and all chain types. The restrictions are
  listed in the `manual page
  <https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#chains>`_.
* **priority**: dictates the order in which chains and other standard Netfilter
  operations are performed at a particular hook point, as described in the
  :ref:`Packet flow` section. Can be given as either a symbolic name (e.g.
  ``filter``, ``raw``, ``mangle``), a signed integer (e.g. ``0``, ``-300``) or a
  value relative to a symbolic name (e.g. ``raw - 10``). You should note that
  symbolic names may map to different integer values, depending on the address
  family (``filter`` is ``0`` for ``inet``, ``ip``, ``ip6``, ``arp`` and
  ``netdev``, but ``-200`` for ``bridge``).
* **policy**: dictates the verdict that is associated with a packet, if, during
  processing, none of the matched rules have a verdict. It must be one of
  ``accept`` (the default) or ``drop``.

It should be noted that, as described in the :ref:`Packet flow` section, a
packet stops being handled by the networking subsystem when it is either dropped
or it traverses the entire processing flow and is either sent out to an
interface or handled by an application or the kernel. As such, a verdict of
``drop`` is final for a packet, but one of ``accept`` is not: it is sufficient
for one chain in one table to ``drop`` a packet for it to be discarded, but the
packet must be ``accept``-ed by all chains in all tables for it to continue its
journey (i.e. an ``accept`` verdict only terminates the processing in a
particular base chain, but does not influence the processing in any other base
chains the packet will subsequently traverse).

Rule composition
~~~~~~~~~~~~~~~~

Rules are composed of expressions and statements, both of which are optional.
Expressions are used to match packets, while statements dictate what actions
should be be taken. A rule without statements is valid and be used for debugging
purposes, as it will be reported by the :ref:`rule tracing <Rule tracing>` for
any matched packets. For example, the following rule will match
locally-generated IPv4 UDP packets without taking any actions (note the use of
the `ip protocol udp` expression, as opposed to `meta l4proto udp`):

.. code-block:: nft
    :caption: /etc/nftables.conf

    #!/usr/sbin/nft -f

    table inet host-firewall {
        chain test-outbound {
            type filter hook output priority filter; policy accept;

            ip protocol udp
        }
    }

Expressions within a rule are combined with a logical **AND** when evaluated:
all of them must succeed for the rule's statements to be executed. Combining
expressions with a logical **OR** requires the use of multiple rules, :ref:`sets
<Sets>`, :ref:`maps <Maps>` or intervals. In the following example, the first
rule will match both IPv4 and IPv6 packets if both the transport protocol is UDP
(``meta l4proto udp``) and the destination port is ``53`` (``udp dport 53``).
The second rule will match packets if network protocol is IPv4 (implied), the
transport protocol is UDP (implied) and either:

* the IPv4 destination address is ``10.1.1.1`` and the destination port is
  ``53``
* the IPv4 destination address is ``10.2.2.2`` and the destination port is
  ``80`` or ``443``

The ``ip daddr . udp dport`` syntax is explained in the :ref:`Concatenations`
section.

.. code-block:: nft
    :caption: /etc/nftables.conf

    #!/usr/sbin/nft -f

    table inet host-firewall {
        chain test-outbound {
            type filter hook output priority filter; policy accept;

            # Transport protocol is UDP and destination port is 53.
            meta l4proto udp udp dport 53

            # Network protocol is IPv4, transport protocol is UDP and the
            # combination of IPv4 destination address and UDP destination port
            # is one of the following:
            ip daddr . udp dport {
                10.1.1.1 . 53,
                10.2.2.2 . 80,
                10.2.2.2 . 443
            }
        }
    }

A rule can contain zero or more statements. There are two types of statements:
`terminal` and `non-terminal`. Terminal statements unconditionally terminate the
rule's evaluation and may also terminate the chain's evaluation or entirely stop
the pocket's processing. Non-terminal statements results in actions which either
do no terminate the rule's evaluation or only do so conditionally. The only
limitation is that a rule may have at most one terminal statement, which must
also be placed last. Most of the :ref:`verdict statements <Verdict statements>`
are terminal statements, but there are also some non-verdict terminal statements
(e.g. ``reject``, which drops a packet and generates an ICMP or TCP reset
response).

Verdict statements
^^^^^^^^^^^^^^^^^^

Verdict statements affect the control flow of rule evaluation, with most of them
(apart from ``continue``) being terminal statements. The ``continue`` statement
is implied, if no other terminal statement is associated with a rule. The
following is the list of verdict statements:

* **accept**: terminates the processing of the packet in the current base chain,
  allowing the packet to continue its journey within Netfilter and the Linux
  networking subsystem. Other base chains registered at the current hook,
  registered with a numerical priority value that is higher will still evaluate
  the packet and may still drop it. Using this statement in a regular chain
  called, directly or indirectly, from a base chain stops the processing of all
  subsequent rules, both in the current chain and in chains higher up the call
  stack.
* **drop**: terminates the processing of the packet within the Linux networking
  subsystem with no further action. This statement is the basis of a firewall
  implementation. No further base chains are invoked.
* **queue**: terminates the processing of the packet in the current base chain
  and passes the packet to userspace for further processing. The userspace must
  provide a verdict of ``accept`` or ``drop``. This is explained in the
  `nftables userspace queueing documentation
  <https://wiki.nftables.org/wiki-nftables/index.php/Queueing_to_userspace>`_.
* **continue**: implied action if no other terminal statement is issued: the
  rules' evaluation continues with the next rule in current chain.
* **jump**: continue processing in a new regular chain; upon completion,
  processing returns to the current chain, unless a processing-terminating
  statement (such as ``accept``, ``drop``, ``queue`` or ``reject``) is issued in
  one of the invoked chains. From a procedural programming perspective, this is
  similar to invoking a subprocedure (pseudocode: ``call subprocedure()``).
* **goto**: continue processing in anew regular chain; upon completion, the
  processing does *not* return to the current chain, but the chain higher up in
  the call next (if the current chain is a base chain, the policy action is
  taken, instead). From a procedural programming perspective, this is similar to
  invoking a returning the result of a subprocedure (pseudocode: ``return
  subprocedure()``).

The following example extends the previous firewall definition with the skeleton
structure for two new functions, demonstrating some control flow functionality:

* Setting the Netfilter packet mark (FIXME: authoritative docs on nfmark?) for
  inbound packets to represent where the packet originated from, in order to
  allow subsequent rules to make decisions based on this criteria. We're calling
  this the realm, but it should not be confused with `iproute2 realms
  <https://manpages.ubuntu.com/manpages/en/man8/ip-route.8.html>`_. For example,
  the rules below set the mark to the value ``1`` (via the symbolic variable
  ``MARK_REALM_LOCAL``) if the packet was received on one of the loopback
  interfaces. Two new chains are introduced: ``mark-inbound`` (a base chain) and
  ``mark-inbound-determine`` (a regular chain).

  * When packet processing follows the packet through an input VRF interface
    (``meta iifkind "vrf"``), we're terminating the packet processing in this
    chain via ``return``. The ``return`` statement, as it is contained in a base
    chain, is equivalent to the invocation of the chain's policy (``accept`` in
    this instance).
  * If a packet comes in to this chain with a non-zero packet mark (``meta mark
    != 0``), a condition which can occur when functionality such as the GBP
    extension of VXLAN are in use, the packet is dropped completely.
  * The ``mark-inbound-determine`` regular chain is invoked via a ``jump
    mark-inbound-determine``; this allows subsequent rules in the
    ``mark-inbound`` chain to be evaluated.
  * In the ``mark-inbound-determine`` chain, if a packet is received on one of
    the interfaces defined in the ``IF_LOOPBACK`` symbolic variable (``meta iif
    $IF_LOOPBACK``), two statements are executed:

    * the packet mark is set to the ``MARK_REALM_LOCAL`` value, defined as ``1``
      (``meta mark set $MARK_REALM_LOCAL``), a non-terminal statement;
    * the processing in the ``mark-inbound-determine`` chain is terminated via a
      ``return`` statement, with the packet continuing its processing in the
      caller chain (``mark-inbound``).
* In the ``firewall-input`` base chain, processing of multicast packets is
  delegated to the ``firewall-input-multicast`` regular chain.

  * The ``goto`` statement ensures that the subsequent rules in
    ``firewall-input`` are not evaluated, even if the called chain executes a
    ``return`` statements or some packets are not matched by any rules; instead,
    the policy (``drop``) will apply in these instances.
  * The ``accept`` statement is necessary in the ``firewall-input-multicast``
    chain to allow packets through. Once one of the conditions is reached (e.g.
    ``ip protocol igmp``), the processing is finalised and no further rules in
    ``firewall-input-multicast`` or ``firewall-input`` are evaluated.

.. code-block:: nft
    :caption: /etc/nftables.conf

    #!/usr/sbin/nft -f

    define IF_LOOPBACK = lo

    define MARK_REALM_LOCAL = 1

    # This empty definition is needed to allow the flush command to work if the
    # table is not already defined.
    table inet host-firewall; flush table inet host-firewall

    # Note that the flush command does not destroy the table or the objects
    # contained within, only clearing the rules within all of the chains. Use the
    # following instead, if the object definitions need to be changed or chains
    # completely destroyed.
    #destroy table inet host-firewall

    table inet host-firewall {
        chain mark-inbound {
            type filter hook prerouting priority raw; policy accept;

            # When VRF interfaces are in use, packets go through the prerouting hook
            # twice, once with the VRF interface set as input and another time with
            # actual interface set as input.
            meta iifkind "vrf" return

            # Do not allow inbound packets that have an externally-determined packet
            # mark (this is possible, for example, by using VXLAN with the GBP
            # extension).
            meta mark != 0 drop
            jump mark-inbound-determine
        }

        chain mark-inbound-determine {
            # Set the realm to LOCAL for packets received on the loopback interface.
            meta iif $IF_LOOPBACK meta mark set $MARK_REALM_LOCAL return
        }

        chain firewall-input {
            # Process packets destined for this host.
            type filter hook input priority filter;
            # Use a default-deny policy for packets.
            policy drop;

            # Allow traffic on the loopback interface(s).
            meta iif $IF_LOOPBACK accept

            # Process multicast packets. Upon returning, do not evaluate any more
            # rules and apply the policy verdict (drop).
            meta pkttype multicast goto firewall-input-multicast

            # Drop-in files can add rules here.
            include "/etc/nftables/input-rules.d/*.conf"
        }

        chain firewall-input-multicast {
            # Allow any IPv4 IGMP.
            ip protocol igmp accept

            # Allow inbound Multicast DNS packets.
            udp dport 5353 accept

            # If no prior action was taken, this will return to the calling chain
            # (firewall-input).
        }
    }

Other statements
^^^^^^^^^^^^^^^^

``nftables`` supports a large number of statements. These are documented in the
`Statements section of the manual package
<https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#statements>`_. While
this document is not meant to exhaustively list all of them, some of the more
commonly-used ones are:

* **reject statement**: drops a packet, but also generates an appropriate ICMP
  or TCP reset response. For example, the rule ``udp dport 389 reject with icmpx
  admin-prohibited`` will match packets destinated for the LDAP port (``udp
  dport 389``) and generate a network-protocol-appropriate admin-prohibited ICMP
  response (type ``3`` code ``13`` for `IPv4
  <https://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml#icmp-parameters-codes-3>`_
  and type ``1`` code ``1`` for `IPv6
  <https://www.iana.org/assignments/icmpv6-parameters/icmpv6-parameters.xhtml#icmpv6-parameters-codes-2>`_).
* **log statement**: described in the :ref:`Log statement` section.
* **meta statements**: allow changed meta information tracked by Netfilter for a
  particular packet, such as ``meta mark set 42`` for setting the Netfilter
  packet mark to the constant value ``42`` or ``meta nftrace set 1`` for
  enabling :ref:`rule tracing <Rule tracing>`.
* **nat statements**: allow source and destination network address translation
  (NAT) to occur (including support for dynamic translation for transport
  protocol ports and the stateful processing of ICMP packets).
* **counter statements**: support for counting packets and bytes matched by
  rules.
* **payload statements**: allow changing arbitrary contents of the packets: for
  example, ``ip dscp set 46`` sets the IPv4 DSCP field to 46 (EF - Expedited
  Forwarding).
* **set statement**: allows dynamically adding elements to :ref:`sets <Sets>`
  and :ref:`maps <Maps>`. These are explained in the respective sections.
* **map statement**: allows looking up elements in a :ref:`map <Maps>` by an
  arbitrary key and returning the associated value for use as an argument to a
  different statement. This is an example of a non-terminal statement that can
  conditionally terminate the rule's processing, if no element in the map
  matches the input key. It is explained in more detail in the :ref:`Maps`
  section.
* **vmap statement**: allows dynamically determining the verdict for a rule
  based on an abitrary key and is explained in more detail in the :ref:`Verdict
  maps` section.

Expressions
^^^^^^^^^^^

``nftables`` expressive power comes from its implementation of a bytecode-based
virtual machine for the evaluation of expressions. An expression has an
associated data type, which determines how operations are evaluated on the
expression and how it can be combined with other expressions or used as
arguments to a statement. For example, the ``meta mark`` expression has an
32-bit integer data type. These are listed in the `manual page's Data Types
<https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#data%20types>`_
section.

An expression's data type can be displayed using the ``nft describe`` command,
such as the following:

.. code-block:: console

    nft describe udp dport.

The expressions generally follow the convention of a class followed by an
attribute (e.g. ``udp dport``, ``ip protocol`` or ``meta mark``). These are
documented in the manual page in the `Primary Expressions
<https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#primary%20expressions>`_
and `Payload Expressions
<https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#payload%20expressions>`_
sections.

Expressions can be combined with comparison operators to form `relational
expressions
<https://wiki.nftables.org/wiki-nftables/index.php/Building_rules_through_expressions>`_,
which are used to matching packets. These are:

* ``eq`` or ``==``: this is the implied comparison (``udp dport 53`` is
  equivalent to ``udp dport == 53``). It can compare an arbitrary expression
  with a constant value or look the expression up in a set (``udp dport == { 80,
  443 }`` matches if the destination port is either 80 or 443).
* ``ne`` or ``!=``: this matches if an arbitrary expression is not equal to a
  constant value (e.g. ``udp dport != 53``) or does not exist in a set (``udp
  dport != { 80, 443}`` matches if the destination is neither 80, nor 443).
* ``lt`` / ``<``, ``gt`` / ``>``, ``le`` / ``<=`` and ``ge`` / ``>=``: these
  match if the comparison of an arbitrary expression is lower than, greater
  than, lower than or equal and greater than or equal, respectively, to a
  constant value (e.g. ``udp dport < 1024`` matches privileged UDP ports).

Expressions can also be combinary with binary operators, such as a:

* ``and`` / ``&``: binary AND
* ``or`` / ``|``: binary OR
* ``xor`` / ``^``: binary exclusive-OR
* ``lshift`` / ``<<``: binary left shift
* ``rshift`` / ``>>``: binary right shift

The right-hand side of the binary operators must be a constant expression. For
example, the following expression would match IPv4 packets for which the second
most-significant byte of the destination IP address is smaller than 16:

.. code-block:: nft

    (ip daddr >> 16) & 0xFF < 0x10

Then same condition can be written as:

.. code-block:: nft

    ip daddr & 0x00F00000 == 0

Or, in a rather less readable manner, as:

.. code-block:: nft

    ip daddr & 0x00F00000 0

The equality and non-equality operators can also be used with `intervals
<https://wiki.nftables.org/wiki-nftables/index.php/Intervals>`_, matching if the
expression's value is (or, respectively, isn't) within the closed interval. The
following expression matches IPv4 packets for which the destination address has
the form A.B.C.D, with B having a value between 10 and 20 (inclusive):

.. code-block:: nft

    (ip daddr >> 16) & 0xFF == 10-20

IPv4 and IPv6 addresses also support prefix notation, with the following
matching if the destination IPv4 address is not one of the RFC1918 private
addresses:

.. code-block:: nft

    ip daddr != { 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 }

Not all of the operations are supported by all data types. For example, IPv6
addresses do not support bit shifting, and the ``and``, ``or`` and ``xor``
operators require full IPv6 addresses on the right-hand side, as do the
comparison operators.

Combining expression operators with statements that support expressions is also
possible. For example, the following expression sets the Netfilter packet mark
to the least-significant 16 bits of the IPv4 source address, combined with bit
16 set, but only if the IPv4 source address is within the 10.0.0.0/16 prefix.

.. code-block:: nft
    ip saddr 10.0.0.0/16 meta mark set (ip saddr & 0xFFFF) | 0x10000

Concatenations
^^^^^^^^^^^^^^

Sets
~~~~

Maps
~~~~

Verdict maps
~~~~~~~~~~~~

Stateful objects
~~~~~~~~~~~~~~~~

Flowtables
~~~~~~~~~~
