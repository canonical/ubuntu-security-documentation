nftables
########

`nftables <https://www.nftables.org/projects/nftables/index.html>`_ is a
component in the Linux Netfilter subsystem that provides the most modern
framework for defining packet classification and filtering functionality. As
such, it is a successor to the ``xtables`` kernel component and its associated
``iptables``, ``ip6tables``, ``arptables``, and ``ebtables`` userspace
utilities.

This documentation uses the term ``nftables`` when referring to the Linux
kernel component and ``nft`` when referring to the userspace utility. Note that
the Ubuntu package that provides the userspace utility is also called
``nftables``, and this documentation refers to it as the ``nftables`` Ubuntu
package.

This page gradually builds an example ``nftables`` configuration file adequate
for a Linux host offering network services (such as SSH and HTTP) over IPv4 and
IPv6 connectivity to a Local Area Network (LAN).

Advantages
==========

Using ``nftables`` offers several advantages over older alternatives:

* **Flexibility:** The expressions forming the packet classification rules are
  compiled in userspace to bytecode and executed by the kernel using a
  purpose-built virtual machine.
* **Performance:** You can achieve high performance through maps and
  concatenations. Instead of linear rule processing (O(n)), you can achieve
  constant time (O(1)).
* **Declarative Syntax:** The syntax used by the userspace ``nft`` utility is
  declarative, unlike the procedural format required for
  ``ip/ip6/arp/ebtables``, simplifying firewall configuration management.
* **Dynamic Structure:** Tables and chains aren't predefined. The structure
  allows you to register an arbitrary number of them, facilitating independent
  rule management by multiple applications.
* **Acceleration:** You can accelerate packet forwarding using ``flowtables``
  functionality, which also integrates with selected hardware.
* **Unified Rules:** You can define common rules for IPv4 and IPv6, unlike with
  the older ``iptables`` and ``ip6tables``.
* **Tracing:** You can easily enable rule evaluation tracing for specific
  packets.

Compatibility
=============

In general, you can define most rules available in ``iptables``, ``ip6tables``,
``arptables``, and ``ebtables`` using ``nftables``, but not the other way
around. Use only one of the two approaches to manage firewall rules. Otherwise,
the interaction between different rules or services might be unexpected,
leading to insecure configurations or blocked traffic. Furthermore, certain
applications, such as container orchestration systems or VPN utilities, may
configure firewall rules, resulting in unexpected rule interactions.

There are still certain ``xtables`` rules you can't define using ``nftables``,
as documented in the `feature compatibility nftables wiki page
<https://wiki.nftables.org/wiki-nftables/index.php/Supported_features_compared_to_xtables>`_.
The gaps have reduced over recent ``nft`` and Linux kernel releases, meaning
older Ubuntu versions might have more limited support. Additionally, note that
some functionality available via the ``nftables`` Netlink interface may not be
supported by the userspace ``nft`` utility yet (for example, support for rules
invoking eBPF programs).

Starting with Ubuntu 16.04 LTS (Xenial Xerus), the ``iptables`` package
provides versions of the ``iptables``, ``ip6tables``, ``arptables``, and
``ebtables`` tools that work with the ``nftables`` API and provide a compatible
interface to the legacy implementation. The ``nftables`` backend, used by
``iptables-nft``, ``ip6tables-nft``, ``arptables-nft``, and ``ebtables-nft``
utilities, has been the default since Ubuntu 20.10 (Groovy Gorilla). You can
manage these through the alternatives system and display the current
configuration with the following commands:

.. code-block:: console

   update-alternatives --display iptables
   update-alternatives --display ip6tables
   update-alternatives --display arptables
   update-alternatives --display ebtables

The ``*-nft`` utilities assume that no other application manages ``nftables``
rules natively. Therefore, you shouldn't combine them with other approaches to
Netfilter firewall rule management.

``ufw`` works by invoking the legacy ``iptables`` and ``ip6tables`` utilities.
As such, you shouldn't use it concurrently with native ``nftables`` firewall
rules.

Usage
=====

You can configure ``nftables`` rules using the userspace ``nft`` utility,
provided by the ``nftables`` Ubuntu package. Communication with Netfilter
happens over `AF_NETLINK
<https://manpages.ubuntu.com/manpages/en/man7/netlink.7.html>`_ sockets,
allowing applications to use this low-level interface. This documentation only
covers the use of the ``nft`` utility, focusing on the configuration file
format.

Starting with Ubuntu 15.04 (Vivid Vervet), the ``nftables`` package provides a
systemd service unit file disabled by default. If enabled, the service unit
file automatically loads ``nftables`` configuration from the
``/etc/nftables.conf`` file (a mock file that performs no filtering is provided
in the package). You can enable this and load the configuration using the
following commands:

.. code-block:: console

   sudo systemctl enable nftables.service
   sudo systemctl start nftables.service

Command-line usage
------------------

The ``nft`` utility accepts one or more commands as arguments to manage any
supported objects (tables, rules, sets, and so on). For example, the following
command lists all firewall rules:

.. code-block:: console

   sudo nft list ruleset

All operations are atomic: packet processing sees either the firewall rules
defined prior to the utility invocation or the rules with all requested changes
applied. The following command creates two tables that process both IPv4 and
IPv6 packets:

.. code-block:: console

   sudo nft "add table inet foo; add table inet bar"

Changes to ``nftables`` rulesets performed via the utility are ephemeral and
are lost upon reboot (specifically, upon the destruction of the associated
`network namespace
<https://manpages.ubuntu.com/manpages/en/man7/network_namespaces.7.html>`_).
Persistence requires the aforementioned systemd service unit or similar
mechanisms.

Alternatively, you can pass a filename to the ``nft`` utility using the ``-f``
flag. The file can contain commands and object definitions using a declarative
syntax. As with command-line usage, all operations are atomic. The default
``/etc/nftables.conf`` file contains a command to delete all configured rules
(``flush ruleset``) and a declarative definition of a table named ``filter``
that processes both IPv4 and IPv6 packets in three empty chains:

.. code-block:: nftables
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

The ``-f`` option allows you to use the ``nft`` utility as an interpreter, as
demonstrated in the shebang line above. Since the file is executable by
default, you can atomically reload the rules by executing the file:

.. code-block:: console

   sudo /etc/nftables.conf

Alternatively, the systemd unit file supports the ``reload`` command:

.. code-block:: console

   sudo systemctl reload nftables.service

Configuration file format
-------------------------

The configuration file is line-oriented. You can combine multiple commands on
the same line by separating them with semicolons (``;``). Comments start with a
hash sign (``#``) and span until the end of the line. You can split commands
across multiple lines by escaping the end-of-line with a backslash (``\``). A
line containing only comments isn't considered a continuation line, but an
empty line is, effectively ending the rule. Whitespace (and indentation)
doesn't matter.

Even though the declarative syntax uses braces (``{`` and ``}``) to define
blocks, strict line-oriented processing still applies. For example, the opening
brace (``{``) must be on the same line as the object type and name. The
following example establishes a base for a host firewall configuration file,
which we will expand upon throughout this documentation:

.. code-block:: nftables
   :caption: /etc/nftables.conf
   :linenos:

   #!/usr/sbin/nft -f

   # This empty definition allows the flush command to work if the table is not
   # already defined.
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

When using configuration files to load firewall rules, you must clear the prior
configuration. The declarative syntax doesn't replace chain rules but appends
them to the previously defined chain. Deciding which command to use to clear
prior configuration depends on several considerations:

* ``flush ruleset`` clears the entire ``nftables`` configuration, including
  all :ref:`tables, chains, and rules <Structure>`, :ref:`sets <Sets>`,
  :ref:`maps <Maps>`, :ref:`stateful objects <Stateful objects>`, and
  :ref:`flowtables <Flowtables>`. While appropriate for a central definition,
  it may lead to unexpected results if elements in sets or maps are managed
  externally or if other applications manage tables.
* ``destroy table`` deletes a table and all associated objects. This is useful
  when settings associated with objects change across versions (such as chain
  priority) or when you need to delete and recreate elements in sets or maps.
* ``flush table`` clears rules within tables but doesn't delete chains, sets,
  maps, stateful objects, or flowtables. This is appropriate when external
  tools manage set elements or when you want to preserve stateful object data.

The include directive
^^^^^^^^^^^^^^^^^^^^^

You can include files using the ``include`` directive. The system interprets
these in the context where you use the directive. For example, the highlighted
lines below allow drop-in files to add rules to the ``firewall-input`` chain
from ``/etc/nftables/input-rules.d/`` and any other tables defined in files
under ``/etc/nftables/tables.d/`` (if wildcards are used, the files need not
exist):

.. code-block:: nftables
   :caption: /etc/nftables.conf
   :linenos:
   :emphasize-lines: 21,25

   #!/usr/sbin/nft -f

   # This empty definition allows the flush command to work if the table is not
   # already defined.
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
associating names to arbitrary expressions, which you can then reuse throughout
the configuration. Associating the name ``IF_LOOPBACK`` to the interface name
``lo`` (the standard Linux loopback interface) allows defining a rule that
references it, as the highlighted lines show:

.. code-block:: nftables
   :caption: /etc/nftables.conf
   :linenos:
   :emphasize-lines: 3,22-23

   #!/usr/sbin/nft -f

   define IF_LOOPBACK = lo

   # This empty definition allows the flush command to work if the table is not
   # already defined.
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

If you create a new loopback interface later, you can use set notation to
modify only the symbolic variable:

.. code-block:: nftables

   define IF_LOOPBACK = { lo, lo1 }

The scope of the symbolic variable is the file interpreted by the ``nft``
utility (and any included files), but restricted to the block where it is
defined and all inner blocks, to reduce clashes. The symbolic variable is only
interpreted in userspace. Any other configuration file passed to ``nft`` won't
be able to reference it. Similarly, retrieving the ruleset installed in
``nftables`` (such as by using the ``nft list ruleset`` command) reconstructs
the rules without references to symbolic variables.

Debugging
^^^^^^^^^

``nftables`` provides several means to debug firewall rules:

* **Log statement:** You can associate this with any rule to log packet
  information, either to the kernel log (readable via ``dmesg``) or to a
  userspace application. This is described in more detail in the `nftables
  documentation
  <https://wiki.nftables.org/wiki-nftables/index.php/Logging_traffic>`_ and
  in the `manual page
  <https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#statements>`_
  under ``LOG STATEMENT``.
* **Tracing:** Setting the ``nftrace`` flag on a packet allows you to trace all
  rules matched by a packet within all chains and tables, identifying any
  actions taken. This is described in more detail in the `nftables
  documentation
  <https://wiki.nftables.org/wiki-nftables/index.php/Ruleset_debug/tracing>`_.

Log statement
.............

The highlighted lines in the following example demonstrate using the ``log``
statement to send packets arriving on the loopback interface to the kernel log
before accepting them:

.. code-block:: nftables
   :caption: /etc/nftables.conf
   :linenos:
   :emphasize-lines: 23-27

   #!/usr/sbin/nft -f

   define IF_LOOPBACK = lo

   # This empty definition allows the flush command to work if the table is not
   # already defined.
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

Checking ``dmesg`` shows messages like the following (assuming packets are
flowing through the loopback interface):

.. code-block:: text

   [694077.575927] loopback packet: IN=lo OUT= MAC=00:00:00:00:00:00:00:00:00:00:00:00:08:00 SRC=127.0.0.1 DST=127.0.0.53 LEN=73 TOS=0x00 PREC=0x00 TTL=64 ID=24453 DF PROTO=UDP SPT=37969 DPT=53 LEN=53

Rule tracing
............

The ``nftrace`` flag enables tracing of a packet's flow through ``nftables``
rules across chains and tables, from the moment the flag is set until packet
processing completes or the flag is cleared. This allows complex debugging of
``nftables`` firewall rules. The system sends packet information, along with
references to the traversed rules, to a userspace application through the
netlink interface. Use the ``nft monitor trace`` command to receive this
information.

You can combine the ``meta nftrace set 1`` statement with a match expression to
set the flag, while ``meta nftrace set 0`` clears it. To identify all traversed
rules, set the flag as early as possible. The highlighted lines in the
following example create two chains attached to the ``prerouting`` and
``output`` hooks, running as early as feasible (even before other chains
registered at the ``raw`` priority):

.. code-block:: nftables
   :caption: /etc/nftables.conf
   :linenos:
   :emphasize-lines: 16-22,24-29

   #!/usr/sbin/nft -f

   define IF_LOOPBACK = lo

   # This empty definition allows the flush command to work if the table is not
   # already defined.
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

The two rules match only UDP datagrams, irrespective of whether they are
transported by IPv4 or IPv6 (``meta l4proto udp``), and then activate rule
tracing for those packets (``meta nftrace set 1``). Running the ``nft monitor
trace`` command produces messages such as:

.. code-block:: text

   trace id 78653943 inet host-firewall trace-inbound packet: iif "lo" @ll,0,112 0x800 ip saddr 127.0.0.53 ip daddr 127.0.0.1 ip dscp cs0 ip ecn not-ect ip ttl 1 ip id 64669 ip protocol udp ip length 168 udp sport 53 udp dport 36520 udp length 148 @th,64,96 0x2e4881800001000100000004
   trace id 78653943 inet host-firewall trace-inbound rule meta l4proto udp meta nftrace set 1 (verdict continue)
   trace id 78653943 inet host-firewall trace-inbound policy accept
   trace id 78653943 inet host-firewall firewall-input packet: iif "lo" @ll,0,112 0x800 ip saddr 127.0.0.53 ip daddr 127.0.0.1 ip dscp cs0 ip ecn not-ect ip ttl 1 ip id 64669 ip protocol udp ip length 168 udp sport 53 udp dport 36520 udp length 148 @th,64,96 0x2e4881800001000100000004
   trace id 78653943 inet host-firewall firewall-input rule ct state established,related accept (verdict accept)

The ``trace id`` is the same for the same packet across different tables and
chains, allowing you to correlate different output lines. Whenever a packet
starts being handled by a chain, a ``packet`` line is output with information
about the packet contents.

Note that the tracing notifications received by the ``nft monitor trace``
utility only contain identifier references to the tables, chains, and rules.
``nft monitor trace`` reads all rules when it first starts. It reconstructs the
table and chain names and actual rule content from that initial read for every
logged packet. This means if you change rules after starting ``nft monitor
trace``, the output will be incomplete or inaccurate (especially since rule
identifiers can be reused), so a printed rule might not be the actual rule that
a packet matched.

Bytecode inspection
...................

You can observe the bytecode interpreted by the Linux kernel using the
``--debug=netlink`` argument to ``nft``. This works for commands that modify
rules (for example, adding a new rule) and for those that retrieve rules. The
bytecode prints alongside the rule handle (rule identifier). The ``--handle``
option is useful for printing the handles associated with each rule.

For example, listing the ``trace-inbound`` chain created above:

.. code-block:: console

   sudo nft --handle --debug=netlink list chain inet host-firewall trace-inbound

Produces the following output:

.. code-block:: nftables

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

The ``nftables`` component integrates into the existing Netfilter subsystem and
uses the same hooks, stateful processing for connection tracking or Network
Address Translation (NAT), and functionality for userspace packet queueing and
processing as the ``xtables`` subsystem.

A high-level understanding of the Netfilter framework is important for managing
firewall rules. This section provides necessary information and references
additional documentation.

Packet flow
~~~~~~~~~~~

A packet starts being handled by the Linux networking subsystem (and, by
extension, Netfilter) through one of three options:

* It is received by a network interface driver (whether for a physical Network
  Interface Controller (NIC) or a virtual one).
* It is generated by an application process on the system (via a socket).
* It is generated by the kernel.

Netfilter integrates into the wider Linux network subsystem. Packet processing
goes through multiple decision points, potentially modifying the packet, such
as:

* Fragment reassembly.
* Connection tracking.
* Routing decisions.
* Source and destination NAT (including port translation).

Netfilter provides hooks that allow Netfilter components to process a packet at
various stages. Both ``nftables`` and ``xtables`` use these to execute
user-defined rules. The names of the predefined chains in the legacy
``iptables``, ``ip6tables``, ``ebtables``, and ``arptables`` utilities derive
from the names of the Netfilter hooks:

* ``ingress`` (only available for ``nftables``)
* ``prerouting`` (for bridge and IP)
* ``input`` (for ARP, bridge, and IP)
* ``forward`` (for bridge and IP)
* ``postrouting`` (for bridge and IP)
* ``output`` (for ARP, bridge, and IP)
* ``egress`` (only available for ``nftables``)

Packets don't traverse all hook points, depending on decisions made during
processing. This is represented graphically in the diagram on the `Netfilter
hooks nftables wiki page
<https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks>`_. Using
bridges results in a different packet flow, but one that partially overlaps
with the flow taken by non-bridged packets.

Note that some standard packet processing happens at certain hook points
(fragment reassembly, connection tracking lookup, NAT), while others occur
in-between hook points (routing decision). At each hook point, a priority
defines the order of operations. For example, these are some standard
operations executed at the IP layer ``prerouting`` hook:

.. csv-table::
   :header: Netfilter priority value, Operation
   :widths: auto

   -400, fragment reassembly
   -200, connection tracking lookup and association
   -100, destination NAT

You can list the registered functions, including ``nftables`` chains and
standard Netfilter processing, with the following command (note that numerical
values are priorities listed in decimal format):

.. code-block:: console

   sudo nft list hooks

If you register rules to execute at a priority value lower than ``-400`` (for
example, ``-500``), they execute before IP datagram fragments reassemble. As
such, the rules may see IP datagram fragments for which the transport header
may not be available, because they aren't the first fragment. On the other
hand, rules registered at a priority value higher than ``-400`` (for example,
``-300``) won't be able to make decisions based on fragmentation information
(the packet looks as if the entire IP datagram was received).

The priority values themselves don't hold intrinsic meaning, other than the
fact that some standard operations execute at well-known priority values. For
example, without other context, registering rules at priority ``1000`` is no
different from using priority ``1500``. The `nftables documentation
<https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks#Priority_within_hook>`_
lists the well-known priority values.

A packet stops being handled by the Linux networking subsystem, implying that
no more Netfilter hooks are invoked, when one of these conditions occurs:

* The packet is dropped, either through a firewall rule or some other condition
  in the standard processing (for example, blackhole route).
* The packet is passed to an application process on the system (via a socket).
* The packet is handled by the kernel (for example, ICMP echo request - a
  ping).
* The packet is sent out a network interface (whether for a physical NIC or a
  virtual one).

It should be noted that a particular packet can traverse the Netfilter hooks
several times, in conditions such as the followings:

* The packet is sent out a virtual interface that loops the packet back to the
  same Linux kernel (for example, `veth
  <https://manpages.ubuntu.com/manpages/en/man4/veth.4.html>`_ interfaces),
  although the list of hooks **won't** overlap completely. FIXME: does
  this even make sense? Of course a packet sent out a veth is going to come back
  in on the pair... nfmark is not maintained - for all intents and purposes,
  this is a new packet.
* Virtual Routing and Forwarding (VRF) is in use - a packet will traverse the L3
  prerouting hook twice, once with the input interface set to the L3 interface
  and once with the input interface set to the VRF interface.
* The packet is processed and reinjected by the kernel into the networking
  stack (for example, after IPsec encryption/decryption and ESP
  encapsulation/decapsulation in tunnel mode). Although the packet is
  admittedly different, some of the state is maintained across this operation,
  such as the Netfilter mark. FIXME: technically, this is a different packet -
  does it even make sense? Same applies to other L3 encapsulations, e.g. vxlan.

The Netfilter hooks and, hence, the ``nftables`` rules are managed
independently per `network namespace
<https://manpages.ubuntu.com/manpages/en/man7/network_namespaces.7.html>`_. As
such, different firewall rules are configured in each network namespace,
facilitating functionality such as containers. This also means that if the two
ends of a veth pair are associated with different namespaces, they will be
processed by independent firewall rules.

Structure
---------

``nftables`` structures objects for managing the firewall in a hierarchy. The
primary terminology used is:

* **Rulesets:** This refers to all objects defined in ``nftables``. The
  command ``nft list ruleset`` outputs everything defined in ``nftables``
  (within a particular network namespace), while ``nft flush ruleset`` destroys
  all objects: tables, :ref:`sets <Sets>`, :ref:`maps <Maps>`, and so on. This
  includes elements defined in sets and maps, or the contents of stateful
  objects (for example, counter values). As such, a command such as ``(echo
  "nft flush rulset"; nft list ruleset) | nft -f -`` is effectively a no-op
  (although the state may change between reading and overwriting).
* **Tables:** Unlike ``xtables``, you can define any number of tables in
  ``nftables``. These are collections of chains, :ref:`sets <Sets>`, :ref:`maps
  <Maps>`, and stateful objects (for example, counters). The table name doesn't
  hold intrinsic meaning; system administrators or applications can name them
  as desired. Tables associate with an address family, dictating limitations on
  chains and determining what Netfilter hooks the chains associate with. The
  address families are documented in the `manual page
  <https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#address%20families>`_.
  These are:
    * **ip:** For IPv4 packets (managed by legacy ``iptables``).
    * **ip6:** For IPv6 packets (managed by legacy ``ip6tables``).
    * **inet:** For both IPv4 and IPv6 packets, simplifying management of
      consistent rules across both network protocols.
    * **arp:** For IPv4 ARP packets (managed by legacy ``arptables``).
    * **bridge:** For Ethernet packets traversing bridges (managed by legacy
      ``ebtables``).
    * **netdev:** For very early (on ingress) or very late (on egress) packet
      processing. Useful for efficient filtering or load balancing, but imposes
      limitations, such as only supporting ``ingress`` and ``egress`` hooks and
      requiring strict association of chains with a *single* network interface.
      Note that starting with Linux 5.10, the **inet** family also supports the
      ``ingress`` hook without the single network interface limitation, largely
      reducing the usefulness of the **netdev** address family. Using a single
      table in the **inet** family also facilitates sharing :ref:`sets <Sets>`
      and :ref:`maps <Maps>` with chains registered at other hooks.
* **Chains:** Containers for firewall rules. Similarly to ``xtables``, there is
  a distinction between base chains and regular chains. Unlike ``xtables``,
  base chains aren't predefined, and you can create as many as necessary,
  including multiple chains at the same hooks (with or without the same
  priority).
    * **Base chains** have a ``type``, a ``policy``, and register with a
      Netfilter ``hook`` point at a specific ``priority``. They can have
      additional attributes, as described in the `manual page
      <https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#chains>`_.
      Their rules evaluate whenever packet processing traverses the specified
      Netfilter hook.
    * **Regular chains** are simply called upon by rules in other chains and
      act as subprocedures. They simplify rule maintenance or optimize rule
      processing (for example, by using :ref:`verdict maps <Verdict maps>`).
      Rules within a regular chain aren't evaluated during packet processing
      unless called upon, directly or indirectly, from a base chain.

For base chains, the most important attributes are:

* **type:** Dictates the conditions on which the chain processes a packet and
  the available hooks. Some statements are only available in certain chain
  types. Possible values are:
    * **filter:** Generic type, applicable to all address families and hooks.
      Used for typical firewall actions and arbitrary packet modifications.
    * **nat:** Equivalent to chains defined in the legacy ``iptables`` /
      ``ip6tables`` ``nat`` table. Only the first packet of a connection is
      processed by chains of this type. NAT actions (``snat``, ``dnat``,
      ``masquerade``, ``redirect``) can only be taken in these chains.
    * **route:** Has no equivalent in ``xtables`` but allows integrating
      ``nftables`` rules with policy routing. Can only be used with
      locally-generated packets (from processes or kernel), with only the
      ``output`` hook available. Per the `Netfilter flow diagram
      <https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks#Netfilter_hooks_into_Linux_networking_packet_flows>`_,
      the routing decision for locally-generated packets happens before any
      hooks. However, if rules in a ``route`` type chain modify parts of a
      packet or its metadata (such as the Netfilter mark) used in `policy
      routing decisions
      <https://manpages.ubuntu.com/manpages/en/man8/ip-rule.8.html>`_,
      another route lookup occurs. Packets received from a network interface
      don't require this special chain type, as several hooks are available to
      prepare a packet before it goes through routing decisions.
* **hook:** The processing point at which rules evaluate, as described in the
  :ref:`Packet flow` section. Not all hooks are available for all address
  families and chain types. Restrictions are listed in the `Chains section of
  the manual page
  <https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#chains>`_.
* **priority:** Dictates the order in which chains and other standard Netfilter
  operations perform at a particular hook point, as described in the
  :ref:`Packet flow` section. Can be given as a symbolic name (e.g.
  ``filter``, ``raw``, ``mangle``), a signed integer (e.g. ``0``, ``-300``),
  or a value relative to a symbolic name (e.g. ``raw - 10``). Note that
  symbolic names may map to different integer values depending on the address
  family (``filter`` is ``0`` for ``inet``, ``ip``, ``ip6``, ``arp``, and
  ``netdev``, but ``-200`` for ``bridge``).
* **policy:** Dictates the verdict associated with a packet if none of the
  matched rules have a verdict during processing. Must be either ``accept``
  (the default) or ``drop``.

As described in the :ref:`Packet flow` section, a packet stops being handled by
the networking subsystem when it is either dropped or traverses the entire
processing flow and is sent out to an interface or handled by an application or
the kernel. As such, a verdict of ``drop`` is final for a packet, but
``accept`` is not: it is sufficient for one chain in one table to ``drop`` a
packet for it to be discarded, but the packet must be ``accept``-ed by all
chains in all tables to continue its journey (an ``accept`` verdict only
terminates processing in a particular base chain, but doesn't influence
processing in other base chains the packet subsequently traverses).

Rule composition
~~~~~~~~~~~~~~~~

Rules comprise expressions and statements, both optional. Expressions match
packets, while statements dictate actions. A rule without statements is valid
and useful for debugging, as :ref:`rule tracing <Rule tracing>` reports it for
any matched packets. For example, the highlighted rule below matches
locally-generated IPv4 UDP packets without taking actions (note the ``ip
protocol udp`` expression, as opposed to ``meta l4proto udp``, matches only
IPv4 packets):

.. code-block:: nftables
   :caption: /etc/nftables/tables.d/test-firewall.conf
   :linenos:
   :emphasize-lines: 8

   #!/usr/sbin/nft -f

   destroy table inet test-firewall
   table inet test-firewall {
       chain test-outbound {
           type filter hook output priority filter; policy accept;

           ip protocol udp
       }
   }

Expressions within a rule combine with a logical **AND** when evaluated: all
must succeed for the rule's statements to execute. Combining expressions with a
logical **OR** requires multiple rules, :ref:`sets <Sets>`, :ref:`maps <Maps>`,
or intervals. In the example below, the first rule matches both IPv4 and IPv6
packets if the transport protocol is UDP (``meta l4proto udp``) and the
destination port is ``53`` (``udp dport 53``). The second rule matches packets
if the network protocol is IPv4 (implied), the transport protocol is UDP
(implied), and either:

* The IPv4 destination address is ``10.1.1.1`` and the destination port is
  ``53``.
* The IPv4 destination address is ``10.2.2.2`` and the destination port is
  ``80`` or ``443``.

The ``ip daddr . udp dport`` syntax is explained in the :ref:`Concatenations`
section.

.. code-block:: nftables
   :caption: /etc/nftables/tables.d/test-firewall.conf
   :linenos:
   :emphasize-lines: 9,14-18

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

A rule can contain zero or more statements. There are two types: `terminal` and
`non-terminal`. Terminal statements unconditionally terminate the rule's
evaluation and may terminate the chain's evaluation or stop packet processing
entirely. Non-terminal statements result in actions that either don't terminate
rule evaluation or only do so conditionally. A rule may have at most one
terminal statement, which must be placed last. Most :ref:`verdict statements
<Verdict statements>` are terminal, but some non-verdict statements are also
terminal (for example, ``reject``, which drops a packet and generates an ICMP
or TCP reset response).

Verdict statements
^^^^^^^^^^^^^^^^^^

Verdict statements affect the control flow of rule evaluation. Most are
terminal (apart from ``continue``). The ``continue`` statement is implied if no
other terminal statement is issued.

* **accept:** Terminates packet processing in the current base chain, allowing
  the packet to continue within Netfilter and the Linux networking subsystem.
  Other base chains at the current hook with a higher numerical priority still
  evaluate the packet and may drop it. Using this in a regular chain called
  from a base chain stops processing of all subsequent rules in the current
  chain and chains higher up the call stack.
* **drop:** Terminates packet processing within the Linux networking subsystem
  with no further action. This is the basis of a firewall implementation. No
  further base chains are invoked.
* **queue:** Terminates packet processing in the current base chain and passes
  the packet to userspace for processing. Userspace must provide a verdict of
  ``accept`` or ``drop``. See the `nftables userspace queueing documentation
  <https://wiki.nftables.org/wiki-nftables/index.php/Queueing_to_userspace>`_.
* **continue:** Implied action if no other terminal statement is issued: rule
  evaluation continues with the next rule in the current chain.
* **jump:** Continue processing in a new regular chain. Upon completion,
  processing returns to the current chain, unless a processing-terminating
  statement (``accept``, ``drop``, ``queue``, ``reject``) issues in one of the
  invoked chains. Similar to invoking a subprocedure.
* **goto:** Continue processing in a new regular chain. Upon completion,
  processing returns to the chain higher up in the call stack (if the current
  chain is a base chain, the policy action is taken). Similar to invoking and
  returning the result of a subprocedure.

The following example extends the firewall definition with skeleton structures
for two new functions in the highlighted lines, demonstrating control flow
functionality:

* Setting the Netfilter packet mark for inbound packets to represent where the
  packet originated (the "realm"), allowing subsequent rules to decide based on
  this criteria. For example, rules below set the mark to ``1`` (via
  ``MARK_REALM_LOCAL``) if the packet was received on a loopback interface. Two
  new chains are introduced: ``early-inbound`` (base chain) and
  ``mark-inbound-determine`` (regular chain).
    * When packet processing follows the packet through an input VRF interface
      (``meta iifkind "vrf"``), we terminate processing in this chain via
      ``return``. In a base chain, ``return`` is equivalent to the chain's
      policy (``accept`` here).
    * If a packet arrives with a non-zero packet mark (``meta mark != 0``),
      possible with functionality like VXLAN GBP extension, drop the packet.
    * Invoke ``mark-inbound-determine`` via ``jump mark-inbound-determine``;
      this allows subsequent rules in ``early-inbound`` to evaluate.
    * In ``mark-inbound-determine``, if a packet is received on an interface
      defined in ``IF_LOOPBACK`` (``meta iif $IF_LOOPBACK``):
        * Set the packet mark to ``MARK_REALM_LOCAL`` (``1``) via ``meta mark
          set $MARK_REALM_LOCAL`` (non-terminal).
        * Terminate processing in ``mark-inbound-determine`` via ``return``,
          continuing in the caller chain (``early-inbound``).
* In ``firewall-input`` base chain, delegate multicast packet processing to
  ``firewall-input-multicast`` regular chain. This encapsulates multicast
  logic. The configuration accepts IPv4 IGMP packets (needed for multicast
  queriers and snooping). The IPv6-equivalent MLD rule appears in the
  :ref:`Sets` section. Separately, Multicast DNS (mDNS) packets allow ad-hoc
  service discovery (``udp dport 5353 accept``).
    * ``goto`` ensures subsequent rules in ``firewall-input`` aren't evaluated,
      even if the called chain executes ``return`` or no rules match; instead,
      the policy (``drop``) applies.
    * ``accept`` is necessary in ``firewall-input-multicast`` to allow packets.
      Once a condition is met (e.g., ``ip protocol igmp``), processing
      finalizes.

.. code-block:: nftables
   :caption: /etc/nftables.conf
   :linenos:
   :emphasize-lines: 5,18-31,33-36,49,55-64

   #!/usr/sbin/nft -f

   define IF_LOOPBACK = lo

   define MARK_REALM_LOCAL = 1

   # This empty definition allows the flush command to work if the table is not
   # already defined.
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

``nftables`` supports many statements, documented in the `Statements section of
the manual package
<https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#statements>`_. Commonly
used ones include:

* **reject statement:** Drops a packet and generates an appropriate ICMP or TCP
  reset response. For example, ``udp dport 389 reject with icmpx
  admin-prohibited`` matches packets for the LDAP port and generates an
  admin-prohibited ICMP response (type ``3`` code ``13`` for `IPv4
  <https://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml#icmp-parameters-codes-3>`_
  and type ``1`` code ``1`` for `IPv6
  <https://www.iana.org/assignments/icmpv6-parameters/icmpv6-parameters.xhtml#icmpv6-parameters-codes-2>`_).
* **log statement:** Described in the :ref:`Log statement` section.
* **meta statements:** Changes meta information tracked by Netfilter for a
  packet, such as ``meta mark set 42`` or ``meta nftrace set 1`` (:ref:`rule
  tracing <Rule tracing>`).
* **nat statements:** Allow source and destination NAT (including dynamic
  translation for transport ports and stateful ICMP processing).
* **counter statements:** Support counting packets and bytes matched by rules.
* **payload statements:** Change arbitrary packet contents. For example, ``ip
  dscp set 46`` sets IPv4 DSCP to 46 (EF).
* **set statement:** Dynamically adds elements to :ref:`sets <Sets>` and
  :ref:`maps <Maps>`.
* **map statement:** Looks up elements in a :ref:`map <Maps>` by key and
  returns the value for use as an argument. A non-terminal statement that can
  conditionally terminate rule processing if no element matches.
* **vmap statement:** Dynamically determines a verdict based on a key (:ref:`Verdict
  maps`).

Expressions
^^^^^^^^^^^

``nftables`` uses a bytecode-based virtual machine for expression evaluation.
An expression has a data type determining operations and combinations. For
example, ``meta mark`` has a 32-bit integer type. See `Data Types
<https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#data%20types>`_. Data
types are a feature of the ``nft`` userspace utility; the kernel bytecode
operates on raw bytes.

Display an expression's data type using ``nft describe``:

.. code-block:: console

   nft describe udp dport

Expressions generally follow ``class attribute`` convention (e.g., ``udp
dport``, ``ip protocol``). See `Primary Expressions
<https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#primary%20expressions>`_
and `Payload Expressions
<https://manpages.ubuntu.com/manpages/en/man8/nft.8.html#payload%20expressions>`_.

Combine expressions with comparison operators to form `relational expressions
<https://wiki.nftables.org/wiki-nftables/index.php/Building_rules_through_expressions>`_:

* ``eq`` or ``==``: Implied comparison. Compares an expression with a constant
  or set lookup (``udp dport == { 80, 443 }``).
* ``ne`` or ``!=``: Matches if expression is not equal to constant or not in
  set.
* ``lt`` / ``<``, ``gt`` / ``>``, ``le`` / ``<=``, ``ge`` / ``>=``: Matches if
  comparison is lower, greater, lower/equal, or greater/equal to constant.

Combine with binary operators:

* ``and`` / ``&``: Bitwise AND
* ``or`` / ``|``: Bitwise OR
* ``xor`` / ``^``: Bitwise exclusive-OR
* ``lshift`` / ``<<``: Bitwise left shift
* ``rshift`` / ``>>``: Bitwise right shift

The right-hand side must be a constant expression. For example, match IPv4
packets where the second most-significant byte of destination IP is < 16:

.. code-block:: nftables

   (ip daddr >> 16) & 0xFF < 0x10

Equivalent to:

.. code-block:: nftables

   ip daddr & 0x00F00000 == 0

Or:

.. code-block:: nftables

   ip daddr & 0x00F00000 0

Equality/non-equality operators work with `intervals
<https://wiki.nftables.org/wiki-nftables/index.php/Intervals>`_. Match IPv4
packets where destination is A.B.C.D, with B between 10 and 20:

.. code-block:: nftables

   (ip daddr >> 16) & 0xFF == 10-20

IPv4/IPv6 addresses support prefix notation. Match destination IPv4 not in
RFC1918 private addresses:

.. code-block:: nftables

   ip daddr != { 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 }

Not all operations are supported by all data types. For example, IPv6 addresses
don't support bit shifting, and ``and``/``or``/``xor`` require full IPv6
addresses on the right-hand side.

You can combine expression operators with statements supporting expressions.
For example, set Netfilter packet mark to least-significant 16 bits of IPv4
source, combined with bit 16 set, only if source is in 10.0.0.0/16:

.. code-block:: nftables

   ip saddr 10.0.0.0/16 meta mark set (ip saddr & 0xFFFF) | 0x10000

Bitmasks support specific operations:

* No operator: matches if any specified bits are set (``tcp flags syn,ack``
  matches if SYN or ACK set).
* ``/`` operator: specifies a mask. ``tcp flags syn / syn,ack`` matches if, out
  of SYN and ACK, only SYN is set.
* Equality operators: compare exact bitmask. ``tcp flags == syn,ack`` matches
  if only SYN and ACK are set.

Using these concepts, we create a framework for using the Netfilter mark as a
bitfield for generic firewall rules. Since the mark can be determined
externally (e.g., VXLAN GBP) and copied during decapsulation (e.g., IPsec), one
bit flags local validation.

The following configuration extends the example in highlighted lines:

* Extend ``early-inbound`` with regular chains ``mark-inbound-determine`` and
  ``mark-inbound-external-validate``.
* Add rules to ``firewall-input`` using ``ct state`` bitmask:
    * Allow ``established`` or ``related`` flows.
    * Drop ``invalid`` flows.

.. code-block:: nftables
   :caption: /etc/nftables.conf
   :linenos:
   :emphasize-lines: 5-13,15,17-20,22,43-50,53-60,66-79,88-91

   #!/usr/sbin/nft -f

   define IF_LOOPBACK = lo

   # The packet mark is interpreted as follows (big endian):
   #    3                   2                   1                   0
   #  1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0
   # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   # |V| Unused                                      | Realm (6) |
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

   # This empty definition allows the flush command to work if the table is not
   # already defined.
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

Concatenations allow combining expressions into compound expressions with a
complex type using the ``.`` operator. This is powerful with :ref:`sets <Sets>`
and :ref:`maps <Maps>` for defining keys based on multiple attributes. For
example:

.. code-block:: nftables

   meta mark . meta l4proto . th dport

Using binary operators and :ref:`anonymous sets <Sets>`:

.. code-block:: nftables

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

Sets act as containers for values with efficient lookup, addition, and removal.
They support arbitrary types via :ref:`Concatenations`.

* **Named sets:** Defined within tables, allowing management by external
  applications and rules.
* **Anonymous sets:** Defined inline (``tcp dport { 80, 443 }``), enabling logical
  ``OR``.

Named sets can be defined multiple times additively. Unlike anonymous sets, you
can control behavior with options:

* **type** or **typeof:** Defines element format. ``typeof`` allows derivation
  from expression.
* **flags interval:** Allows intervals.
* **flags dynamic:** Allows adding elements from rules.
* **flags timeout:** Allows automatic element removal.
* **timeout:** Default expiration interval.
* **size:** Maximum number of elements.

The highlighted lines extend the firewall configuration with:

* Named set ``input-services`` for allowed services.
* Rule referencing the set in ``firewall-input``.
* Rule in ``firewall-input-multicast`` allowing IPv6 MLD and ND via anonymous
  set.

.. code-block:: nftables
   :caption: /etc/nftables.conf
   :linenos:
   :emphasize-lines: 30-45,112-114,124-134

   #!/usr/sbin/nft -f

   define IF_LOOPBACK = lo

   # The packet mark is interpreted as follows (big endian):
   #    3                   2                   1                   0
   #  1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0
   # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   # |V| Unused                                      | Realm (6) |
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

Element management in rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can dynamically add named set elements using ``add`` or ``update``.
Requires ``dynamic`` flag. ``add`` terminates rule early if element exists.
``update`` updates metadata (like timeout).

Example: trivial rate limit for new connections. Accepts new connections only
if source address, protocol, and port combination can be added to set.

.. code-block:: nftables
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

Example: ``update`` statement refreshes timeout, tracking any IPv4 /24 prefix
initiating a new flow in last 10 minutes.

.. code-block:: nftables
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

Inspect and manage named set elements using ``nft``:

* List elements: ``sudo nft list set ip flow-track connections``
* Remove all elements: ``sudo nft flush set ip flow-track connections``
* Reset stateful objects: ``sudo nft reset set ip flow-track connections``
* Retrieve elements: ``sudo nft get element ip flow-track connections '{ 127.0.0.0 }'``
* Add element: ``sudo nft add element ip flow-track connections '{ 10.0.0.0 }'``
* Delete element: ``sudo nft delete element ip flow-track connections '{ 10.0.0.0 }'``

Maps
~~~~

Maps associate keys to values. Sets are maps where keys have no values. Usage
is similar to :ref:`sets <Sets>`, including named/anonymous maps.

The ``map`` statement looks up a key and returns the value.

The highlighted lines extend the example with maps from IPv4/IPv6 prefixes to
Netfilter marks representing origin realm.

.. code-block:: nftables
   :caption: /etc/nftables.conf
   :linenos:
   :emphasize-lines: 47-58,60-69,105-107

   #!/usr/sbin/nft -f

   define IF_LOOPBACK = lo

   # The packet mark is interpreted as follows (big endian):
   #    3                   2                   1                   0
   #  1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 0
   # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   # |V| Unused                                      | Realm (6) |
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

Verdict maps associate keys to :ref:`verdict statements <Verdict statements>`.
Use with ``vmap`` statement to look up key and execute associated verdict.

Example: rewriting ``early-inbound`` branching with ``vmap``.

.. code-block:: nftables
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

Stateful objects track information across unrelated packets (counters, quotas,
limits, connection limits).

* **Named objects:** Associated with table, referenced by multiple rules.
* **Anonymous objects:** Bound to single rule or set key.

Example: creating and referencing a named counter.

.. code-block:: nftables
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

Example extension using anonymous objects:

* HTTP traffic: Connection limit (1000), limit rate (20/min burst 500).
* Non-HTTP: Connection limit (500), limit rate (10/min burst 100).

.. code-block:: nftables
   :caption: /etc/nftables/tables.d/limits.conf
   :linenos:
   :emphasize-lines: 12-16,18-19,22-36,38-53

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

Example: using extended ``add``/``update`` syntax for tracking flow count and
rate per subnet.

.. code-block:: nftables
   :caption: /etc/nftables/tables.d/limits.conf
   :linenos:
   :emphasize-lines: 6-22,24-40,59-66,84-97,99-112

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

Flowtables accelerate packet forwarding. They act as a cache, bypassing the
forwarding stack for known flows. Cannot be used for local process flows.

The following example enables accelerated forwarding for packets between a set of
interfaces.

.. code-block:: nftables
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

The ``fib`` expression allows route lookups. Useful for checking if an address
is local or for reverse-path filtering.

Example: counting packets with local or broadcast destination.

.. code-block:: nftables
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

Example: reverse-path filtering dropping packets if arriving on incorrect
interface.

.. code-block:: nftables
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
           # be determined.
           fib saddr . mark . iif oif 0 drop
       }
   }

Payload expressions
~~~~~~~~~~~~~~~~~~~

Use raw payload expressions for Deep Packet Inspection (DPI) or when specific
fields aren't supported. Format: ``@base,offset,length``.

.. list-table::
   :header-rows: 1
   :widths: auto

   * - Base
     - Description
     - Example
   * - ``@ll``
     - Link layer (e.g. Ethernet)
     - ``@ll,0,48`` (Dest MAC)
   * - ``@nh``
     - Network header (e.g. IPv4)
     - ``@nh,48,8`` (IPv6 Next Header)
   * - ``@th``
     - Transport header (e.g. TCP)
     - ``@th,110,2`` (TCP SYN/FIN)
   * - ``@ih``
     - Inner header
     - ``@ih,8,16`` (TLS version)
