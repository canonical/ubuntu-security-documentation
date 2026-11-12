Dovecot
=======

Dovecot advertises its version in the initial greeting upon client connection. The version
can be removed completely by modifying the message displayed as part of the greeting. As covered
in the :ref:`Version banners may not be precise` section, this could lead to false positives from
network vulnerability management scanners.

Note that the Dovecot package available in Ubuntu is modified to display
``Dovecot (Ubuntu) ready.`` as part of the login greeting and already strips away the version
advertisement.

Disabling the version advertised by Dovecot can be accomplished by changing the ``login_greeting``
option as part of either an existing Dovecot .conf file such as ``/etc/dovecot/dovecot.conf`` or 
``/etc/dovecot/conf.d/10-master.conf``, or by creating a custom override conf file 
``(e.g., /etc/dovecot/conf.d/99-no-banner.conf)`` containing the global login_greeting option:

.. code-block:: console

    echo -e "login_greeting = Dovecot ready." | sudo tee /etc/dovecot/conf.d/99-no-banner.conf
    sudo systemctl reload dovecot.service
