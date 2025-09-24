nftables
========

`nftables <https://www.nftables.org/projects/nftables/index.html>`_ is a
component in the Linux Netfilter subsystem that provides the most modern
framework for defining packet classification and filtering functionality. As
such, it is a successor to the ``xtables`` kernel component and its associated
``iptables`` / ``ip6tables`` / ``arptables`` / ``ebtables`` userspace utilities.

This documentation uses the term ``nftables`` when referring to the Linux kernel
component and ``nft`` when referring to the userspace utility. Please note that
the Ubuntu package that provides the userspace utility is called ``nftables``
and this documentation will refer to it as the ``nftables`` Ubuntu package.

This page gradually builds an example ``nftables`` configuration file that is
adequate for a Linux host which offers network services (such as SSH and HTTP)
over IPv4 and IPv6 connectivity to a Local Area Network (LAN).

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

In general, most of the rules that can be defined using ``iptables``,
``ip6tables``, ``arptables`` and ``ebtables`` can also be defined using
``nftables``, but not the other way around. It is strongly recommended that you
only use one of two approaches to managing firewall rules. Otherwise, the
interaction between the different rules or services that set them up may be
unexpected and lead to either insecure configurations or block traffic that is
meant to be allowed. Furthermore, certain applications, such as container
orchestration systems or VPN utilities may configure firewall rules, resulting
in unexpected rule interactions.

There are still certain ``xtables`` rules which cannot be defined using
``nftables``, as documented in the `feature compatibility nftables wiki page
<https://wiki.nftables.org/wiki-nftables/index.php/Supported_features_compared_to_xtables>`_.
The gaps have been reduced over recent ``nft`` and Linux kernel releases,
which means that older Ubuntu versions might have more limited support.
Additionally, it should be noted that some of the functionality available via
the ``nftables`` Netlink interface may not be supported by the userspace ``nft``
utility yet (e.g. support for rules invoking eBPF programs).

Starting with Ubuntu 16.04 Xenial Xerus, the ``iptables`` package has provided
versions of the ``iptables``, ``ip6tables``, ``arptables`` and ``ebtables``
tools that work with the ``nftables`` API and provide a compatible interface to
the legacy implementation. The ``nftables`` backend, used by the
``iptables-nft`` / ``ip6tables-nft`` / ``arptables-nft`` / ``ebtables-nft``
utilities, has been the default since Ubuntu 20.10 Groovy Gorilla. These are
managed through the alternatives system and the current configuration can be
displayed with the following commands:

.. code-block:: console

    update-alternatives --display iptables
    update-alternatives --display ip6tables
    update-alternatives --display arptables
    update-alternatives --display ebtables

The ``iptables-nft`` / ``ip6tables-nft`` / ``arptables-nft`` / ``ebtables-nft``
utilities assume that no other application manages ``nftables`` rules natively
and hence should not be combined with other approaches to Netfilter firewall
rule management.

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
documentation will only cover the use of the ``nft`` utility, with a focus on
the configuration file format.

Starting with Ubuntu 15.04 Vivid Vervet, the ``nftables`` package provides a
systemd service unit file that is disabled by default. If enabled, the service
unit file will automatically load ``nftables`` configuration from the
``/etc/nftables.conf`` file (a mock file that does not perform any filtering is
provided in the ``nftables`` package). You can enable this and load the
configuration using the following commands:

.. code-block:: console

    sudo systemctl enable nftables.service
    sudo systemctl start nftables.service

Command-line usage
~~~~~~~~~~~~~~~~~~

The ``nft`` utility can accept one or more commands as arguments to manage any
of the objects (tables, rules, sets, etc.) supported. For example, the following
command will list all of the firewall rules:

.. code-block:: console

    sudo nft list ruleset

All operations are performed atomically: the processing of a packet will either
see the firewall rules defined prior to the invocation of the utility or the
firewall rules with all of the requested changes applied. The following command
will create two tables that process both IPv4 and IPv6 packets:

.. code-block:: console

    sudo nft "add table inet foo; add table inet bar"

Changes to the ``nftables`` rulesets performed via the utility are ephemeral and
will be lost upon a reboot (or, more specifically, upon the destruction of the
`network namespace
<https://manpages.ubuntu.com/manpages/en/man7/network_namespaces.7.html>`_ to
which they are associated). Persistence can be achieved through the
aforementioned systemd service unit or similar mechanisms.

As an alternative invocation, a filename can be passed to the ``nft`` utility as
an argument using the ``-f`` flag. The file can contain both commands, as well
as object definitions using a declarative syntax, which are implied to be
created. As with the command-line usage, all of the operations are performed
atomically. The default ``/etc/nftables.conf`` file contains a command to delete
all of the configured rules (``flush ruleset``) and a declarative definition of
a table named ``filter`` that processes both IPv4 and IPv6 packets in three
empty chains:

.. code-block:: nft
    :caption: /etc/nftables.conf
    :linenos:

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

    sudo /etc/nftables.conf

Alternatively, the systemd unit file supports the ``reload`` command to achieve
the same objective:

.. code-block:: console

    sudo systemctl reload nftables.service

Configuration file format
~~~~~~~~~~~~~~~~~~~~~~~~~

The configuration file is line-oriented. Multiple commands can be combined on
the same line by separating them with semicolons (``;``). Comments can be
included by using the hash sign (``#``) and span until the end of the line.
Commands can be split across multiple lines by escaping the end-of-line with a
backslash (``\``); a line containing only comments will not be considered a
continuation line (it will be skipped over), but an empty line would be
considered a continuation line, effectively ending the rule. Whitespace (and
hence, indentation) does not matter.

Even though the declarative syntax uses braces (``{`` and ``}``) to define
blocks containing an object's definition, the line-oriented processing is still
enforced and must be taken into account (e.g. the opening brace (``{``) must be
on the same line as the object type and name. The following example establishes
a base for a host firewall configuration file, which will be expanded upon
throughout this documentation:

.. code-block:: nft
    :caption: /etc/nftables.conf
    :linenos:

    #!/usr/sbin/nft -f

    # This empty definition is needed to allow the flush command to work if the
    # table is not already defined.
    table inet host-firewall; flush table inet host-firewall

    # Note that the flush command does not destroy the table or the objects
    # contained within, only clearing the rules within all of the chains. Use the
    # following instead, if the object definitions need to be changed, chains
    # completely destroyed or sets/maps cleared.
    #destroy table inet host-firewall

    table inet host-firewall {
        chain firewall-input {
            # Process packets destined for this host.
            type filter hook input priority filter;
            # Use a default-deny policy for packets.
            policy drop;
        }
    }

When using configuration files to load firewall rules, it is imperative to clear
the prior configuration. The declarative syntax will not replace chain rules,
but rather append them at the end of the previously defined chain. Deciding
which command to use to clear the prior configuration depends on several
considerations:

* ``flush ruleset`` will clear the entire ``nftables`` configuration, including
  all :ref:`tables, chains and rules <Structure>`, :ref:`sets <Sets>` or
  :ref:`maps <Maps>`, :ref:`stateful objects <Stateful objects>` and their
  contents, and :ref:`flowtables <Flowtables>`. While appropriate for a single
  central definition of the firewall rules, it may lead to unexpected results if
  elements in sets or maps are managed externally or if tables are managed by
  any other application.
* ``destroy table`` will delete a table and all objects associated with them,
  including :ref:`chains and rules <Structure>`, :ref:`sets <Sets>` or
  :ref:`maps <Maps>`, :ref:`stateful objects <Stateful objects>`, and
  :ref:`flowtables <Flowtables>`. This is particularly useful when settings
  associated to the objects can be changed across versions of the configuration
  file (such as the priority associated to a base chain) or when elements in
  sets or maps should be deleted and recreated.
* ``flush table`` will clear the rules within tables, but will not delete the
  chains, :ref:`sets <Sets>` and :ref:`maps <Maps>` or their elements,
  :ref:`stateful objects` or :ref:`flowtables <Flowtables>`. This is appropriate
  when elements in sets or maps are managed externally or state kept by
  :ref:`stateful objects <Stateful objects>` should not be reset.

The include directive
^^^^^^^^^^^^^^^^^^^^^

Files can be included by using the ``include`` directive. These are interpreted
in the context in which the directive is used. For example, the following allows
drop-in files to add rules to the defined ``firewall-input`` chain from
``/etc/nftables/input-rules.d/`` and any other tables to be defined in files
under ``/etc/nftables/tables.d/`` (if wildcards are used, the files need not
exist):

.. code-block:: nft
    :caption: /etc/nftables.conf
    :linenos:
    :emphasize-lines: 21,25

    #!/usr/sbin/nft -f

    # This empty definition is needed to allow the flush command to work if the
    # table is not already defined.
    table inet host-firewall; flush table inet host-firewall

    # Note that the flush command does not destroy the table or the objects
    # contained within, only clearing the rules within all of the chains. Use the
    # following instead, if the object definitions need to be changed, chains
    # completely destroyed or sets/maps cleared.
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

    include "/etc/nftables/tables.d/*.conf"

Symbolic variables
^^^^^^^^^^^^^^^^^^

Symbolic variables increase the maintainability of the firewall rules by
associating names to arbitrary expressions, which can then be reused throughout
the configuration. Associating the name ``IF_LOOPBACK`` to the interface name
``lo`` (the standard Linux loopback interface) allows defining a rule that
references it:

.. code-block:: nft
    :caption: /etc/nftables.conf
    :linenos:

    #!/usr/sbin/nft -f

    define IF_LOOPBACK = lo

    # This empty definition is needed to allow the flush command to work if the
    # table is not already defined.
    table inet host-firewall; flush table inet host-firewall

    # Note that the flush command does not destroy the table or the objects
    # contained within, only clearing the rules within all of the chains. Use the
    # following instead, if the object definitions need to be changed, chains
    # completely destroyed or sets/maps cleared.
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

    include "/etc/nftables/tables.d/*.conf"

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
reconstruct the rules, but without any references to symbolic variables.

Debugging
^^^^^^^^^

``nftables`` provides several means to debug firewall rules:

* Using the ``log`` statement, which can be associated with any rule and will
  result in packet information being logged, either to the kernel log (which can
  read via ``dmesg``) or to a userspace application. This is described in more
  detail in the `nftables documentation
  <https://wiki.nftables.org/wiki-nftables/index.php/Logging_traffic>`_ and in
  the `manual page
  <https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#statements>`_, under
  ``LOG STATEMENT``.
* Setting the ``nftrace`` flag on a packet, which allows tracing all of the
  rules which a packet matches, within all chains and all tables, also
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
    :linenos:

    #!/usr/sbin/nft -f

    define IF_LOOPBACK = lo

    # This empty definition is needed to allow the flush command to work if the
    # table is not already defined.
    table inet host-firewall; flush table inet host-firewall

    # Note that the flush command does not destroy the table or the objects
    # contained within, only clearing the rules within all of the chains. Use the
    # following instead, if the object definitions need to be changed, chains
    # completely destroyed or sets/maps cleared.
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

    include "/etc/nftables/tables.d/*.conf"

Checking ``dmesg`` would show messages such as the following (assuming packets
are actually flowing through the loopback interface):

.. code-block::

    [694077.575927] loopback packet: IN=lo OUT= MAC=00:00:00:00:00:00:00:00:00:00:00:00:08:00 SRC=127.0.0.1 DST=127.0.0.53 LEN=73 TOS=0x00 PREC=0x00 TTL=64 ID=24453 DF PROTO=UDP SPT=37969 DPT=53 LEN=53

Rule tracing
............

The ``nftrace`` flag enables tracing of a packet's flow through ``nftables``
rules across chains and tables, from the moment the flag is set to the moment
the packet processing is completed or the flag is cleared. This functionality
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
    :linenos:

    #!/usr/sbin/nft -f

    define IF_LOOPBACK = lo

    # This empty definition is needed to allow the flush command to work if the
    # table is not already defined.
    table inet host-firewall; flush table inet host-firewall

    # Note that the flush command does not destroy the table or the objects
    # contained within, only clearing the rules within all of the chains. Use the
    # following instead, if the object definitions need to be changed, chains
    # completely destroyed or sets/maps cleared.
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

    include "/etc/nftables/tables.d/*.conf"

The two rules will only match UDP datagrams, but irrespective of whether they're
transported by IPv4 or IPv6 (``meta l4proto udp``) and then activate rule
tracing for those packets (``meta nftrace set 1``). Running the ``nft monitor
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

Bytecode inspection
...................

The bytecode interpreted by the Linux kernel can be observed by using the
``--debug=netlink`` argument to ``nft``. This works both for commands that
modify rules (e.g. adding a new rule), as well as for those that retrieve rules.
The bytecode is printed alongside the rule handle (rule identifier). The
``--handle`` option can also be useful to print the handles associated with each
rule.

For example, listing the ``trace-inbound`` chain created above:

.. code-block:: console

    sudo nft --handle --debug=netlink list chain inet host-firewall trace-inbound

Produces the following output:

.. code-block:: nft-output

    inet host-firewall trace-inbound 13
      [ meta load l4proto => reg 1 ]
      [ cmp eq reg 1 0x00000011 ]
      [ immediate reg 1 0x00000001 ]
      [ meta set nftrace with reg 1 ]

    table inet host-firewall {
        chain trace-inbound { # handle 1
            type filter hook prerouting priority raw - 10; policy accept;
            meta l4proto udp meta nftrace set 1 # handle 13
        }
    }

Netfilter integration
---------------------

The ``nftables`` component is integrated into the existing Netfilter subsystem
and uses the same hooks, stateful processing for connection tracking or Network
Address Translation (NAT), and functionality for userspace packet queueing and
processing as the ``xtables`` subsystem.

A high-level understanding of the Netfilter framework is important for managing
firewall rules. This section provides the necessary information and references
additional documentation.

Packet flow
~~~~~~~~~~~

A packet starts being handled by the Linux networking subsystem (and, by
extension, by Netfilter) through one of three options:

* it is received by a network interface driver (whether for a physical Network
  Interface Controller (NIC) or a virtual one);
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

Packets will not traverse all hook points, depending on some of the decisions
made during the processing. This is represented graphically in the diagram on
the `Netfilter hooks nftables wiki page
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

If you register rules to be executed at a priority value lower than ``-400``
(e.g.  ``-500``), these will be executed before IP datagram fragments are
reassembled. As such the rules may see IP datagram fragments for which the
transport header may not be available, because they are not the first fragment.
On the other hand, rules registered at priority value higher than ``-400`` (e.g.
``-300``) would not be able to make decisions based on fragmentation information
(the packet would look as if the entire IP datagram was received).

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
several times, in conditions such as the followings:

* the packet is sent out a virtual interface that loops the packet back to the
  same Linux kernel (e.g. `veth
  <https://manpages.ubuntu.com/manpages/en/man4/veth.4.html>`_ interfaces),
  although the list of hooks are not going to overlap completely; FIXME: does
  this even make sense? Of course a packet sent out a veth is going to come back
  in on the pair... nfmark is not maintained - for all intents and purposes,
  this is a new packet.
* Virtual Routing and Forwarding (VRF) is in use - a packet will traverse the L3
  prerouting hook twice, once with the input interface set to the L3 interface
  and once with the input interface set to the VRF interface.
* the packet is processed and reinjected by the kernel into the networking stack
  (e.g. after IPsec encryption/decryption and ESP encapsulation/decapsulation in
  tunnel mode - although the packet is admittedly different, some of the state
  is maintained across this operation, such as the Netfilter mark). FIXME:
  technically, this is a different packet - does it even make sense? Same
  applies to other L3 encapsulations, e.g. vxlan.

The Netfilter hooks and, hence, the ``nftables`` rules are managed independently
per `network namespace
<https://manpages.ubuntu.com/manpages/en/man7/network_namespaces.7.html>`_. As
such, different firewall rules are configured in each network namespace,
facilitating functionality such as containers. This also means that if the two
ends of a veth pair are associated with different namespaces, they will be
processed by independent firewall rules.

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
  following is effectively a no-op (although the state may change between the
  moment it is read and the moment it is overwritten): ``(echo "nft flush
  rulset"; nft list ruleset) | nft -f -``.
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
    of the ``nftables`` rules with policy routing. This can only be used with
    locally-generated packets (either from processes or the kernel), with the
    only hook available being ``output``. As per the `Netfilter flow diagram
    <https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks#Netfilter_hooks_into_Linux_networking_packet_flows>`_,
    the routing decision for locally-generated packets is performed before any
    hooks. However, if the rules in a chain of type ``route`` modify parts of a
    packet or its metadata (e.g. the Netfilter mark) that are used in `policy
    routing decisions
    <https://manpages.ubuntu.com/manpages/en/man8/ip-rule.8.html>`_, another
    route lookup will be performed. Packets received from a network interface do
    not require this special chain type, as there are several hooks available
    that can prepare a packet before it goes through routing decisions.
* **hook**: the processing point at which rules are evaluated, as described in
  the :ref:`Packet flow` section. It should be noted that not all hooks are
  available for all address families and all chain types. The restrictions are
  listed in the `Chains section of the manual page
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
should be be taken. A rule without statements is valid and can be used for
debugging purposes, as it will be reported by the :ref:`rule tracing <Rule
tracing>` for any matched packets. For example, the following rule will match
locally-generated IPv4 UDP packets without taking any actions (note the use of
the `ip protocol udp` expression, as opposed to `meta l4proto udp`: this will
match only IPv4 packets):

.. code-block:: nft
    :caption: /etc/nftables/tables.d/test-firewall.conf
    :linenos:

    #!/usr/sbin/nft -f

    destroy table inet test-firewall
    table inet test-firewall {
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
The second rule will match packets if the network protocol is IPv4 (implied),
the transport protocol is UDP (implied) and either:

* the IPv4 destination address is ``10.1.1.1`` and the destination port is
  ``53``
* the IPv4 destination address is ``10.2.2.2`` and the destination port is
  ``80`` or ``443``

The ``ip daddr . udp dport`` syntax is explained in the :ref:`Concatenations`
section.

.. code-block:: nft
    :caption: /etc/nftables/tables.d/test-firewall.conf
    :linenos:

    #!/usr/sbin/nft -f

    destroy table inet test-firewall
    table inet test-firewall {
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
the pocket's processing. Non-terminal statements result in actions which either
do not terminate the rule's evaluation or only do so conditionally. The only
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
* **goto**: continue processing in a new regular chain; upon completion, the
  processing does *not* return to the current chain, but the chain higher up in
  the call stack (if the current chain is a base chain, the policy action is
  taken, instead). From a procedural programming perspective, this is similar to
  invoking and returning the result of a subprocedure (pseudocode: ``return
  subprocedure()``).

The following example extends the previous firewall definition with the skeleton
structure for two new functions, demonstrating some control flow functionality:

* Setting the Netfilter packet mark for inbound packets to represent where the
  packet originated from, in order to allow subsequent rules to make decisions
  based on this criteria. We're calling this the realm, but it should not be
  confused with `iproute2 realms
  <https://manpages.ubuntu.com/manpages/en/man8/ip-route.8.html>`_. For example,
  the rules below set the mark to the value ``1`` (via the symbolic variable
  ``MARK_REALM_LOCAL``) if the packet was received on one of the loopback
  interfaces. Two new chains are introduced: ``early-inbound`` (a base chain)
  and ``mark-inbound-determine`` (a regular chain).

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
    ``early-inbound`` chain to be evaluated.
  * In the ``mark-inbound-determine`` chain, if a packet is received on one of
    the interfaces defined in the ``IF_LOOPBACK`` symbolic variable (``meta iif
    $IF_LOOPBACK``), two statements are executed:

    * the packet mark is set to the ``MARK_REALM_LOCAL`` value, defined as ``1``
      (``meta mark set $MARK_REALM_LOCAL``), a non-terminal statement;
    * the processing in the ``mark-inbound-determine`` chain is terminated via a
      ``return`` statement, with the packet continuing its processing in the
      caller chain (``early-inbound``).
* In the ``firewall-input`` base chain, processing of multicast packets is
  delegated to the ``firewall-input-multicast`` regular chain. This allows
  multicast logic to be encapsulated in a separate chain, aiding
  maintainability. The base configuration accepts IPv4 IGMP packets, as they are
  needed for a standard multicast-ready network topology with multicast queriers
  (and possibly bridge multicast snooping, required for efficient layer-2
  multicast forwarding). The IPv6-equivalent MLD rule is introduced in the
  :ref:`Sets` section. Separately, Multicast DNS (mDNS) packets, which are also
  used by the DNS Service Discovery (DNS-SD) protocol, are allowed through a
  separate rule (``udp dport 5353 accept``). mDNS is typically used in LANs for
  ad-hoc service discovery, such as for network printers and network shares.
  In Ubuntu, applications such as `Avahi
  <https://manpages.ubuntu.com/manpages/en/man8/avahi-daemon.8.html>`_ (generic
  service discovery) and `cups-browsed
  <https://manpages.ubuntu.com/manpages/en/man8/cups-browsed.8.html>`_ (network
  printer discovery) make use of these protocols.

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
    :linenos:

    #!/usr/sbin/nft -f

    define IF_LOOPBACK = lo

    define MARK_REALM_LOCAL = 1

    # This empty definition is needed to allow the flush command to work if the
    # table is not already defined.
    table inet host-firewall; flush table inet host-firewall

    # Note that the flush command does not destroy the table or the objects
    # contained within, only clearing the rules within all of the chains. Use the
    # following instead, if the object definitions need to be changed, chains
    # completely destroyed or sets/maps cleared.
    #destroy table inet host-firewall

    table inet host-firewall {
        chain early-inbound {
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

    include "/etc/nftables/tables.d/*.conf"

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
* **meta statements**: allows changing meta information tracked by Netfilter for
  a particular packet, such as ``meta mark set 42`` for setting the Netfilter
  packet mark to the constant value ``42`` or ``meta nftrace set 1`` for
  enabling :ref:`rule tracing <Rule tracing>`.
* **nat statements**: allow source and destination network address translation
  (NAT) to occur (including support for dynamic translation for transport
  protocol ports and the stateful processing of ICMP packets).
* **counter statements**: support for counting packets and bytes matched by
  rules.
* **payload statements**: allows changing arbitrary contents of the packets: for
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
section. Please note that the data types are a feature of the ``nft`` userspace
utility, with the bytecode interpreted by the Linux kernel operating exclusively
on raw bytes.

An expression's data type can be displayed using the ``nft describe`` command,
such as the following:

.. code-block:: console

    nft describe udp dport

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
which are used for matching packets. These are:

* ``eq`` or ``==``: this is the implied comparison (``udp dport 53`` is
  equivalent to ``udp dport == 53``). It can compare an arbitrary expression
  with a constant value or look the expression up in a set (``udp dport == { 80,
  443 }`` matches if the destination port is either 80 or 443).
* ``ne`` or ``!=``: this matches if an arbitrary expression is not equal to a
  constant value (e.g. ``udp dport != 53``) or does not exist in a set (``udp
  dport != { 80, 443 }`` matches if the destination is neither 80, nor 443).
* ``lt`` / ``<``, ``gt`` / ``>``, ``le`` / ``<=`` and ``ge`` / ``>=``: these
  match if the comparison of an arbitrary expression is lower than, greater
  than, lower than or equal and greater than or equal, respectively, to a
  constant value (e.g. ``udp dport < 1024`` matches privileged UDP ports).

Expressions can also be combinated with binary operators, such as:

* ``and`` / ``&``: bitwise AND
* ``or`` / ``|``: bitwise OR
* ``xor`` / ``^``: bitwise exclusive-OR
* ``lshift`` / ``<<``: bitwise left shift
* ``rshift`` / ``>>``: bitwise right shift

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

Bitmasks support specific operations that simplify management, especially
through the use of symbolic names associated to individual bits:

* Without an operator, a relational expression matches if any of the specified
  bits are set. The expression ``tcp flags syn,ack`` matches if packets have at
  least one of the ``SYN`` or ``ACK`` bits set. This is equivalent to ``tcp
  flags & (syn|ack) != 0``.
* The ``/`` operator can be used to specify a mask, in addition to a set of
  values that need to be configured. The expression ``tcp flags syn / syn,ack``
  matches if, out of the ``SYN`` and ``ACK`` bits, only the ``SYN`` bit is set
  (no other bits matter). This is equivalent to ``tcp flags & (syn|ack) ==
  syn``.
* The equality (``eq`` / ``==``) and non-equality (``ne`` / ``!=``) operators
  compare an exact bitmask value. The expression ``tcp flags == syn,ack``
  matches if and only if both the ``SYN`` and ``ACK`` bits are set and all other
  bits are cleared. This is equivalent to ``tcp flags == (syn|ack)``.

Putting these concepts together allows the creation of a framework for using the
Netfilter mark as a bitfield that facilitates generic firewall rules. As the
packet mark can be determined from external sources (e.g. VXLAN with the GBP
extension) and is copied when packets are decapsulated (e.g. IPsec), special
processing is required: one bit (a flag) is used to determine if the packet mark
can be trusted as having been validated locally.

The following ``nftables`` configuration containss two changes from the previous
example:

* An extension to the ``early-inbound`` chain, with the two regular chains that
  it invokes (``mark-inbound-determine`` and
  ``mark-inbound-external-validate``). The convention used for the format of the
  Netfilter mark is explained in a comment at the top of the file, with symbolic
  variables defined to simplify the bitfield operations.
* Two new rules in the ``firewall-input`` chain that use the ``ct state``
  bitmask expression:

  * allow packets marked as either ``established`` or ``related`` by the
    conntrack module through (``ct state established,related accept``);
  * drop packets marked as ``invalid`` by the conntrack module (``ct state
    invalid drop``).

.. code-block:: nft
    :caption: /etc/nftables.conf
    :linenos:

    #!/usr/sbin/nft -f

    define IF_LOOPBACK = lo

    # The packet mark is interpreted as follows (big endian):
    #    3                   2                   1                   0
    #  1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |V| Unused                                          | Realm (6) |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #
    # V - validated flag (1 - packet mark was validated locally; 0 - it wasn't)
    # Realm - class of hosts the packet originated from (64 possible values)

    define MARK_MASK_REALM  = 0x0000003f

    define MARK_REALM_UNKNOWN   = 0  # Other provenance of packet
    define MARK_REALM_LOCAL     = 1  # Packet from local host
    define MARK_REALM_VIRT      = 2  # Packet from local VMs / containers
    define MARK_REALM_LAN       = 3  # Packet from internal network

    define MARK_FLAG_VALIDATED  = 0x80000000

    # This empty definition is needed to allow the flush command to work if the
    # table is not already defined.
    table inet host-firewall; flush table inet host-firewall

    # Note that the flush command does not destroy the table or the objects
    # contained within, only clearing the rules within all of the chains. Use the
    # following instead, if the object definitions need to be changed, chains
    # completely destroyed or sets/maps cleared.
    #destroy table inet host-firewall

    table inet host-firewall {
        chain early-inbound {
            type filter hook prerouting priority raw; policy accept;

            # When VRF interfaces are in use, packets go through the prerouting hook
            # twice, once with the VRF interface set as input and another time with
            # actual interface set as input.
            meta iifkind "vrf" return

            # If the mark was previously set with the validated flag set (e.g.
            # decapsulated packet), reset it. This also resets the mark for remote
            # packets that automatically set the mark and attempt to forge the
            # validated flag (e.g. VXLAN with the GBP extension).
            (meta mark & $MARK_FLAG_VALIDATED) != 0 meta mark set 0
            meta mark != 0 jump mark-inbound-external-validate
            meta mark == 0 jump mark-inbound-determine
            meta mark set (meta mark | $MARK_FLAG_VALIDATED)
        }

        chain mark-inbound-external-validate {
            # Do not allow externally-determined marks to have the realm set to
            # LOCAL or VIRT.
            meta mark & $MARK_MASK_REALM == {
                $MARK_REALM_LOCAL,
                $MARK_REALM_LAN,
            } drop
        }

        chain mark-inbound-determine {
            # Set the realm to LOCAL for packets received on the loopback interface.
            meta iif $IF_LOOPBACK meta mark set $MARK_REALM_LOCAL return

            # Set the realm to VIRT for packets received on bridge interfaces.
            meta iifkind "bridge" meta mark set $MARK_REALM_VIRT return

            # Set the realm to LAN for link-local and private addresses.
            ip saddr {
                169.254.0.0/16,
                10.0.0.0/8,
                172.16.0.0/12,
                192.168.0.0/16,
            } meta mark set $MARK_REALM_LAN return
            ip6 saddr {
                fe80::/64,
                fc00::/7,
            } meta mark set $MARK_REALM_LAN return
        }

        chain firewall-input {
            # Process packets destined for this host.
            type filter hook input priority filter;
            # Use a default-deny policy for packets.
            policy drop;

            # Use conntrack state to allow packets belonging to already established
            # flows, while dropping packets which conntrack considers invalid.
            ct state established,related accept
            ct state invalid drop

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

    include "/etc/nftables/tables.d/*.conf"

Concatenations
^^^^^^^^^^^^^^

Concatenations allow combining expressions into compound expressions that have a
complex type, by using the ``.`` operator. These are particularly powerful when
used in combination with :ref:`sets <Sets>` and :ref:`maps <Maps>` to define
keys based on multiple attributes of a packet. For example, the following
expression combines three different fields - the Netfilter mark, the transport
protocol (``meta l4proto`` matches irrespective of the encapsulating network
protocol, IPv4 or IPv6), and the transport protocol destination port (``th
dport`` matches irrespective of the transport protocol, such as TCP, UDP or
SCTP):

.. code-block:: nft

    meta mark . meta l4proto . th dport

The use of binary operators for extracting information based on the Netfilter
mark convention established earlier, along with :ref:`anonymous sets <Sets>` for
specifying alternative values and intervals result in powerful matching
expressions:

.. code-block:: nft

    (meta mark & $MARK_MASK_REALM) . meta l4proto . th dport {
        # Web service allowed from anywhere
        0-63                . tcp   . 80,
        # SSH allowed from local machine and local VMs
        $MARK_REALM_LOCAL   . tcp   . 22,
        $MARK_REALM_VIRT    . tcp   . 22,
        # SIP signalling allowed from LAN over any transport
        $MARK_REALM_LAN     . sctp  . 5060-5061,
        $MARK_REALM_LAN     . tcp   . 5060-5061,
        $MARK_REALM_LAN     . udp   . 5060-5061,
    } accept

Sets
~~~~

Sets are a generic data structure in ``nftables`` that act as a container for
values with support for efficient lookup, addition and removal operations. They
are similar to the `ipset
<https://manpages.ubuntu.com/manpages/en/man8/ipset.8.html>`_ functionality
available in ``xtables``, but support arbitrary types via the use of
:ref:`Concatenations`. The implementation uses hashtables and red-black trees.
Sets come in two types:

* **Named sets**: defined within tables and with an associated name, these allow
  both external applications, as well as ``nftables`` rules to manage the elements.
* **Anonymous sets**: defined inline within rules, these allow the expression of
  the logical ``OR`` operator. The expression ``tcp dport { 80, 443 }`` matches
  if the TCP destination port is either 80 or 443.

Named sets, like other objects such as tables or chains, can be defined multiple
times with an additive effect. This allows the sets' elements to be added in
multiple places, such as by using ``include`` directives with wildcards for
drop-in files. Unlike anonymous sets, various configuration options can be added
as part of the definition to control the behavior of the sets. These are all
documented in the `Sets section of the manual page
<https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#sets>`_, but some of
the more useful ones are:

* **type** or **typeof**: these are necessary for a named set and define the
  format of the elements. **type** requires the use of `data type names
  <https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#data%20types>`_,
  possibly with concatenations, while **typeof** receives an expression that is
  used to derive the elements' type. The **typeof** configuration is
  particularly useful for expressions that have only an variable-length integer
  data type associated and cannot be be expressed with **type** (e.g. ``typeof
  meta cgroup`` cannot be expressed with ``type``).
* **flags interval**: allows the use of intervals in elements. An anonymous set
  that uses intervals effectively activates this flag, as well.
* **flags dynamic**: allows the addition of elements from rules, using the
  **set** statement.
* **flags timeout**: allows elements to be automatically removed after an
  interval has elapsed since the element was (last) added to the set.
* **timeout**: expression that defines the default interval after which an
  element will be removed from the set. For example: ``timeout 5m`` for a
  5-minute interval.
* **size**: defines the maximum number of elements that the set can hold.

The following extends the example firewall configuration with:

* A named set (``input-services``) for services allowed to the local host. These
  are defined based on the Netfilter mark (only the realm bits), the transport
  protocol and the transport destination port. An ``include`` directive
  facilitates the definition of additional services in drop-in files.
* A rule to reference the new named set in the ``firewall-input`` base chain.
* A new rule in the ``firewall-input-multicast`` regular chain that allows IPv6
  Multicast Listener Discovery (MLD) and Neighbour Discovery (ND) ICMPv6 packets
  through, by using an anonymous set. These are generally required for the
  correct functioning of IPv6 in local networks.

.. code-block:: nft
    :caption: /etc/nftables.conf
    :linenos:

    #!/usr/sbin/nft -f

    define IF_LOOPBACK = lo

    # The packet mark is interpreted as follows (big endian):
    #    3                   2                   1                   0
    #  1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |V| Unused                                          | Realm (6) |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #
    # V - validated flag (1 - packet mark was validated locally; 0 - it wasn't)
    # Realm - class of hosts the packet originated from (64 possible values)

    define MARK_MASK_REALM  = 0x0000003f

    define MARK_REALM_UNKNOWN   = 0  # Other provenance of packet
    define MARK_REALM_LOCAL     = 1  # Packet from local host
    define MARK_REALM_VIRT      = 2  # Packet from local VMs / containers
    define MARK_REALM_LAN       = 3  # Packet from internal network

    define MARK_FLAG_VALIDATED  = 0x80000000

    # Note that the flush command does not destroy the table or the objects
    # contained within, only clearing the rules within all of the chains. The
    # destroy command is used in order to clear the sets' elements.
    destroy table inet host-firewall

    table inet host-firewall {
        set input-services {
            type mark . inet_proto . inet_service
            flags interval
            elements = {
                # Web service allowed from anywhere
                0-63                . tcp   . 80,
                # SSH allowed from local machine and local VMs
                $MARK_REALM_LOCAL   . tcp   . 22,
                $MARK_REALM_VIRT    . tcp   . 22,
                # SIP signalling allowed from LAN over any transport
                $MARK_REALM_LAN     . sctp  . 5060-5061,
                $MARK_REALM_LAN     . tcp   . 5060-5061,
                $MARK_REALM_LAN     . udp   . 5060-5061,
            }
        }
        include "/etc/nftables/input-services.d/*.conf"

        chain early-inbound {
            type filter hook prerouting priority raw; policy accept;

            # When VRF interfaces are in use, packets go through the prerouting hook
            # twice, once with the VRF interface set as input and another time with
            # actual interface set as input.
            meta iifkind "vrf" return

            # If the mark was previously set with the validated flag set (e.g.
            # decapsulated packet), reset it. This also resets the mark for remote
            # packets that automatically set the mark and attempt to forge the
            # validated flag (e.g. VXLAN with the GBP extension).
            (meta mark & $MARK_FLAG_VALIDATED) != 0 meta mark set 0
            meta mark != 0 jump mark-inbound-external-validate
            meta mark == 0 jump mark-inbound-determine
            meta mark set (meta mark | $MARK_FLAG_VALIDATED)
        }

        chain mark-inbound-external-validate {
            # Do not allow externally-determined marks to have the realm set to
            # LOCAL or VIRT.
            meta mark & $MARK_MASK_REALM == {
                $MARK_REALM_LOCAL,
                $MARK_REALM_LAN,
            } drop
        }

        chain mark-inbound-determine {
            # Set the realm to LOCAL for packets received on the loopback interface.
            meta iif $IF_LOOPBACK meta mark set $MARK_REALM_LOCAL return

            # Set the realm to VIRT for packets received on bridge interfaces.
            meta iifkind "bridge" meta mark set $MARK_REALM_VIRT return

            # Set the realm to LAN for link-local and private addresses.
            ip saddr {
                169.254.0.0/16,
                10.0.0.0/8,
                172.16.0.0/12,
                192.168.0.0/16,
            } meta mark set $MARK_REALM_LAN return
            ip6 saddr {
                fe80::/64,
                fc00::/7,
            } meta mark set $MARK_REALM_LAN return
        }

        chain firewall-input {
            # Process packets destined for this host.
            type filter hook input priority filter;
            # Use a default-deny policy for packets.
            policy drop;

            # Use conntrack state to allow packets belonging to already established
            # flows, while dropping packets which conntrack considers invalid.
            ct state established,related accept
            ct state invalid drop

            # Allow traffic on the loopback interface(s).
            meta iif $IF_LOOPBACK accept

            # Process multicast packets. Upon returning, do not evaluate any more
            # rules and apply the policy verdict (drop).
            meta pkttype multicast goto firewall-input-multicast

            # Allow services based on the origin realm, the transport protocol and
            # the destination port.
            (meta mark & $MARK_MASK_REALM) . meta l4proto . th dport @input-services accept

            # Drop-in files can add rules here.
            include "/etc/nftables/input-rules.d/*.conf"
        }

        chain firewall-input-multicast {
            # Allow any IPv4 IGMP.
            ip protocol igmp accept

            # Allow IPv6 MLD (for multicast group management) and neighbour
            # discovery (note that unicast packets would not be handled here).
            icmpv6 type {
                mld-listener-query,
                mld-listener-report,
                mld-listener-reduction,
                mld2-listener-report,
                nd-router-advert,
                nd-neighbor-solicit,
                nd-neighbor-advert,
            } accept

            # Allow inbound Multicast DNS packets.
            udp dport 5353 accept

            # If no prior action was taken, this will return to the calling chain
            # (firewall-input).
        }
    }

    include "/etc/nftables/tables.d/*.conf"

A drawback of the drop-in file configuration is that each file will have to
redefine the set with the exact same settings:

.. code-block:: nft
    :caption: /etc/nftables/input-services.d/ldap.conf
    :linenos:

    #!/usr/sbin/nft -f

    set input-services {
        type mark . inet_proto . inet_service
        flags interval
        elements = {
            # LDAP server access allowed from local machine and LAN
            $MARK_REALM_LOCAL   . tcp   . 389,
            $MARK_REALM_LAN     . tcp   . 389,
        }
    }

Element management in rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^

A named set's elements can be dynamically added from rules by the use of the
``add`` or ``update`` statements. Their use requires the presence of the
``dynamic`` flag on the defined set. The major different between the two
statements is that the ``add`` statement will conditionally terminate the rule
early if the element already exists in the set, while the ``update`` statement
will update any meta information associated with the element (such as resetting
the timeout or modifying any :ref:`stateful objects <Stateful objects>`
associated).

To demonstrate this functionality, the following example implements a very
trivial rate limit for new connections, which only accepts new connections if
the source address, transport protocol and destination port concatenation can be
added to a set (i.e. if the element did not previously exist). Elements expire
after 2 minutes, so this effectively applies a limit of one connection every 2
minutes. Note the size limit of the set, necessary in order to ensure that the
amount of memory used is bounded. This is only meant for illustration of the
``add`` statement, with limits being the preferred means of implementing rate
limiting - these are explained in the :ref:`Stateful objects` section.

.. code-block:: nft
    :caption: /etc/nftables/tables.d/limits.conf
    :linenos:

    destroy table ip limits
    table ip limits {
        set connections {
            type ipv4_addr . inet_proto . inet_service
            flags dynamic, timeout
            timeout 2m
            size 65536
        }
        chain limits-inbound {
            # This must execute after conntrack lookup (priority -200).
            type filter hook prerouting priority filter; policy drop;

            # Only apply limits to packets that establish new flows.
            ct state != new accept

            # Accept packets that can be added to the set.
            add @connections { ip saddr . meta l4proto . th dport } accept

            # Anything that reaches here is dropped by policy.
        }
    }

Similarly, the ``update`` statement can be used to add elements to a set, but
will not fail if the element already exists. In the following example, the
timeout is reset, which allows the set to track any IPv4 /24 prefix that
initiated a new flow in the last 10 minutes.

.. code-block:: nft
    :caption: /etc/nftables/tables.d/flow-track.conf
    :linenos:

    destroy table ip flow-track
    table ip flow-track {
        set connections {
            type ipv4_addr
            flags dynamic, timeout
            timeout 10m
            size 65536
        }
        chain track-inbound {
            # This must execute after conntrack lookup (priority -200).
            type filter hook prerouting priority filter; policy accept;

            # Only bother with packets that establish new flows.
            ct state != new accept

            # Add /24 prefix to the connections set.
            ct state new update @connections { ip saddr & 255.255.255.0 }
        }
    }

Element management in userspace
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Named set elements can be inspected and managed from userspace, too. This is
implemented over the standard ``AF_NETLINK`` communication for ``nftables``, with
the ``nft`` utility offering convenient commands, as described in the manual
page's `Sets <https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#sets>`_
and `Elements
<https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#elements>`_ sections.
The following are example commands that apply to the previously-defined
``connections`` set from the ``ip`` address family ``flow-track`` table.

Listing all elements in the set:

.. code-block:: console

    sudo nft list set ip flow-track connections

Removing all elements from the same set:

.. code-block:: console

    sudo nft flush set ip flow-track connections

Resetting any stateful objects associated with the elements in the set (such as
counters or limits, explained in the :ref:`Stateful objects` section):

.. code-block:: console

    sudo nft reset set ip flow-track connections

Retrieving elements from a set:

.. code-block:: console

   sudo nft get element ip flow-track connections '{ 127.0.0.0 }'

Adding an element to a set (alternatively, the similar ``create`` command
succeeds only if the element does not exist):

.. code-block:: console

   sudo nft add element ip flow-track connections '{ 10.0.0.0 }'

Deleting an element from a set (alternatively, the similar ``destroy`` command
succeeds even if the element does not exist):

.. code-block:: console

   sudo nft delete element ip flow-track connections '{ 10.0.0.0 }'

Maps
~~~~

Maps are ``nftables`` data structures that associate keys to values, a form of
associative arrays or dictionaries. Maps are similar to :ref:`sets <Sets>`: in
fact, sets are implemented as maps, with elements being keys without associated
values. As such, maps usage is very similar to that of sets, including:

* anonymous maps and named maps;
* similar configuration settings for named maps;
* ability to manage elements from other applications or rules (the same
  statements and commands are used - see the :ref:`Sets` section for more
  details).

Maps support a lookup operation, the ``map`` statement, that returns the value
associated with a lookup key. The returned value can then be used as an
expression with the same type as the value type of the map. If a corresponding
key is not found, the statement terminates rule evaluation early and no further
statements are evaluated.

The following extension of the example makes use of a map from IPv4 and IPv6
prefixes to Netfilter marks representing the origin realm and sets the Netfilter
mark using an extensible rule: new elements can be added to map other addresses
to different Netfilter mark values. In addition to the two new maps
(``ip4-known-addresses`` and ``ip6-known-addresses``), the changes are made to
the ``mark-inbound-determine`` regular chain. The rule ``meta mark set ip saddr
map @ip4-known-addresses return`` can be broken down as:

1. Form the key for the map lookup: ``ip saddr``. This implies that the network
   protocol must be IPv4. For any other packets, the rule is terminated early
   and evaluation continues with the next rule in the chain.
#. Lookup the key in the ``@ip4-known-addresses`` map: ``ip saddr map
   @ip4-known-addresses``. The value type of the map is a Netfilter mark. If no
   key is found, the rule is terminated early and evaluation continues with the
   next rule in the chain.
#. Set the packet's Netfilter mark to the value returned by the map lookup:
   ``meta mark set ip saddr map @ip4-known-addresses``.
#. Return from the current chain: ``return``. This is only executed if the
   previous ``ip saddr`` expression or the ``map`` statement did not terminate
   evaluation of the rule, either because the packet was not IPv4 or the key
   could not be found.

.. code-block:: nft
    :caption: /etc/nftables.conf
    :linenos:

    #!/usr/sbin/nft -f

    define IF_LOOPBACK = lo

    # The packet mark is interpreted as follows (big endian):
    #    3                   2                   1                   0
    #  1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |V| Unused                                          | Realm (6) |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #
    # V - validated flag (1 - packet mark was validated locally; 0 - it wasn't)
    # Realm - class of hosts the packet originated from (64 possible values)

    define MARK_MASK_REALM  = 0x0000003f

    define MARK_REALM_UNKNOWN   = 0  # Other provenance of packet
    define MARK_REALM_LOCAL     = 1  # Packet from local host
    define MARK_REALM_VIRT      = 2  # Packet from local VMs / containers
    define MARK_REALM_LAN       = 3  # Packet from internal network

    define MARK_FLAG_VALIDATED  = 0x80000000

    # Note that the flush command does not destroy the table or the objects
    # contained within, only clearing the rules within all of the chains. The
    # destroy command is used in order to clear the sets' elements.
    destroy table inet host-firewall

    table inet host-firewall {
        set input-services {
            type mark . inet_proto . inet_service
            flags interval
            elements = {
                # Web service allowed from anywhere
                0-63                . tcp   . 80,
                # SSH allowed from local machine and local VMs
                $MARK_REALM_LOCAL   . tcp   . 22,
                $MARK_REALM_VIRT    . tcp   . 22,
                # SIP signalling allowed from LAN over any transport
                $MARK_REALM_LAN     . sctp  . 5060-5061,
                $MARK_REALM_LAN     . tcp   . 5060-5061,
                $MARK_REALM_LAN     . udp   . 5060-5061,
            }
        }
        include "/etc/nftables/input-services.d/*.conf"

        map ip4-known-addresses {
            type ipv4_addr : mark
            flags interval
            elements = {
                # link-local addresses
                169.254.0.0/16  : $MARK_REALM_LAN,
                # RFC1918 private addresses
                10.0.0.0/8      : $MARK_REALM_LAN,
                172.16.0.0/12   : $MARK_REALM_LAN,
                192.168.0.0/16  : $MARK_REALM_LAN,
            }
        }

        map ip6-known-addresses {
            type ipv6_addr : mark
            flags interval
            elements = {
                # link-local addresses
                fe80::/64   : $MARK_REALM_LAN,
                # RFC4193 local addresses
                fc00::/7    : $MARK_REALM_LAN,
            }
        }

        chain early-inbound {
            type filter hook prerouting priority raw; policy accept;

            # When VRF interfaces are in use, packets go through the prerouting hook
            # twice, once with the VRF interface set as input and another time with
            # actual interface set as input.
            meta iifkind "vrf" return

            # If the mark was previously set with the validated flag set (e.g.
            # decapsulated packet), reset it. This also resets the mark for remote
            # packets that automatically set the mark and attempt to forge the
            # validated flag (e.g. VXLAN with the GBP extension).
            (meta mark & $MARK_FLAG_VALIDATED) != 0 meta mark set 0
            meta mark != 0 jump mark-inbound-external-validate
            meta mark == 0 jump mark-inbound-determine
            meta mark set (meta mark | $MARK_FLAG_VALIDATED)
        }

        chain mark-inbound-external-validate {
            # Do not allow externally-determined marks to have the realm set to
            # LOCAL or VIRT.
            meta mark & $MARK_MASK_REALM == {
                $MARK_REALM_LOCAL,
                $MARK_REALM_LAN,
            } drop
        }

        chain mark-inbound-determine {
            # Set the realm to LOCAL for packets received on the loopback interface.
            meta iif $IF_LOOPBACK meta mark set $MARK_REALM_LOCAL return

            # Set the realm to VIRT for packets received on bridge interfaces.
            meta iifkind "bridge" meta mark set $MARK_REALM_VIRT return

            # Set the realm for known addresses.
            meta mark set ip saddr map @ip4-known-addresses return
            meta mark set ip6 saddr map @ip6-known-addresses return
        }

        chain firewall-input {
            # Process packets destined for this host.
            type filter hook input priority filter;
            # Use a default-deny policy for packets.
            policy drop;

            # Use conntrack state to allow packets belonging to already established
            # flows, while dropping packets which conntrack considers invalid.
            ct state established,related accept
            ct state invalid drop

            # Allow traffic on the loopback interface(s).
            meta iif $IF_LOOPBACK accept

            # Process multicast packets. Upon returning, do not evaluate any more
            # rules and apply the policy verdict (drop).
            meta pkttype multicast goto firewall-input-multicast

            # Allow services based on the origin realm, the transport protocol and
            # the destination port.
            (meta mark & $MARK_MASK_REALM) . meta l4proto . th dport @input-services accept

            # Drop-in files can add rules here.
            include "/etc/nftables/input-rules.d/*.conf"
        }

        chain firewall-input-multicast {
            # Allow any IPv4 IGMP.
            ip protocol igmp accept

            # Allow IPv6 MLD (for multicast group management) and neighbour
            # discovery (note that unicast packets would not be handled here).
            icmpv6 type {
                mld-listener-query,
                mld-listener-report,
                mld-listener-reduction,
                mld2-listener-report,
                nd-router-advert,
                nd-neighbor-solicit,
                nd-neighbor-advert,
            } accept

            # Allow inbound Multicast DNS packets.
            udp dport 5353 accept

            # If no prior action was taken, this will return to the calling chain
            # (firewall-input).
        }
    }

    include "/etc/nftables/tables.d/*.conf"

Verdict maps
~~~~~~~~~~~~

Verdict maps are similar to :ref:`maps <Maps>`, with the primary difference
being that the values associated to keys are :ref:`verdict statements <Verdict
statements>`. This allows them to be used with the ``vmap`` statements, which
looks up a key in the map and, if the key is found, executes the associated
verdict statement; if the key is not found, the next rule in the chain is
evaluated (an implied ``continue`` statement). The ``vmap`` statement is
terminal (i.e. it must be the last statement in a rule).

This functionality allows efficient branching decisions to be made. For example,
the above rules in the ``early-inbound`` chain that either validate an external
Netfilter mark or determine one locally if it is not already set, can be
rewritten with a ``vmap`` statement. It should be noted that the two rules might
still be more efficient than the use of a red-black tree for this simple branch.

.. code-block:: nft
    :caption: Rule extract from 'table inet host-firewall' 'chain early-inbound'.

    # Instead of the following two rules...
    #meta mark != 0 jump mark-inbound-external-validate
    #meta mark == 0 jump mark-inbound-determine

    # ... use a vmap statement:
    meta mark vmap {
        0:              jump mark-inbound-determine,
        1-0xFFFFFFFF:   jump mark-inbound-external-validate,
    }

Stateful objects
~~~~~~~~~~~~~~~~

Stateful objects allow the tracking of information across unrelated packets, in
order to implement functionality such as:

* byte and packet counters: count number of packets or total size of packets
  that pass through a rule;
* byte quotas: count total size of packets that pass through a rule and execute
  statements when the size is either below or above a threshold (e.g. allow only
  a particular amount of data to be transferred across different flows);
* limits: a packet count or packet size token bucket rate limiter that allows
  statements to be executed whenever the rate of packets or data transferred is
  below or above a certain threshold;
* connection limits: integrated with Netfilter's conntrack, allows statements to
  be executed when the number of matching flows is above or below a certain
  threshold.

Stateful objects come in two types, dictating whether the state is shared across
different contexts:

* **Named objects** are associated with a particular table and can be referenced
  by more than one rule. As such, the same data can be interrogated or modified
  from multiple places (e.g. the same counter incremented by more than one
  rule). These can also be queried or managed from userspace.
* **Anonymous objects** do not have an associated name and are bound to single
  context: a particular rule or a :ref:`set's <Sets>` key. In particular,
  connection limit objects, as explained in the `nftables documentation
  <https://wiki.nftables.org/wiki-nftables/index.php/Connlimits>`_, can only be
  anonymous objects.

The creation of named stateful objects follows the same convention as for all
other objects. For example, the following file creates a counter which is
referenced once the end of the ``limits-inbound`` chain is reached:

.. code-block:: nft
    :caption: /etc/nftables/tables.d/limits.conf
    :linenos:

    destroy table inet limits
    table inet limits {
        counter dropped-flows {
        }
        chain limits-inbound {
            # This must execute after conntrack lookup (priority -200).
            type filter hook prerouting priority filter; policy accept;

            # Only apply limits to packets that establish new flows.
            ct state != new accept

            # Anything that reaches here is dropped.
            counter name dropped-flows drop
        }
    }

Retrieving the counter data:

.. code-block:: console

    sudo nft list counter ip limits dropped-flows

Resetting the counter data:

.. code-block:: console

    sudo nft reset counter ip limits dropped-flows

Anonymous objects can be associated to rules. The following extension to the
previous example adds some functionality:

* For HTTP traffic (selected using ``tcp dport { 80, 443 }``), use an anonymous
  connection limit (``ct count over 1000``) which conditionally terminates the
  rule evaluation if the threshold isn't reached, stopping the subsequent
  statements in the rule from being executed (``counter name dropped-flows`` and
  ``drop``). Any conntrack flows which match the selection criteria are kept
  track of by the connection limit; as soon as a flow stops being tracked by
  conntrack, it is removed from this connection limit.
* For non-HTTP traffic, similarly use an anonymous connection limit to drop new
  flow-initiating packets once the threshold (500 flows) is reached.
* For HTTP traffic, use an anonymous limit (``limit rate over 20/minute burst
  500 packets``) which conditionally terminates rule evaluation if the threshold
  isn't reached, stopping the subsequent statements in the rule from being
  executed (``counter name dropped-flows`` and ``drop``). A token bucket rate
  limiter is updated for each packet that matches the rule.
* For non-HTTP traffic, similarly use an anonymous limit to drop new
  flow-initiating packets once the token bucket's threshold is reached.

Note that new flow-initiating packets are dropped if *either* of the criteria is
met: active number of conntrack flows or rate of creation of new conntrack flows.

.. code-block:: nft
    :caption: /etc/nftables/tables.d/limits.conf
    :linenos:

    destroy table inet limits
    table inet limits {
        counter dropped-flows {
        }

        chain limits-inbound {
            # This must execute after conntrack lookup (priority -200).
            type filter hook prerouting priority filter; policy accept;

            # Only apply limits to packets that establish new flows.
            ct state != new accept
            # Do not apply limits to local and VMs communication.
            meta mark & $MARK_MASK_REALM {
                $MARK_REALM_LOCAL,
                $MARK_REALM_VIRT
            } accept

            jump drop-on-flow-count
            jump drop-on-new-flow-rate
        }

        chain drop-on-flow-count {
            # Allow at most 1000 simultaneous flows for HTTP.
            tcp dport { 80, 443 } ct count over 1000 \
                counter name dropped-flows \
                drop
            # If this rule is reached, the above threshold did not get reached, so
            # return in order to avoid counting this traffic towards subsequent
            # limits.
            tcp dport { 80, 443 } return

            # Allow at most 500 simultaneous flows for everything else.
            ct count over 500 \
                counter name dropped-flows \
                drop
        }

        chain drop-on-new-flow-rate {
            # Allow at most 20 new flows per minute (with a burst of 500) for HTTP.
            tcp dport { 80, 443 } limit rate over 20/minute burst 500 packets \
                counter name dropped-flows \
                drop
            # If this rule is reached, the above threshold did not get reached, so
            # return in order to avoid counting this traffic towards subsequent
            # limits.
            tcp dport { 80, 443 } return

            # Allow at most 10 new flows per minute (with a burst of 100) for
            # everything else.
            limit rate over 10/minute burst 100 packets \
                counter name dropped-flows \
                drop
        }
    }

Anonymous stateful objects associated to set elements are created via an
extension to the ``add`` and ``update`` statements that follows the same syntax
as the rule expressions. This allows individual stateful objects to be
associated with an arbitrary set of criteria. In effect, this extended syntax
transforms the ``add`` and ``update`` statements to a lookup operation for a
stateful object associated to a key and can terminate a rule early (e.g. if a
token bucket limiter's threshold is reached). The following example adds support
for tracking flow count and new flow rate per subnet:

* For tracking flow counts, two sets are created: ``flow-count-ip4`` and
  ``flow-count-ip6``. Elements with IPv4 /24 subnets and IPv6 /48 subnets are
  added to these sets with associated connection limits. Rule evaluation is
  terminated early if the threshold isn't reached; if it is, the new
  flow-initiating packet is dropped. Elements are automatically removed from the
  sets when there are no more conntrack entries associated.
* For tracking flow rates, two sets are created: ``flow-rate-ip4`` and
  ``flow-rate-ip6``. Elements with IPv4 /24 subnets and IPv6 /48 subnets are
  added to these sets with associated limit stateful objects. The update
  operation effectively refreshes the timeout after which elements from the sets
  expire (1 minute). Rule evaluation is terminated early if the threshold isn't
  reached; if it is, the prefix is added to a blocklist and the new
  flow-initiating packet is dropped. Elements are automatically removed from the
  sets when they are not refreshed (i.e. if no new flow-initiating packet for
  the given subnet is received within the set's 1 minute timeout).
* The blocklist sets, ``blocklist-ip4`` and ``blocklist-ip6`` contain IPv4 /24
  subnets and IPv6 /48 subnets which have exceeded the connection rate
  thresholds. Elements expire from these sets after 10 minutes, during which no
  new flows are allowed. It would certainly be possible to not use these extra
  sets, in which case a new flow could be established as soon as the token
  bucket rate limiter would allow it.
* The previously demonstrated global restrictions, applicable to any IPv4 or
  IPv6 source address, are maintained.

.. code-block:: nft
    :caption: /etc/nftables/tables.d/limits.conf
    :linenos:

    destroy table inet limits
    table inet limits {
        counter dropped-flows {
        }

        set blocklist-ip4 {
            type ipv4_addr
            flags dynamic
            timeout 10m
            size 65536
        }
        set flow-rate-ip4 {
            type ipv4_addr
            flags dynamic, timeout
            timeout 1m
            size 65536
        }
        set flow-count-ip4 {
            type ipv4_addr
            flags dynamic
            size 65536
        }

        set blocklist-ip6 {
            type ipv6_addr
            flags dynamic
            timeout 10m
            size 65536
        }
        set flow-rate-ip6 {
            type ipv6_addr
            flags dynamic, timeout
            timeout 1m
            size 65536
        }
        set flow-count-ip6 {
            type ipv6_addr
            flags dynamic
            size 65536
        }

        chain limits-inbound {
            # This must execute after conntrack lookup (priority -200).
            type filter hook prerouting priority filter; policy accept;

            # Only apply limits to packets that establish new flows.
            ct state != new accept
            # Do not apply limits to local and VMs communication.
            meta mark & $MARK_MASK_REALM {
                $MARK_REALM_LOCAL,
                $MARK_REALM_VIRT
            } accept

            jump drop-on-flow-count
            jump drop-on-new-flow-rate
        }

        chain drop-on-flow-count {
            # Allow at most 50 simultaneous flows per IPv4 /24 subnet or IPv6 /48
            # subnet.
            add @flow-count-ip4 { ip saddr & 255.255.255.0 ct count over 50 } \
                counter name dropped-flows \
                drop
            add @flow-count-ip6 { ip6 saddr & ffff:ffff:ffff:: ct count over 50 } \
                counter name dropped-flows \
                drop

            # Allow at most 1000 simultaneous flows for HTTP.
            tcp dport { 80, 443 } ct count over 1000 \
                counter name dropped-flows \
                drop
            # If this rule is reached, the above threshold did not get reached, so
            # return in order to avoid counting this traffic towards subsequent
            # limits.
            tcp dport { 80, 443 } return

            # Allow at most 500 simultaneous flows for everything else.
            ct count over 500 \
                counter name dropped-flows \
                drop
        }

        chain drop-on-new-flow-rate {
            # Drop packets from IPv4 /24 subnets that have been added to the
            # blocklist.
            ip saddr & 255.255.255.0 @blocklist-ip4 \
                counter name dropped-flows \
                drop
            # Update token bucket rater limiter per IPv4 /24 subnets; if over the
            # threshold, add the subnet to the blocklist and drop the packet.
            update @flow-rate-ip4 { \
                    ip saddr & 255.255.255.0 \
                    limit rate over 5/second burst 50 packets \
                } \
                add @blocklist-ip4 { ip saddr & 255.255.255.0 } \
                counter name dropped-flows \
                drop

            # Drop packets from IPv6 /48 subnets that have been added to the
            # blocklist.
            ip6 saddr & ffff:ffff:ffff:: @blocklist-ip6 \
                counter name dropped-flows \
                drop
            # Update token bucket rater limiter per IPv6 /48 subnets; if over the
            # threshold, add the subnet to the blocklist and drop the packet.
            update @flow-rate-ip6 { \
                    ip6 saddr & ffff:ffff:ffff:: \
                    limit rate over 5/second burst 50 packets \
                } \
                add @blocklist-ip6 { ip6 saddr & ffff:ffff:ffff:: } \
                counter name dropped-flows \
                drop

            # Allow at most 20 new flows per minute (with a burst of 500) for HTTP.
            tcp dport { 80, 443 } limit rate over 20/minute burst 500 packets \
                counter name dropped-flows \
                drop
            # If this rule is reached, the above threshold did not get reached, so
            # return in order to avoid counting this traffic towards subsequent
            # limits.
            tcp dport { 80, 443 } return

            # Allow at most 10 new flows per minute (with a burst of 100) for
            # everything else.
            limit rate over 10/minute burst 100 packets \
                counter name dropped-flows \
                drop
        }
    }

Flowtables
~~~~~~~~~~

Flowtables are a feature that accelerate packet forwarding for hosts that act as
a layer 3 router or layer 2 bridge. The functionality acts as a cache for
determining if a packet belongs to a known flow and can be almost directly sent
out on a network interface after it is received by a (potentially different)
network interface. As such, the feature cannot be used for flows for which one
end is a local process via a socket. The flow is identified by an input
interface, together with layer 2, layer 3 and layer 4 information, such as PPPoE
session, source and destination network addresses, or source and destination
transport protocol ports.

For matching flows, the forwarding stack is completely bypassed, including most
Netfilter hooks and bridging or routing decisions, up until the point where a
layer 2 address needs to be determined (via IPv4 ARP or IPv6 NDP). Queuing
disciplines are still applied, allowing for traffic shaping. The forwarding
logic bypass may be problematic for dynamic setups where the cached information
can become stale (e.g. layer 3 forwarding integrated with layer 2 bridging, if
the next hop could move to a different bridge port).

Flowtables are integrated with conntrack, with the flowtable fast path only
being activated once a flow has seen packets in both directions. The flows are
then refreshed at short, fixed intervals, as long as packets are received and
the conntrack timeouts do not occur. The refresh intervals can be configured for
TCP and UDP via the ``net.netfilter.nf_flowtable_tcp_timeout`` and
``net.netfilter.nf_flowtable_udp_timeout`` sysctls, but are otherwise fixed in
other cases (30 seconds as of Linux 6.15). The conntrack state is synchronized
according to the received packets.

Certain network interface cards (NICs) also support hardware offload of the flow
information, further optimizing packet forwarding. When this is not available or
not enabled (via the ``offload`` flag on the flowtable), software offload in the
Linux kernel is used instead.

Flowtables are implemented by using an ``ingress`` hook. The priority associated
with a flowtable is in effect the ``ingress`` hook priority at which the lookup
is performed: this means that any chains registered at a lower numerical
priority value would still process a packet matching a flowtable, while chains
at a higher numerical priority value would not, nor would chains registered at
any other Netfilter hook point, apart from ``egress``. More information on
flowtables can be found in the `Netfilter documentation
<https://wiki.nftables.org/wiki-nftables/index.php/Flowtables>`_ and `Linux
kernel documentation <https://docs.kernel.org/networking/nf_flowtable.html>`_.

The following example enables accelerated forwarding for packets between a set
of interfaces. The actual network interface which receive a packet needs to be
registered, even if bridging is enabled.

.. code-block:: nft
    :caption: /etc/nftables/tables.d/flow-offload.conf
    :linenos:

    define LAN_DEVICES = { eth0, eth1, eth2 }

    destroy table inet flow-offload
    table inet flow-offload {
        flowtable lan-forwarding {
            hook ingress priority 0;
            devices = $LAN_DEVICES;
        }
        chain offload-forward {
            type filter hook forward priority filter; policy accept;

            # Only offload UDP packets.
            meta l4proto udp flow add @lan-forwarding
        }
    }

Other features
--------------

FIB lookup and reverse-path filtering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Forwarding Information Base (FIB) is a generic term for a lookup table used in
network layer 2 or layer 3 packet forwarding (switching or routing). In this
context, it refers to the Linux Routing Policy Database (`RPDB
<https://manpages.ubuntu.com/manpages/en/man8/ip-rule.8.html>`_), which manages
the layer 3 routing decision lookup structures. The ``fib`` expression can be
used in rules to perform route lookups and make decisions based on the result.
Its syntax is flexible and supports several invocation types, as described in
the `manual page
<https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#primary%20expressions>`_.

One possible use is to determine if a network address is local to the host. Such
a test can be performed early, before a routing decision for the packet is made,
and need not take the Netfilter mark into account, as the ``local`` routing
table is usually the first one queried. The following example counts packets for
which the network layer destination address (``fib daddr``) is either a local or
broadcast one.

.. code-block:: nft
    :caption: /etc/nftables/tables.d/test-firewall.conf
    :linenos:

    #!/usr/sbin/nft -f

    destroy table inet test-firewall
    table inet test-firewall {
        chain test-prerouting {
            type filter hook prerouting priority filter; policy accept;

            fib daddr type { local, broadcast } counter
        }
    }

A different use case for the route lookups is to perform reverse-path filtering:
dropping packets if they arrive on an interface that is not associated with a
route that covers the network source address of the packet. If policy routing is
employed, different pieces of information may be used to perform routing table
selection, in which case the reverse-path filter check may not be accurate; the
Netfilter mark can be taken into account by ``fib`` expressions, which should
cover the majority of the policy routing configurations. The following example
demonstrates this use case. It should be noted that:

* The Netfilter mark must be set prior to the ``fib`` expression being employed,
  as if it were set for a packet before a routing decision in the reverse
  direction (i.e. a packet with a destination address set to the source address
  of the reverse-path verified packet).
* IPv6 configurations usually employ the same link-local prefix (``fe80::/64``)
  on all interfaces, requiring special handling.

.. code-block:: nft
    :caption: /etc/nftables/tables.d/test-firewall.conf
    :linenos:

    #!/usr/sbin/nft -f

    destroy table inet test-firewall
    table inet test-firewall {
        chain test-prerouting {
            type filter hook prerouting priority filter; policy accept;

            # Must determine Netfilter mark as if for reverse direction here.

            # Chain will drop packets which do not pass the reverse-path filter check
            jump rp-filter
        }

        chain rp-filter {
            # Ignore IPv6 packets with a link-local source address.
            ip6 saddr fe80::/64 return
            # FIB expression with oif output will return 0 if interface cannot
            be determined.
            fib saddr . mark . iif oif 0 drop
        }
    }

Payload expressions
~~~~~~~~~~~~~~~~~~~

Payload expressions allow selecting specific fields within a packet. The ``nft``
utility supports a large number of such expressions for simple rule management,
as documented in the `Payload Expressions section of the manual page
<https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#payload%20expressions>`_.

Where these do not suffice or deep packet inspection (DPI) is necessary, raw
payload expressions can be used: these allow selecting arbitrary parts (up to
128 bits long) of a packet from a fixed offset off one of the layer 2, layer 3
or layer 4 headers. In fact, the symbolic payload expressions (such as ``icmpv6
taddr``, which selects the target address of NDP or MLD IPv6 packets) are
translated by the userspace utility to raw payload expressions, not requiring
any special support in the ``nftables`` Linux kernel component. The general
format used is ``@base,offset,length``, with offset and length defined in bits. The
following are the bases off which the offsets can be calculated:

.. list-table::
    :header-rows: 1
    :widths: auto

    * - Base
      - Description
      - Example
    * - ``@ll``
      - link layer (e.g. Ethernet header)
      - ``@ll,0,48`` is 48 bits from the start of the link layer header - for
        Ethernet, the destination MAC address
    * - ``@nh``
      - network header (e.g. IPv4, IPv6)
      - ``@nh,48,8`` is 8 bits from 48 bits off the start of the network header
        - for IPv6, the next header field
    * - ``@th``
      - transport header (e.g. TCP, UDP)
      - ``@th,110,2`` is 2 bits from 110 bits off the start of the transport
        header - for TCP, the SYN and FIN flags
    * - ``@ih``
      - inner header (payload after transport header)
      - ``@ih,8,16`` is 16 bits from 8 bits off the start of the payload
        encapsulated in the transport protocol - for TLS, this is the version

It should be noted that, for the userspace ``nft`` utility, there are
distinctions between using the raw payload expressions and the symbolic ones,
such as:

* An expression such as ``ip6 nexthdr`` will have an implied ``meta nfproto
  ip6`` if the expression is added to a ``inet`` or ``bridge`` table, as packets
  which are not IPv6 would traverse these, too. ``@nh,48,8`` will take the 7th
  byte from the start of the network header, whatever protocol that may be (e.g.
  IPv4, ARP, etc.).
* The ``nft`` utility performs type checking. ``icmpv6 taddr`` has an
  ``ipv6_addr`` type (in userspace), allowing comparisons with IPv6 addresses
  (including prefixes, such as ``fe80::/64``). ``@th,64,128`` is treated as an
  128-bit integer, even if preceded by an expression such as ``icmpv6 type
  nd-neighbor-advert``, which would imply that the 128 bits would be supposed to
  be interpreted as the IPv6 NDP target address. As such, the use of raw payload
  expressions for set/map lookups or comparisons may be limited.
