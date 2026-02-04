Troubleshoot common issues
##########################

FIPS modules fail to install with NVIDIA drivers
================================================

Machines using NVIDIA drivers might fail to install FIPS modules. This occurs
because installed i386 libraries lack FIPS-compliant replacements. While we
address this issue, you can work around it by uninstalling the i386 libraries.

If you see the following error message:

.. code-block:: text

   Unexpected APT error.
   Failed running command 'apt-get install --assume-yes --allow-downgrades -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" ubuntu-fips' [exit(100)]. Message: E: Unable to correct problems, you have held broken packages.

Purge the unneeded library:

.. code-block:: bash

   sudo apt remove libssl3:i386 --purge
