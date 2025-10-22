File Encryption
===============

.. tab-set::

    .. tab-item:: 24.04.2

        `fscrypt <https://github.com/google/fscrypt>`_ is available for encrypting directories on ``ext4`` filesystems but **not officially supported**.

    .. tab-item:: 22.04.5 

        `fscrypt <https://github.com/google/fscrypt>`_ is available for encrypting directories on ``ext4`` filesystems but **not officially supported**.

    .. tab-item:: 20.04.6 

        `fscrypt <https://github.com/google/fscrypt>`_ is available for encrypting directories on ``ext4`` filesystems but **not officially supported**.

    .. tab-item:: 18.04.6
        
        Encrypted Home directories are no longer supported.

        Encrypted Private directories using `eCryptfs <https://ecryptfs.org/>`_ are no longer supported.

        `fscrypt <https://github.com/google/fscrypt>`_ is available for encrypting directories on ``ext4`` filesystems but **not officially supported**.

    .. tab-item:: 16.04.7

        Encrypted Home directories are supported.

        Encrypted Private directories using `eCryptfs <https://ecryptfs.org/>`_ are supported.
   

    .. tab-item:: 14.04.6

        Encrypted Home directories are supported.

        Encrypted Private directories using `eCryptfs <https://ecryptfs.org/>`_ are supported.


Encrypted Private Directories were introduced in Ubuntu 8.10 using `eCryptfs <https://ecryptfs.org/>`_, allowing users to store sensitive data securely. 

- Ubuntu 9.04 introduced Encrypted home directories
- Support for Encrypted Private and Encrypted Home directories was dropped in Ubuntu 18.04 LTS.
- Encrypted directories can still be set up manually using `ecryptfs-setup-private`.

