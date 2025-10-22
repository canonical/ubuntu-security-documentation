
How to troubleshoot and solve common issues
############################################

FIPS modules fail to install on machines with NVIDIA drivers
============================================================

There can be cases where machines using NVIDIA drivers fail to install the FIPS modules, which is due to an i386 libraries being installed without any option to replace them with FIPS versions. Whilst this issue is being addressed, the workaround is to uninstall the i386 libraries.

If the following error message is shown:

.. code-block:: bash

   Unexpected APT error.
   Failed running command 'apt-get install --assume-yes --allow-downgrades -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" ubuntu-fips' [exit(100)]. Message: E: Unable to correct problems, you have held broken packages.

The solution is to purge the unneeded library:

.. code-block:: bash

   sudo apt remove libssl3:i386 --purge