FIPS mode with full disk encryption
###################################

Ubuntu supports numerous file systems. The installer provides the option to use
Full Disk Encryption (FDE) using either LUKS or ZFS. FIPS mode doesn't support
ZFS. You can use LUKS encryption, but you must perform an additional manual
configuration step.

By default, LUKS uses the Argon2i password hashing algorithm to generate a disk
encryption key from the user-supplied password. This modern algorithm provides
better security against current hardware capabilities than the older PBKDF2
algorithm (see the Password Hashing Competition for details). Currently, NIST
hasn't certified the Argon2 algorithms for use in FIPS 140-3, though PBKDF2 is
allowed. Therefore, Argon2i isn't available in FIPS mode.

The installer creates the LUKS encrypted partitions using Argon2i. Before
enabling FIPS mode, you need to add a key slot that uses PBKDF2 to decrypt and
mount the partition in FIPS mode.

Run the following commands to do this.

First, determine which partition is encrypted with LUKS (your partition will
likely be named differently):

.. code-block:: bash

   lsblk --fs -p -r | grep LUKS | awk '{print $1}'

Output:

.. code-block:: text

   /dev/nvme0n1p3

Then, add a key slot to LUKS using the PBKDF2 algorithm (substitute
``<partition name>`` with the partition listed in the previous command):

.. code-block:: bash

   sudo cryptsetup --pbkdf=pbkdf2 luksAddKey <partition name>

You can reuse the existing disk encryption password for this step.

Finally, enable FIPS and reboot.
