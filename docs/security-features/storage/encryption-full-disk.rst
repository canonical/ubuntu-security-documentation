Full disk encryption (FDE)
==========================

.. tab-set::
     
     .. tab-item:: 24.04

          **LUKS**: supported

          **TPM**: supported in Ubuntu Core and Ubuntu Desktop

     .. tab-item:: 22.04

          **LUKS**: supported

          **TPM**: supported in Ubuntu Core and Ubuntu Desktop

     .. tab-item:: 20.04

         **LUKS**: supported

         **TPM**: supported in Ubuntu Core and Ubuntu Desktop

     .. tab-item:: 18.04
        
          **LUKS**: supported

     .. tab-item:: 16.04

          **LUKS**: supported
   
     .. tab-item:: 14.04

          **LUKS**: supported

Full Disk Encryption (FDE) ensures that all data on the disk or on selected partitions is encrypted at rest, protecting information from unauthorized access in case of device theft or loss. 

Data encryption mechanism
-------------------------

Encryption on Ubuntu is achieved using the Linux Unified Key Setup (LUKS) framework, which provides disk encryption at the block level. Users can encrypt data on a partition or an entire disk.

At the core of the encryption process is a securely generated Volume Key (also called the master encryption key). This key is used to encrypt and decrypt the data stored on the device. LUKS supports various encryption algorithms and cipher modes, offering users flexibility to choose their desired level of security and performance. By default, Ubuntu uses AES-256 in XTS mode, but users can specify alternative algorithms, key sizes, and modes if needed.

When a device is encrypted, the Volume Key itself is encrypted and stored in the LUKS header at the beginning of the device. The encrypted device is mapped to a virtual block device using the ``device-mapper`` subsystem. ``device-mapper`` invokes ``dm-crypt`` to encrypt or decrypt data as it is written to or read from the encrypted block device. The virtual block device typically appears under ``/dev/mapper/``.

To decrypt the data, the Volume Key must be decrypted using one of the available key unlocking mechanisms. On Ubuntu, two methods are supported:

* User-supplied passphrases

* Trusted Platform Module (TPM) via integration tools such as Clevis

Users can combine these key unlocking methods. For example, you can configure multiple passphrases to unlock the encrypted block device, or set up a system that allows either a passphrase or TPM-based unlocking.

Password-based FDE 
------------------

To configure password-based encryption, the user provides a passphrase, which is processed through a Key Derivation Function (KDF) to generate a key suitable for encrypting the Volume Key (the actual encryption key for the disk data).

During installation, the user is prompted to enable Full Disk Encryption (FDE). If the user triggers the FDE process, they must provide a passphrase. This passphrase is not used directly as the encryption key. Instead, it is passed through a KDF that produces a Key Encryption Key (KEK). The KEK is then used to encrypt the Volume Key, which is securely stored in the LUKS header. LUKS1 uses the PBKDF2 and LUKS2 uses Argon2 algorithm for key derivation.

Once the user boots Ubuntu system, the user enters the passphrase they initially provided. ``cryptsetup`` reads the LUKS header, derives the KEK via PBKDF2 or Argon2, and uses the KEK to decrypt the Volume Key. The Volume Key finally unlocks the encrypted disk.

Security considerations
~~~~~~~~~~~~~~~~~~~~~~~

With password-based encryption, the security of encrypted data relies heavily on the strength of the passphrase. 

TPM-backed FDE
--------------

Trusted platform modules (TPMs) backed FDE is an alternative way of encryption.

A TPM is a hardware-based security component that resides on the motherboard of a computer. It is a dedicated microcontroller that can be used for in generating, storing, and managing cryptographic keys and performing various security-related tasks. These keys can be used to authenticate the system, ensure secure communication, and protect sensitive data.

Hardware requirements
~~~~~~~~~~~~~~~~~~~~~

Built-in FDE support requires:

* UEFI Secure Boot 26 support 

* TPM 2.0 (Trusted Platform Module) support

* IOMMU support to secure data transfers.

External I2C/SPI-based TPM modules are not supported as they are considered generally insecure.

TPM hierarchies
~~~~~~~~~~~~~~~~~~~~~~~~

The TPM has four hierarchies used to protect cryptographic objects. Each hierarchy is rooted in a primary seed, from which primary keys (objects) can be derived. For FDE, we are primarily concerned with the storage hierarchy, which is associated with the device owner and used to manage persistent keys. The other hierarchies are:

The other hierarchies are:

* Endorsement hierarchy – tied to the TPM’s identity and typically used for attestation.

* Platform hierarchy – controlled by the system firmware and used for firmware-level configuration and access control.

* Null hierarchy – an ephemeral hierarchy that receives a new seed on each system reset.

TPM objects can serve different functions:

* Asymmetric keys for signing or key exchange

* Symmetric keys for encryption or HMACs

* Sealed data objects that contain external non-TPM data 

* Storage keys that can be used to protect other objects

Since a TPM has a limited amount of storage space, TPM objects are often encrypted by a key derived from a seed associated with the parent storage key and stored externally outside of the TPM.

TPM encryption 
~~~~~~~~~~~~~~

TPM-based Full Disk Encryption (FDE) setup uses a Unified Kernel Image (UKI), which contains both the kernel and ``initramfs`` stored in the EFI partition. The ``initramfs`` is responsible for unlocking the encrypted block device during early boot.

During installation, ``cryptsetup`` generates the KEK and uses it to encrypt the Volume Key. The encrypted Volume Key is then stored in a LUKS header. The KEK is then sealed to the TPM. Sealing involves:

* Encrypting the KEK using a TPM-resident key (typically derived from the TPM's Storage Root Key),

* Recording specific system state measurements at the time of sealing in the Platform Configuration Registers (PCRs). These typically include measurements of the bootloader, kernel, ``initramfs``, kernel command line, device model, and other EFI-related metadata. 

* Storing policy attributes, such as usage permissions (e.g., decrypt-only, no duplication).

The resulting sealed TPM object is then stored on disk as a binary blob.

When the system boots, ``initramfs`` loads the sealed blob from the disk and requests the TPM to unseal it. The unsealing only succeeds if the current PCR values match those recorded at sealing time. If successful, the TPM releases the KEK. ``initramfs`` then reads the LUKS header, decrypts the Volume Key using the KEK, and unlocks the data partition. The boot process then continues.

Further reading
~~~~~~~~~~~~~~~

* `Ubuntu Core - Full disk encryption <https://ubuntu.com/core/docs/full-disk-encryption#heading--grade>`_ describes the implementation principles of  TPM-backed FDE on Core.
