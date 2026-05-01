Nginx
=====

Nginx advertises its version in the ``Server`` header of responses. The version
can be removed completely. As covered in the :ref:`Version banners may not be
precise` section, this could lead to false positives from network vulnerability
management scanners.

Disabling the version advertised by nginx can be achieved with the
``server_tokens`` directive:

.. code-block:: console

    echo "server_tokens off;" | sudo tee /etc/nginx/conf.d/no-banner.conf
    sudo systemctl reload nginx.service
