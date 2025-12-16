Ubuntu image integrity verification
###################################

You must manually verify the authenticity of Ubuntu installation images, as
standard HTTP or FTP clients (such as browsers) don't have this capability.
This is important even if you use a secure channel (TLS), as it reduces risks
to the authenticity of the downloaded artifacts even when using a mirror or in
the unlikely event of a compromise to distribution channels.

Ubuntu uses GPG signing for all installation media using the ``Ubuntu CD Image
Automatic Signing Key`` (hereafter referred to as the Ubuntu Image Signing
key). These instructions require a GnuPG installation, along with ``coreutils``
(for ``sha256sum``) and an HTTP client (``cURL`` is used in the examples).
These tools work on any Linux distribution, but you can also use them on other
operating systems, such as Microsoft Windows (using `Windows Subsystem for
Linux <https://documentation.ubuntu.com/wsl/>`_) or macOS.

There are four steps to the verification process:

:ref:`step-1`

:ref:`step-2`

:ref:`step-3`

:ref:`step-4`


.. _step-1:

Step 1. Download verification public key
========================================

Download the Ubuntu Image Signing public key from the following location:

.. code-block:: console

   curl -o ubuntu.gpg "https://archive.ubuntu.com/ubuntu/project/ubuntu-archive-keyring.gpg"

Note that the downloaded GPG keyring contains multiple public keys, including
the Ubuntu Image Signing public keys (labeled ``Ubuntu CD Image Automatic
Signing Key``).


.. _step-2:

Step 2. Verify public key authenticity
======================================

You must verify the authenticity of the downloaded Ubuntu Image Signing public
key before using it to verify signatures. You need to establish a chain of
trust.

You can achieve this through multiple routes, which provide different levels of
assurance.

.. tab-set::

    .. tab-item:: Prior signature

        Step 4 recommends establishing trust in the Ubuntu Image Signing public
        keys so that you can easily verify them in the future. Note that this
        is a chicken-and-egg problem. You can only use this method if you
        completed Step 4 on a previous occasion. Otherwise, you must use an
        alternative verification method to bootstrap trust for the first time.

        This verification method relies on trusting whatever GPG signing keys
        you use to establish trust in the Ubuntu Image Signing public key.
        Anyone with access to the private keys used in Step 4 can sign
        alternative fraudulent public keys, which would invalidate the
        integrity verification process described here.

        Assuming you previously trusted all public keys in the keyring
        downloaded in Step 1, the following command must not print anything:

        .. code-block:: console

            gpg --quiet --with-colons --no-default-keyring --keyring ./ubuntu.gpg --list-keys 2>/dev/null | awk -F: '$1 == "fpr" { print $10 }' | xargs gpg --quiet --with-colons --max-cert-depth 1 --check-signatures | awk -F: '$1 == "pub" && $2 != "f"'

        This check will succeed for any public key trusted by a key with
        ultimate trust in the default GnuPG keyring. Therefore, we recommend
        using a special-purpose keyring for this method and ensuring that no
        other keys are trusted by the ultimate trust in that keyring.

    .. tab-item:: Trusted Debian/Ubuntu system

        Ubuntu comes with the Ubuntu Image signing public keys preinstalled.
        You can verify that the keys downloaded in Step 1 match those installed
        on a trusted system.

        This method anchors trust in the public key found at
        ``/usr/share/keyrings/ubuntu-archive-keyring.gpg``. Any user that can
        modify that file can invalidate the integrity verification process
        described here.

        Debian distributes the Ubuntu Image signing public key in the
        ``ubuntu-archive-keyring`` package. Install it with the following
        command:

        .. code-block:: console

            apt install ubuntu-archive-keyring

        Compare the two keys using the following command. It must not print
        anything (it prints an error for each key not found in the keyring):

        .. code-block:: console

            gpg --quiet --with-colons --no-default-keyring --keyring ./ubuntu.gpg --list-keys 2>/dev/null | awk -F: '$1 == "fpr" { print $10 }' | xargs gpg --no-default-keyring --list-keys --keyring /usr/share/keyrings/ubuntu-archive-keyring.gpg >/dev/null

    .. tab-item:: Fingerprint comparison

        You can manually compare the fingerprint (cryptographic hash derived
        from the public key data) of the downloaded Ubuntu Image Signing public
        keys with the fingerprints listed here or in another trusted source.

        The fingerprints are the 40 hexadecimal characters displayed alongside
        each key. This verification method relies on the second pre-image
        resistance of the underlying hash function. These particular values
        will no longer be appropriate once that cryptographic property is
        broken.

        Compare the output of the following command:

        .. code-block:: console

            gpg --no-default-keyring --keyring ./ubuntu.gpg --list-keys ./ubuntu.gpg

        Output:

        .. code-block:: text

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


.. _step-3:

Step 3. Validate downloaded image
=================================

The SHA256 hashsums of installation media are provided in a text file signed
using the Ubuntu Image Signing key, alongside the installation media itself.
For a particular Ubuntu release, download the hashsums and the signature of the
hashsums using the following commands. Because the integrity of the files is
cryptographically verified, you don't need to download these over a secure
channel.

.. code-block:: console

    export RELEASE=noble
    curl -O "http://releases.ubuntu.com/$RELEASE/SHA256SUMS"
    curl -O "http://releases.ubuntu.com/$RELEASE/SHA256SUMS.gpg"

Assuming the previously downloaded Ubuntu Image Signing keyring is in the same
directory, run the following command to verify that the file with the SHA256
hashsums has been signed by the Ubuntu Image Signing key:

.. code-block:: console

    gpgv --keyring ./ubuntu.gpg ./SHA256SUMS.gpg ./SHA256SUMS

Once you have established the authenticity of the SHA256 hashsums, and based on
the second pre-image resistance of SHA256, you can validate the Ubuntu
installation image. Ensure the image is in the same directory as the
``SHA256SUMS`` file and run the following command. It must output one line per
downloaded image.

.. code-block:: console

    sha256sum -c --ignore-missing ./SHA256SUMS


.. _step-4:

Step 4. Sign verification key for future validation
===================================================

With a trusted GnuPG setup, you can sign the Ubuntu Image Signing public keys
(validated in Step 2) to use the **Prior signature** verification method in
subsequent validations. Note that this relies on ensuring the confidentiality
of the ultimate-trust private key used. You must take appropriate measures to
prevent unauthorized access to it.

Run the following commands to sign all public keys in the downloaded keyring:

.. code-block:: console

    # Import keys to local keyring
    gpg --import ./ubuntu.gpg

    # Sign keys for future validation
