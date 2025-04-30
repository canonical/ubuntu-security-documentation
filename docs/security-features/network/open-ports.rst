No Open Ports
-------------

Default installations of Ubuntu must have no listening network services after initial install. Exceptions to this rule on desktop systems include network infrastructure services such as a DHCP client and mDNS (Avahi/ZeroConf, see `ZeroConfPolicySpec <https://wiki.ubuntu.com/ZeroConfPolicySpec>`_ for implementation details and justification). For Ubuntu in the cloud, exceptions include network infrastructure services for the cloud and OpenSSH running with client public key and port access configured by the cloud provider. When installing Ubuntu Server, the administrator can, of course, select specific services to install beyond the defaults (e.g. Apache).


Testing for this can be done with:

.. code-block:: bash

   netstat -an --inet | grep LISTEN | grep -v 127.0.0.1

on a fresh install.
