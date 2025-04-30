Ubuntu VEX data
###############

Canonical's Security Team publishes vulnerability data conforming to the structured, human and machine-readable Vulnerability Explitability eXchange (VEX) format for all supported Ubuntu releases. In particular, the Ubuntu VEX
data feed follows the `OpenVEX <https://openvex.dev/>`_ specification. As with the other vulnerability data feeds, Ubuntu's VEX data can be used in vulnerability and patch management processes.

The VEX data describes the exploitability status of known, publicly disclosed vulnerabilities, focusing on clarifying whether these are exploitable in
specific configurations.


Available VEX data
==================

The following types of vulnerability data are available in the VEX format:

* CVE records, which mirror the per-vulnerability information available in the `Ubuntu Security Tracker <https://ubuntu.com/security/cves>`_ and contain information for known, publicly-disclosed vulnerabilities, even if security updates are not yet available. 
  
* Ubuntu Security Notices (USNs), which contain `announcements <https://ubuntu.com/security/notices>`_ of available security updates and the
  vulnerabilities they address.

VEX data for Ubuntu releases is available from three official sources:

* The `Canonical security metadata page <https://security-metadata.canonical.com/vex/>`_, as a compressed tarball updated whenever changes to the vulnerability are made available.

* The `Ubuntu Security Notices GitHub repository <https://github.com/canonical/ubuntu-security-notices>`_, under the ``vex`` directory, with individual files for each CVE record or USN.


Using VEX data
==============

As a standardized, machine-friendly format, the VEX data feed can be used by any vulnerability management tool that supports it.
