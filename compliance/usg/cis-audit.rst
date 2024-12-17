Auditing an Ubuntu system for CIS compliance
###########################################################


Audit the system
================

An Ubuntu system can be audited for the CIS rules using the ``usg`` command.    

.. code-block:: bash
    
    sudo usg audit cis_level1_server

The output of this command will show the compliance status and will generate an HTML file with the audit report as well as an XML report at ``/var/lib/usg/``.


Customizing the audit
=====================

Compliance with a benchmark is not an all-or-nothing task. Each environment is different and options that are considered as niche in one place can be essential in another. As such, USG allows to tailor the profile and remove unnecessary rules, as well as customize the rules that have multiple options available. See the customizing the profile section for more information.