Ubuntu image integrity verification
###################################

Verifying the authenticity of Ubuntu installation images must be performed
manually, as the HTTP or FTP clients (e.g. a browser) normally employed do not
have this capability. This is important even when a secure channel is employed,
such as through TLS, as it reduces risks to the authenticity of the downloaded
artifacts even when a mirror is used or in the unlikely event of a compromise to
distribution channels.

Ubuntu uses GPG signing for all installation media using the ``Ubuntu CD Image
Automatic Signing Key``, hereafter referred to as the Ubuntu Image Signing key.
As such, the instructions provided in this section require a GnuPG installation,
along with ``coreutils`` (for ``sha256sum``) and an HTTP client (``cURL`` is
used in the examples). These will work on any Linux distribution, but can also
be employed on other operating systems, such as Microsoft Windows (using
`Windows Subsystem for Linux <https://documentation.ubuntu.com/wsl/>`_) or
macOS.

The verification process is split in 4 steps:

#. Download verification public key
#. Verify public key authenticity
#. Validate downloaded image
#. Sign verification key for future validation


Step 1. Download verification public key
========================================

The Ubuntu Image Signing public key can be obtained from the following location:

.. code-block:: console
   
   $ curl -o ubuntu.gpg "https://archive.ubuntu.com/ubuntu/project/ubuntu-archive-keyring.gpg"

Please note the downloaded GPG keyring contains multiple public keys, amongst
which is the Ubuntu Image Signing public keys, with the label ``Ubuntu CD Image
Automatic Signing Key``.

Step 2. Verify public key authenticity
======================================

The authenticity of the previously-downloaded Ubuntu Image Signing public key
needs be verified, before the public key itself can be used for verifying
signatures: a chain of trust needs to be established.

This can be achieved through multiple routes, which may provide different levels
of assurance.

.. tab-set::

    .. tab-item:: Prior signature

        Step 4 recommends establishing trust in the Ubuntu Image Signing public
        keys, so that these can be more easily verified in the future. Please
        note that this is a chicken-and-egg problem and this method can only be
        employed once Step 4 had already been completed on a previous occasion,
        implying the need to use an alternative verification method to bootstrap
        trust for the first time.

        This verification method relies on trusting whatever GPG signing keys
        are used to establish trust in the Ubuntu Image Signing public key.
        Anyone with access to the private keys used in Step 4 would be able to
        sign alternative fraudulent public keys, which would then invalidate the
        integrity verification process described here.

        Assuming that all of the public keys in the keyring downloaded at Step 1
        had previously been trusted, the following command must NOT print
        anything:

        .. code-block:: console

            # This command must not print anything
            $ gpg --quiet --with-colons --no-default-keyring --keyring ./ubuntu.gpg --list-keys 2>/dev/null | awk -F: '$1 == "fpr" { print $10 }' | xargs gpg --quiet --with-colons --max-cert-depth 1 --check-signatures | awk -F: '$1 == "pub" && $2 != "f"'

        This check will succeed for any public key trusted by a key with
        ultimate trust in the default GnuPG keyring. As such, it is recommended
        that a special-purpose keyring is used if this method is employed and
        that no other keys are trusted by the ultimate trust in that keyring.

    .. tab-item:: Trusted Debian/Ubuntu system

        Ubuntu comes with the Ubuntu Image signing public keys preinstalled. As
        such, you can verify that the keys downloaded in Step 1 are the same to
        those installed on a trusted system.

        This method anchors trust in the public key found at
        ``/usr/share/keyrings/ubuntu-archive-keyring.gpg``. Any user that can
        modify that file can invalidate the integrity verification process
        described here.

        Debian distributes the Ubuntu Image signing public key in the
        ``ubuntu-archive-keyring`` package, which can be installed with the
        following command:

        .. code-block:: console

            $ apt install ubuntu-archive-keyring

        The two keys can be compared using the following command, which must NOT
        print anything:

        .. code-block:: console

            # This command must not print anything
            # Prints "gpg: error reading key: No public key" for each key that isn't in that keyring.
            $ gpg --quiet --with-colons --no-default-keyring --keyring ./ubuntu.gpg --list-keys 2>/dev/null | awk -F: '$1 == "fpr" { print $10 }' | xargs gpg --no-default-keyring --list-keys --keyring /usr/share/keyrings/ubuntu-archive-keyring.gpg >/dev/null

    .. tab-item:: Fingerprint comparison

        You can manually compare the fingerprint (cryptographic hash derived
        from the public key data) of the downloaded Ubuntu Image Signing public
        keys with the fingerprints listed here or in another trusted source.

        The fingerprints are the 40 hexadecimal characters displayed alongside
        each key. This verification method relies on the second pre-image
        resistance of the underlying hash function and these particular values
        will no longer be appropriate once that cryptographic property is
        broken.

        You should compare the output of the following command:

        .. code-block:: console

            $ gpg --no-default-keyring --keyring ./ubuntu.gpg --list-keys ./ubuntu.gpg

            ------------
            pub   rsa4096 2012-05-11 [SC]
                  790BC7277767219C42C86F933B4FE6ACC0B21F32
            uid           [ unknown] Ubuntu Archive Automatic Signing Key (2012) <ftpmaster@ubuntu.com>

            pub   rsa4096 2012-05-11 [SC]
                  843938DF228D22F7B3742BC0D94AA3F0EFE21092
            uid           [ unknown] Ubuntu CD Image Automatic Signing Key (2012) <cdimage@ubuntu.com>

            pub   rsa4096 2018-09-17 [SC]
                  F6ECB3762474EDA9D21B7022871920D1991BC93C
            uid           [ unknown] Ubuntu Archive Automatic Signing Key (2018) <ftpmaster@ubuntu.com>


Step 3. Validate downloaded image
=================================

The SHA256 hashsums of installation media are provided in a text file signed
using the Ubuntu Image Signing key, alongside the installation media itself. For
a particular Ubuntu release, the hashsums and the signature of the hashsums can
be downloaded using the following commands. Because the integrity of the files
will be cryptographically verified, these need not be downloaded over a secure
channel or from trusted location, for that matter.

.. code-block:: console
   
    $ export RELEASE=noble
    $ curl -O "http://releases.ubuntu.com/$RELEASE/SHA256SUMS"
    $ curl -O "http://releases.ubuntu.com/$RELEASE/SHA256SUMS.gpg"

Assuming the previously-downloaded Ubuntu Image Signing keyring is in the same
directory, the following command will verify that the file with the SHA256
hashsums has been signed by the Ubuntu Image Signing key:

.. code-block:: console

    $ gpgv --keyring ./ubuntu.gpg ./SHA256SUMS.gpg ./SHA256SUMS

Once you have established the authenticity of the SHA256 hashsums and based on
the second pre-image resistance of SHA256, you can validate that a Ubuntu
installation image downloaded in the same directory as the ``SHA256SUMS`` file
is authentic by using the following command:

.. code-block:: console

    # Validate hashsum (must output one line per downloaded image)
    $ sha256sum -c --ignore-missing ./SHA256SUMS


Step 4. Sign verification key for future validation
===================================================

With a trusted GnuPG setup, you can sign the Ubuntu Image Signing public keys,
previously-validated in Step 2, in order to be able to use the **Prior
signature** verification method in subsequent validations. Please note that this
relies on ensuring the confidentiality of the ultimate-trust private key that is
used and that appropriate measures have been taken against risks to unauthorized
access to it.

The following commands will sign all of the public keys in the
previously-downloaded keyring:

.. code-block:: console

    # Import keys to local keyring
    $ gpg --import ./ubuntu.gpg

    # Sign keys for future validation
    $ gpg --quiet --with-colons --no-default-keyring --keyring ./ubuntu.gpg --list-keys 2>/dev/null | awk -F: '$1 == "fpr" { print $10 }' | xargs gpg --quick-lsign-key
