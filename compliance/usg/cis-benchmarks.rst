CIS Benchmarks and profiles
###########################

`CIS Benchmarks <https://www.cisecurity.org/benchmark/ubuntu_linux>`_ are
security configuration recommendations developed for Ubuntu Linux.

The levels represent different sets of recommendations depending on the
security requirements of the environment. See the `CIS Benchmarks FAQ
<https://www.cisecurity.org/cis-benchmarks/cis-benchmarks-faq>`_ to learn what
each level represents.

We provide Level 1 and Level 2 configuration profiles for Ubuntu.

.. csv-table::
   :header: "Profile name", "Corresponding CIS profile"

   "cis_level1_workstation", "Level 1 Workstation profile"
   "cis_level1_server", "Level 1 Server profile"
   "cis_level2_workstation", "Level 2 Workstation profile"
   "cis_level2_server", "Level 2 Server profile"


Install CIS profiles
====================

To use Canonical's profiles to audit your system, you must install them first:

.. code-block:: bash

   sudo apt install usg-benchmarks-1
