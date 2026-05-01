OpenSSH Server
==============

The OpenSSH daemon will always advertise at least part of its version to
clients. As such, it is at particular risk of false positives from scanners, as
covered in the :ref:`Version banners may not be precise` section.

Disabling the Ubuntu version can be achieved with the ``DebianBanner``
configuration option:

.. code-block:: console

    echo "DebianBanner no" | sudo tee /etc/ssh/sshd_config.d/no-banner.conf
    sudo systemctl reload ssh.service
