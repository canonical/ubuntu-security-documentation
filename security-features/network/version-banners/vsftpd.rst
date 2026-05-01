vsftpd
=======

vsftpd advertises its version as part of its FTP communication. The version can
be removed completely. As covered in the :ref:`Version banners may not be
precise` section, this could lead to false positives from network vulnerability
management scanners.

Disabling the version advertised by vsftpd can be achieved with the
``ftpd_banner`` directive:

.. code-block:: console

    echo "ftpd_banner=FTP server" | sudo tee -a /etc/vsftpd.conf
    sudo systemctl reload vsftpd.service

Please note that this modifies the configuration file distributed by the
package, which could interfere with subsequent :ref:`unattended upgrades
<Automatic security updates>`.
