Patch security
##############

This document acts as a reference on how patches are secured and
outlines the cryptography used by the Livepatch client for this purpose.

Patch Verification
------------------

Patches are downloaded in a multi-step process,

1. Client queries for any new patches from the Livepatch-server.
2. The server returns a SHA256 checksum of the patch contents and a link
   to the patch file.
3. The client downloads the patch and verifies that a checksum of the
   downloaded patch matches the expected value.

This process ensures the integrity of the downloaded file using SHA256
hashing.

Patch Signatures
----------------

Patch files are distributed as tarballs. Within each tarball is some
metadata and a Linux kernel module (.ko file). The kernel module is
responsible for modifying the running kernel to patch high and critical
vulnerabilities.

All kernel modules are signed by Canonical to verify their authenticity.
This process is done using asymmetric encryption.

-  Signature algorithm: SHA512 with RSA
-  Canonical’s `Public
   key <https://git.launchpad.net/~ubuntu-kernel/ubuntu/+source/linux/+git/jammy/plain/debian/certs/canonical-livepatch-all.pem>`__

Kernel modules are authenticated before they are installed, ensuring
that the patch was made by Canonical and securing the Livepatch client
against installation of maliciously crafted patches.

TLS communication
-----------------

The Livepatch client supports HTTPS as a transport layer protocol. This
relies on TLS communication. Without delving into TLS, the Livepatch
client uses certificates from the host machine’s CA cert pool to verify
the authenticity of the Livepatch server.

The client supports a minimum of TLS v1.2.

The ``remote-server`` config option on the client influences the
upstream Livepatch server. There is no client side enforcement that TLS
be used, and an on-premises deployment of the Livepatch server may
decide to forgo TLS although this is not recommended.

The Canonical hosted Livepatch server redirects HTTP traffic to HTTPS.
