Overview of FIPS-certified modules
##################################

All of the certified modules are available with Ubuntu Pro. The validated modules are API and ABI compatible with the default Ubuntu packages. The validation testing for Ubuntu was performed by atsec Information Security, a NIST accredited laboratory. 

Certifications under :ref:`FIPS 140-2 Level 1` will be moved to the historical list after September 2026 (although these products can still be purchased and used), and new products are expected to be certified under :ref:`FIPS 140-3 Level 1`. 

FIPS 140-3 Level 1
==================

`FIPS 140-3 Level 1 <https://ubuntu.com/blog/ubuntu-22-04-fips-140-3-modules-available-for-preview>`_ is a combined effort of NIST and ISO with the Security and Testing requirements for cryptographic modules being published as ISO/IEC 19790 and ISO/IEC 24759. 

Ubuntu 22.10 LTS
----------------

The modules in this release were certified and tested on on x86_64/AMD6 and IBM Z architectures.  

.. csv-table:: 
   :header: "Cryptographic module", "Module version", "Associated package(s)", "Status", "Certificate"

   "Linux Kernel (GA) Crypto API", "5.15.0-73-fips", "Linux v5.15", "Pending", "`#4894 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4894>`_"
   "GnuTLS", "3.7.3-4ubuntu1.2+Fips1.1", "GnuTLS v3.7.3 ", "Pending", "`#4855 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4855>`_"
   "OpenSSL", "3.0.5-0ubuntu0.1+Fips2.1", "OpenSSL v3.0.5", "Pending", "`#4794 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4794>`_"
   "libgcrypt", "1.9.4-3ubuntu3+Fips1.2", "Libgcrypt v1.9.4", "Pending", "`#4793 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4793>`_"
   "StrongSwan", "1.9.4-3ubuntu3+Fips1.2", "Strongswan v5.9.5", "Pending", "`#4911 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4911>`_"

FIPS 140-2 Level 1
==================

Modules in these releases have been assessed and certified for `FIPS 140-2 Level 1› <https://csrc.nist.gov/pubs/fips/140-2/upd2/final>`.

Ubuntu 20.10 LTS
----------------

The modules in this release were certified and tested on on x86_64/AMD6 and IBM Z architectures.  

.. csv-table:: 
   :header: "Cryptographic module", "Module version", "Associated package(s)", "Status", "Certificate"

   "Linux Kernel (GA) Crypto API", "3.0, 3.1", "?", "Active", "`#4366 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4366>`_, `#4132 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4132>`_ (AWS), `#4126 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4126>`_ (Azure), `#4127 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4127>`_ (GCP)"
   "OpenSSH client", "3.1", "?", "Active", "`#4292 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4292>`_"
   "OpenSSL", "3.1", "?", "Active", "`#4292 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4292>`_"
   "OpenSSH server","3.1", "?", "Active", "`#4292 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4292>`_"
   "libgcrypt", "3.0", "?", "Active", "`#3902 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3902>`_"
   "StrongSwan", "3.0", "?", "Active", "`#4046 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4046>`_"



Ubuntu 18.10 LTS
----------------

The modules in this release were certified and tested on on x86_64/AMD6 and IBM Z architectures.  


.. csv-table:: 
   :header: "Cryptographic module", "Module version", "Associated package(s)", "Status", "Certificate"

   "Linux Kernel (GA) Crypto API", "2.0 and 2.1", "?", "Historical", "`#3647 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3647>`_, `#4018 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/4018>`_, `#3664 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/3664>`_ (AWS), `#3683 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/3683>`_ (Azure), `#3954 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/3954>`_ (GCP)"
   "OpenSSH client", "2.1", "?", "Historical", "`#3633 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3633>`_"
   "OpenSSL", "2.0 and 2.1", "?", "Historical", "`#3622 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3622>`_, `#3980 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3980>`_"
   "libgcrypt", "1.0 and 1.1", "?", "Active", "`#3748 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3748>`_"
   "StrongSwan", "2.0 and 2.1", "?", "Historical", "`#3648 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3648>`_"


Ubuntu 16.10 LTS
----------------

The modules in this release were certified and tested on on x86_64/AMD6, IBM Z, and IBM Power8 architectures.  

.. csv-table:: 
   :header: "Cryptographic module", "Module version(s)", "Associated package(s)", "Status", "Certificate"

   "Linux Kernel (GA) Crypto API", "1.0 and 2.0", "?", "Historical", "`#2962 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/2962>`_, `#3724 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3724>`_"
   "OpenSSH client", "1.0, 1.1, and 1.2", "?", "Historical", "`#2907 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/2907>`_"
   "OpenSSL", "1.0", "?", "Historical", "`#2888 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/2888>`_"
   "OpenSSL", "2.0", "?", "Historical", "`#3725 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3725>`_"
   "OpenSSH server", "1.0, 1.1 and 1.2", "", "Historical", "`#2906 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/2906>`_"
   "StrongSwan", "1.0 and 1.1", "?", "Historical", "`#2978 <https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/2978>`_"

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

