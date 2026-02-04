Apply the DISA-STIG rules
#########################

Run the following command to check the system for compliance with DISA-STIG
rules and fix (remediate) failed rules.

Ensure you have a password set on the administrative account before applying
the fix. The DISA profile requires one and will lock you out if it's missing.

Reboot the system after completion. We recommend auditing again to check for
potential rules that need custom modifications.


Install the FIPS packages
=========================

DISA-STIG requires the system to contain Ubuntu's FIPS-validated packages. We
recommend using the ``fips-updates`` stream.

.. code-block:: bash

   sudo ua enable fips-updates


Apply system changes
====================

.. code-block:: bash

   sudo usg fix disa_stig

This step takes some time.

.. warning::
   **Fresh installations only**

   Always run the DISA-STIG hardening scripts on fresh installations of Ubuntu.
   The hardening scripts adjust system configuration. If you have installed
   additional non-core services, the compliance scripts may break them by
   modifying essential configuration.


Apply rules to multiple systems
===============================

When applying rules to hundreds of systems, it isn't always practical to have
the ``usg`` tool on every system. In that case, you can generate a bash script
to apply the rules to all systems. Run the following command:

.. code-block:: bash

   sudo usg generate-fix disa_stig --output fix.sh

You can distribute and execute that script on each system that needs to comply
with the ruleset.
