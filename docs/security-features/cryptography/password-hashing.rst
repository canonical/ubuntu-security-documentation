Password Hashing
-----------------

Cryptographic hashing enables passwords to be stored without revealing its content. The hash created can be thought of as a digital fingerprint that is compared for login attempts rather than your password directly.
A cryptographic salt is added to your password before being hashed to prevent an adversary from precomputing hashes for common passwords. This greatly increases the difficulty of finding a collision with your password.

Password hashes used for logging into Ubuntu is stored in ``/etc/shadow``. They are of the form ``$id$param$salt$hash`` where ``id`` is the hashing algorithm used for that password, ``param`` is an optional field for any additional settings used by the hashing algorithm, ``salt`` is the text added when hashing your password and finally ``hash`` is the output of your password hash.

Ubuntu 14.04 LTS through Ubuntu 20.04 LTS used ``SHA-512`` which produced a fixed length 512 bit output. It is a commonly used hashing algorithm due to its strength and resistance to cryptographic attacks.

Ubuntu 22.04 LTS and later use ``yescrypt`` which is based on ``scrypt``, a computationally expensive hashing algorithm. This makes it less feasible for adversaries to perform brute-force attacks when attempting to find a hash collision.

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


Historically, very old-style password hashes were based on DES and visible in ``/etc/passwd``. Modern Linux has long since moved to ``/etc/shadow`` and used salted MD5-based hashes (crypt id 1) for password verification. Since MD5 is considered weak, Ubuntu 8.10 and later proactively moved to using salted SHA-512-based password hashes (crypt id 6), which are significantly harder to brute-force. 

Ubuntu 22.04 LTS and later switched to ``yescrypt`` to provide increased protection against offline password cracking. 

For more details, see the `crypt <https://man7.org/linux/man-pages/man3/crypt.3.html>`_ manpage.

Regression tests: `test-glibc-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-glibc-security.py>`_.
