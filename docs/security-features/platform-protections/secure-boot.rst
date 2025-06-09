UEFI Secure Boot
################

.. tab-set::

   .. tab-item:: 25.04

        amd64, kernel signature enforcement

   .. tab-item:: 24.04

        amd64, kernel signature enforcement

   .. tab-item:: 22.10

        amd64, kernel signature enforcement

   .. tab-item:: 20.04

        amd64, kernel signature enforcement


UEFI Secure Boot is a security mechanism that prevents untrusted code from executing during system boot.

To use UEFI Secure Boot, each binary loaded at boot must be validated against trusted keys stored in firmware. These keys identify either trusted vendors or are used to verify specific signed binaries.

Most x86 hardware comes with Microsoft certificates in firmware, allowing Secure Boot to recognize and trust Microsoft-signed binaries. The Linux community relies on this model for Secure Boot compatibility.



Secure Boot in Ubuntu
=====================

On Ubuntu, Secure Boot was first introduced in 12.04 LTS with enforcing mode enabled for the bootloader but non-enforcing mode for the kernel. Starting with Ubuntu 18.04 LTS, Secure Boot allows to verify all critical components -- bootloader, kernel, and kernel modules.

Supported architectures
-----------------------

amd64
     A ``shim`` binary signed by Microsoft and GRUB binary signed by Canonical are provided in the Ubuntu ``main`` archive as ``shim-signed`` or ``grub-efi-amd64-signed``.

arm64
     As of 20.04, a ``shim`` binary signed by Microsoft and GRUB binary signed by Canonical are provided in the Ubuntu ``main`` archive as ``shim-signed`` or ``grub-efi-arm64-signed``.

Boot process
------------

Boot variables
~~~~~~~~~~~~~~

Secure Boot process relies on boot variables stored in the system’s NVRAM to determine what software to execute execute when the system boots. The ``BootXXXX`` (for example, ``Boot0000, Boot0001``) variable contains configurations and instructions for the firmware, and the ``BootOrder`` variable defines the priority of the ``Boot####`` entries.

Firmware validation of the ``shim`` binary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the system boots, firmware loads the ``shim`` binary as specified in ``BootXXXX``. ``shim`` works as a pre-bootloader and has been signed by Microsoft. Firmware validates the ``shim`` signature against the certificates in the firmware.

``shim`` contains an embedded trust database, which includes Canonical's signing certificate, which it can use to validate components like GRUB and the kernel if they have been signed using Canonical’s UEFI key.

Once firmware validates ``shim`` successfully, ``shim`` loads the second-stage image, which is either GRUB used for normal booting or ``MokManager`` used for key management tasks.

Key management
~~~~~~~~~~~~~~

If booting requires with key management tasks, such as enrolling or deleting Machine Owner Keys (MOKs) , ``shim`` loads the ``MokManager`` binary. ``MokManager`` is signed by Canonical using the same UEFI key as GRUB, and is validated ``shim``.

``MokManager`` provides a console for users to enroll new public keys (for example, for custom kernels or bootloaders), remove previously trusted keys, enroll binary hashes that can be used for hash-based verification, and enable or disable Secure Boot enforcement at the ``shim`` level. Most of these operations require authentication of the user, so the user must configure a password  during the previous boot phase. This password is valid for a single run of ``shim`` and  ``MokManager``, and is cleared as soon as the process is completed or cancelled.

Once key management is completed, the system is rebooted since the updated keys may be required to validate the next stages of the boot process.

Booting with GRUB
~~~~~~~~~~~~~~~~~~

As in the case of ``MokManager``, GRUB is signed by Canonical with the UEFI key. ``shim`` validates it and loads GRUB.

Once validated, GRUB loads its configuration from the ``/boot`` partition, and uses the configuration to locate the kernel and initrd.

In Secure Boot mode, the kernel is typically a self-contained EFI binary signed by Canonical. GRUB loads this signed kernel validates its signature. If valid, the kernel takes the control of the system. Note that initrd images are not validated.

Kernel
~~~~~~

If ``shim`` or any later bootloader component such as GRUB fails to validate an image at any point, the boot process stops to prevent an untrusted binary from running.

Once the kernel is loaded and validated, it disables the firmware's Boot Services and enters the user mode, where access to UEFI variables is limited to read-only. Given the broad permissions afforded to kernel modules, any module not built into the kernel must also be validated before it can be loaded. Modules built and shipped by Canonical are signed by the Canonical UEFI key. Custom-built modules require the user to sign the modules before they can be loaded by the kernel. See `How to sign your own UEFI binaries for Secure Boot <https://wiki.ubuntu.com/UEFI/SecureBoot/Signing>`_

Unsigned modules are not loaded by the kernel. Any attempt to insert them with ``insmod`` or ``modprobe`` will fail with an error message.

Since many users rely on third-party modules. Since these third-party modules often must be built locally,  Ubuntu provides tools to automate and simplify the process of signing these modules, ensuring they can be loaded into the kernel.

Machine-Owner Keys (MOK) management
===================================

The MOKs generated at installation time or on upgrade are machine-specific, and are only allowed by the kernel or ``shim`` to sign kernel modules, by use of a specific KeyUsage OID (``1.3.6.1.4.1.2312.16.1.2``) denoting the limitations of the MOK.

Recent ``shim`` versions have stricter limitations for module-signing-only keys. Keys marked with the ``Module-signing only`` KeyUsage OID (``1.3.6.1.4.1.2312.16.1.2``) will be  enrolled in the firmware in ``shim`` trust database, but will be ignored when ``shim`` or GRUB validate images to load in firmware. This approach guarantees that module-signing-only keys keys are used solely for kernel module signing, but not for loading other components during boot. The Ubuntu kernels use the global trust database which includes ``shim`` and the firmware trust databases, and accept any of the included keys as signing keys when loading kernel modules.

Given the limitations imposed on the automatically generated MOK and the fact that users with superuser access to the system and access to the system console to enter the password required when enrolling keys already have high-level access to the system; the generated MOK key is kept on the filesystem as regular files owned by root with read-only permissions.

This is deemed sufficient to limit access to the MOK for signing by malicious users or scripts, especially given that no MOK exists on the system unless it requires third-party drivers. This limits the possibility of compromise from the misuse of a generated MOK key to signing a malicious kernel module. Saving a MOK to the filesystem accessible by root effectively eliminates the security boundary between root and kernel mode. While convenient and is considered an acceptable compromise for systems that require third-party modules, administrators should be aware that this weakens Secure Boot’s protections and should be used cautiously.

In the case of unofficial kernels, or kernels built by users, additional steps need to be taken if users wish to load such kernels while retaining the full capabilities of UEFI Secure Boot. All kernels must be signed to be allowed to load by GRUB when UEFI Secure Boot is enabled, so the user will require to proceed with their own signing. Alternatively, users may wish to disable validation in shim while booted with Secure Boot enabled on an official kernel by using 'sudo mokutil --disable-validation', providing a password when prompted, and rebooting; or to disable Secure Boot in firmware altogether.

MOK generation and signing process
----------------------------------

The key generation and signing process is slightly different based on whether we are dealing with a brand new installation or an upgrade of system previously running Ubuntu.

In all cases, if the system is not booting in UEFI mode, no special kernel module signing steps or key generation will happen.

If Secure Boot is disabled, MOK generation and enrollment still happens, as the user may later enable Secure Boot. They system should work properly if that is the case.

A new installation
~~~~~~~~~~~~~~~~~~

The user steps through the installer. Early on, when preparing to install and only if the system requires third-party modules to work, the user is prompted for a system password that is clearly marked as being required after the install is complete, and while the system is being installed, a new MOK is automatically generated without further user interaction.

Third-party drivers or kernel modules required by the system will be automatically built when the package is installed, and the build process includes a signing step. The signing step automatically uses the MOK generated earlier to sign the module, such that it can be immediately loaded once the system is rebooted and the MOK is included in the system's trust database.

Once the installation is complete and the system is restarted, at first boot the user is presented with the MokManager program (part of the installed shim loader), as a set of text-mode panels that all the user to enroll the generated MOK. The user selects "Enroll MOK", is shown a fingerprint of the certificate to enroll, and is prompted to confirm the enrollment. Once confirmed, the new MOK will be entered in firmware and the user will be asked to reboot the system.

When the system reboots, third-party drivers signed by the MOK just enrolled will be loaded as necessary.

Upgrade of a system
~~~~~~~~~~~~~~~~~~~

On upgrade, the shim and shim-signed packages are upgraded. The shim-signed package's post-install tasks proceeds to generate a new MOK, and prompts the user for a password that is clearly mentioned as being required once the upgrade process is completed and the system rebooted.

During the upgrade, the kernel packages and third-party modules are upgraded. Third-party modules are rebuilt for the new kernels and their post-build process proceeds to automatically sign them with the MOK.

After upgrade, the user is recommended to reboot their system.

On reboot, the user is presented with the MokManager program (part of the installed shim loader), as a set of text-mode panels that all the user to enroll the generated MOK. The user selects "Enroll MOK", is shown a fingerprint of the certificate to enroll, and is prompted to confirm the enrollment. The user is also presented with a prompt to re-enable Secure Boot validation (in the case it was found to be disabled); and MokManager again requires confirmation from the user. Once all steps are confirmed, shim validation is re-enabled, the new MOK will be entered in firmware and the user will be asked to reboot the system.

When the system reboots, third-party drivers signed by the MOK just enrolled will be loaded as necessary.

In all cases, once the system is running with UEFI Secure Boot enabled and a recent version of shim; the installation of any new DKMS module (third-party driver) will proceed to sign the built module with the MOK. This will happen without user interaction if a valid MOK key exists on the system and appears to already be enrolled.

If no MOK exists or the existing MOK is not enrolled, a new key will automatically created just before signing and the user will be prompted to enroll the key by providing a password which will be required upon reboot.

UEFI Secure Boot Key Management
===============================

Key management is an important process in maintaining a working UEFI Secure Boot policy. Ubuntu handles this automatically by guiding users through the steps they need to take when signing keys change, or as new keys are required. For the most part, for typical Ubuntu users, no extra work is necessary as the keys are managed as part of the embedded Canonical public certificate in the shim binary signed by Microsoft, and the GRUB bootloader and kernel images and modules are signed with the private portion of that key.

The Canonical key is held as trusted by the Ubuntu boot process by way of being part of the binary image of shim, itself `signed by Microsoft <https://techcommunity.microsoft.com/blog/hardwaredevcenter/updated-uefi-signing-requirements/1062916>`_ after a review process.
