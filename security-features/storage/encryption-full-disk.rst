Full disk encryption (FDE)
==========================

.. tab-set::

   .. tab-item:: Ubuntu 24.04 LTS (Noble Numbat)

       **LUKS:** Supported

       **TPM:** Supported in Ubuntu Core and Ubuntu Desktop

   .. tab-item:: Ubuntu 22.04 LTS (Jammy Jellyfish)

       **LUKS:** Supported

       **TPM:** Supported in Ubuntu Core and Ubuntu Desktop

   .. tab-item:: Ubuntu 20.04 LTS (Focal Fossa)

       **LUKS:** Supported

       **TPM:** Supported in Ubuntu Core and Ubuntu Desktop

   .. tab-item:: Ubuntu 18.04 LTS (Bionic Beaver)

       **LUKS:** Supported

   .. tab-item:: Ubuntu 16.04 LTS (Xenial Xerus)

       **LUKS:** Supported

   .. tab-item:: Ubuntu 14.04 LTS (Trusty Tahr)

       **LUKS:** Supported

Full Disk Encryption (FDE) ensures that all data on the disk or on selected
partitions is encrypted at rest. This protects information from unauthorized
access in case of device theft or loss.

Data encryption mechanism
-------------------------

Ubuntu achieves encryption using the Linux Unified Key Setup (LUKS) framework,
which provides disk encryption at the block level. You can encrypt data on a
partition or an entire disk.

At the core of the encryption process is a securely generated Volume Key (also
called the master encryption key). The system uses this key to encrypt and
decrypt data stored on the device. LUKS supports various encryption algorithms
and cipher modes, offering flexibility to choose the desired level of security
and performance. By default, Ubuntu uses AES-256 in XTS mode (which requires a 512-bit key), but you can
specify alternative algorithms, key sizes, and modes if needed.

When you encrypt a device, the system encrypts the Volume Key itself and stores
it in the LUKS header at the beginning of the device. The ``device-mapper``
subsystem maps the encrypted device to a virtual block device.
``device-mapper`` invokes ``dm-crypt`` to encrypt or decrypt data as it is
written to or read from the encrypted block device. The virtual block device
typically appears under ``/dev/mapper/``.

To decrypt the data, you must decrypt the Volume Key using one of the available
key unlocking mechanisms. Ubuntu supports two methods:

* User-supplied passphrases
* Trusted Platform Module (TPM) via integration tools such as Clevis

You can combine these key unlocking methods. For example, you can configure
multiple passphrases to unlock the encrypted block device, or set up a system
that allows either a passphrase or TPM-based unlocking.

Password-based FDE
------------------

To configure password-based encryption, you'll need to provide a passphrase. The system
processes this through a Key Derivation Function (KDF) to generate a key
suitable for encrypting the Volume Key (the actual encryption key for the disk
data).

During installation of Ubuntu, the system prompts you to enable Full Disk Encryption
(FDE). If you trigger the FDE process, you must provide a passphrase. The
system doesn't use this passphrase directly as the encryption key. Instead, it
passes it through a KDF that produces a Key Encryption Key (KEK). The system
uses the KEK to encrypt the Volume Key, which is securely stored in the LUKS
header. LUKS1 uses PBKDF2, and LUKS2 uses the Argon2 algorithm for key
derivation.

When you boot the Ubuntu system, you enter the passphrase you initially
provided. ``cryptsetup`` reads the LUKS header, derives the KEK via PBKDF2 or
Argon2, and uses the KEK to decrypt the Volume Key. Finally, the Volume Key
unlocks the encrypted disk.

Security considerations
~~~~~~~~~~~~~~~~~~~~~~~

With password-based encryption, the security of encrypted data relies heavily
on the strength of the passphrase.

TPM-backed FDE
--------------

Trusted Platform Module (TPM)-backed FDE is an alternative encryption method.

A TPM is a hardware-based security component that resides on the computer's
motherboard. It is a dedicated microcontroller used for generating, storing,
and managing cryptographic keys and performing various security-related tasks.
You can use these keys to authenticate the system, ensure secure communication,
and protect sensitive data.

Hardware requirements
~~~~~~~~~~~~~~~~~~~~~

Built-in FDE support requires:

* UEFI Secure Boot support
* TPM 2.0 (Trusted Platform Module) support
* IOMMU support to secure data transfers

We don't support external I2C/SPI-based TPM modules because they are generally
considered insecure.

TPM hierarchies
~~~~~~~~~~~~~~~

The TPM has four hierarchies used to protect cryptographic objects. Each
hierarchy is rooted in a primary seed, from which primary keys (objects) can be
derived. For FDE, we are primarily concerned with the storage hierarchy, which
is associated with the device owner and used to manage persistent keys.

The other hierarchies are:

* **Endorsement hierarchy:** Tied to the TPM’s identity and typically used for
  attestation.
* **Platform hierarchy:** Controlled by the system firmware and used for
  firmware-level configuration and access control.
* **Null hierarchy:** An ephemeral hierarchy that receives a new seed on each
  system reset.

TPM objects can serve different functions:

* Asymmetric keys for signing or key exchange.
* Symmetric keys for encryption or HMACs.
* Sealed data objects that contain external non-TPM data.
* Storage keys that can be used to protect other objects.

Since a TPM has a limited amount of storage space, the system often encrypts
TPM objects with a key derived from a seed associated with the parent storage
key and stores them externally outside the TPM.

TPM encryption
~~~~~~~~~~~~~~

TPM-based Full Disk Encryption (FDE) setups use a Unified Kernel Image (UKI),
which contains both the kernel and ``initramfs`` stored in the EFI partition.
The ``initramfs`` unlocks the encrypted block device during early boot.

During installation, ``cryptsetup`` generates the KEK and uses it to encrypt
the Volume Key. It stores the encrypted Volume Key in a LUKS header. The system
then seals the KEK to the TPM. Sealing involves:

* Encrypting the KEK using a TPM-resident key (typically derived from the TPM's
  Storage Root Key).
* Recording specific system state measurements at the time of sealing in the
  Platform Configuration Registers (PCRs). These typically include measurements
  of the bootloader, kernel, ``initramfs``, kernel command line, device model,
  and other EFI-related metadata.
* Storing policy attributes, such as usage permissions (for example,
  decrypt-only, no duplication).

The system stores the resulting sealed TPM object on disk as a binary blob.

When the system boots, ``initramfs`` loads the sealed blob from the disk and
requests the TPM to unseal it. The unsealing succeeds only if the current PCR
values match those recorded at sealing time. If successful, the TPM releases
the KEK. ``initramfs`` then reads the LUKS header, decrypts the Volume Key
using the KEK, and unlocks the data partition. The boot process then continues.

Further reading
~~~~~~~~~~~~~~~

* `Ubuntu Core - Full disk encryption
  <https://ubuntu.com/core/docs/full-disk-encryption#heading--grade>`_
  describes the implementation principles of TPM-backed FDE on Core.
* `Ubuntu Desktop - Hardware-backed disk encryption
  <https://canonical-ubuntu-desktop-documentation.readthedocs-hosted.com/en/latest/explanation/hardware-backed-disk-encryption/>`_
