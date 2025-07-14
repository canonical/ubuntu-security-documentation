No Open Ports
=============

A port bound to a service that is actively listening for incoming packets on 
a network is referred to as an "open port". Exposing open ports on untrusted 
networks can pose a security risk if the listening service has a vulnerability 
or is misconfigured.

Starting with Ubuntu 6.06 LTS Dapper Drake, Ubuntu has adhered to a "No Open Ports" policy, which 
states that, besides certain exceptions, default installations of Ubuntu must 
have no listening network services after initial install.

The `"DefaultNetworkServices" policy 
<https://wiki.ubuntu.com/DefaultNetworkServices>`_ provides detailed 
and structured guidelines on when it is acceptable to expose network services 
on default installations of Ubuntu. Based on this policy, such network services
must:

* not expose any application-level data to the network (unless the user explicitly requests it using an understandable interface).

* confine its privileges to limit the impact of any potential arbitrary code execution vulnerabilities.

* be free from problems that would make it difficult to identify and fix security issues in the software (such as lack of code quality or poor upstream security response processes).

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

These services allow the system to communicate with other devices on a network
with minimal manual configuration. A DHCP client is needed so that the system 
can receive incoming communication from a router to automatically obtain an 
IP address when connecting to a network. An mDNS/DNS-SD daemon is needed 
for device discovery over a network when using ZeroConf technologies.

Ubuntu Server
-------------

When installing Ubuntu Server, it is possible to select specific services to 
install beyond the defaults, such as Apache and OpenSSH server. These services
are often necessary for the server to perform its function (for example, serving websites
to the internet), and so the installer provides an option to include them in the
default installation.

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