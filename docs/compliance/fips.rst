FIPS for Ubuntu 22.04
#####################

Ubuntu Pro provides FIPS 140 certified cryptographic modules. This allows you to use Ubuntu within the Federal Government, DoD and other agencies which have a requirement to for NIST certified crypto. We certify the Linux kernel and core system libraries: OpenSSL, libgcrypt and GnuTLS.

FIPS 140-3
==========

Ubuntu 22.04 is being certified against the new FIPS 140-3 standard. The modules have been assessed by our testing lab partner and are in the NIST queue awaiting final certification.

Canonical released these candidate modules for testing purposes in advance in December 2023, and you can use the Pro client to install them.

Updates and Preview
===================

Security vulnerabilities are discovered all the time and Canonical provides fixes for all the software packages within the Ubuntu ecosystem. However, the NIST certification process for FIPS applies to a specific binary version of the cryptographic module, which fixes these packages to the versions that were current at the time we submit the modules to NIST for review. This means that the FIPS certified modules may contain security vulnerabilities.

In order to address this obvious shortcoming, we provide updated versions of the FIPS modules that we patch to fix all relevant security vulnerabilities, and we strongly recommend that you use the updated modules so that your systems remain fully secure.

As the certification process takes some time, we also provide access to the modules that are awaiting NIST approval in the queue as a preview. At certain intervals we will submit the latest patched modules for recertification, and these will then be available for preview. These modules will have been validated by our testing lab partner and we do not anticipate making any further changes at this point.

Installation with the Pro client
================================

FIPS requires an Ubuntu Pro token, which you can get here - Ubuntu Pro is available for free for up to 5 machines and only requires an email address to sign up.

.. code-block:: bash

   sudo apt update && sudo apt -y upgrade
   sudo pro attach <token>
   sudo pro enable fips-updates

Pro channels
============

There are several FIPS options listed in the Pro client, depending on whether the modules have been reviewed by NIST. Which should you use? If in doubt, choose the fips-updates.

``fips-updates``
This is the recommended channel. These modules receive all the latest security updates, and the package versions will keep track with the default non-FIPS packages in Ubuntu.

``fips-preview``
This channel contains the modules that have been submitted to NIST for review but haven’t been certified yet. The latest FedRAMP guidelines, for instance, require you to install FIPS-certified modules but does allow you to use pre-approved packages that are awaiting NIST certification.

``fips``
This channel provides the exact binary versions that NIST has certified. These packages do not include the security updates and are likely to contain vulnerabilities.

Hardware Platforms
==================

Canonical provides FIPS modules for various hardware platforms and architectures, depending upon demand. For Ubuntu 22.04 LTS these architectures are supported:

* AMD64 - this will be compatible with almost any 64-bit Intel or AMD x86_64 CPU
* IBM z15 - IBM Z systems
* ARM64 - this has been built and tested against the AWS Graviton2 platform

FIPS and Livepatch
==================

The Livepatch service provides security updates to the running Linux kernel, allowing you to patch critical workloads without rebooting immediately. Livepatch continues to work with fips-updates but is not available with the strict fips or fips-preview modes.

FIPS and Full Disk Encryption
===============================

Ubuntu 22.04 supports numerous file systems, and the installer provides the option to use Full Disk Encryption (FDE) using either LUKS or ZFS. ZFS is not supported in FIPS mode. It is possible to use LUKS encryption, although an additional manual configuration step is required.

By default LUKS uses the Argon2i password hashing algorithm to generate a disk encryption key from the user-supplied password. This modern algorithm was chosen as it is believed to be more secure against the current hardware capabilities available to attackers (see the Password Hashing Competition for more details) than the older PBKDF2 algorithm. At this time, the Argon2 algorithms have not yet been certified by NIST for use in FIPS 140-3, although it is possible to use PBKDF2, and Argon2i is therefore unavailable in FIPS mode.

The installer creates the LUKS encrypted partitions using Argon2i. Before enabling FIPS mode, you need to add a key slot that uses PBKDF2 in order to be able to decrypt and mount the partition in FIPS mode. This can be done by running the following commands.

First determine which partition is encrypted with LUKS (your partition will likely be named differently):

.. code-block:: bash
   
   lsblk --fs -p -r | grep LUKS | awk '{print $1}'
   > /dev/nvme0n1p3

Then add a keyslot to LUKS using the PBKDF2 algorithm (substituting the partition name listed in the previous command):

.. code-block:: bash

   sudo cryptsetup --pbkdf=pbkdf2 luksAddKey <partition name>

You can re-use the existing disk encryption password for this step.
Now enable FIPS, as detailed previously, and reboot.

FIPS and WiFi
=============

You can connect to WiFi networks on a FIPS-enabled machine, as long as the network is set up to be compatible with the FIPS 140-3 requirements. WiFi uses encryption, and on Ubuntu this is handled by the wpa_supplicant package, which is linked against the system OpenSSL library.

When operating in FIPS mode, only FIPS-approved algorithms can be used. In particular, the WPA2 security protocol for WiFi networks, as specified in IEEE 802.11i-2004, calls for Pre-Shared Key networks to compute a shared secret based on the SSID network name and the password, using the PBKDF2-SHA1 hash function, with the SSID being the salt. The minimum security parameters for PBKDF2 are specified in NIST SP800-132, with a minimum key-length of 8 characters and a minimum salt-length of 16 characters.

This means that for WPA2 networks the SSID must be at least 16 characters, and the password at least 8 characters (which is in accordance with the WPA2 specifications already).

FIPS and NVIDIA driver issue
============================

There can be cases where machines using NVIDIA drivers fail to install the FIPS modules, which is due to an i386 libraries being installed without any option to replace them with FIPS versions. Whilst this issue is being addressed, the workaround is to uninstall the i386 libraries.

If the following error message is shown:

.. code-block:: bash

   Unexpected APT error.
   Failed running command 'apt-get install --assume-yes --allow-downgrades -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" ubuntu-fips' [exit(100)]. Message: E: Unable to correct problems, you have held broken packages.

The solution is to purge the unneeded library:

.. code-block:: bash

   sudo apt remove libssl3:i386 --purge

Keeping up to date with the FIPS status
========================================

A mailing list is used to announce patches and news related to the FIPS packages and certifications. To request to join the mailing list, please send “join” in the email body to ubuntu-certs-announce-request@lists.canonical.com. Announcements will be sent to the email address ubuntu-certs-announce@lists.canonical.com from an “@canonical.com” email address.