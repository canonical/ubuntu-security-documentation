SYN Cookies
-----------

Before establishing a TCP connection, the client and the server have to go through the 3-way-handshake process. In order to initiate a connection, the client sends a SYN packet (first step), indicating the client would like to establish a connection with the server. The server then responds with a SYN/ACK packet (second step), indicating the acknowledgment from the server. Once the client replies with an ACK packet (third step), the connection is established.

The TCP SYN flood is a denial of service attack in which a client sends many SYN packets without completing the 3-way-handshake with the third step, by not sending an ACK packet to the server after receiving the SYN/ACK packet. The server keeps track of all the half-open connections that are being initiated, and if these connections are not finalized, they will fill up the connection queue, after which no client will be able to connect to the server.

One of the techniques to resist TCP SYN flood attacks is called SYN cookies, which allow a system to respond to SYN packets with SYN/ACK packets statelessly and only construct the TCP connection entry state on receipt of the third TCP 3-way-handshake packet, the ACK packet from the client, thus avoiding the attack.

On Linux, this protection is implemented in the kernel using the ``net.ipv4.tcp_syncookies`` sysctl parameter. Despite the name, this option applies to both IPv4 and IPv6.

When the parameter is set to ``1``, SYN cookies will be enabled if the kernel detects a possible SYN flood attack. ``0`` will disable this behavior, while ``2`` will leave SYN cookies permanently enabled. As SYN cookies increase the computational load on the server, it is generally recommended to leave it at ``1`` unless some circumstance would require setting it to another value. By default, the parameter's value is ``1`` on Ubuntu, since the Ubuntu 9.04 release.

The following command shows the value of the parameter:

.. code-block:: shell

    sysctl -n net.ipv4.tcp_syncookies

If needed, this parameter can be temporarily disabled with the following command:

.. code-block:: shell

    sudo sysctl -w net.ipv4.tcp_syncookies=0

In order to permanently disable this option, a drop-in file like  ``/etc/sysctl.d/50-syncookies.conf`` has to be used, with the following configuration option in the file:

.. code-block::
    :caption: /etc/sysctl.d/50-syncookies.conf

    net.ipv4.tcp_syncookies = 0

As SYN cookies involve encoding of information in the SYN/ACK packet, their usage increases the computational load on the server, especially with large incoming number of connections. While it is recommended to leave this option enabled, in some circumstances it may be necessary to disable SYN cookies, in which case other protection mechanisms against SYN flood attacks should be enabled.

Other aspects have to be considered as well with SYN cookies. For example, SYN packets still reach the system, which may have implications with bandwidth saturation. Additionally, the SYN/ACK packet is not retransmitted if the server does not receive the ACK packet (3rd packet in the three-way handshake), which could potentially lead to hung connections.

More information about the kernel option is available on the `kernel ip-sysctl documentation page <https://www.kernel.org/doc/html/latest/networking/ip-sysctl.html>`_.
