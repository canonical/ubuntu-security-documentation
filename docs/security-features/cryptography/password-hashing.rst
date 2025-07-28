Password Hashing
-----------------

Cryptographic hashing enables passwords to be stored without revealing their contents. The hash created can be thought of as a digital fingerprint, with a insignificantly low probability of two different passwords having the same fingerprint, while being computationally intractable to recover the plain text password from the fingerprint. When a password needs to be verified, its hash is computed and compared to the stored hash.

A cryptographic salt is added to passwords before they are hashed to prevent an adversary from precomputing hashes for common passwords. It results in the same password used for different logins having different hashes.

Ubuntu stores the password hashes for local users in ``/etc/shadow``. See the `man 5 shadow` and `man 5 crypt` pages for more information.


.. list-table::

   * - Release
     - Hashing Algorithm
   * - Trusty LTS (14.04)
     - SHA-512
   * - Xenial LTS (16.04)
     - SHA-512
   * - Bionic LTS (18.04)
     - SHA-512
   * - Focal LTS (20.04)
     - SHA-512
   * - Jammy LTS (22.04)
     - yescrypt
   * - Noble LTS (24.04)
     - yescrypt
   * - Plucky (25.04)
     - yescrypt
   * - Questing (25.10)
     - yescrypt

Ubuntu 14.04 LTS through Ubuntu 20.04 LTS uses the ``SHA-512`` key derivation which produces a fixed length 512 bit output. Although it is considered efficient to compute, its usage has declined due to brute-forcing being more feasible when compared to stronger algorithms.

Ubuntu 22.04 LTS and later use ``yescrypt`` which is based on ``scrypt``, a computationally expensive key derivation. This makes it less practical for adversaries to perform brute-force attacks when attempting to find a hash collision.

Regression tests: `test-glibc-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-glibc-security.py>`_.
