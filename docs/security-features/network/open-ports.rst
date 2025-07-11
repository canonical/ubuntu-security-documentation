No Open Ports
=============

A port bound to a service that is actively listening for incoming packets on 
a network is referred to as an "open port". Exposing open ports on untrusted 
networks can pose a security risk if the service has a vulnerability or is 
misconfigured.

The ``ss`` utility can be used to identify open ports on a system:

.. code-block:: bash

   ss -utln | grep -vE '127\.0\.0|\[::1\]'

With ``sudo`` permissions, the ``-p`` flag can be passed to see which process
is listening on each of the open ports:

.. code-block:: bash

   sudo ss -utlnp | grep -vE '127\.0\.0|\[::1\]'

Historically, Ubuntu adhered to an informal "No Open Ports" policy, which 
states that default installations of Ubuntu must have no listening network 
services after initial install. However, as exceptions had to be made for certain
services that greatly improved the out-of-the-box user experience, this policy was 
ultimately superseded by the `"DefaultNetworkServices" policy 
<https://wiki.ubuntu.com/DefaultNetworkServices>`_, which provides detailed 
and structured guidelines on what network services can be enabled by default on 
Ubuntu.

Based on the DefaultNetworkServices policy, any software that accepts packets 
from the network and is enabled as part of the default Ubuntu installation must:

* not expose any application-level data to the network (unless the user explicitly requests it using an understandable interface).

* confine its privileges to limit the impact of any potential arbitrary code execution vulnerabilities.

* be free from problems such as lack of code quality, poor upstream security response processes, and others that would make it difficult to identify and fix security issues in the software.

Ubuntu still adheres as closely as possible to the "No Open Ports" policy
by keeping the number of network services exposed on default installations to a
minimum. Some notable exceptions to the policy are described below.

Exceptions to the "No Open Ports" Policy
++++++++++++++++++++++++++++++++++++++++

Ubuntu Desktop
--------------

For Ubuntu Desktop systems, exceptions include network infrastructure services
such as a DHCP client and the Avahi mDNS/DNS-SD daemon.

Ubuntu Server
-------------

When installing Ubuntu Server, it is possible to select specific services to 
install beyond the defaults, including Apache and OpenSSH server.

Ubuntu in the Cloud
-------------------

Ubuntu Cloud Images generally include network infrastructure services 
for the cloud and OpenSSH server configured by the cloud provider to allow the
client to access the machine.