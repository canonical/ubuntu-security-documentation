Applying the CIS rules to the current system
#############################################

Modifying a system to comply with the CIS benchmark with USG is as simple as the following command:

.. code-block:: bash

    $ sudo usg fix <PROFILE>

where profile is one of the following:

.. csv-table:: 
    :header: "Profile name", "Corresponding CIS profile"
    
    "cis_level1_workstation", "Level 1 Workstation profile"
    "cis_level1_server", "Level 1 Server profile"
    "cis_level2_workstation", "Level 2 Workstation profile"
    "cis_level2_server", "Level 2 Server profile"
