Apache2
=======

Apache2 advertises its version in the ``Server`` header of responses, as well as
in directory listings. The version can be removed completely. As covered in the
:ref:`Version banners may not be precise` section, this could lead to false
positives from network vulnerability management scanners.

Disabling the version advertised by apache2 can be achieved with the
``ServerTokens`` and ``ServerSignature`` directives, for the ``Server`` header
and the directory listings, respectively:

.. code-block:: console

    echo "ServerTokens Prod" | sudo tee /etc/apache2/conf-available/zz-no-banner.conf
    echo "ServerSignature Off" | sudo tee -a /etc/apache2/conf-available/zz-no-banner.conf
    sudo a2enconf zz-no-tokens.conf
    sudo systemctl reload apache2.service
