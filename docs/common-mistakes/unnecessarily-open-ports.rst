Unnecessarily open ports
========================
Introduction
++++++++++++
An `unnecessarily` open port is one that is exposed to an untrusted network
when it doesn't need to be, or one that belongs to a service that is no longer
in use.

When a host on a network wishes to provide services (such as a web application
or SSH access) to other hosts on the network, it must bind the process that is
running the service to a port on the corresponding network interface. The
process will then be able to listen for and respond to incoming requests from
other hosts on the network. In these cases, the port that the service listens
on is referred to as an `open port`.

Open ports are essential for allowing hosts to communicate over a network.
However, open ports carry some security risks as they increase the likelihood
of certain types of attacks. Thus, it is important to ensure that ports are
configured correctly and only opened when required.

Ubuntu ships with minimal open ports by default. More details about Ubuntu's
policy on open ports can be found :doc:`here <../security-features/network/open-ports>`.

Identifying open ports
++++++++++++++++++++++

The ``ss`` utility can be used to identify open ports on a system:

.. code-block:: bash

   ss -utln

It is often desirable to exclude ports listening on the loopback interface:

.. code-block:: bash

   ss -utln | grep -vE '127\.0\.0|\[::1\]'

With ``root`` access, the ``-p`` flag can be used to see which process
is listening on each of the open ports:

.. code-block:: bash

   sudo ss -utlnp | grep -vE '127\.0\.0|\[::1\]'

Here is what the output of ``ss`` might look like for a system connected to two
networks and running three network services: an Apache web server, an SSH
server, and a PostgreSQL database.

.. code-block:: bash

   $ sudo ss -utlnp | grep -vE '127\.0\.0|\[::1\]'
   Netid State  Recv-Q Send-Q         Local Address:Port Peer Address:PortProcess                                                
   udp   UNCONN 0      0      192.168.122.37%enp1s0:68        0.0.0.0:*    users:(("systemd-network",pid=421,fd=22))             
   udp   UNCONN 0      0        172.16.0.155%enp2s0:68        0.0.0.0:*    users:(("systemd-network",pid=421,fd=23))             
   tcp   LISTEN 0      4096          192.168.122.37:22        0.0.0.0:*    users:(("sshd",pid=852,fd=3),("systemd",pid=1,fd=140))
   tcp   LISTEN 0      511                        *:80              *:*    users:(("apache2",pid=2053,fd=3),("apache2",pid=2052,fd=3),("apache2",pid=2050,fd=3))
   $ sudo ss -utlnp | grep postgres
   tcp   LISTEN 0      200                127.0.0.1:5432      0.0.0.0:*    users:(("postgres",pid=5157,fd=6))                    

In this example, the system is using the IP address ``192.168.122.37`` on one
network and ``172.16.0.155`` on the other. 

The Apache web server (``apache2``) is bound to ``*:80``. This means that
it is listening on port ``80`` on **all** of the system's network interfaces.
Hosts on either of the two networks can send packets to the Apache web server via
port ``80``.

On the other hand, the SSH server (``sshd``) is listening on port ``22`` of only
the ``192.168.122.37`` network interface, and so only hosts on that network can
send packets to the SSH server.

Finally, the PostgreSQL database (``postgres``) is bound to ``127.0.0.1:5432``.
Since this is an address on the system's loopback interface, only
other processes running on the same system can send packets to the PostgreSQL database
via this open port.

The ``ss`` output also shows a DHCP client listening on ``192.168.122.37:68``
and ``172.16.0.155:68``. This is expected behavior, as the system uses this
port to obtain its IP address from the network.

Security implications of open ports
+++++++++++++++++++++++++++++++++++
Denial-of-service attacks
-------------------------
An open port allows a host to receive packets from other hosts on a network.
However, if any of these hosts are malicious, they could send packets
in a way that consumes excessive resources on the host and prevents it from
servicing legitimate requests or performing other work.

For example, if there are multiple malicious hosts on the network, they can be
used to simultaneously flood the victim host with packets. This is
known as a distributed denial-of-service (DDoS) attack.

Other types of denial-of-service attacks include Slowloris and SYN flood attacks,
which exploit certain weaknesses in network protocols.

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

Exposure of privileged services or sensitive information
--------------------------------------------------------
Systems may be connected to several different networks, each with its own set
of ports that services can be bound to. Some networks may be more trusted than
others. For example, a server may be connected to both an organization's private
intranet (generally more trusted) and the public Internet (generally less trusted).
In this case, the server may not want to bind certain services (such as those
exposing sensitive information or privileged functionality) to a port on its public
Internet-facing network interface, since doing so may lead to unauthorized
access of those services.

An example of this is given by the `Ghostcat <https://ubuntu.com/security/CVE-2020-1938>`_
vulnerability. Certain versions of Apache Tomcat were configured to have an AJP
listener that would bind to port 8009 on all the network interfaces of the host
by default (including any Internet-facing or untrusted networks). Since AJP
provides unauthenticated access to read certain files on the host, this configuration
could allow a malicious host on the network to obtain potentially sensitive
information by sending requests to the AJP port.

.. note::
   Apache Tomcat versions shipped in Ubuntu were configured with the AJP
   listener `disabled` by default, and were therefore not impacted by this
   particular vulnerability.

Best practices for open ports
+++++++++++++++++++++++++++++
Disable unnecessary network services
------------------------------------
Any network services that are no longer required should be stopped and disabled
from running automatically on boot.

If the service is managed by ``systemd``, this can be done by running:

.. code-block:: bash

   sudo systemctl stop <service>
   sudo systemctl disable <service>

Limit open ports to the required network interfaces
---------------------------------------------------
Most network services support binding to *wildcard addresses* such as:

* ``0.0.0.0``: the service listens on all IPv4 network interfaces of the host
* ``[::]``: the service listens on all IPv6 network interfaces of the host
* ``*``: the service listens on all network interfaces of the host

Unless configured otherwise, many services will bind to a wildcard address by
default.

Whenever possible, wildcard addresses should be avoided, and network services
should be configured to bind only to the specific network interfaces where they
are required. This helps prevent unintentionally exposing the services to
untrusted networks or the Internet.

Use firewalls to control access to open ports
---------------------------------------------
Firewalls are network security tools that monitor and filter network traffic
based on a set of rules. They can be configured to allow or deny traffic based
on various criteria, such as the source IP addresses and port number.

If only certain hosts on a network need access to a service, a firewall should
be used to block packets from other sources from reaching the open port.

Firewall rules on Ubuntu can be configured using ``iptables``, ``nftables``, or
``ufw``. Additional guidance on configuring firewalls in Ubuntu can be found here
:doc:`here <../security-features/network/firewall/index>`.

Keep software up to date
------------------------
To prevent malicious hosts from exploiting vulnerabilities in network services,
software updates and security patches should be applied regularly.

The Ubuntu Security Team prepares security updates for supported Ubuntu releases.
More information about the security update process for software in Ubuntu can
be found :doc:`here <../security-updates/index>`.