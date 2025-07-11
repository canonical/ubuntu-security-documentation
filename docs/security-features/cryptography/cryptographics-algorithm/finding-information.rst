Finding information
-------------------

Here are some notes on how to find this stuff for encryption libraries (and the kernel) that are supported in main:

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 10 10

   * - **Source package**
     - **Algorithm application**
     - **Name of encryption algorithm**
     - **Name of hash function**
     - **Max key length/hash value (in bits)**
     - **Notes**
   * - OpenSSL
     - bulk encryption
     - ``openssl ciphers | sed 's/:/\n/g' | sort -u`` (or ``openssl enc -help``) (or ``openssl enc -ciphers``) (or ``openssl list -cipher-algorithms``)
     - 
     - interpret output/research
     - compare sorted output in diff for changes
   * - OpenSSL
     - digital signature
     - research (or ``openssl list -signature-algorithms``)
     - 
     - research
     - 
   * - OpenSSL
     - authentication/integrity
     - 
     - ``openssl dgst -help`` (or ``openssl list -mac-algorithms`` and ``openssl list -digest-algorithms``)
     - interpret output/research
     - compare sorted output in diff for changes
   * - gcrypt* (eg, gcrypt20)
     - bulk encryption
     - ``src/gcrypt.h``
     - ``gcry_cipher_algos``
     - 
     - compare ``src/gcrypt.h`` for changes
   * - gcrypt* (eg, gcrypt20)
     - digital signatures
     - ``src/gcrypt.h``
     - ``gcry_pk_algos``
     - 
     - compare ``src/gcrypt.h`` for changes
   * - gcrypt* (eg, gcrypt20)
     - authentication/integrity
     - ``src/gcrypt.h``
     - 
     - ``gcry_pk_algos``
     - compare ``src/gcrypt.h`` for changes
   * - gnutls* (eg, gnutls28)
     - bulk encryption
     - ``gnutls-cli -l | grep Ciphers:``
     - 
     - interpret output/research
     - compare sorted output in diff for changes
   * - gnutls* (eg, gnutls28)
     - digital signatures
     - ``gnutls-cli -l | grep 'Public Key'``
     - 
     - interpret output/research
     - compare sorted output in diff for changes
   * - gnutls* (eg, gnutls28)
     - authentication/integrity
     - 
     - ``gnutls-cli -l | grep MACs:``
     - interpret output/research
     - compare sorted output in diff for changes
   * - nettle
     - bulk encryption
     - ``nettle.html documentation`` (use ``w3m -dump path/to/nettle.html`` for text file)
     - 
     - interpret output/research
     - 
   * - nettle
     - digital signatures
     - ``nettle.html documentation`` (use ``w3m -dump path/to/nettle.html`` for text file)
     - 
     - interpret output/research
     - 
   * - nettle
     - authentication/integrity
     - 
     - ``nettle.html documentation`` (use ``w3m -dump path/to/nettle.html`` for text file)
     - interpret output/research
     - 
   * - nss
     - bulk encryption
     - ``modutil -rawlist`` (this may not be complete)
     - 
     - interpret output/research
     - compare output between releases
   * - nss
     - digital signatures
     - ``modutil -rawlist`` (this may not be complete)
     - 
     - interpret output/research
     - compare output between releases
   * - nss
     - authentication/integrity
     - 
     - ``modutil -rawlist`` (this may not be complete)
     - interpret output/research
     - compare output between releases
   * - kernel
     - bulk encryption
     - ``grep CRYPTO_ /boot/config...``
     - 
     - filter/interpret output/research
     - 
   * - kernel
     - digital signatures
     - ``grep CRYPTO_ /boot/config...``
     - 
     - filter/interpret output/research
     - 
   * - kernel
     - authentication/integrity
     - 
     - ``grep CRYPTO_ /boot/config...``
     - filter/interpret output/research
     - 
