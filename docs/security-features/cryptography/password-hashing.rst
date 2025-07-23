Password Hashing
-----------------

Cryptographic hashing enables passwords to be stored without revealing their contents. The hash created can be thought of as a digital fingerprint that is checked for login attempts rather than your password itself.

A cryptographic salt is added to passwords before they are hashed to prevent an adversary from precomputing hashes for common passwords. This greatly increases the difficulty of finding a collision with your password.

Ubuntu stores your password hashes in ``/etc/shadow``. The related information is stored in entries of the format::

${id}${param}${salt}${hash}

* ``id``    - Hashing algorithm used
* ``param`` - Additional settings used by the hashing algorithm
* ``salt``  - Salt to be added before hashing
* ``hash``  - Your password hash

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

Ubuntu 14.04 LTS through Ubuntu 20.04 LTS uses the ``SHA-512`` hashing algorithm which produces a fixed length 512 bit output. It is a commonly used hashing algorithm due to its strength and resistance to cryptographic attacks.

Ubuntu 22.04 LTS and later use ``yescrypt`` which is based on ``scrypt``, a computationally expensive hashing algorithm. This makes it less feasible for adversaries to perform brute-force attacks when attempting to find a hash collision.

For more details, see the `crypt <https://man7.org/linux/man-pages/man3/crypt.3.html>`_ manpage.

Regression tests: `test-glibc-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-glibc-security.py>`_.
