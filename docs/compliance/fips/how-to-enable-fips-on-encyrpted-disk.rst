FIPS mode with full fisk encryption
===================================

|ubuntu-latest-version| supports numerous file systems, and the installer provides the option to use Full Disk Encryption (FDE) using either LUKS or ZFS. ZFS is not supported in FIPS mode. It is possible to use LUKS encryption, although an additional manual configuration step is required.

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
