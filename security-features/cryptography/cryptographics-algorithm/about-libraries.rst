Encryption libraries in Ubuntu
==============================

This table lists encryption libraries supported in ``main``, along with
instructions on how to find relevant information about algorithms from a
specific library.

Overview of the libraries
-------------------------

Source package
    The package that contains the library.

Algorithm application
    * **Bulk encryption**: Encrypting large amounts of data such as network
        traffic or storage.
    * **Digital signature**: Authenticating messages or documents.
    * **Authentication/integrity**: Verifying that the data's integrity is
        intact via message authentication codes, hashes, TLS handshake, and so
        on.

Name of encryption algorithm/hash function
    A command to list all encryption algorithms or hash functions that this
    library provides.

Max key length/hash value (in bits)
    * **Filter**: If the command that lists algorithms displays too many
        algorithms (including deprecated or experimental ones), you must
        filter only the relevant ones.
    * **Interpret**: Derive the max key length/hash value from the name of
        the displayed algorithm.
    * **Research**: Consult the documentation for that specific algorithm
        implementation in the library.

Notes
    Additional instructions on how to find more information about a specific
    library, for example, changes between releases.

.. list-table::
   :header-rows: 1
   :widths: auto

   * - **Source package**
     - **Algorithm application**
     - **Name of encryption algorithm/hash function**
     - **Max key length/hash value (in bits)**
     - **Notes**

   * - :ref:`OpenSSL`
     - Bulk encryption
     - ``openssl ciphers | sed 's/:/\n/g' | sort -u`` (or ``openssl enc -help``, ``openssl enc -ciphers``, ``openssl list -cipher-algorithms``)
     - Interpret output/research
     - Compare sorted output in diff for changes

   * - :ref:`OpenSSL`
     - Digital signature
     - Research (or ``openssl list -signature-algorithms``)
     - Research
     -

   * - :ref:`OpenSSL`
     - Authentication/integrity
     - ``openssl dgst -help`` (or ``openssl list -mac-algorithms`` and ``openssl list -digest-algorithms``)
     - Interpret output/research
     - Compare sorted output in diff for changes

   * - :ref:`gcrypt` (for example, gcrypt20)
     - Bulk encryption
     - ``src/gcrypt.h`` ``gcry_cipher_algos``
     -
     - Compare ``src/gcrypt.h`` for changes

   * - :ref:`gcrypt` (for example, gcrypt20)
     - Digital signatures
     - ``src/gcrypt.h`` ``gcry_pk_algos``
     -
     - Compare ``src/gcrypt.h`` for changes

   * - :ref:`gcrypt` (for example, gcrypt20)
     - Authentication/integrity
     - ``src/gcrypt.h`` ``gcry_pk_algos``
     -
     - Compare ``src/gcrypt.h`` for changes

   * - :ref:`gnutls` (for example, gnutls28)
     - Bulk encryption
     - ``gnutls-cli -l | grep Ciphers:``
     - Interpret output/research
     - Compare sorted output in diff for changes

   * - :ref:`gnutls` (for example, gnutls28)
     - Digital signatures
     - ``gnutls-cli -l | grep 'Public Key'``
     - Interpret output/research
     - Compare sorted output in diff for changes

   * - :ref:`gnutls` (for example, gnutls28)
     - Authentication/integrity
     - ``gnutls-cli -l | grep MACs:``
     - Interpret output/research
     - Compare sorted output in diff for changes

   * - :ref:`nettle`
     - Bulk encryption
     - ``nettle.html documentation`` (use ``w3m -dump path/to/nettle.html`` for text file)
     - Interpret output/research
     -

   * - :ref:`nettle`
     - Digital signatures
     - ``nettle.html documentation`` (use ``w3m -dump path/to/nettle.html`` for text file)
     - Interpret output/research
     -

   * - :ref:`nettle`
     - Authentication/integrity
     - ``nettle.html documentation`` (use ``w3m -dump path/to/nettle.html`` for text file)
     - Interpret output/research
     -

   * - :ref:`NSS`
     - Bulk encryption
     - ``modutil -rawlist`` (this may not be complete)
     - Interpret output/research
     - Compare output between releases

   * - :ref:`NSS`
     - Digital signatures
     - ``modutil -rawlist`` (this may not be complete)
     - Interpret output/research
     - Compare output between releases

   * - :ref:`NSS`
     - Authentication/integrity
     - ``modutil -rawlist`` (this may not be complete)
     - Interpret output/research
     - Compare output between releases

   * - :ref:`Kernel`
     - Bulk encryption
     - ``grep CRYPTO_ /boot/config...``
     - Filter/interpret output/research
     -

   * - :ref:`Kernel`
     - Digital signatures
     - ``grep CRYPTO_ /boot/config...``
     - Filter/interpret output/research
     -

   * - :ref:`Kernel`
     - Authentication/integrity
     - ``grep CRYPTO_ /boot/config...``
     - Filter/interpret output/research
     -

OpenSSL
-------

`OpenSSL <https://www.openssl.org/>`_ is a library that provides secure
communications over computer networks, such as TLS/SSL protocols, and a
collection of core cryptographic primitives such as symmetric, asymmetric,
hashing, and signing.

gcrypt
------

`GNU libgcrypt <https://www.gnupg.org/software/libgcrypt/index.html>`_ is a
library that provides core primitives such as block ciphers, public-key
algorithms, and digests.

gnutls
------

`GnuTLS <https://gnutls.org/>`_ is a library that provides TLS/SSL protocols
similar to OpenSSL but with a GNU licensing model.

nettle
------

`Nettle <https://www.lysator.liu.se/~nisse/nettle/>`_ is a low-level library
designed to be easy to integrate into higher-level libraries.

NSS
---

`Network Security Services (NSS) <https://github.com/nss-dev/nss>`_ is a set of
libraries that provide TLS/SSL, PKI, and cryptographic functions.

Kernel
------

The `Linux kernel <https://www.kernel.org/doc/html/latest/crypto/index.html>`_
provides a cryptographic API and implementations of primitives (AES, SHA, RNG,
etc.).
