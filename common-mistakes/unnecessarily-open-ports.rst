Unnecessarily open ports
========================
Introduction
++++++++++++
An `unnecessarily` open port is one that is exposed to an untrusted network
when it doesn't need to be, or one that belongs to a service that is no longer
in use.

When a host on a network wishes to provide a service (such as a web application
or SSH access) to other hosts on the network, it must bind the process that is
running the service to a transport protocol port and one or more of its IP
addresses. Other hosts on the network can then use this combination of the
chosen network address and port number to send packets to the listening service.
In these cases, the host that provides the services is known as the `server`,
while the other hosts are the `clients`. The port that the service listens on
is referred to as an `open port`.

Open ports are the very building blocks of network communication. However, since
the listening service might have vulnerabilities, unnecessarily open ports
increase the attack surface of the system. Furthermore, threat actors could derive
information from the very presence of the service. Therefore, it is considered
good practice to limit the network traffic that can reach open ports (for example,
by using a firewall) and to close any unnecessarily open ports.

Ubuntu ships with minimal open ports by default. More details about Ubuntu's
policy on open ports can be found :doc:`here <../security-features/network/open-ports>`.

Identifying open ports
++++++++++++++++++++++

The ``ss`` utility can be used to identify open ports on a system.

The following command lists all open ports for TCP and UDP, which are the most
commonly used transport protocols for communication over the Internet:

.. code-block:: bash

   ss -utln

.. note::
   By default, the results from ``ss`` will be for the network namespace of the
   shell process. The ``-N`` option can be used to specify a specific network
   namespace to examine with ``ss``.

It is often desirable to exclude open ports that are only reachable from the
host itself, particularly if everything running on the host is assumed to be
trusted. This is done by filtering out loopback addresses:

.. code-block:: bash

   ss -utln | grep -vE '127(\.[0-9]+){3}|\[::1\]'

With ``root`` access, the ``-p`` flag can be used to see which process
is listening on each of the open ports:

.. code-block:: bash

   ss -utlnp | grep -vE '127(\.[0-9]+){3}|\[::1\]'

Here is what the output of ``ss`` might look like for a system running three
network services: an Apache web server, an SSH server, and a PostgreSQL database.

.. code-block:: bash

   $ sudo ss -utlnp | grep -vE '127(\.[0-9]+){3}|\[::1\]'
   Netid State  Recv-Q Send-Q          Local Address:Port Peer Address:PortProcess
   udp   UNCONN 0      0       192.168.122.37%enp1s0:68        0.0.0.0:*    users:(("systemd-network",pid=418,fd=22))
   udp   UNCONN 0      0         172.16.0.155%enp2s0:68        0.0.0.0:*    users:(("systemd-network",pid=418,fd=23))
   tcp   LISTEN 0      4096           192.168.122.37:22        0.0.0.0:*    users:(("sshd",pid=935,fd=3),("systemd",pid=1,fd=92))
   tcp   LISTEN 0      511                         *:80              *:*    users:(("apache2",pid=822,fd=4),("apache2",pid=821,fd=4),("apache2",pid=820,fd=4))

   $ sudo ss -utlnp | grep -E '127(\.[0-9]+){3}|\[::1\]'
   udp   UNCONN 0      0                  127.0.0.54:53        0.0.0.0:*    users:(("systemd-resolve",pid=545,fd=16))
   udp   UNCONN 0      0               127.0.0.53%lo:53        0.0.0.0:*    users:(("systemd-resolve",pid=545,fd=14))
   tcp   LISTEN 0      4096            127.0.0.53%lo:53        0.0.0.0:*    users:(("systemd-resolve",pid=545,fd=15))
   tcp   LISTEN 0      200                 127.0.0.1:5432      0.0.0.0:*    users:(("postgres",pid=732,fd=6))
   tcp   LISTEN 0      4096               127.0.0.54:53        0.0.0.0:*    users:(("systemd-resolve",pid=545,fd=17))

In this example, the system has been assigned two IP addresses: ``192.168.122.37`` 
and ``172.16.0.155``.

The Apache web server (``apache2``) is bound to ``*:80``. This means that
it is listening on port ``80`` on **all** of the system's network addresses.

On the other hand, the SSH server (``sshd``) is listening on port ``22`` on only
the ``192.168.122.37`` address. Only TCP packets with a destination address of
``192.168.122.37`` and a destination port of ``22`` will be passed to the SSH
server.

Finally, the PostgreSQL database (``postgres``) is bound to ``127.0.0.1:5432``.
``127.0.0.1`` is an example of a `loopback` address. Only other processes running
on the same system can send packets to open ports on these addresses.

The ``ss`` output also shows a DHCP client listening on port ``68`` and a DNS
resolver listening on port ``53``. This is expected behaviour, as the DHCP
client is used by the system to obtain its IP addresses from the network, while
the DNS resolver provides name resolution for other processes on the system.

Security implications of open ports
+++++++++++++++++++++++++++++++++++
Exposure of system information
------------------------------
Many network services reveal certain information about the host system. By
sending requests to a network service listening on an open port and analyzing
the response, it may be possible to determine what software and operating system
is running on the host, as well as their versions.

Although the exposure of this information is not inherently a security risk,
it could help a threat actor determine which attacks or exploits can be
used to target the system.

Denial-of-service attacks
-------------------------
A denial-of-service attack occurs when a host connected to a network receives
packets in a way that consumes excessive resources on the host and prevents it
from performing other work. Although it is possible to conduct a denial-of-service
attack against a host with no open ports, certain types of denial-of-service
attacks require a listening service on the victim host.

For example, a SYN flood attack requires the victim host to have an open TCP
port accepting incoming connections, and a Slowloris attack requires the victim
host to have an HTTP server listening on an open port.

.. note::
   All currently supported Ubuntu releases provide some protection against SYN
   flood attacks in the form of :doc:`SYN cookies <../security-features/network/syn-cookies>`.

Exploit of software vulnerabilities
-----------------------------------
The software that listens on an open port may have bugs or security 
vulnerabilities. Malicious hosts on the network could send specially-crafted 
packets to exploit these vulnerabilities. The impact of these exploits
could range from the software crashing (leading to a denial of service) to 
remote code execution.

For example, `Log4Shell <https://ubuntu.com/security/vulnerabilities/log4shell>`_
is a vulnerability in a popular logging library. If the software bound to an
open port is using a vulnerable version of the library, a malicious host
could potentially exploit the vulnerability to execute arbitrary code on the
victim host.

Unauthorized access to services due to misconfiguration
-------------------------------------------------------
A host can have several IP addresses, each with its own set of ports that
services can be bound to. These IP addresses may be `public` or `globally
routable`, which means that they can be reached from the Internet, or they may
be `private`, which means that they can only be reached from other hosts on
a private network (such as a local area network or an organization's private
intranet).

Exposing services on public IP addresses, or on private IP addresses when
connected to untrusted networks (such as public Wi-Fi networks) could allow
malicious hosts to access those services.

An example of this is given by the `Ghostcat <https://ubuntu.com/security/CVE-2020-1938>`_
vulnerability. Certain versions of Apache Tomcat were configured to have an AJP
listener that would bind to port 8009 on all the network addresses of the host
by default. Since AJP provides unauthenticated access to read certain files on
the host, this configuration could allow a malicious host on the same network to
obtain potentially sensitive information by sending requests to the open AJP port.

.. note::
   Apache Tomcat versions shipped in Ubuntu were configured with the AJP
   listener `disabled` by default, and were therefore not impacted by this
   particular vulnerability.

Best practices for open ports
+++++++++++++++++++++++++++++
Disable unnecessary network services
------------------------------------
Any network services that are no longer required should be stopped and disabled
from running automatically when the system boots up.

If the service is managed by ``systemd``, this can be done by running:

.. code-block:: bash

   sudo systemctl stop <service>
   sudo systemctl disable <service>

.. note::
   A service disabled using the ``systemctl disable`` command may still start
   on boot if it is a dependency of other enabled services. In these cases,
   to truly prevent the service from running on boot, those service must be
   disabled as well.

Avoid binding to wildcard or public addresses
---------------------------------------------
Most network services support binding to *wildcard addresses* such as:

* ``0.0.0.0``: the service listens on all IPv4 addresses of the host
* ``[::]``: the service listens on all IPv6 addresses of the host
* ``*``: the service listens on all IPv4 and IPv6 addresses of the host

Many services will bind to a wildcard address by default, unless configured
otherwise.

Whenever possible, wildcard addresses should be avoided, and network services
should be configured to bind only to the specific network addresses where they
are required. Binding to public addresses should be avoided unless
the service needs to be accessible from the Internet.

Services that only need to be exposed to other processes on the same host
should bind to a loopback address.

Use firewalls to control access to open ports
---------------------------------------------
Firewalls are network security tools that monitor and filter network traffic
based on a set of rules. They can be configured to allow or deny traffic based
on various criteria, such as the source IP addresses and port number.

If only certain hosts on a network need access to a service, a firewall should
be used to block packets from other sources from reaching the open port.

Guidance on configuring firewalls in Ubuntu can be found
:doc:`here <../security-features/network/firewall/index>`.

Keep software up to date
------------------------
To reduce the risk of malicious hosts exploiting vulnerabilities in network
services, software updates and security patches should be applied regularly.

The Ubuntu Security Team prepares security updates for supported Ubuntu releases.
More information about the security update process for software in Ubuntu can
be found :doc:`here <../security-updates/index>`.