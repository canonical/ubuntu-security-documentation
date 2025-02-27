Cryptography
============

Password Hashing
-----------------

The system password used for logging into Ubuntu is stored in ``/etc/shadow``. 

Historically, very old-style password hashes were based on DES and visible in ``/etc/passwd``. Modern Linux has long since moved to ``/etc/shadow`` and used salted MD5-based hashes (crypt id 1) for password verification. Since MD5 is considered weak, Ubuntu 8.10 and later proactively moved to using salted SHA-512-based password hashes (crypt id 6), which are significantly harder to brute-force. 

Ubuntu 22.04 LTS and later switched to yescrypt to provide increased protection against offline password cracking. 

For more details, see the `crypt <https://man7.org/linux/man-pages/man3/crypt.3.html>`_ manpage.

Regression tests: `test-glibc-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-glibc-security.py>`_.

Disable Legacy TLS
------------------

Older versions of the Transport Layer Security (TLS) protocol, including SSL 3.0, TLS 1.0, and TLS 1.1, contain inherent vulnerabilities and do not provide the necessary security. 

For this reason, Ubuntu 20.04 and later proactively disable these protocols, requiring more secure alternatives.

To communicate with legacy systems, it is possible to re-enable these protocols. More information is available in `this discourse article <https://discourse.ubuntu.com/t/default-to-tls-v1-2-in-all-tls-libraries-in-20-04-lts/12464/8>`_.

Trusted Platform Module (TPM)
-----------------------------

- TPM 1.2 support was introduced in Ubuntu 7.10.
- TPM 2.0 support is available via `tpm2-tools`.


Cloud PRNG Seed
---------------

`Pollinate <https://bazaar.launchpad.net/~kirkland/pollen/trunk/view/head:/README>`_ is a client application that retrieves entropy from one or more Pollen servers and seeds the local Pseudo Random Number Generator (PRNG). 

Pollinate is essential for systems in cloud environments, ensuring secure and adequate PRNG seeding. Starting with Ubuntu 14.04 LTS, Ubuntu cloud images include the Pollinate client, which seeds the PRNG with input from `Ubuntu's entropy service <https://entropy.ubuntu.com>`_ during the first boot.

Regression tests: `pollen_test.go <https://bazaar.launchpad.net/~kirkland/pollen/trunk/view/head:/pollen_test.go>`_.




