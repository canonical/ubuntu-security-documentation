Auditing an Ubuntu system for CIS Benchmarks compliance
#######################################################

Audit the system
================

An Ubuntu system can be audited for the CIS rules using the ``usg`` command.

.. code-block:: bash
    
    sudo usg audit cis_level1_server

The command output shows the compliance status. It also generates an HTML file
with the audit report and an XML report at ``/var/lib/usg/``.

Customizing the audit
=====================

Compliance with a benchmark is not an all-or-nothing task.
Each environment is different and options that are considered as niche in one place can be essential in another.
Therefore, USG allows to tailor the profile and remove unnecessary rules, as well as customize the rules that have multiple options available.
See the :doc:`cis-customize` section for more information.
