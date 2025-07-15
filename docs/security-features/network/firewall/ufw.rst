ufw - Uncomplicated firewall
============================

`ufw <https://help.ubuntu.com/community/UFW>`_ or `Uncomplicated Firewall` is the default firewall configuration tool for Ubuntu. It acts as a frontend for both ``iptables`` and ``nftables`` and is designed to be a user-friendly tool for creating an IPv4 or IPv6 host-based firewall.

It is important to note that ``ufw`` is disabled by default and is intended to be an easy tool for adding or removing simple rules. For more complex configurations and use-cases, it may be necessary to directly use ``iptables`` or ``nftables``.

Starting with ufw
-----------------

Enable or Disable ufw
~~~~~~~~~~~~~~~~~~~~~
To enable ``ufw`` on your system, run the command:

.. code-block:: bash
    
    sudo ufw enable
    
To disable ``ufw``, use the command:

.. code-block:: bash

    sudo ufw disable

Check ufw Status
~~~~~~~~~~~~~~~~

To see the current status of the firewall, run the command:

.. code-block:: bash

    sudo ufw status
    
For a more detailed status description, run the command:

.. code-block:: bash

    sudo ufw status verbose


ufw Default Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

``ufw`` includes a default set of rules intended to be sufficient protection for the average home user. 

This set of rules follows the standard network security policy of default-deny. 
What this means is that, by default, all incoming traffic is denied and all outgoing traffic is allowed. 
You can confirm this default behaviour by running the ``sudo ufw status verbose`` command after enabling ``ufw`` on your machine.

These rules are stored in the ``*.rules`` files present in ``/etc/ufw``.


Basic ufw Usage
---------------

ufw is used primarily by creating rules which are then applied to the network traffic on your machine. 
There are several different ways to implement rules. This section will cover the simplest usages. 

Crafting ufw Rules
~~~~~~~~~~~~~~~~~~

There are several components to a ufw command line rule:

 - Actions: allow/deny/reject/limit
 - Direction: in/outgoing
 - Protocol: tcp/udp 
 - Port: single port or range
 - IP Address Origin: single address or subnet
 - IP Address Destination: single address or subnet
 - Interface: eth0/etc


Open or Close a Port 
~~~~~~~~~~~~~~~~~~~~

To create a rule that opens a port (SSH in this example):

.. code-block:: bash
    
    sudo ufw allow 22
    
To close an opened port:

.. code-block:: bash

    sudo ufw deny 22

Remove a Rule
~~~~~~~~~~~~~

To remove an existing rule, use the `delete` command followed by the rule:

.. code-block:: bash
    
    sudo ufw remove allow 22


Numbering Rules
~~~~~~~~~~~~~~~

Rules can also be added using a umbered format:

.. code-block:: bash

    sudo ufw insert 1 allow 22

To view the rules in the numbered format:

.. code-block:: bash

    sudo ufw status numbered

Specifying Hosts
~~~~~~~~~~~~~~~~
With ``ufw``, it is possible to allow access only from specific hosts or networks to specific ports, as shown by the following examples.

To allow SSH access from host 192.168.0.2 to any IP address on this host:

.. code-block:: bash

    sudo ufw allow proto tcp from 192.168.0.2 to any port 22

To allow SSH access from the entire subnet:

.. code-block:: bash

        sudo ufw allow proto tcp from 192.168.0.0/24 to any port 22


The --dry-run Option
~~~~~~~~~~~~~~~~~~~~

Adding the --dry-run option to a ufw command will output the resulting rules, but not apply them. For example, the following is what would be applied if opening the HTTP port:

.. code-block:: bash

    sudo ufw --dry-run allow http

    *filter
    :ufw-user-input - [0:0]
    :ufw-user-output - [0:0]
    :ufw-user-forward - [0:0]
    :ufw-user-limit - [0:0]
    :ufw-user-limit-accept - [0:0]
    ### RULES ###

    ### tuple ### allow tcp 80 0.0.0.0/0 any 0.0.0.0/0
    -A ufw-user-input -p tcp --dport 80 -j ACCEPT

    ### END RULES ###
    -A ufw-user-input -j RETURN
    -A ufw-user-output -j RETURN
    -A ufw-user-forward -j RETURN
    -A ufw-user-limit -m limit --limit 3/minute -j LOG --log-prefix "[UFW LIMIT]: "
    -A ufw-user-limit -j REJECT
    -A ufw-user-limit-accept -j ACCEPT
    COMMIT
    Rules updated

Create Custom Rules
-------------------

Rules are primarily split into two different files in :file:`/etc/ufw`:

#. :file:`before.rules` - rules execeuted before ``ufw`` command line rules
#. :file:`after.rules` - rules executed after ``ufw`` command line rules


Application ufw Integration
---------------------------

Applications may include a ``ufw`` profile, located in :file:`/etc/ufw/applications.d`. These profiles detail the ports and protocol necessary for the application to function and can be easily created or edited to appropriately secure local configurations.


IP Masquerading
---------------

The purpose of IP masquerading is to allow machines with private, non-routable IP addresses on your network to access the Internet through the machine doing the masquerading. Traffic from your private network destined for the Internet must be manipulated for replies to be routable back to the machine that made the request.

To do this, the kernel must modify the source IP address of each packet so that replies will be routed back to it, rather than to the private IP address that made the request, which is impossible over the Internet. Linux uses Connection Tracking (conntrack(8)) to keep track of which connections belong to which machines and reroute each return packet accordingly. Traffic leaving your private network is thus “masqueraded” as having originated from your Ubuntu gateway machine. This process is referred to in Microsoft documentation as “Internet Connection Sharing”.

TODO: add masquerading vs SNAT.

IP Masquerading with ufw
~~~~~~~~~~~~~~~~~~~~~~~~

IP masquerading can be achieved using custom ufw rules. This is possible because the current back-end for ufw is iptables-restore with the rules files located in /etc/ufw/*.rules. These files are a great place to add legacy iptables rules used without ufw, and rules that are more network gateway or bridge related.

The rules are split into two different files; rules that should be executed before ufw command line rules, and rules that are executed after ufw command line rules.


Logging
-------

Firewall logs are essential for recognising attacks, troubleshooting your firewall rules, and noticing unusual activity on your network. You must include logging rules in your firewall for them to be generated, though, and logging rules must come before any applicable terminating rule (a rule with a target that decides the fate of the packet, such as ACCEPT, DROP, or REJECT).

If you are using ufw, you can turn on logging by entering the following in a terminal:

.. code-block:: bash

    sudo ufw logging on


Recommended Practices
---------------------

Further Reading
---------------

The `ufw(8) <https://manpages.ubuntu.com/manpages/noble/en/man8/ufw.8.html>`_ man page contains lots of useful information for using ``ufw``.