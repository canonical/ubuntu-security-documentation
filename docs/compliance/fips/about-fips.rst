About FIPS
==========

Ubuntu Pro provides FIPS 140 certified cryptographic modules. This allows you to use Ubuntu within the Federal Government, DoD and other agencies which have a requirement to for NIST certified crypto. We certify the Linux kernel and core system libraries: OpenSSL, libgcrypt and GnuTLS.

FIPS 140-3
-----------

Ubuntu 22.04 is being certified against the new FIPS 140-3 standard. The modules have been assessed by our testing lab partner and are in the NIST queue awaiting final certification.

Canonical released these candidate modules for testing purposes in advance in December 2023, and you can use the Pro client to install them.

Updates and Preview
-------------------

Security vulnerabilities are discovered all the time and Canonical provides fixes for all the software packages within the Ubuntu ecosystem. However, the NIST certification process for FIPS applies to a specific binary version of the cryptographic module, which fixes these packages to the versions that were current at the time we submit the modules to NIST for review. This means that the FIPS certified modules may contain security vulnerabilities.

In order to address this obvious shortcoming, we provide updated versions of the FIPS modules that we patch to fix all relevant security vulnerabilities, and we strongly recommend that you use the updated modules so that your systems remain fully secure.

As the certification process takes some time, we also provide access to the modules that are awaiting NIST approval in the queue as a preview. At certain intervals we will submit the latest patched modules for recertification, and these will then be available for preview. These modules will have been validated by our testing lab partner and we do not anticipate making any further changes at this point.

Channels overview
-----------------

Security vulnerabilities are discovered all the time and Canonical provides fixes for all the software packages within the Ubuntu ecosystem. However, the NIST certification process for FIPS applies to a specific binary version of the cryptographic module, which fixes these packages to the versions that were current at the time we submit the modules to NIST for review. This means that the FIPS certified modules may contain security vulnerabilities.

In order to address this obvious shortcoming, we provide updated versions of the FIPS modules that we patch to fix all relevant security vulnerabilities, and we strongly recommend that you use the updated modules so that your systems remain fully secure.

As the certification process takes some time, we also provide access to the modules that are awaiting NIST approval in the queue as a preview. At certain intervals we will submit the latest patched modules for recertification, and these will then be available for preview. These modules will have been validated by our testing lab partner and we do not anticipate making any further changes at this point.

There are several FIPS options listed in the Pro client, depending on whether the modules have been reviewed by NIST. Which should you use? If in doubt, choose the fips-updates.

``fips-updates``
This is the recommended channel. These modules receive all the latest security updates, and the package versions will keep track with the default non-FIPS packages in Ubuntu.

``fips-preview``
This channel contains the modules that have been submitted to NIST for review but haven’t been certified yet. The latest FedRAMP guidelines, for instance, require you to install FIPS-certified modules but does allow you to use pre-approved packages that are awaiting NIST certification.

``fips``
This channel provides the exact binary versions that NIST has certified. These packages do not include the security updates and are likely to contain vulnerabilities.


Supported architectures
-----------------------

Canonical provides FIPS modules for various hardware platforms and architectures, depending upon demand. For Ubuntu 22.04 LTS these architectures are supported:

* AMD64 - this will be compatible with almost any 64-bit Intel or AMD x86_64 CPU
* IBM z15 - IBM Z systems
* ARM64 - this has been built and tested against the AWS Graviton2 platform


FIPS and Livepatch
------------------

The Livepatch service provides security updates to the running Linux kernel, allowing you to patch critical workloads without rebooting immediately. Livepatch continues to work with fips-updates but is not available with the strict fips or fips-preview modes.