No Open Ports
=============

A port bound to a service that is actively listening for incoming packets on 
a network is referred to as an "open port". Exposing open ports on untrusted 
networks can pose a security risk if the listening service has a vulnerability 
or is misconfigured.

Starting with Ubuntu 6.06 LTS Dapper Drake, Ubuntu has adhered to a "No Open Ports" policy, which 
states that, besides certain exceptions, default installations of Ubuntu must 
have no listening network services after initial install.

Guidelines for Default Network Services
+++++++++++++++++++++++++++++++++++++++

While the network services exposed on default Ubuntu installations are kept to 
a minimum, some exceptions have been permitted. These are generally limited only
to services that provide substantial improvement to out-of-the-box user experience.

All such network services must adhere to the following guidelines:

Exposing local information to the network
-----------------------------------------

* A default Ubuntu installation must not expose any application-level data to 
  the network (unless the user explicitly requests it using an understandable interface). 
  
  * It is legitimate to expose global machine information on the IP network level,
    such as the network controller's MAC address, IP address, local host name, 
    and availability of network-facing services. For example, a DHCP client will
    broadcast the device's MAC address over the network during DHCP discovery.

  * *Note:* Packages which are **not** part of the default installation can automatically expose 
    application-level data to the network, since the user must explicitly install them.

* Package or distribution upgrades must not expose any information which was 
  previously unexposed.

Detecting and using remote services
-----------------------------------

* The default Ubuntu Desktop installation can automatically detect services 
  offered by other computers in the network and present them to the user (for
  example, via the Avahi mDNS/DNS-SD daemon). As these services are 
  untrustworthy and potentially dangerous, applications that can use the 
  detected services must:

  * Always clearly separate local (or locally configured) trustworthy services 
    from automatically detected remote services.
  
  * Never automatically communicate with detected services without an explicit 
    user request.
    
  * Offer a discoverable way to disable the presentation and usage of 
    autodetected remote services. 

* The default Ubuntu Server installation must not detect any services offered 
  by other computers in the network.

Additional security considerations
----------------------------------

* A process that is part of the default Ubuntu installation and accepts any 
  packets from the network must confine its privileges in a way that a potential 
  arbitrary code execution vulnerability in the process cannot access any user's 
  data nor any other system processes. This generally means that the process must
  be run under a system user ID, perhaps with some additional 
  non-root-equivalent group memberships.

* There may be other security problems with software which offers services to the 
  network, such as complexity, lack of code quality or poor upstream security 
  response processes. These problems make it more difficult to identify and fix 
  security issues, and so programs with these kinds of problems should not be 
  enabled by default.

Sign-off process
---------------

* Each piece of software which, in the default install, listens on or is advertised 
  to the network, must be approved by the Ubuntu Technical Board and a member of 
  the Ubuntu core developers' security team.

Exceptions to the "No Open Ports" Policy
++++++++++++++++++++++++++++++++++++++++

Some notable exceptions to the "No Open Ports" policy are given below.

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