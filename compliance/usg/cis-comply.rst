Apply the CIS rules to the current system
#########################################

To modify a system to comply with the CIS benchmark using USG, run the following
command:

.. code-block:: bash

   sudo usg fix <PROFILE>

Replace ``<PROFILE>`` with one of the following:

.. csv-table::
   :header: "Profile name", "Corresponding CIS profile"

   "cis_level1_workstation", "Level 1 Workstation profile"
   "cis_level1_server", "Level 1 Server profile"
   "cis_level2_workstation", "Level 2 Workstation profile"
   "cis_level2_server", "Level 2 Server profile"
