Firewall
========

.. tab-set::

    .. tab-item:: 24.04

        ufw 0.36.2-6 

    .. tab-item:: 24.04

        ufw  0.36.2-6

    .. tab-item:: 22.04

        ufw 0.36.1-4 

    .. tab-item:: 20.04

        ufw 0.36-6 

    .. tab-item:: 18.04
        
        ufw 0.36-0ubuntu0.18.04.1 
    
    .. tab-item:: 16.04

        ufw 0.35-0ubuntu2   

    .. tab-item:: 14.04

        ufw 0.34~rc-0ubuntu2 


`ufw <https://help.ubuntu.com/community/UFW>`_ is a default firewall configuration tool for Ubuntu. It works as a frontend for ``iptables`` and ``nftables`` and is available in Ubuntu but disabled by default. 

iptables
--------

Hisotircally, `iptables <https://netfilter.org/projects/iptables/index.html>`_ has been the primary tool used in Linux systems for many years. It allows us to configure and inspect the Linux kernel’s firewall rules. Operating at a low level, it interacts directly with the network stack to manage how packets are handled.

nftables
--------

`nftables <https://www.nftables.org/projects/nftables/index.html>`_ is a successor to iptables, which was designed to simplify and enhance Linux firewall management. 

``nftables`` reduces complexity of ``iptables`` and offers improved performance. 

ufw
----
`ufw <https://help.ubuntu.com/community/UFW>`_ is a firewall framework that acts as a frontend for both ``iptables`` and ``nftables``.

Regression tests: `ufw tests <https://bazaar.launchpad.net/~jdstrand/ufw/trunk/files>`_.

Tables, chains, rules
----------------------

``iptables``, ``nftables``, and by extention ``ufw`` operate on a *table → chain → rule* hierarchy:

**Tables** are logical grouping for the rules of a firewall configuration. They are the top-level container that holds **chains**. 

``iptables`` have default tables that manage different rule chains:

* **Filter**: basic packet filtering rules that control which packets enter and leave a network. 

* **Network Address Translation (NAT)**: rules for routing packets to remote networks. It is used for packets that require alterations.

* **Mangle**: rules for modifying IP header properties.

* **Raw**: rules that exempt packets from connection tracking.

* **Security**: mandatory access control (MAC) rules for access management.

``nftables`` do not provide any default tables, tables can be named and configured by the users freely, and are not limited to a single type of processing.

**Chains** are a set of **rules** that define the direction or context in which rules are applied:

* **INPUT**: packets destined for the local machine

* **OUTPUT**: packets originating from the local machine

* **FORWARD**: packets that are being forwarded through the system

* Custom chains (user-defined)

**Rules** are actual filtering or processing commands that determine how packets are handled within a chain. A rule defines conditions (for example., source IP, destination port, protocol) and specifies the action to be taken when those conditions are met (for examoke., accept, drop, log, etc.).
        

Stateful vs. stateless filtering
--------------------------------

A *stateless* firewall makes decisions based only on the current packet, with no memory of previous packets in the connection.

A *stateful* firewall tracks the state of connections and makes decisions based on the context of each packet.

``ufw``, ``iptables``, or ``nftables`` are *stateful* by design, the connection tracking is provided by ``conntrack``.

``conntrack`` for connection tracking
--------------------------------------

Connection tracking is a kernel-level feature that keeps track of the state of every network connection passing through the system. Connection tracking is provided through `conntrack <https://conntrack-tools.netfilter.org/>`_ tool. When a packet enters the system, ``conntrack`` inspects the packet’s headers, compares it to an internal connection table, ipdates the connection state, and then passes the state to the firewall for rule evaluation.

``conntrack`` allows to 

* list the contents of the conntrack table in plain text/XML

* search for individual entries in the conntrack table

* add new entries to the conntrack table

* list entries in the expect table

* add new entries to the expect table
  
* add/delete/update connection tracking timeout policies

Port ranges and protocols   
-------------------------

``uwf`` allows to define rules for specific port range and protocols.

Application profiles in UFW
---------------------------

``uwf`` allows to define rules for common applications and services. These profiles are stored in files within the ``/etc/ufw/applications.d/`` directory and help integrate firewall management with specific applications.

IPv6 considerations
-------------------

``ufw`` supports both IPv4 and IPv6 and applies the same default policy for both IPv4 and IPv6:

* Default allow outgoing, deny incoming for both IPv4 and IPv6.

* ``ufw`` will automatically apply firewall rules to both IP versions unless users disable one.

``ufw`` on boot 
-----------------------------------------------------

``ufw`` is controlled as a ``systemd`` service and can be enabled to start at boot.

The ``ufw`` systemd service file is typically located at ``/lib/systemd/system/ufw.service``.

Using iptables and nftables directly instead of ``ufw``
-------------------------------------------------------

``ufw`` is a suitable choice for most common cases, however, ``iptables`` and ``nftables`` can be used directly if there is a need to define granular rule chains, for example:

* Creating custom chains to filter traffic differently based on network conditions.

* Filter based on more granular factors such as packet size, time of day, or multi-layer protocol inspection.


