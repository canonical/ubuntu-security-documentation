Unnecessarily open ports
########################

An "unnecessarily" open port is one exposed to an untrusted network when it
doesn't need to be, or one that belongs to a service no longer in use.

When a host on a network provides a service (such as a web application or SSH
access) to other hosts, it binds the process running the service to a transport
protocol port and one or more of its IP addresses. Other hosts on the network
use this combination of network address and port number to send packets to the
listening service. In these cases, the host providing the services is the
"server", while the other hosts are the "clients". The port the service listens
on is an "open port".

Open ports are the building blocks of network communication. However, since the
listening service might have vulnerabilities, unnecessarily open ports increase
the system's attack surface. Furthermore, threat actors could derive
information from the service's presence. Therefore, it's good practice to limit
the network traffic that can reach open ports (for example, by using a
firewall) and to close any unnecessarily open ports.

Ubuntu ships with minimal open ports by default. You can find more details
about Ubuntu's policy on open ports :doc:`here
<../security-features/network/open-ports>`.


Identifying open ports
======================

Use the ``ss`` utility to identify open ports on a system.

Run the following command to list all open ports for TCP and UDP, the most
commonly used transport protocols for communication over the internet:

.. code-block:: bash

   ss -utln

.. note::
   By default, ``ss`` results show the network namespace of the shell process.
   Use the ``-N`` option to specify a network namespace to examine.

You can filter out loopback addresses to exclude open ports reachable only from the
host itself, particularly if everything running on the host is trusted:

.. code-block:: bash

   ss -utln | grep -vE '127(\.[0-9]+){3}|\[::1\]'

With ``root`` access, use the ``-p`` flag to see which process listens on each
open port:

.. code-block:: bash

   ss -utlnp | grep -vE '127(\.[0-9]+){3}|\[::1\]'

Here is an example of ``ss`` output for a system running three network
services: an Apache web server, an SSH server, and a PostgreSQL database.

Run the command to check non-local ports:

.. code-block:: bash

   sudo ss -utlnp | grep -vE '127(\.[0-9]+){3}|\[::1\]'

The output should look similar to this:

.. code-block:: text

   Netid State  Recv-Q Send-Q           Local Address:Port Peer Address:PortProcess
   udp   UNCONN 0      0       192.168.122.37%enp1s0:68         0.0.0.0:* users:(("systemd-network",pid=418,fd=22))
   udp   UNCONN 0      0         172.16.0.155%enp2s0:68         0.0.0.0:* users:(("systemd-network",pid=418,fd=23))
   tcp   LISTEN 0      4096            192.168.122.37:22         0.0.0.0:* users:(("sshd",pid=935,fd=3),("systemd",pid=1,fd=92))
   tcp   LISTEN 0      511                          *:80               *:* users:(("apache2",pid=822,fd=4),("apache2",pid=821,fd=4),("apache2",pid=820,fd=4))

Now check the local loopback ports:

.. code-block:: bash

   sudo ss -utlnp | grep -E '127(\.[0-9]+){3}|\[::1\]'

.. code-block:: text

   udp   UNCONN 0      0                  127.0.0.54:53         0.0.0.0:* users:(("systemd-resolve",pid=545,fd=16))
   udp   UNCONN 0      0               127.0.0.53%lo:53         0.0.0.0:* users:(("systemd-resolve",pid=545,fd=14))
   tcp   LISTEN 0      4096            127.0.0.53%lo:53         0.0.0.0:* users:(("systemd-resolve",pid=545,fd=15))
   tcp   LISTEN 0      200                 127.0.0.1:5432       0.0.0.0:* users:(("postgres",pid=732,fd=6))
   tcp   LISTEN 0      4096               127.0.0.54:53         0.0.0.0:* users:(("systemd-resolve",pid=545,fd=17))

In this example, the system has two IP addresses: ``192.168.122.37`` and
``172.16.0.155``.

The Apache web server (``apache2``) binds to ``*:80``. This means it listens on
port ``80`` on **all** the system's network addresses.

The SSH server (``sshd``) listens on port ``22`` on only the ``192.168.122.37``
address. Only TCP packets with a destination address of ``192.168.122.37`` and
a destination port of ``22`` pass to the SSH server.

Finally, the PostgreSQL database (``postgres``) binds to ``127.0.0.1:5432``.
``127.0.0.1`` is an example of a "loopback" address. Only other processes
running on the same system can send packets to open ports on these addresses.

The ``ss`` output also shows a DHCP client listening on port ``68`` and a DNS
resolver listening on port ``53``. This is expected behavior, as the DHCP
client obtains IP addresses from the network, while the DNS resolver provides
name resolution for other processes on the system.


Security implications of open ports
===================================

Exposure of system information
------------------------------

Many network services reveal information about the host system. By sending
requests to a network service listening on an open port and analyzing the
response, attackers can potentially determine what software and operating
system runs on the host, as well as their versions.

Although exposing this information isn't inherently a security risk, it helps
threat actors determine which attacks or exploits they can use to target the
system.

Denial-of-service attacks
-------------------------

A denial-of-service attack occurs when a host connected to a network receives
packets in a way that consumes excessive resources, preventing it from
performing other work. Although denial-of-service attacks are possible against
hosts with no open ports, certain types require a listening service on the
victim host.

For example, a SYN flood attack requires the victim host to have an open TCP
port accepting incoming connections, and a Slowloris attack requires the victim
host to have an HTTP server listening on an open port.

.. note::
   All currently supported Ubuntu releases provide protection against SYN flood
   attacks in the form of :doc:`SYN cookies
   <../security-features/network/syn-cookies>`.

Exploit of software vulnerabilities
-----------------------------------

The software listening on an open port might have bugs or security
vulnerabilities. Malicious hosts on the network could send specially-crafted
packets to exploit these vulnerabilities. The impact ranges from software
crashes (leading to a denial of service) to remote code execution.

For example, `Log4Shell
<https://ubuntu.com/security/vulnerabilities/log4shell>`_ is a vulnerability in
a popular Java logging library. If the software bound to an open port uses a
vulnerable version of the library, a malicious host could potentially exploit
the vulnerability to execute arbitrary code on the victim host.

Unauthorized access to services due to misconfiguration
-------------------------------------------------------

A host can have several IP addresses, each with its own set of ports that
services can bind to. These IP addresses may be "public" or "globally routable"
(reachable from the internet), or "private" (reachable only from other hosts on
a private network, such as a LAN or intranet).

Exposing services on public IP addresses, or on private IP addresses when
connected to untrusted networks (such as public Wi-Fi), allows malicious hosts
to access those services.

An example of this is the `Ghostcat
<https://ubuntu.com/security/CVE-2020-1938>`_ vulnerability. Certain versions
of Apache Tomcat configured an AJP listener to bind to port 8009 on all network
addresses by default. Since AJP provides unauthenticated access to read certain
files, this configuration allowed malicious hosts on the same network to obtain
potentially sensitive information.

.. note::
   Apache Tomcat versions shipped in Ubuntu configured the AJP listener as
   "disabled" by default, so they weren't impacted by this vulnerability.


Best practices for open ports
=============================

Disable unnecessary network services
------------------------------------

We strongly advise that you stop any network services that are no longer required and disable them from
running automatically at boot.

If ``systemd`` manages the service, run:

.. code-block:: bash

   sudo systemctl stop <service>
   sudo systemctl disable <service>

.. note::
   A service disabled using ``systemctl disable`` might still start on boot if
   it is a dependency of other enabled services. In these cases, you must
   disable those services as well.

Avoid binding to wildcard or public addresses
---------------------------------------------

Most network services support binding to *wildcard addresses* such as:

* ``0.0.0.0``: The service listens on all IPv4 addresses of the host.
* ``[::]``: The service listens on all IPv6 addresses of the host.
* ``*``: The service listens on all IPv4 and IPv6 addresses of the host.

Many services bind to a wildcard address by default unless configured
otherwise.

Avoid wildcard addresses whenever possible. Configure network services to bind
only to the specific network addresses where they are required. Avoid binding
to public addresses unless the service needs to be accessible from the
internet.

You should bind services that only need exposure to other processes on the same host to a
loopback address.

Use firewalls to control access to open ports
---------------------------------------------

Firewalls are network security tools that monitor and filter network traffic
based on a set of rules. You can configure them to allow or deny traffic based
on criteria such as source IP addresses and port number.

If only certain hosts on a network need access to a service, use a firewall to
block packets from other sources.

See :doc:`here <../security-features/network/firewall/index>` for guidance on
configuring firewalls in Ubuntu.

Keep software up to date
------------------------

To reduce the risk of malicious hosts exploiting vulnerabilities in network
services, apply software updates and security patches regularly.

The Ubuntu Security Team prepares security updates for supported Ubuntu
releases. See :doc:`here <../security-updates/index>` for more information
about the security update process for software in Ubuntu.
