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

Full Disk Encryption (FDE) ensures that all data on the disk is encrypted at rest, protecting information from unauthorized access in case of device theft or loss. Full-disk encryption on Ubuntu is achieved using the Linux Unified Key Setup (LUKS) framework, which provides disk encryption at the block level. 

Password-based FDE 
------------------

The Linux Unified Key Setup (LUKS) has historically been the main mechanism that provided disk encryption at the block level.

LUKS key encryption
~~~~~~~~~~~~~~~~~~~

During installation, user is promted to start the process of FDE. If the user triggers the FDE process, they must provide a passphrase. This passphrase is not used directly as the encryption key, instead, it goes through a key derivation process that generates a more secure encryption key, which is then used to encrypt the the Volume Key (also referred to as master encryption key). 

LUKS allows for various encryption algorithms and modes to be used, providing flexibility to choose the level of security and performance that suits your needs. Ubuntu uses well-established algorithms, namely AES-256 with XTS cipher mode. 

LUKS key storage
~~~~~~~~~~~~~~~~~

The encrypted key is stored in a LUKS header at the beginning of the encrypted device.

LUKS authentication
~~~~~~~~~~~~~~~~~~~~

Once the user boots Ubuntu system, the user enters the passphrase they initially provided. ``cryptsetup`` reads the LUKS header, derives the key via PBKDF2 or Argon2 and decrypts the Volume Key.

LUKS device encryption and decryption mechanisms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a device is encrypted, which can be a partition or an entire disk, it is mapped to a virtual block device using the device mapper subsystem. 
``cryptsetup`` calls device mapper to create a virtual block device mapped to the encrypted physical device. Device mapper invokes ``dm-crypt``, to encrypt or decrypt the data on-the-fly as the data is read from or written to the encrypted block device.

Security considerations
~~~~~~~~~~~~~~~~~~~~~~~

With password-based encyrption, the security of encrypted data relies heavily on the strength of the passphrase. 

TPM-backed FDE
--------------

Trusted platform modules (TPMs) backed FDE is an alternative, more secure way of encryption.

A trusted platform module, TPM, is a hardware-based security component that resides on the motherboard of a computer. It is a dedicated microcontroller that plays a pivotal role in generating, storing, and managing cryptographic keys and performing various security-related tasks. These keys can be used to authenticate the system, ensure secure communication, and protect sensitive data.

Platform Configuration Registers, PCRs, are a central part of TPMs. They are a set of registers which store cryptographic hashes representing measurements of critical system components. These hashes create a chain of trust that allows for remote attestation, ensuring the integrity and authenticity of the system. 

Hardware requirements
~~~~~~~~~~~~~~~~~~~~~

Built-in FDE support requires:

* UEFI Secure Boot 26 support 

* TPM 2.0 (Trusted Platform Module) support

* IOMMU support to secure data transfers.

External I2C/SPI-based TPM modules are not supported as they are considered generally insecure.

TPM encryption mechanism
~~~~~~~~~~~~~~~~~~~~~~~~

The TPM has 4 hierarchies in which objects can be protected, with the root of each hierarchy being a primary seed which is used to derive primary objects. For FDE, we’re only concerned with the storage hierarchy, which is associated with the device owner. The other hierarchies are the endorsement hierarchy (associated with the device identity and the root of trust for attestations), the platform hierarchy (which is only available to the platform firmware) and the null hierarchy (which is ephemeral and gets a new seed on every reset).

Objects can have several uses. They can be asymmetric keys used for signatures or key exchange, symmetric keys used for symmetric encryption or HMACs, sealed objects that contain external data, or storage keys that can be used to protect other objects, forming a hierarchy of TPM objects. Because a TPM has a limited amount of storage space, objects don’t have to be stored within its internal storage. Instead, they are often encrypted by a key derived from a seed associated with the parent storage key, and then stored outside of the TPM. 

On installation, TPM-based FDE seals the FDE secret key to an expected chain of boot assets, parts of the EFI state, the device model and to the kernel command line. 

The TPM will only reveal the key to code executing inside of the ``initramfs`` if the boot environment has previously been authorised to access the confidential data. If certain components of the boot environment are modified, then the TPM will not permit access to the key. In order to achieve this, the TPM object must have an appropriate authorisation policy.


TPM FDE key storage
~~~~~~~~~~~~~~~~~~~

Ubuntu stores the disk encryption key outside of the TPM, protected by the TPM’s storage hierarchy inside a sealed data object.

TPM FDE authentication
~~~~~~~~~~~~~~~~~~~~~~

When the system is booted any time after installation, the key is subsequently unsealed by the ``initramfs`` code that is part of the secure-boot protected UKI binary that also contains the kernel, ``kernel.efi``. This will be possible only if the boot follows the expected sequence of boot assets and if the other bits used when sealing match the state of the system at unsealing time. With the key, the system opens the data partition and the boot moves on.

TPM resources can have an authorisation policy in order to require that a set of conditions are met in order to access or use them. An authorisation policy describes the set of conditions that have to be met before the TPM will allow the resource to be used. An authorisation policy consists of a single digest value, but despite this they can be arbitrarily complex. Authorisation policies can contain branches that allow a policy to be satisfied by multiple different conditions.

In order to access or use a resource that has an authorisation policy, a policy session is created. The policy is then executed by running a set of policy assertion commands that modify the digest associated with the policy session. When executing a command that uses a resource with an authorisation policy, the TPM will check that the digest associated with the supplied policy session matches the resource’s policy digest.

An authorisation policy can be created that requires that the values of a selection of PCRs match a set of pre-calculated values. The sealed data object that protects the disk encryption key makes use of this to ensure that the key can only be accessed by a specific boot environment. This policy is configured to ensure that access is denied if any components of the boot environment that are fundamental to the protection of the data are modified. This includes the bootloader, kernel and initramfs code, secure boot configuration and kernel command line.


Further reading
~~~~~~~~~~~~~~~

* `Ubuntu Core - Full disk encryption <https://ubuntu.com/core/docs/full-disk-encryption#heading--grade>`_ describes the implementation principles of  TPM-backed FDE on Core.

* Ubuntu Desktop - Full disk encryption 
