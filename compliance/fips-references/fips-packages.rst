FIPS certification information
##############################

Canonical has certified cryptographic packages in Ubuntu Base OS at Level 1 for Ubuntu 16.04, 18.04, and 20.04.

.. csv-table:: FIPS-certified packages 
   :header: "Release", "Architecture", "Platform", "Validated packages"

   "20.04", "amd64", "Supermicro SYS-1019P-WTR", "GA Kernel Crypto API, OpenSSL, Strongswan, (OpenSSH now uses OpenSSL for cryptography"
   "18.04", "amd64, s390x", "Supermicro SYS-5018R-WR, IBM z/VM running on IBM z/14", "GA Kernel Crypto API, OpenSSL, OpenSSH Client, OpenSSH Server, Strongswan"
   "16.04", "amd64, ppc64el, s390x", "IBM Power System S822L (PowerNV 8247-22L), IBM Power System S822LC (PowerNV 8001-22C), IBM Power System S822LC (PowerNV 8335-GTB), Supermicro SYS-5018R-WR, IBM z13 (running on LPAR)", "GA Kernel Crypto API, OpenSSL, OpenSSH Client, OpenSSH Server, Strongswan"

 	 	 	
Recertifications
================

Each FIPS certification is valid for 5 years, however each Ubuntu release is being updated periodically to bring the latest bug fixes and security updates. Each Ubuntu LTS release is recertified periodically, when feasible, closely aligned with the point releases during the `standard support phase <https://ubuntu.com/about/release-cycle>`_.

During the `Extended Security Maintenance (ESM) <https://ubuntu.com/about/release-cycle>`_ phase, the validated packages are updated via the :doc:`fips-updates stream<../fips-howtos/how-to-download-security-patches>`.