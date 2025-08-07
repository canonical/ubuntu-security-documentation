Direct downloading of .debs from the archive
############################################

While it may be tempting to download a :file:`.deb` file directly from the
Ubuntu Archive website, this installation method circumvents the management
and verification processes provided by the standard APT tool. The APT 
ecosystem is designed to handle more than just the download of software; it
manages dependencies, verifies package integrity, and ensures seamless 
integration into the system's update cycle. Opting to download and install a
file manually bypasses these critical safeguards, introducing some risks that 
are detailed below.

Lack of integrity verification
==============================

The APT package management system uses a cryptographic chain of trust to
ensure that software is authentic and has not been altered. More information
about this scheme can be found :doc:`here <../software-integrity/archive-verification>`.
Repository metadata is digitally signed with Ubuntu's official GPG keys,
and this metadata contains the cryptographic hash for every individual package.
When using APT, the integrity of a downloaded :file:`.deb` is always verified
up to the trust anchor against these trusted cryptographic hashes before 
installation begins.

A :file:`.deb` file downloaded directly through a web browser or HTTP client 
completely bypasses this integrity check. While HTTPS provides encryption and 
integrity protection that reduce tampering-related risks when the archive 
integrity verification scheme is employed, it does not verify the file's
authenticity against the repository's chain of trust. This leaves an opening
for machine-in-the-middle (MitM) attacks where an attacker could serve a
modified, malicious package.

To package integrity protection and prevent tampering, software should always be
installed via package managers such as APT that perform cryptographic
verification.

Missed security updates
=======================

Software installed from Ubuntu's official repositories is managed by the APT
package manager, which ensures it receives timely security patches. When you
manually install a :file:`.deb` file, you risk missing these crucial updates
in a couple of common ways.

For example, if the software you installed is not available in any of your 
configured repositories, the APT package manager has no way to check for or
apply new versions. You become solely responsible for manually tracking, 
downloading, and installing any future security patches.

Additionally, there may be instances where you might download a package from
a newer Ubuntu release or a testing repository. This package will have a 
higher version number than the one in the official repositories for your
current release. Because the installed version number is higher, the update 
process will not replace it to apply a security patch to the officially
supported version, effectively pinning your system to the manually installed,
unpatched software.

To ensure you have the most secure version of software, it is highly recommended
to source :file:`.deb` files via configuring APT sources and installing packages
through APT frontends.
