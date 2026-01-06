File encryption
===============

.. tab-set::

    .. tab-item:: Ubuntu 24.04.2 LTS (Noble Numbat)

        `fscrypt <https://github.com/google/fscrypt>`_ is available for
        encrypting directories on ``ext4`` filesystems, but it **is not
        officially supported**.

    .. tab-item:: Ubuntu 22.04.5 LTS (Jammy Jellyfish)

        `fscrypt <https://github.com/google/fscrypt>`_ is available for
        encrypting directories on ``ext4`` filesystems, but it **is not
        officially supported**.

    .. tab-item:: Ubuntu 20.04.6 LTS (Focal Fossa)

        `fscrypt <https://github.com/google/fscrypt>`_ is available for
        encrypting directories on ``ext4`` filesystems, but it **is not
        officially supported**.

    .. tab-item:: Ubuntu 18.04.6 LTS (Bionic Beaver)

        We no longer support Encrypted Home directories.

        We no longer support Encrypted Private directories using `eCryptfs
        <https://ecryptfs.org/>`_.

        `fscrypt <https://github.com/google/fscrypt>`_ is available for
        encrypting directories on ``ext4`` filesystems, but it **is not
        officially supported**.

    .. tab-item:: Ubuntu 16.04.7 LTS (Xenial Xerus)

        We support Encrypted Home directories.

        We support Encrypted Private directories using `eCryptfs
        <https://ecryptfs.org/>`_.

    .. tab-item:: Ubuntu 14.04.6 LTS (Trusty Tahr)

        We support Encrypted Home directories.

        We support Encrypted Private directories using `eCryptfs
        <https://ecryptfs.org/>`_.

Ubuntu 8.10 (Intrepid Ibex) introduced Encrypted Private directories using
`eCryptfs <https://ecryptfs.org/>`_, allowing users to store sensitive data
securely.

* Ubuntu 9.04 (Jaunty Jackalope) introduced Encrypted Home directories.
* Ubuntu 18.04 LTS (Bionic Beaver) dropped support for Encrypted Private and
  Encrypted Home directories.
* You can still set up encrypted directories manually using
  ``ecryptfs-setup-private``.
