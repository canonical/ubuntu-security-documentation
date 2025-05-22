Developing FIPS-compliant applications
======================================

FIPS-140 is a set of standards that specify requirements for cryptographic modules. Developing FIPS-compliant applications in the context of FIPS-140 means that any cryptographic operations in this application are performed by FIPS-validated modules.

Choose an appropriate package 
-----------------------------

Various modules contain different packages for different purposes, see :ref:`Overview of FIPS-certified modules`. Among modules available for Ubuntu, OpenSSL is often considered the most universal for application development and the easiest to integrate across various programming languages.  


.. csv-table:: Recommended packages for popular programming languages
   :header: "Environment", "Recommended package", "FIPS module"
   "Python", "python3-cryptography", "OpenSSL"
   "Ruby, "openssl module ", "OpenSSL"
   "Perl", "Net::SSLeay", "OpenSSL"
   "Nodejs", "crypto and tls APIs", "OpenSSL"

Analyze cryptographic operations in your application
-----------------------------------------------------

The standard demands that operations that are critical for security or used for protecting sensitive data must be FIPS-validated. While it is recommended that a FIPS-validated module handles all cryptographic operations, there might instances where cryptograpy is used for non-cryptographic purposes. For example, generating a hash for an ID of some object within your application. In such cases, you must document all operations that are not FIPS-validated and explain their role in the security of your application. 

.. _WARNING: Be careful when working with legacy software -- switching from non-FIPS-validated cryptographic algorithms to validated ones might break existing functionality. Assess your software carefully and document all of your cryptographic operations. 

Use the FIPS-validated packages correctly
-----------------------------------------

It's not enough to just use a FIPS-validated package for cryptographic operations. Each validated package comes with a security policy attached to its certificate which provides detailed guidance about using the module. You can find the security policy document on the certificate page in the **Related files** section. 

These instructions contain guidance about where to apply particular algorithms and details about initialization and other aspects relevant to the package.

Some packages provide a variety of cryptographic algorithms, but only some of them are FIPS-approved. These packages come in two modes of operation:
* FIPS mode (also called the Approved mode), which means that you can only use FIPS-approved algorithms in a specific way (with a specific key length or a padding scheme)
• non-FIPS mode (also called the non-Approved mode) that permits only non-approved security functions to be used

For example, OpenSSL is FIPS-compliant, but hash functions such as Blake2, MD4, MD5, RMD160, SM3 are not FIPS-approved and, therefore, cannot be used in a FIPS mode.

Verify that the system has FIPS enabled
---------------------------------------

When the Ubuntu FIPS kernel is present and runs with FIPS enabled, the ``/proc/sys/crypto/fips_enabled`` file exists and contains the 0x31 byte (character ``1`` in ASCII). In Ubuntu, this file indicates that FIPS is enabled. 

Use an appropriate random number generator 
------------------------------------------

When using a validated cryptographic module such as OpenSSL, we recommend using the random generator provided by this module. In other cases, we recommend using one of the following generators.

.. csv-table:: Recommended random number generators
   :header: "Random generator interface", "Description", "Recommended"
   
   "getrandom()", "getrandom() is NIST SP800-90B compliant unless the GRND_RANDOM flag is specified. This is the recommended interface to use in Ubuntu.", "Yes"
   "/dev/urandom", "It is wired to the NIST SP800-90B compliant Kernel Crypto API hash-based DRBG but does not block before the random generator is fully seeded.", "No"
   "/dev/random", "It uses the traditional random number generator from the Linux kernel and it is not SP800-90B compliant. Since it can block indefinitely, we do not recommend using it for any operation.", "No"
   
