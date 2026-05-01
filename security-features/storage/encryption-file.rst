File encryption
===============

.. tab-set::

    .. tab-item:: 24.04.2

        `fscrypt <https://github.com/google/fscrypt>`_ is available for
        encrypting directories on ``ext4`` filesystems, but it **is not
        officially supported**.

    .. tab-item:: 22.04.5

        `fscrypt <https://github.com/google/fscrypt>`_ is available for
        encrypting directories on ``ext4`` filesystems, but it **is not
        officially supported**.

    .. tab-item:: 20.04.6

        `fscrypt <https://github.com/google/fscrypt>`_ is available for
        encrypting directories on ``ext4`` filesystems, but it **is not
        officially supported**.

    .. tab-item:: 18.04.6

        We no longer support Encrypted Home directories.

        We no longer support Encrypted Private directories using `eCryptfs
        <https://ecryptfs.org/>`_.

        `fscrypt <https://github.com/google/fscrypt>`_ is available for
        encrypting directories on ``ext4`` filesystems, but it **is not
        officially supported**.

    .. tab-item:: 16.04.7

        We support Encrypted Home directories.

        We support Encrypted Private directories using `eCryptfs
        <https://ecryptfs.org/>`_.

    .. tab-item:: 14.04.6

        We support Encrypted Home directories.

        We support Encrypted Private directories using `eCryptfs
        <https://ecryptfs.org/>`_.

Ubuntu 8.10 (Intrepid Ibex) introduced Encrypted Private directories using
`eCryptfs <https://ecryptfs.org/>`_, allowing users to store sensitive data
securely. Ubuntu 9.04 (Jaunty Jackalope) introduced Encrypted Home directories
using the same technology.

Ubuntu 18.04 LTS (Bionic Beaver) dropped support for Encrypted Private and
Encrypted Home directories. eCryptfs is considered deprecated. You can still set
up encrypted directories manually using `fscrypt
<https://www.kernel.org/doc/html/v4.18/filesystems/fscrypt.html>`_ and the
``ecryptfs-setup-private`` utility. Similarly to ``eCryptfs``, ``fscrypt`` is a
Linux kernel feature, but these are distinct implementations.

Full Disk Encryption (FDE) using :doc:`dm-crypt with LUKS
<encryption-full-disk>` is the recommended approach for file system encryption
and should be preferred instead of ``fscrypt``.
