NSD
=====

NSD advertises its version in response to CHAOS class queries (specifically CH TXT
version.server and version.bind queries). The version can be removed completely. As
covered in the :ref:`Version banners may not be precise` section, this could lead to
false positives from network vulnerability management scanners.

Disabling the version advertised by NSD can be achieved via the
``hide-version`` option as part of a ``server`` block in an nsd.conf file:

.. code-block:: console

    echo -e "server:\n  hide-version: yes" | sudo tee /etc/nsd/nsd.conf.d/no-banner.conf
    sudo systemctl restart nsd.service

In order for the ``no-banner.conf`` file above to be used, the following must be
specified in the main ``/etc/nsd/nsd.conf`` file:

.. code-block:: text

   include: "/etc/nsd/nsd.conf.d/*.conf"

Otherwise, the ``hide-version: yes`` configuration must be specified in a ``server`` block
within your main conf file.
