Password hashing
################

Cryptographic hashing allows you to store passwords without revealing their
contents. You can think of the hash as a digital fingerprint. It has an
insignificantly low probability of two different passwords sharing the same
fingerprint, while making it computationally intractable to recover the plain
text password from the fingerprint. When verifying a password, the system
computes its hash and compares it to the stored hash.

The system adds a cryptographic salt to passwords before hashing them to
prevent an adversary from precomputing hashes for common passwords. This ensures
that the same password used for different logins results in different hashes.

Ubuntu stores password hashes for local users in ``/etc/shadow``. See the
`shadow(5) <https://manpages.ubuntu.com/manpages/en/man5/shadow.5.html>`_ and
`crypt(5) <https://manpages.ubuntu.com/manpages/en/man5/crypt.5.html>`_ manual
pages for more information.

.. list-table::
   :header-rows: 1

   * - Release
     - Hashing algorithm
   * - Ubuntu 14.04 LTS (Trusty Tahr)
     - SHA-512
   * - Ubuntu 16.04 LTS (Xenial Xerus)
     - SHA-512
   * - Ubuntu 18.04 LTS (Bionic Beaver)
     - SHA-512
   * - Ubuntu 20.04 LTS (Focal Fossa)
     - SHA-512
   * - Ubuntu 22.04 LTS (Jammy Jellyfish)
     - yescrypt
   * - Ubuntu 24.04 LTS (Noble Numbat)
     - yescrypt
   * - Ubuntu 25.04 (Plucky Puffin)
     - yescrypt
   * - Ubuntu 25.10 (Questing Quokka)
     - yescrypt

Ubuntu 14.04 LTS (Trusty Tahr) through Ubuntu 20.04 LTS (Focal Fossa) use the
``SHA-512`` hash function, which produces a fixed-length 512-bit output.
Although efficient to compute, its usage has declined because brute-forcing is
more feasible compared to stronger algorithms.

Ubuntu 22.04 LTS (Jammy Jellyfish) and later use ``yescrypt``, which is based
on ``scrypt``, a computationally expensive key derivation. This makes it less
practical for adversaries to perform brute-force attacks when attempting to
find a hash collision.

Regression tests: `test-glibc-security.py
<https://git.launchpad.net/qa-regression-testing/tree/scripts/test-glibc-security.py>`_.
