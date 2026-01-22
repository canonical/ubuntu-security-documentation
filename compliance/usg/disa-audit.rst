Auditing an Ubuntu system for DISA-STIG compliance
##################################################

You can audit an Ubuntu system for DISA-STIG rules using the ``usg`` command:

.. code-block:: bash

   sudo usg audit disa_stig

The ``usg audit`` command automatically creates an HTML report viewable in a
browser, as well as an XML report. These files are stored in ``/var/lib/usg/``.
