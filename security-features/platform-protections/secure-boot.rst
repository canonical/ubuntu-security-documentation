UEFI Secure Boot
################

.. tab-set::

   .. tab-item:: Ubuntu 25.04 (Plucky Puffin)

       amd64, kernel signature enforcement

   .. tab-item:: Ubuntu 24.04 (Noble Numbat)

       amd64, kernel signature enforcement

   .. tab-item:: Ubuntu 22.10 (Kinetic Kudu)

       amd64, kernel signature enforcement

   .. tab-item:: Ubuntu 20.04 (Focal Fossa)

       amd64, kernel signature enforcement

UEFI Secure Boot is a security mechanism that prevents untrusted code from
executing during system boot.

To use UEFI Secure Boot, each binary loaded at boot must be validated against
trusted keys stored in firmware. These keys identify trusted vendors or verify
specific signed binaries.

Most x86 hardware comes with Microsoft certificates in firmware, allowing
Secure Boot to recognize and trust Microsoft-signed binaries. The Linux
community relies on this model for Secure Boot compatibility.


Secure Boot in Ubuntu
=====================

On Ubuntu, Secure Boot was first introduced in Ubuntu 12.04 LTS (Precise
Pangolin) with enforcing mode enabled for the bootloader but non-enforcing mode
for the kernel. Starting with Ubuntu 18.04 LTS (Bionic Beaver), Secure Boot
verifies all critical components: bootloader, kernel, and kernel modules.

Supported architectures
-----------------------

amd64
    A ``shim`` binary signed by Microsoft and a GRUB binary signed by Canonical
    are provided in the Ubuntu ``main`` archive as ``shim-signed`` or
    ``grub-efi-amd64-signed``.

arm64
    As of Ubuntu 20.04 LTS (Focal Fossa), a ``shim`` binary signed by Microsoft
    and a GRUB binary signed by Canonical are provided in the Ubuntu ``main``
    archive as ``shim-signed`` or ``grub-efi-arm64-signed``.

Boot process
------------

Boot variables
~~~~~~~~~~~~~~

The Secure Boot process relies on boot variables stored in the system’s NVRAM
to determine what software to execute when the system boots. The ``BootXXXX``
(for example, ``Boot0000``, ``Boot0001``) variable contains configurations and
instructions for the firmware, and the ``BootOrder`` variable defines the
priority of the ``Boot####`` entries.

Firmware validation of the shim binary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the system boots, firmware loads the ``shim`` binary as specified in
``BootXXXX``. ``shim`` works as a pre-bootloader and is signed by Microsoft.
Firmware validates the ``shim`` signature against the certificates in the
firmware.

``shim`` contains an embedded trust database, which includes Canonical's
signing certificate. It uses this to validate components like GRUB and the
kernel if they have been signed using Canonical’s UEFI key.

Once firmware validates ``shim`` successfully, ``shim`` loads the second-stage
image, which is either GRUB (for normal booting) or ``MokManager`` (for key
management tasks).

Key management
~~~~~~~~~~~~~~

If booting requires key management tasks, such as enrolling or deleting Machine
Owner Keys (MOKs), ``shim`` loads the ``MokManager`` binary. ``MokManager`` is
signed by Canonical using the same UEFI key as GRUB and is validated by
``shim``.

``MokManager`` provides a console for users to enroll new public keys (for
example, for custom kernels or bootloaders), remove previously trusted keys,
enroll binary hashes for hash-based verification, and enable or disable Secure
Boot enforcement at the ``shim`` level. Most of these operations require user
authentication, so the user must configure a password during the previous boot
phase. This password is valid for a single run of ``shim`` and ``MokManager``
and is cleared as soon as the process completes or is canceled.

Once key management completes, the system reboots since the updated keys might
be required to validate the next stages of the boot process.

Booting with GRUB
~~~~~~~~~~~~~~~~~

As with ``MokManager``, GRUB is signed by Canonical with the UEFI key. ``shim``
validates it and loads GRUB.

Once validated, GRUB loads its configuration from the ``/boot`` partition and
uses it to locate the kernel and initrd.

In Secure Boot mode, the kernel is typically a self-contained EFI binary signed
by Canonical. GRUB loads this signed kernel and validates its signature. If
valid, the kernel takes control of the system. Note that initrd images aren't
validated.

Kernel
~~~~~~

If ``shim`` or any later bootloader component such as GRUB fails to validate an
image at any point, the boot process stops to prevent an untrusted binary from
running.

Once loaded and validated, the kernel disables the firmware's Boot Services and
enters user mode, where access to UEFI variables is read-only. Given the broad
permissions afforded to kernel modules, any module not built into the kernel
must also be validated before loading. Modules built and shipped by Canonical
are signed by the Canonical UEFI key. Custom-built modules require you to sign
them before the kernel can load them. See `How to sign your own UEFI binaries
for Secure Boot <https://wiki.ubuntu.com/UEFI/SecureBoot/Signing>`_.

Unsigned modules aren't loaded by the kernel. Any attempt to insert them with
``insmod`` or ``modprobe`` fails with an error message.

Since many users rely on third-party modules that must be built locally, Ubuntu
provides tools to automate and simplify the signing process, ensuring these
modules can be loaded into the kernel.


Machine-Owner Keys (MOK) management
===================================

The MOKs generated at installation time or on upgrade are machine-specific. The
kernel or ``shim`` allows them only to sign kernel modules by using a specific
KeyUsage OID (``1.3.6.1.4.1.2312.16.1.2``) denoting the limitations of the MOK.

Recent ``shim`` versions have stricter limitations for module-signing-only
keys. Keys marked with the ``Module-signing only`` KeyUsage OID
(``1.3.6.1.4.1.2312.16.1.2``) are enrolled in the firmware in the ``shim``
trust database but are ignored when ``shim`` or GRUB validate images to load in
firmware. This approach guarantees that module-signing-only keys are used
solely for kernel module signing, but not for loading other components during
boot. Ubuntu kernels use the global trust database, which includes ``shim`` and
the firmware trust databases, and accept any of the included keys as signing
keys when loading kernel modules.

Given the limitations imposed on the automatically generated MOK, and the fact
that users with superuser access and console access already have high-level
system access, the generated MOK key is kept on the filesystem as regular files
owned by root with read-only permissions.

This limits access to the MOK for signing by malicious users or scripts,
especially since no MOK exists on the system unless it requires third-party
drivers. This reduces the possibility of compromise from the misuse of a
generated MOK key to sign a malicious kernel module. Saving a MOK to the
filesystem accessible by root effectively eliminates the security boundary
between root and kernel mode. While convenient and considered an acceptable
compromise for systems requiring third-party modules, administrators should be
aware that this weakens Secure Boot’s protections and should use it cautiously.

For unofficial kernels or kernels built by users, you need to take additional
steps to load such kernels while retaining UEFI Secure Boot capabilities. All
kernels must be signed to load by GRUB when UEFI Secure Boot is enabled, so you
must proceed with your own signing. Alternatively, you can disable validation
in shim while booted with Secure Boot enabled on an official kernel by using
``sudo mokutil --disable-validation``, providing a password when prompted, and
rebooting; or disable Secure Boot in firmware altogether.

MOK generation and signing process
----------------------------------

The key generation and signing process differs slightly depending on whether it
is a new installation or an upgrade of a system previously running Ubuntu.

In all cases, if the system isn't booting in UEFI mode, no special kernel
module signing steps or key generation occur.

If Secure Boot is disabled, MOK generation and enrollment still happen, as you
might enable Secure Boot later. The system should work properly in that case.

A new installation
~~~~~~~~~~~~~~~~~~

You step through the installer. Early on, when preparing to install and only if
the system requires third-party modules, you are prompted for a system password
clearly marked as required after the install is complete. While the system
installs, a new MOK is automatically generated without further user
interaction.

Third-party drivers or kernel modules required by the system are automatically
built when the package is installed, and the build process includes a signing
step. This step automatically uses the MOK generated earlier to sign the
module, so it can be immediately loaded once the system reboots and the MOK is
included in the system's trust database.

Once the installation is complete and the system restarts, ``MokManager`` (part
of the installed shim loader) presents a set of text-mode panels allowing you
to enroll the generated MOK at first boot. Select **Enroll MOK**, view the
certificate fingerprint, and confirm enrollment. Once confirmed, the new MOK is
entered in firmware, and you are asked to reboot the system.

When the system reboots, third-party drivers signed by the newly enrolled MOK
load as necessary.

Upgrade of a system
~~~~~~~~~~~~~~~~~~~

On upgrade, the ``shim`` and ``shim-signed`` packages upgrade. The
``shim-signed`` package's post-install tasks generate a new MOK and prompt you
for a password required once the upgrade completes and the system reboots.

During the upgrade, kernel packages and third-party modules upgrade.
Third-party modules rebuild for the new kernels, and their post-build process
automatically signs them with the MOK.

After the upgrade, we recommend rebooting the system.

On reboot, ``MokManager`` presents a set of text-mode panels allowing you to
enroll the generated MOK. Select **Enroll MOK**, view the certificate
fingerprint, and confirm enrollment. You are also presented with a prompt to
re-enable Secure Boot validation (if it was disabled); ``MokManager`` again
requires confirmation. Once all steps are confirmed, shim validation is
re-enabled, the new MOK is entered in firmware, and you are asked to reboot the
system.

When the system reboots, third-party drivers signed by the newly enrolled MOK
load as necessary.

In all cases, once the system runs with UEFI Secure Boot enabled and a recent
version of shim, the installation of any new DKMS module (third-party driver)
proceeds to sign the built module with the MOK. This happens without user
interaction if a valid MOK key exists on the system and appears to be enrolled.

If no MOK exists or the existing MOK isn't enrolled, a new key is automatically
created just before signing, and you are prompted to enroll the key by
providing a password required upon reboot.


UEFI Secure Boot key management
===============================

Key management is crucial for maintaining a working UEFI Secure Boot policy.
Ubuntu handles this automatically by guiding users through the steps needed
when signing keys change or new keys are required. For typical Ubuntu users, no
extra work is necessary as keys are managed as part of the embedded Canonical
public certificate in the shim binary signed by Microsoft. The GRUB bootloader
and kernel images and modules are signed with the private portion of that key.

The Ubuntu boot process trusts the Canonical key because it is part of the
binary image of shim, itself `signed by Microsoft
<https://techcommunity.microsoft.com/blog/hardwaredevcenter/updated-uefi-signing-requirements/1062916>`_
after a review process.
