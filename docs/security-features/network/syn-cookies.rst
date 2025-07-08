SYN Cookies
-----------

One of the techniques to resist SYN flood attacks is called SYN cookies, which allow for reconstructing the SYN queue entries without needing to process subsequent queries, avoiding the attack.

On Linux, this protection is implemented in the kernel using the ``net.ipv4.tcp_syncookies`` parameter. Despite the name, this option applies to both IPv4 and IPv6.

When the parameter is set to ``1``, SYN cookies will be enabled if the kernel detects a possible SYN flood attack. ``0`` will disable this behavior, while ``2`` will leave SYN cookies permanently enabled. As SYN cookies increase the computational load on the server, it is generally recommended to leave it at ``1`` unless some circumstance would require setting it to another value. By default, the parameter's value is ``1`` on Ubuntu, since the Ubuntu 9.04 release.

The following command shows the value of the parameter:

.. code-block:: shell

    sudo sysctl -n net.ipv4.tcp_syncookies

If needed, this parameter can be disabled with the following command:

.. code-block:: shell

    sudo sysctl -w net.ipv4.tcp_syncookies=0

In order to permanently disable this option, the ``/etc/sysctl.conf`` file has to be edited, with the following configuration option added:

.. code-block::
    :caption: /etc/sysctl.conf

    net.ipv4.tcp_syncookies = 0

As SYN cookies involve encrypting responses, their usage increases the computational load on the server, especially with large incoming number of connections. While it is recommended to leave this option enabled, in some circumstances it may be necessary to disable SYN cookies, in which case other protection mechanisms against SYN flood attacks should be enabled, such as firewall configurations, rate limiting, etc.

More information about the kernel option is available on the `kernel ip-sysctl documentation page <https://www.kernel.org/doc/html/latest/networking/ip-sysctl.html>`_.
