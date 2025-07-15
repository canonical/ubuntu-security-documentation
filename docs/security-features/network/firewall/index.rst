Firewall
========

.. toctree::
   :maxdepth: 1
   :glob:

   *

.. tab-set::

    .. tab-item:: 25.04

        iptables 1.8.11-2ubuntu1

        nftables 1.1.1-1build1

        ufw 0.36.2-9

    .. tab-item:: 24.10

        iptables 1.8.10-3ubuntu2

        nftables 1.1.0-2

        ufw 0.36.2-6

    .. tab-item:: 24.04

        iptables 1.8.10-3ubuntu2

        nftables 1.0.9-1build1

        ufw 0.36.2-6

    .. tab-item:: 22.04

        iptables 1.8.7-1ubuntu5.2

        nftables 1.0.2-1ubuntu2

        ufw 0.36.1-4

    .. tab-item:: 20.04

        iptables 1.8.4-3ubuntu2.1

        nftables 0.9.3-2

        ufw 0.36-6

    .. tab-item:: 18.04

        iptables 1.6.1-2ubuntu2.1

        nftables 0.8.2-1

        ufw 0.36-0ubuntu0.18.04.1

    .. tab-item:: 16.04

        iptables 1.6.0-2ubuntu3

        nftables 0.5+snapshot20151106-1

        ufw 0.35-0ubuntu2

    .. tab-item:: 14.04

        iptables 1.4.21-1ubuntu1

        ufw 0.34~rc-0ubuntu2


The Linux kernel includes the Netfilter subsystem, which is used to manipulate or decide the fate of network traffic headed into or through your Linux system. All modern Linux firewall solutions use this system for packet filtering. There are currently two components in the Netfilter subsystem which can be used for packet filter: ``iptables`` and ``nftables``. The latter is considered the successor and has been introduced into the mainline Linux kernel since version 3.13 released in 2014.

The Linux kernel rules are typically managed through userspace utilities:

* ``iptables``, ``ip6tables``, ``arptables`` and ``ebtables`` for the ``iptables`` Linux Netfilter component;
* ``nft`` for the ``nftables`` Linux Netfilter component.

`ufw <https://help.ubuntu.com/community/UFW>`_ is a simplified firewall configuration tool for Ubuntu. It works as a frontend for ``iptables`` and ``nftables`` and is available in Ubuntu, but disabled by default.


ufw - Uncomplicated Firewall
----

`ufw <https://help.ubuntu.com/community/UFW>`_ is a firewall framework that acts as a frontend for both ``iptables`` and ``nftables``. Details on configuring ``ufw`` can be found in the `Ubuntu Server documentation <https://documentation.ubuntu.com/server/how-to/security/firewalls/>`_.

Stateful vs. stateless filtering
--------------------------------

A *stateless* firewall makes decisions based only on the current packet, with no memory of previous packets in the connection.

A *stateful* firewall tracks the state of connections and makes decisions based on the context of each packet.

The ``iptables`` and ``nftables`` components of the Linux Netfilter subsystem can both be used for *stateless* and *stateful* processing and this carries over to the respective userspace utilities. The ``ufw`` utility is stateful by design. Connection tracking is a Linux kernel Netfilter feature that keeps track of the state of every network connection passing through the system. Connection tracking can be managed in userspace through the `conntrack <https://conntrack-tools.netfilter.org/>`_ tool.

Using iptables and nftables directly instead of ``ufw``
-------------------------------------------------------

``ufw`` is a suitable choice for many common cases, however, ``iptables`` and ``nft`` can be used directly if there is a need to define granular rule chains, for example:

* Creating custom chains to filter traffic differently based on network conditions.

* Filter based on more granular factors such as packet size, time of day, or multi-layer protocol inspection.

iptables, ip6tables, arptables and ebtables
-------------------------------------------

Historically, ``iptables``, ``ip6tables``, ``arptables`` and ``ebtables`` have been the primary tools used in Linux systems for managing firewall configurations. They allow us to configure and inspect the Linux kernel’s Netfilter configuration. Operating at a low level, they interact directly with the network stack to manage how packets are handled.

Starting with Ubuntu 16.04 Xenial Xerus, the ``iptables`` package has provided versions of the ``iptables``, ``ip6tables``, ``arptables`` and ``ebtables`` tools that work with ``nftables`` API and provide a compatible interface to the legacy implementation. The ``nftables`` backend has been the default since Ubuntu 20.10 Groovy Gorilla. These are managed through the alternatives system and the current configuration can be displayed with the following commands:

.. code-block:: bash

    update-alternatives --display iptables
    update-alternatives --display ip6tables
    update-alternatives --display arptables
    update-alternatives --display ebtables


nftables
--------

`nftables <https://www.nftables.org/projects/nftables/index.html>`_ is a successor to the ``iptables`` component in the Linux Netfilter subsystem and was designed to simplify and enhance Linux firewall management.

``nftables`` reduces complexity of ``iptables`` and offers improved performance. The ``nftables`` package provides the ``nft`` utility to natively manage the ``nftables`` component of the Linux Netfilter subsystem. It can also be used to manage rules that would've previously been managed by ``arptables`` and ``ebtables``, while additionally supporting common IPv4 and IPv6 rules.

Starting with Ubuntu 15.04 Vivid Vervet, the ``nftables`` package provides a systemd service unit file that is disabled by default. If enabled, the service unit file will automatically load ``nftables`` configuration from the ``/etc/nftables.conf`` file (a mock file that does not perform any filtering is provided in the ``nftables`` package). You can enable this and load the configuration using the following commands:

.. code-block:: bash

    sudo systemctl enable nftables.service
    sudo systemctl start nftables.service

For more information on configuring nftables, please see the `nft manual page <https://manpages.ubuntu.com/manpages/man8/nft.8.html>`_ and the `nftables documentation <https://wiki.nftables.org/wiki-nftables/index.php/Main_Page>`_.



Further reading
---------------

* `Ubuntu Server documentation - Firewalls <https://documentation.ubuntu.com/server/how-to/security/firewalls/>`_
