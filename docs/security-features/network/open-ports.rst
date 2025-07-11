No Open Ports
=============

A port bound to a service that is actively listening for incoming packets on 
a network is referred to as an "open port". Exposing open ports on untrusted 
networks can pose a security risk if the listening service has a vulnerability 
or is misconfigured.

Historically, Ubuntu adhered to a "No Open Ports" policy, which 
states that default installations of Ubuntu must have no listening network 
services after initial install. Ubuntu continues to adhere as closely as possible 
to this policy, with some exceptions. 

The `"DefaultNetworkServices" policy 
<https://wiki.ubuntu.com/DefaultNetworkServices>`_ provides detailed 
and structured guidelines on when it is acceptable to expose network services 
on default installations of Ubuntu. Based on the DefaultNetworkServices policy, 
any software that accepts packets from the network and is enabled as part of the 
default Ubuntu installation must:

* not expose any application-level data to the network (unless the user explicitly requests it using an understandable interface).

* confine its privileges to limit the impact of any potential arbitrary code execution vulnerabilities.

* be free from problems such as lack of code quality, poor upstream security response processes, and others that would make it difficult to identify and fix security issues in the software.

The network services exposed on default installations are kept to a minimum, and
are generally limited only to services that provide substantial improvement to 
out-of-the-box user experience. Some notable exceptions to the 
"No Open Ports" policy are given below.

Exceptions to the "No Open Ports" Policy
++++++++++++++++++++++++++++++++++++++++

Ubuntu Desktop
--------------

For Ubuntu Desktop systems, exceptions include network infrastructure services
such as a DHCP client and the Avahi mDNS/DNS-SD daemon.

Ubuntu Server
-------------

When installing Ubuntu Server, it is possible to select specific services to 
install beyond the defaults, such as Apache and OpenSSH server.

Ubuntu in the Cloud
-------------------

Ubuntu Cloud Images generally include network infrastructure services 
for the cloud and OpenSSH server configured by the cloud provider to allow the
client to access the machine.

Identifying Open Ports
++++++++++++++++++++++

The ``ss`` utility can be used to identify open ports on a system:

.. code-block:: bash

   ss -utln | grep -vE '127\.0\.0|\[::1\]'

With ``sudo`` permissions, the ``-p`` flag can be used to see which process
is listening on each of the open ports:

.. code-block:: bash

   sudo ss -utlnp | grep -vE '127\.0\.0|\[::1\]'