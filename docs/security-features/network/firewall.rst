Firewall
========

.. tab-set::

    .. tab-item:: 25.04 

        ufw 0.36.2-9 

    .. tab-item:: 24.10
        
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


`ufw <https://help.ubuntu.com/community/UFW>`_ is a default firewall configuration tool for Ubuntu. It works as a frontend for ``iptables`` and is available in Ubuntu but disabled by default.

iptables, ip6tables, arptables and ebtables
-------------------------------------------

Historically, `iptables <https://netfilter.org/projects/iptables/index.html>`_, ip6tables, arptables and ebtables have been the primary tools used in Linux systems for managing firewall configurations. It allows us to configure and inspect the Linux kernel’s netfilter configuration. Operating at a low level, it interacts directly with the network stack to manage how packets are handled.

Starting with Ubuntu FIXME, the ``iptables`` package has provided versions of the ``iptables``, ``ip6tables``, ``arptables`` and ``ebtables`` tools that work with nftables API and provide a compatible interface to the legacy implementation. The nftables have been the default since Ubuntu FIXME. These are managed through the alternatives system and the current configuration can be displayed with the following commands:

.. code-block:: bash
    update-alternatives --display iptables
    update-alternatives --display ip6tables
    update-alternatives --display arptables
    update-alternatives --display ebtables


nftables
--------

`nftables <https://www.nftables.org/projects/nftables/index.html>`_ is a successor to iptables, which was designed to simplify and enhance Linux firewall management. 

``nftables`` reduces complexity of ``iptables`` and offers improved performance. It can also be used to manage rules that would've previously been managed by arptables and ebtables, while additionally supporting common IPv4 and IPv6 rules.

Starting with Ubuntu FIXME, the ``nftables`` package provides a systemd service unit file that is disabled by default. If enabled, the service unit file will automatically load ``nftables`` configuration from the ``/etc/nftables.conf`` file (a mock file that does not perform any filtering is provided in the ``nftables`` package). You can enable this and load the configuration using the following commands:

.. code-block:: bash
    sudo systemctl enable nftables.service
    sudo systemctl start nftables.service

For more information on configuring nftables, please see the `nft manual page <https://manpages.ubuntu.com/manpages/man8/nft.8.html>`_ and the `nftables documentation <https://wiki.nftables.org/wiki-nftables/index.php/Main_Page>`_.

ufw
----
`ufw <https://help.ubuntu.com/community/UFW>`_ is a firewall framework that acts as a frontend for both ``iptables`` and ``nftables``.

Regression tests: `ufw tests <https://bazaar.launchpad.net/~jdstrand/ufw/trunk/files>`_.


Stateful vs. stateless filtering
--------------------------------

A *stateless* firewall makes decisions based only on the current packet, with no memory of previous packets in the connection.

A *stateful* firewall tracks the state of connections and makes decisions based on the context of each packet.

``iptables``, or ``nftables`` can be used for *stateless* and *stateful* processing. ``ufw`` stateful by design. Connection tracking is a kernel-level feature that keeps track of the state of every network connection passing through the system. Connection tracking is provided through `conntrack <https://conntrack-tools.netfilter.org/>`_ tool. When a packet enters the system, ``conntrack`` inspects the packet’s headers, compares it to an internal connection table, ipdates the connection state, and then passes the state to the firewall for rule evaluation.

Using iptables and nftables directly instead of ``ufw``
-------------------------------------------------------

``ufw`` is a suitable choice for most common cases, however, ``iptables`` and ``nftables`` can be used directly if there is a need to define granular rule chains, for example:

* Creating custom chains to filter traffic differently based on network conditions.

* Filter based on more granular factors such as packet size, time of day, or multi-layer protocol inspection.

Further reading
---------------

* `Ubuntu Server documentation - Firewalls <https://documentation.ubuntu.com/server/how-to/security/firewalls/>`_