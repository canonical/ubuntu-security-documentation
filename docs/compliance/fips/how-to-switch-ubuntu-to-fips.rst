How to switch Ubuntu to FIPS mode
=================================

FIPS requires an Ubuntu Pro token, which you can get `here <https://ubuntu.com/pro/subscribe>`_ - Ubuntu Pro is available for free for up to 5 machines and only requires an email address to sign up.

.. code-block:: bash

   sudo apt update && sudo apt -y upgrade
   sudo pro attach <token>
   sudo pro enable fips-updates
