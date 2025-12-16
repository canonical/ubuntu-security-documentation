No open ports
=============

An "open port" is a network port bound to a service and actively listening for
incoming connections or packets.

Exposing open ports on untrusted networks poses a security risk if the
listening service has a vulnerability or is misconfigured.

Since Ubuntu 6.06 LTS (Dapper Drake), Ubuntu has followed a "No Open Ports"
policy. By default, a new installation has no listening network services, with
only rare exceptions.

Guidelines for network services exposed by default
++++++++++++++++++++++++++++++++++++++++++++++++++

While default Ubuntu installations keep exposed network services to a minimum, we
allow some exceptions. These are limited to services that substantially improve
the out-of-the-box user experience.

All such network services must comply with the following guidelines.

Expose local information to the network
---------------------------------------

A default Ubuntu installation must not expose any application-level data to the
network unless the user explicitly requests it using a clear and understandable
interface.

.. note::
   Packages not included in the default installation may automatically expose
   application-level data to the network, as their installation requires
   explicit user action.

Automatically exposing global machine information at the IP network level is
acceptable. This includes the network controller's MAC address, IP address,
local hostname, and availability of network-facing services. For example, a
DHCP client broadcasts the device's MAC address during DHCP discovery.

Package or distribution upgrades must not expose any information not previously
exposed.

Detect and use remote services
------------------------------

The default Ubuntu Desktop installation automatically detects services offered
by other computers on the network and presents them to the user (for example,
via the Avahi mDNS/DNS-SD daemon). Because these services might be
untrustworthy or potentially dangerous, applications that use detected services
must:

* Always clearly separate local (or locally configured) trustworthy services
  from automatically detected remote services.
* Never automatically communicate with detected services without an explicit
  user request.
* Offer a discoverable way to disable the presentation and usage of
  autodetected remote services.

The default Ubuntu Server installation must not detect any services offered by
other computers in the network.

Additional security considerations
----------------------------------

A process included in the default Ubuntu installation that accepts network
packets must be privilege-confined. Any potential arbitrary code execution
vulnerability in the process shouldn't be able to access user data or other
system processes. Typically, this means running the process under a system user
ID, possibly with restricted group memberships that don't grant root-equivalent
privileges.

Software that offers network services may have other security problems, such as
complexity, poor code quality, or inadequate upstream security response
processes. These issues make identifying and fixing vulnerabilities more
difficult. Therefore, we don't enable programs with such problems by default.

Sign-off process
----------------

The Ubuntu Technical Board and a member of the Ubuntu core developers' security
team must approve any software that listens on or is advertised to the network
in the default installation.

Exceptions to the "No Open Ports" policy
++++++++++++++++++++++++++++++++++++++++

Notable exceptions to the "No Open Ports" policy include:

Ubuntu Desktop
--------------

Exceptions for Ubuntu Desktop systems include network infrastructure services
such as a DHCP client and the Avahi mDNS/DNS-SD daemon.

These services allow the system to communicate with other devices on a network
with minimal manual configuration. The system needs a DHCP client to receive
incoming communication from a router to automatically obtain an IP address when
connecting to a network. An mDNS/DNS-SD daemon is needed for device discovery
over a network when using ZeroConf technologies.

Ubuntu Server
-------------

When installing Ubuntu Server, you can select specific services to install
beyond the defaults, such as Apache HTTP Server and OpenSSH server. These
services are often necessary for the server to perform its function (for
example, serving websites to the internet), so the installer provides an option
to include them in the default installation.

Ubuntu Cloud Images
-------------------

`Ubuntu Cloud Images <https://cloud-images.ubuntu.com/>`_ generally include
network infrastructure services for the cloud and OpenSSH server configured by
the cloud provider to allow the client to access the machine.

Identifying open ports
++++++++++++++++++++++

Use the ``ss`` utility to identify open ports on a system:

.. code-block:: bash

   ss -utln | grep -vE '127\.0\.0|\[::1\]'

With ``sudo`` permissions, use the ``-p`` flag to see which process is
listening on each of the open ports:

.. code-block:: bash

   sudo ss -utlnp | grep -vE '127\.0\.0|\[::1\]'
