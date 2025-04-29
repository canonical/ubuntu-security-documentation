Overview of FIPS-certified modules
##################################

All of the certified modules are available with Ubuntu Pro. The validated modules are API and ABI compatible with the default Ubuntu packages. The validation testing for Ubuntu was performed by atsec Information Security, a NIST accredited laboratory. 

Certifications under :ref:`FIPS 140-2 Level 1` will be moved to the historical list after September 2026 (although these products can still be purchased and used), and new products will be certified under :ref:`FIPS 140-3 Level 1`. 

FIPS 140-3 Level 1
==================

`FIPS 140-3 Level 1 <https://ubuntu.com/blog/ubuntu-22-04-fips-140-3-modules-available-for-preview>`_ is a combined effort of NIST and ISO with the Security and Testing requirements for cryptographic modules being published as ISO/IEC 19790 and ISO/IEC 24759. 

Ubuntu 22.04 LTS
----------------

The modules in this release were certified and tested on on x86_64/AMD6, ARM64 and IBM Z architectures.  

.. csv-table:: 
   :header: "Cryptographic module", "Version", "Standard", "Status", "Certificate", "Sunset date"

   "Strongswan", "5.9.5", "FIPS 140-3", "Active", "`#4911 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4911>`_", "2026-12-02"
   "Kernel Crypto API", "5.15.0", "FIPS 140-3", "Active", "`#4894 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4894>`_", "2026-11-20"
   "GnuTLS", "3.7.3", "FIPS 140-3", "Active", "`#4855 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4855>`_", "2026-10-27"
   "OpenSSL", "3.0.2", "FIPS 140-3", "Active", "`#4794 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4794>`_", "2026-09-10"
   "Libgcrypt", "1.9.4", "FIPS 140-3", "Active", "`#4793 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4793>`_", "2026-09-09"

FIPS 140-2 Level 1
==================

Modules in these releases have been assessed and certified for `FIPS 140-2 Level 1› <https://csrc.nist.gov/pubs/fips/140-2/upd2/final>`_.

Ubuntu 20.04 LTS
----------------

The modules in this release were certified and tested on on x86_64/AMD6 and IBM Z architectures.  

.. csv-table:: 
   :header: "Cryptographic module", "Version", "Standard", "Status", "Certificate", "Sunset date"

   "Kernel Crypto API", "5.4.0", "FIPS 140-2", "Active", "`#4366 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4366>`_", "2026-09-21"
   "AWS Kernel Crypto API", "5.4.0", "FIPS 140-2", "Active", "`#4132 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4132>`_", "2026-05-18"
   "GCP Kernel Crypto API", "5.4.0", "FIPS 140-2", "Active", "`#4127 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4127>`_", "2026-05-18"
   "Azure Kernel Crypto API", "5.4.0", "FIPS 140-2", "Active", "`#4126 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4126>`_", "2026-05-18"
   "OpenSSL", "1.1.1f", "FIPS 140-2", "Active", "`#4292 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4292>`_", "2026-09-21"
   "Strongswan", "5.8.2", "FIPS 140-2", "Active", "`#4046 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4046>`_", "2026-09-21"
   "Libgcrypt", "1.8.5", "FIPS 140-2", "Active", "`#3902 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/3902>`_", "2026-04-19"

Ubuntu 18.04 LTS
----------------

The modules in this release were certified and tested on on x86_64/AMD6 and IBM Z architectures.  


.. csv-table:: 
   :header: "Cryptographic module", "Version", "Standard", "Status", "Certificate", "Sunset date"

   "Kernel Crypto API", "4.15.0", "FIPS 140-2", "Active", "`#4018 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4018>`_", "2026-08-29"
   "Google Kernel Crypto API", "4.15.0", "FIPS 140-2", "Active", "`#4598 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4598>`_", "2025-04-23"
   "AWS Kernel Crypto API", "4.15.0", "FIPS 140-2", "Active", "`#4597 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4597>`_", "2025-04-23"
   "IBM-GT Kernel Crypto API", "4.15.0", "FIPS 140-2", "Active", "`#4594 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4594>`_", "2025-04-23"
   "Azure Kernel Crypto API", "4.15.0", "FIPS 140-2", "Active", "`#4464 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4464>`_", "2025-04-23"
   "OpenSSL", "1.1.1", "FIPS 140-2", "Active", "`#3980 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/3980>`_", "2026-07-11"
   "Libgcrypt", "1.8.1", "FIPS 140-2", "Active", "`#3748 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/3748>`_", "2025-11-23"
   "Strongswan", "5.6.2", "FIPS 140-2", "Historical", "`#3648 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/3648>`_", "N/A"
   "OpenSSH client", "1:7.9p1", "FIPS 140-2", "Historical", "`#3633 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/3633>`_", "N/A"
   "OpenSSH server", "1:7.9p1", "FIPS 140-2", "Historical", "`#3632 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/3632>`_", "N/A"

Ubuntu 16.04 LTS
----------------

The modules in this release were certified and tested on on x86_64/AMD6, IBM Z, and IBM Power8 architectures.  

.. csv-table:: 
   :header: "Cryptographic module", "Module version(s)", "Associated package(s)", "Status", "Certificate"

   "Kernel Crypto API", "4.4.0", "FIPS 140-2", "Active", "`#4604 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4604>`_", "2025-10-06"
   "OpenSSL", "1.0.2g", "FIPS 140-2", "Active", "`#4589 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4589>`_", "2025-10-08"
   "Strongswan", "5.3.5", "FIPS 140-2", "Historical", "`#3648 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/3648>`_", "SP 800-56Arev3 transition "
   "OpenSSH client", "1:7.2p2", "FIPS 140-2", "Historical", "`#2907 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/2907>`_", "N/A"
   "OpenSSH server", "1:7.2p2", "FIPS 140-2", "Historical", "`#2906 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/2906>`_", "N/A"

Ubuntu Pro services for FIPS modules 
======================================

Security vulnerabilities are discovered all the time and Canonical provides fixes for all the software packages within the Ubuntu ecosystem. However, the NIST certification process for FIPS applies to a specific binary version of the cryptographic module, which fixes these packages to the versions that were current at the time we submit the modules to NIST for review. This means that the FIPS certified modules may contain security vulnerabilities.

In order to address this obvious shortcoming, we provide updated versions of the FIPS modules that we patch to fix all relevant security vulnerabilities, and we strongly recommend that you use the updated modules so that your systems remain fully secure.

As the certification process takes some time, we also provide access to the modules that are awaiting NIST approval in the queue as a preview. At certain intervals we will submit the latest patched modules for recertification, and these will then be available for preview. These modules will have been validated by our testing lab partner and we do not anticipate making any further changes at this point.

There are several FIPS options listed in the Pro client, depending on whether the modules have been reviewed by NIST. 

``fips-updates``
This is the recommended service. These modules receive all the latest security updates, and the package versions will keep track with the default non-FIPS packages in Ubuntu.

``fips-preview``
This service contains the modules that have been submitted to NIST for review but haven’t been certified yet. The latest FedRAMP guidelines, for instance, require you to install FIPS-certified modules but does allow you to use pre-approved packages that are awaiting NIST certification.

``fips``
This servvice provides the exact binary versions that NIST has certified. These packages do not include the security updates and are likely to contain vulnerabilities.

For more information about Ubuntu Pro services, see `Compatibility matrix for Ubuntu Pro services <https://canonical-ubuntu-pro-client.readthedocs-hosted.com/en/latest/references/compatibility_matrix/>`_

