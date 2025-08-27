Encryption libraries in Ubuntu 
==============================

This table contains a list of encryption libraries supported in `main` as well as instructions on how to find relevant information about algorithms from a specific library:

Overview of the libraries
-------------------------

Source package
  the package that contains the library

Algorithm application
   *bulk encryption*: encrypting large amounts of data such as network traffic or storage
   *digital signature*: authenticating messages or documents 
   *authentication/integrity*: verifying that the data's integrity is intact via message authentication codes, hashes, TLS handshake, and so on

Name of encryption algorithm/hash function
    a command to list all encryption algorithms/hash functions that this library provides

Max key length/hash value (in bits)
    *filter*: if the command that lists algorithms displays too many algorithms (including deprecated or experimental ones), you must filter only the relevant ones
    *interpret*: derive the max key length/hash value from the name of the displayed algorithm
    *research*: consult the documentation for that specific algorithm implementation in the library

Notes
  Additional instructions on how to find more information about a specific library, e.g. changes between releases 

.. list-table::
   :header-rows: 1
   :widths: auto

   * - **Source package**
     - **Algorithm application**
     - **Name of encryption algorithm/hash function**
     - **Max key length/hash value (in bits)**
     - **Notes**
   
   * - :ref:`OpenSSL`
     - bulk encryption
     - ``openssl ciphers | sed 's/:/\n/g' | sort -u`` (or ``openssl enc -help``) (or ``openssl enc -ciphers``) (or ``openssl list -cipher-algorithms``)
     - interpret output/research
     - compare sorted output in diff for changes
   
   * - :ref:`OpenSSL`
     - digital signature
     - research (or ``openssl list -signature-algorithms``)
     - research
     - 
   
   * - :ref:`OpenSSL`
     - authentication/integrity
     - ``openssl dgst -help`` (or ``openssl list -mac-algorithms`` and ``openssl list -digest-algorithms``)
     - interpret output/research
     - compare sorted output in diff for changes
   
   * - :ref:`gcrypt` (eg, gcrypt20)
     - bulk encryption
     - ``src/gcrypt.h`` ``gcry_cipher_algos``
     - 
     - compare ``src/gcrypt.h`` for changes
   
   * - :ref:`gcrypt` (eg, gcrypt20)
     - digital signatures
     - ``src/gcrypt.h`` ``gcry_pk_algos``
     -
     - compare ``src/gcrypt.h`` for changes
    
   * - :ref:`gcrypt` (eg, gcrypt20)
     - authentication/integrity
     - ``src/gcrypt.h`` ``gcry_pk_algos``
     -
     - compare ``src/gcrypt.h`` for changes  

   * - :ref:`gnutls` (eg, gnutls28)
     - bulk encryption
     - ``gnutls-cli -l | grep Ciphers:``
     - interpret output/research
     - compare sorted output in diff for changes
   
   * - :ref:`gnutls` (eg, gnutls28)
     - digital signatures
     - ``gnutls-cli -l | grep 'Public Key'``
     - interpret output/research
     - compare sorted output in diff for changes
   
   * - :ref:`gnutls` (eg, gnutls28)
     - authentication/integrity
     - ``gnutls-cli -l | grep MACs:``
     - interpret output/research
     - compare sorted output in diff for changes
   
   * - :ref:`nettle`
     - bulk encryption
     - ``nettle.html documentation`` (use ``w3m -dump path/to/nettle.html`` for text file)
     - interpret output/research
     - 
   
   * - :ref:`nettle`
     - digital signatures
     - ``nettle.html documentation`` (use ``w3m -dump path/to/nettle.html`` for text file)
     - interpret output/research
     - 
   
   * - :ref:`nettle`
     - authentication/integrity
     - ``nettle.html documentation`` (use ``w3m -dump path/to/nettle.html`` for text file)
     - interpret output/research
     - 
   
   * - :ref:`NSS`
     - bulk encryption
     - ``modutil -rawlist`` (this may not be complete)
     - interpret output/research
     - compare output between releases
   
   * - :ref:`NSS`
     - digital signatures
     - ``modutil -rawlist`` (this may not be complete)
     - interpret output/research
     - compare output between releases
   
   * - :ref:`NSS`
     - authentication/integrity
     - ``modutil -rawlist`` (this may not be complete)
     - interpret output/research
     - compare output between releases
   
   * - :ref:`Kernel`
     - bulk encryption
     - ``grep CRYPTO_ /boot/config...``
     - filter/interpret output/research
     - 
   
   * - :ref:`Kernel`
     - digital signatures
     - ``grep CRYPTO_ /boot/config...``
     - filter/interpret output/research
     - 
   
   * - :ref:`Kernel`
     - authentication/integrity
     - ``grep CRYPTO_ /boot/config...``
     - filter/interpret output/research
     - 


OpenSSL
-------

`OpenSSL <https://www.openssl.org/>`_ is a library that provides secure communications over computer networks such as TLS/SSL protocols and collection of core cryptographic primitives such a symmetric, asymmetric, hashing, signing. 


gcrypt
-------

`GNU libgcrypt <https://www.gnupg.org/software/libgcrypt/index.html>`_ is a library that provides the core primitives such as block ciphers, public-key algorithms, digests.

gnutls
-------

`GnuTLS <https://gnutls.org/>`_ is library that provides TLS/SSL protocols similar to OpenSSL but with a GNU licensing model.

nettle
-------

`https://www.lysator.liu.se/~nisse/nettle/ <Nettle>`_ is a low-level library designed to be easy to integrate into higher-level libraries.

NSS
---
`Network Security Services (NSS) <https://github.com/nss-dev/nss>`_ is a set of libraries that provide TLS/SSL, PKI, and cryptographic functions.

Kernel
------
`Linux kernel <https://www.kernel.org/doc/html/latest/crypto/index.html>`_ provides cryptographic API and implementations of primitives (AES, SHA, RNG, etc.).