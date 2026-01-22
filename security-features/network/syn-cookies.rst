SYN cookies
###########

Before establishing a TCP connection, the client and server must complete the
three-way handshake process. To initiate a connection, the client sends a SYN
packet (step 1), indicating it wants to establish a connection. The server
responds with a SYN/ACK packet (step 2), acknowledging the request. Finally,
the client replies with an ACK packet (step 3), establishing the connection.

A TCP SYN flood is a Denial-of-Service (DoS) attack where a client sends many
SYN packets without completing the third step of the handshake. By not sending
the final ACK packet, the client leaves connections half-open. The server
tracks these half-open connections, eventually filling the connection queue and
preventing legitimate clients from connecting.

SYN cookies help resist TCP SYN flood attacks. They allow the system to respond
to SYN packets with SYN/ACK packets statelessly. The system only constructs the
TCP connection entry upon receipt of the final ACK packet from the client,
avoiding the attack's impact on the queue.

Linux implements this protection in the kernel using the
``net.ipv4.tcp_syncookies`` sysctl parameter. Despite the name, this option
applies to both IPv4 and IPv6.

Configuration values
====================

* ``0``: Disables SYN cookies.
* ``1``: Enables SYN cookies only when the kernel detects a possible SYN flood attack.
* ``2``: Permanently enables SYN cookies.

Since SYN cookies increase the computational load on the server, we recommend
leaving the value at ``1`` unless specific circumstances require otherwise.
Since Ubuntu 9.04 (Jaunty Jackalope), the default value is ``1``.

Run the following command to check the current value:

.. code-block:: bash

   sysctl -n net.ipv4.tcp_syncookies

If needed, you can temporarily disable this parameter with the following
command:

.. code-block:: bash

   sudo sysctl -w net.ipv4.tcp_syncookies=0

To permanently disable this option, create a drop-in file such as
``/etc/sysctl.d/50-syncookies.conf`` containing the following configuration:

.. code-block:: ini
   :caption: /etc/sysctl.d/50-syncookies.conf

   net.ipv4.tcp_syncookies = 0

Considerations
==============

Since SYN cookies encode information in the SYN/ACK packet, using them
increases the computational load on the server, especially with a large number
of incoming connections. While we recommend leaving this option enabled, you
might need to disable SYN cookies in some circumstances. In that case, ensure
you enable other protection mechanisms against SYN flood attacks.

Consider other aspects when using SYN cookies. For example, SYN packets still
reach the system, which may saturate bandwidth. Additionally, the server
won't retransmit the SYN/ACK packet if it doesn't receive the ACK
packet (the third packet in the handshake), which could potentially lead to
hung connections.

For more information, see the `kernel ip-sysctl documentation
<https://www.kernel.org/doc/html/latest/networking/ip-sysctl.html>`_.
