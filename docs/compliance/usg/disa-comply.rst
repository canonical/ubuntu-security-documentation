Applying the DISA-STIG rules
############################

The following command will run code to check the system for compliance with the DISA-STIG rules and will fix (remediate) the rules that fail. It is important to have a password set on the administrative account before applying the fix as the DISA profile requires one and will lock you out. After completion, the system must be rebooted, and we recommend auditing again to check potential rules that need custom modifications.  

Install the FIPS packages
==========================

DISA-STIG requires the system to contain the FIPS validated packages of Ubuntu. We recommend using the fips-updates stream.

.. code-block:: bash

    $ sudo ua enable fips-updates

Apply the necessary changes for the system to comply
====================================================

.. code-block:: bash

    $ sudo usg fix disa_stig


This step will take quite a while.

.. WARNING:: Always run the DISA-STIG hardening scripts on fresh installations of Ubuntu. As the hardening scripts adjust the system configuration, if additional non-core services have been installed to the system, the compliance scripts may break them by modifying essential configuration.

Applying the rules to multiple systems
======================================

When applying the rules to hundreds of systems, it is not always practical to have the usg tool on every system. In that case a bash script can be generated to apply the rules to all systems. The following command generates that script.


.. code-block:: bash

    $ sudo usg generate-fix disa_stig --output fix.sh

That script can be distributed and executed on each system that needs to comply with the ruleset.