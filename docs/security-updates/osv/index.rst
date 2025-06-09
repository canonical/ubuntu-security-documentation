Ubuntu OSV data
###############

Canonical's Security Team publishes vulnerability data in the structured, human
and machine-readable `Open Source Vulnerability (OSV)
<https://ossf.github.io/osv-schema/>`_ format for all supported Ubuntu releases.
As with the other vulnerability data feeds, Ubuntu's OSV data can be used in
vulnerability and patch management processes.


Available OSV data
==================

The following types of vulnerability data are available in the OSV format:

* CVE records, which mirror the per-vulnerability information available in the
  `Ubuntu Security Tracker <https://ubuntu.com/security/cves>`_ and contains
  information for known, publicly-disclosed vulnerabilities, even if security
  updates are not yet available.
* Ubuntu Security Notices (USNs), which contain `announcements
  <https://ubuntu.com/security/notices>`_ of available security updates and the
  vulnerabilities they address.
* Livepatch Security Notices (LSNs), which contain announcements of kernel
  security updates available through the `Livepatch service <../livepatch/>`_.

OSV data for Ubuntu releases is available from three official sources:

* The `Canonical security metadata page
  <https://security-metadata.canonical.com/osv/>`_, as a compressed tarball
  updated whenever changes to the vulnerability are made available.
* The `Ubuntu Security Notices GitHub repository
  <https://github.com/canonical/ubuntu-security-notices>`_, under the ``osv``
  directory, with individual files for each CVE record, USN or LSN.
* The `central OSV database <https://osv.dev/list?q=&ecosystem=Ubuntu>`_, which
  provides an API to query the data.


Using OSV data
==============

As a standardized, machine-friendly format, the OSV data feed can be used by any
vulnerability management tool that supports it. In particular, the OSV project
contains a reference implementation for a scanner, `OSV-Scanner
<https://google.github.io/osv-scanner/>`_ and links to `community-maintained
tools <https://google.github.io/osv.dev/third-party/>`_.
