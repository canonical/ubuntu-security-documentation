Use patch cut off date
#######################

See our `explanation </client/explanation/what-is-patch-cut-off-date>`__
to understand the patch cut-off date feature.

Checking the cut-off date
-------------------------

To check the cut-off date, run the following command:

.. code:: bash

   $ sudo canonical-livepatch config cutoff-date --format yaml
   cutoff-date: "2024-02-01T00:00:00Z"

   $ sudo canonical-livepatch config cutoff-date --format json
   {"cutoff-date": "2024-02-01T00:00:00Z"}

Enabling or disabling the cut-off date
--------------------------------------

To enable the cut-off date, run the following command:

.. code:: bash

   sudo canonical-livepatch config cutoff-date="2024-10-01T12:00:00Z"

The argument to ``cutoff-date`` should be in the RFC3339 format. Only
times in the past can be set as the cut-off date.

To disable the cut-off date, run the following command:

.. code:: bash

   sudo canonical-livepatch config cutoff-date=""
