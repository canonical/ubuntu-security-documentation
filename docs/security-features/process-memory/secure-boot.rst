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


UEFI Secure Boot is a security mechanism that ensures only trusted code is executed during system boot.

To use UEFI Secure Boot, each binary loaded at boot must be validated against trusted keys stored in firmware. These keys identify either trusted vendors or specific binaries verified via cryptographic hashing.

Most x86 hardware comes with Microsoft keys preloaded in firmware, allowing Secure Boot to recognize and trust Microsoft-signed binaries. The Linux community relies on this model for Secure Boot compatibility.

While many ARM and other architectures also support UEFI Secure Boot, they may not come with preloaded keys in firmare. In such cases, boot images must be signed with a certificate that the hardware owner loads into firmware.

Secure Boot in Ubuntu
=====================

On Ubuntu, Secure Boot was first introduced in 12.04 LTS with enforcing mode enabled for the bootloader but non-enforcing mode for the kernel. In this initial implementation, an unverified kernel could still boot but without UEFI-specific protections enabled.

Starting with Ubuntu 18.04.2 LTS, Secure Boot was strengthened to enforce signature verification for both the bootloader and the kernel. This enhancement introduced the following security measures:

* Kernels failing verification will no longer boot.

* Kernel modules failing verification will not be loaded.

Supported architectures
-----------------------

amd64
     A shim binary signed by Microsoft and grub binary signed by Canonical are provided in the Ubuntu main archive as shim-signed or grub-efi-amd64-signed.

arm64
     As of 20.04 ('focal'), a shim binary signed by Microsoft and grub binary signed by Canonical are provided in the Ubuntu main archive as shim-signed or grub-efi-arm64-signed. There is a GRUB bug under investigation that needs to be resolved before this works end to end. 

Boot process
------------

BootEntry
~~~~~~~~~

Secure boot process relies on ``BootEntry`` variables. ``BootEntry`` is a list of configurations or instructions that the firmware uses to determine what to execute when the system boots. They are stored in the system’s NVRAM. ``BootEntry`` specifies the path to the GRUB EFI binary and any necessary parameters that might be required to load the GRUB bootloader. On installation, Ubuntu installs ``BootEntry`` and updates them any time the GRUB bootloader is updated. 

Firmware validation of the shim binary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the system boots, firmware loads the shim binary, signed by Microsoft, as specified in ``BootEntry``, validates it against certificates present in firmware and accepts it.

Since the shim binary embeds a Canonical certificate as well as its own trust database, further elements of the boot environment can also be signed by Canonical's UEFI key.

Once the shim binary is loaded and validated, shim loads the second-stage image, which is either GRUB for normal booting or MokManager for key management tasks. 

Key management with MOK
~~~~~~~~~~~~~~~~~~~~~~~

If booting requires with key management tasks, the MokManager binary is loaded. 

This binary is explicitly trusted by shim by being signed by an ephemeral key that only exists while the shim binary is being built. Only the MokManager binary built with a particular shim binary is allowed to run which limits the possibility of compromise from the use of compromised tools. 

MokManager allows users present at the system console to enroll keys, remove trusted keys, enroll binary hashes and toggle Secure Boot validation at the shim level, but most tasks require a previously set password to be entered to confirm that the user at console is indeed the person who requested changes. Such passwords only survive across a single run of shim / MokManager; and are cleared as soon as the process is completed or cancelled.

Once key management is completed, the system is rebooted and does not simply continue with booting, since the key management changes may be required to successfully complete the boot.

Booting with GRUB
~~~~~~~~~~~~~~~~~~

Firmware loads the GRUB binary and validates it against the UEFI Secure Boot trust database. The GRUB binary for Ubuntu is signed by the Canonical UEFI key, so once is successfully validated and the boot process continues. GRUB loads its configuration from the EFI System Partition (ESP) and locates the kernel. GRUB verifies the kernel’s signature against the UEFI trust database, before handing control to the kernel.

.. NOTE:: Initrd images are not validated.

Validating unofficial kernels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the case of unofficial kernels, or kernels built by users, additional steps need to be taken if users wish to load such kernels while retaining the full capabilities of UEFI Secure Boot. All kernels must be signed to be allowed to load by GRUB when UEFI Secure Boot is enabled, so the user will require to proceed with their own signing. Alternatively, users may wish to disable validation in shim while booted with Secure Boot enabled on an official kernel by using 'sudo mokutil --disable-validation', providing a password when prompted, and rebooting; or to disable Secure Boot in firmware altogether.


Kernel 
~~~~~~

Up to this point, any failure to validate an image to load is met with a critical error which stops the boot process. The system will not continue booting, and may automatically reboot after a period of time given that other ``BootEntry`` variables may contain boot paths that are valid and trusted.

Once loaded, validated kernels will disable the firmware's Boot Services, thus dropping privileges and effectively switching to user mode; where access to trusted variables is limited to read-only. Given the broad permissions afforded to kernel modules, any module not built into the kernel will also need to be validated upon loading. Modules built and shipped by Canonical with the official kernels are signed by the Canonical UEFI key and as such, are trusted. Custom-built modules will require the user to take the necessary steps to sign the modules before they loading them is allowed by the kernel. This can be achieved by using the 'kmodsign' command [see {How to sign} section].

Unsigned modules are simply refused by the kernel. Any attempt to insert them with insmod or modprobe will fail with an error message.

Given that many users require third-party modules for their systems to work properly or for some devices to function; and that these third-party modules require building locally on the system to be fitted to the running kernel, Ubuntu provides tooling to automate and simplify the signing process. 

Machine-Owner Key (MOK) management 
==================================

The MOK generated at installation time or on upgrade is machine-specific, and only allowed by the kernel or shim to sign kernel modules, by use of a specific KeyUsage OID (1.3.6.1.4.1.2312.16.1.2) denoting the limitations of the MOK.

Recent shim versions include logic to follow the limitations of module-signing-only keys. These keys will be allowed to be enrolled in the firmware in shim's trust database, but will be ignored when shim or GRUB validate images to load in firmware. Shim's verify() function will only successfully validate images signed by keys that do not include the "Module-signing only" (1.3.6.1.4.1.2312.16.1.2) KeyUsage OID. The Ubuntu kernels use the global trust database (which includes both shim's and the firmware's) and will accept any of the included keys as signing keys when loading kernel modules.

Given the limitations imposed on the automatically generated MOK and the fact that users with superuser access to the system and access to the system console to enter the password required when enrolling keys already have high-level access to the system; the generated MOK key is kept on the filesystem as regular files owned by root with read-only permissions. This is deemed sufficient to limit access to the MOK for signing by malicious users or scripts, especially given that no MOK exists on the system unless it requires third-party drivers. This limits the possibility of compromise from the misuse of a generated MOK key to signing a malicious kernel module. This is equivalent to compromise of the userland applications which would already be possible with superuser access to the system, and securing this is out of the scope of UEFI Secure Boot.

Previous systems may have had Secure Boot validation disabled in shim. As part of the upgrade process, these systems will be migrated to re-enabling Secure Boot validation in shim and enrolling a new MOK key when applicable. 

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

The Canonical key is held as trusted by the Ubuntu boot process by way of being part of the binary image of shim, itself signed by Microsoft after a review process. For more information on the signing process for shim, see the documentation for the WinQual process.
