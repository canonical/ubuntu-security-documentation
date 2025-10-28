Direct downloading of .debs from the archive
############################################

You can download a :file:`.deb` package directly from the Ubuntu Archive website without using the APT manager. However, APT provides critical security features: it manages dependencies, verifies package integrity, and ensures integration with the system’s update mechanism.

By downloading :file:`.deb` packages directly, you bypass these protections and introduce security risks.

Lack of integrity verification
==============================

APT uses a cryptographic chain of trust to ensure software is authentic and unaltered. Repository metadata is digitally signed with Ubuntu’s official GPG keys and includes a cryptographic hash for every package. When you install a package through APT, it verifies the package against these trusted hashes before installation.

See more in :doc:`Ubuntu archive integrity verification <../software-integrity/archive-verification>`.

By downloading :file:`.deb` packages manually through a web browser or HTTP client, you bypass this verification process. While HTTPS reduces the risk of tampering by providing encryption and basic integrity protection, it does not validate the file against the repository’s cryptographic signatures. This leaves an opening for machine-in-the-middle (MitM) attacks where an attacker could serve a modified package.

To ensure package authenticity and prevent tampering, always install software through a package manager like APT, which performs full cryptographic verification.

Missed or blocked security updates 
==================================

Installing :file:`.deb` packages manually bypasses APT’s automatic security updates.

If the manually installed package is not included in your configured repositories, APT will not check for or apply updates. You must manually track, download, and install any future security patches.

If the manually installed package comes from a newer Ubuntu release or a testing repository, it can block future security patches. Such packages may have a higher version number than in your current release. As a result, APT will not replace them with the officially supported version, even if a security update is available. This can leave your system pinned to an unpatched version.

To receive timely security updates, configure the appropriate APT sources and install packages using APT.
