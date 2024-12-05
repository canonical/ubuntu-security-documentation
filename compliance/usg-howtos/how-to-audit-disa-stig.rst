How to audit an Ubuntu System for DISA-STIG compliance
######################################################

An Ubuntu system can be audited for the DISA-STIG rules using the `usg` command:

.. code-block:: bash

    sudo usg audit disa_stig

The `usg audit` command will automatically create an HTML report to be viewed using a browser as well as an XML report and they will be stored at `/var/lib/usg/`.
