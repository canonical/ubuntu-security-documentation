Postfix
=======

Postfix advertises its service name in response to initial SMTP client connections
(specifically in the 220 greeting banner) and may also include its version as part
of the banner. If that is the case, the version can be removed completely. However,
by default as well as on Ubuntu, the version will not be part of the banner. As covered
in the :ref:`Version banners may not be precise` section, this could lead to false
positives from network vulnerability management scanners.

Disabling the version advertised by Postfix can be achieved by setting or modifying the
``smtpd_banner`` option in the main Postfix configuration file (``/etc/postfix/main.cf``):

.. code-block:: console

   sudo postconf -e "smtpd_banner = \$myhostname ESMTP"
   sudo systemctl reload postfix.service
