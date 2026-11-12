BIND 9
=======

BIND 9 advertises its version in response to CHAOS class queries (specifically CH TXT
version.bind queries). The version can be removed completely. As covered in the
:ref:`Version banners may not be precise` section, this could lead to false positives
from network vulnerability management scanners.

Disabling the version advertised by BIND 9 can be achieved via the ``version``
option as part of the global options block of the ``named.conf.options`` file
(``/etc/bind/named.conf.options``):

.. code-block:: text

    options {
        /* ... existing options ... */

        version none;
    };

Once the ``named.conf.options`` file has been updated, reload the BIND 9 service to apply
the changes.

.. code-block:: text

    sudo systemctl reload bind9.service
