Password Hashing
-----------------

.. tab-set::
    
    .. tab-item:: 14.04

        ``sha512``

    .. tab-item:: 16.04
    
        ``sha512``
   
    .. tab-item:: 18.04
    
        ``sha512``

    .. tab-item:: 20.04
    
        ``sha512``

    .. tab-item:: 22.04
    
        ``yescrypt``

    .. tab-item:: 24.04
    
        ``yescrypt``

The system password used for logging into Ubuntu is stored in ``/etc/shadow``. 

Historically, very old-style password hashes were based on DES and visible in ``/etc/passwd``. Modern Linux has long since moved to ``/etc/shadow`` and used salted MD5-based hashes (crypt id 1) for password verification. Since MD5 is considered weak, Ubuntu 8.10 and later proactively moved to using salted SHA-512-based password hashes (crypt id 6), which are significantly harder to brute-force. 

Ubuntu 22.04 LTS and later switched to ``yescrypt`` to provide increased protection against offline password cracking. 

For more details, see the `crypt <https://man7.org/linux/man-pages/man3/crypt.3.html>`_ manpage.

Regression tests: `test-glibc-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-glibc-security.py>`_.
