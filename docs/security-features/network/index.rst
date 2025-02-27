Network and firewalls
=====================

No Open Ports
-------------

Default installations of Ubuntu must have no listening network services after initial install. Exceptions to this rule on desktop systems include network infrastructure services such as a DHCP client and mDNS (Avahi/ZeroConf, see `ZeroConfPolicySpec <https://wiki.ubuntu.com/ZeroConfPolicySpec>_` for implementation details and justification). For Ubuntu in the cloud, exceptions include network infrastructure services for the cloud and OpenSSH running with client public key and port access configured by the cloud provider. When installing Ubuntu Server, the administrator can, of course, select specific services to install beyond the defaults (e.g. Apache).


Testing for this can be done with:

.. code-block:: bash

   netstat -an --inet | grep LISTEN | grep -v 127.0.0.1

on a fresh install.


SYN Cookies
-----------
When a system is overwhelmed by new network connections, SYN cookie use is activated to help mitigate SYN-flood attacks.


Configurable Firewall
---------------------
`ufw <https://help.ubuntu.com/community/UFW>`_ is a frontend for iptables and is installed by default in Ubuntu (users must explicitly enable it). 

Ufw is well-suited for host-based firewalls, providing a framework for managing a netfilter firewall, as well as a command-line interface for firewall manipulation. It simplifies complex iptables commands while still offering advanced controls for experienced users. 

Regression tests: `ufw tests <https://bazaar.launchpad.net/~jdstrand/ufw/trunk/files>`_.

For in-depth information about how firewall works in Ubuntu, see :ref:`Firewall`

.. toctree::
   :maxdepth: 2
   
   firewall