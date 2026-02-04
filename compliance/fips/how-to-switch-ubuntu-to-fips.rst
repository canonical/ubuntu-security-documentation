Enable FIPS mode on Ubuntu
##########################

FIPS requires an Ubuntu Pro token. You can get one `here
<https://ubuntu.com/pro/subscribe>`_. Ubuntu Pro is available for free for up
to 5 machines and only requires an email address to sign up.

.. code-block:: bash

   sudo apt update && sudo apt -y upgrade
   sudo pro attach <token>
   sudo pro enable fips-updates
