Direct downloading of .debs from the archive
############################################

While sourcing a :file:`.deb` file directly from the Ubuntu Archive website
is significantly safer than using an untrusted source, this installation method
still circumvents the management and verification processes provided by the
standard ``apt`` tool. The ``apt`` ecosystem is designed to handle more than 
just the download of software; it manages dependencies, verifies package integrity,
and ensures seamless integration into the system's update cycle. Opting to download
and install a file manually bypasses these critical safeguards, introducing some 
risks that are detailed below.

Lack of integrity verification
==============================

The ``apt`` package management system uses a cryptographic chain of trust to
ensure that software is authentic and has not been altered. Repository metadata
is digitally signed with Ubuntu's official GPG keys, and this metadata contains
checksums for every individual package. When using ``apt``, the integrity of a
downloaded :file:`.deb` is always verified against these trusted checksums before
installation begins.

A :file:`.deb` file downloaded directly through a web browser completely bypasses
this integrity check. While HTTPS provides encryption for the connection, it does
not verify the file's authenticity against the repository's chain of trust. This
leaves an opening for machine-in-the-middle (MitM) attacks where an attacker could
serve a modified, malicious package. Without the integrity verification performed
by ``apt``, you have no guarantee that the file you downloaded is the one you
intended to download.

To guarantee package authenticity and prevent tampering, software should always be
installed via package managers such as ``apt`` that perform cryptographic
verification.

No automatic security updates
=============================

Normally, when installing software from Ubuntu's official repositories, that 
software will automatically receive security patches and updates through the 
standard ``apt`` update process (contingent on the Ubuntu release being under
active support, learn more `here <https://ubuntu.com/about/release-cycle>`_).
If a standalone :file:`.deb` is installed instead, this automatic security
and update process is completely bypassed. Updates need to be manually applied,
potentially leaving a system vulnerable to exploitation.

To ensure you have the most secure version of software, it is highly recommended
to source :file:`.deb` files from trusted sources and avenues that offer 
automatic security updates.
