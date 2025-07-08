SYN Cookies
-----------

One of the techniques to resist SYN flood attacks is called SYN cookies, which allow for reconstructing the SYN queue entries without needing to process subsequent queries, avoiding the attack.

On Linux, this protection is implemented in the kernel using the ``net.ipv4.tcp_syncookies`` parameter. This parameter is enabled by default on Ubuntu. Despite the name, this option applies to both IPv4 and IPv6.

The following command shows whether the parameter is enabled or not, with ``1`` meaning it is enabled and ``0`` if not:

.. code-block:: shell

    sudo sysctl -n net.ipv4.tcp_syncookies

If needed, this parameter can be disabled with the following command:

.. code-block:: shell

    sudo sysctl -w net.ipv4.tcp_syncookies=0

In order to permanently disable this option, the ``/etc/sysctl.conf`` file has to be edited, with the following configuration option added:

.. code-block::
    :caption: /etc/sysctl.conf

    net.ipv4.tcp_syncookies = 0

SYN cookies involve encrypting responses, and therefore as a drawback, they increase the computational load on the server. The usage of SYN cookies can therefore be problematic on servers with a very high load due to a large number of incoming connections, and it can be useful to disable the option in these circumstances and use another form of protection instead.

More information about the kernel option is available on the `kernel ip-sysctl documentation page <https://www.kernel.org/doc/html/latest/networking/ip-sysctl.html>`_.
