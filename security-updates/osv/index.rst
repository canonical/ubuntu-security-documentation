Ubuntu OSV data
***************

The Ubuntu Security Team publishes vulnerability data in the structured, human-
and machine-readable `Open Source Vulnerability (OSV)
<https://ossf.github.io/osv-schema/>`_ format for all supported Ubuntu
releases. As with other vulnerability data feeds, you can use Ubuntu's OSV data
in vulnerability and patch management processes.

.. _osv-data:


Available OSV data
==================

The following types of vulnerability data are available in the OSV format:

* **Ubuntu CVE records:** These mirror the per-vulnerability information
  available in the `Ubuntu Security Tracker
  <https://ubuntu.com/security/cves>`_. They contain information for known,
  publicly disclosed vulnerabilities, even if security updates aren't yet
  available.
* **Ubuntu Security Notices (USNs):** These contain `announcements
  <https://ubuntu.com/security/notices>`_ of available security updates and
  the vulnerabilities they address.
* **Livepatch Security Notices (LSNs):** These contain announcements of kernel
  security updates available through the `Livepatch service <../../compliance/fips/livepatch-and-fips/>`_.

You can get OSV data for Ubuntu releases from three official sources:

* The `Canonical security metadata page
  <https://security-metadata.canonical.com/osv/>`_, as a compressed tarball
  updated whenever changes to the vulnerability are made available.
* The `Ubuntu Security Notices GitHub repository
  <https://github.com/canonical/ubuntu-security-notices>`_, under the ``osv``
  directory, with individual files for each CVE record, USN, or LSN.
* The `central OSV database <https://osv.dev/list?q=&ecosystem=Ubuntu>`_,
  which provides an API to query the data.


Using OSV data
==============

As a standardized, machine-friendly format, any vulnerability management tool
that supports OSV can use the data feed. In particular, the OSV project
contains a reference implementation for a scanner, `OSV-Scanner
<https://google.github.io/osv-scanner/>`_, and links to `community-maintained
tools <https://google.github.io/osv.dev/third-party/>`_.


Understanding Ubuntu's OSV data
===============================

The OSV format, although easy to parse, might still be difficult to interpret.
The next sections cover the relevant details of the data we publish.

To better understand the format, consider the following OSV data file
``UBUNTU-CVE-2025-6491.json``:

.. code-block:: json

   {
     "schema_version": "1.7.0",
     "id": "UBUNTU-CVE-2025-6491",
     "details": "In PHP versions:8.1.* before 8.1.33, 8.2.* before 8.2.29, 8.3.* before 8.3.23, 8.4.* before 8.4.10 when parsing XML data in SOAP extensions, overly large (>2Gb) XML namespace prefix may lead to null pointer dereference. This may lead to crashes and affect the availability of the target server.",
     "aliases": [],
     "upstream": [
       "CVE-2025-6491"
     ],
     "related": [
       "USN-7648-1"
     ],
     "severity": [
       {
         "type": "CVSS_V3",
         "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H"
       },
       {
         "type": "Ubuntu",
         "score": "medium"
       }
     ],
     "published": "2025-07-13T22:15:00Z",
     "modified": "2025-07-18T17:02:45Z",
     "affected": [
       {
         "package": {
           "ecosystem": "Ubuntu:Pro:14.04:LTS",
           "name": "php5",
           "purl": "pkg:deb/ubuntu/php5@5.5.9+dfsg-1ubuntu4.29+esm16?arch=source&distro=esm-infra-legacy/trusty"
         },
         "ranges": [
           {
             "type": "ECOSYSTEM",
             "events": [
               {
                 "introduced": "0"
               }
             ]
           }
         ],
         "versions": [
           "5.5.3+dfsg-1ubuntu2",
           "5.5.3+dfsg-1ubuntu3",
           "5.5.6+dfsg-1ubuntu1",
           "5.5.6+dfsg-1ubuntu2",
           "5.5.8+dfsg-2ubuntu1",
           "5.5.9+dfsg-1ubuntu1",
           "5.5.9+dfsg-1ubuntu2",
           "5.5.9+dfsg-1ubuntu3",
           "5.5.9+dfsg-1ubuntu4",
           "5.5.9+dfsg-1ubuntu4.1",
           "5.5.9+dfsg-1ubuntu4.2",
           "5.5.9+dfsg-1ubuntu4.3",
           "5.5.9+dfsg-1ubuntu4.4",
           "5.5.9+dfsg-1ubuntu4.5",
           "5.5.9+dfsg-1ubuntu4.6",
           "5.5.9+dfsg-1ubuntu4.7",
           "5.5.9+dfsg-1ubuntu4.9",
           "5.5.9+dfsg-1ubuntu4.11",
           "5.5.9+dfsg-1ubuntu4.12",
           "5.5.9+dfsg-1ubuntu4.13",
           "5.5.9+dfsg-1ubuntu4.14",
           "5.5.9+dfsg-1ubuntu4.16",
           "5.5.9+dfsg-1ubuntu4.17",
           "5.5.9+dfsg-1ubuntu4.19",
           "5.5.9+dfsg-1ubuntu4.20",
           "5.5.9+dfsg-1ubuntu4.21",
           "5.5.9+dfsg-1ubuntu4.22",
           "5.5.9+dfsg-1ubuntu4.23",
           "5.5.9+dfsg-1ubuntu4.24",
           "5.5.9+dfsg-1ubuntu4.25",
           "5.5.9+dfsg-1ubuntu4.26",
           "5.5.9+dfsg-1ubuntu4.27",
           "5.5.9+dfsg-1ubuntu4.29",
           "5.5.9+dfsg-1ubuntu4.29+esm5",
           "5.5.9+dfsg-1ubuntu4.29+esm6",
           "5.5.9+dfsg-1ubuntu4.29+esm8",
           "5.5.9+dfsg-1ubuntu4.29+esm10",
           "5.5.9+dfsg-1ubuntu4.29+esm11",
           "5.5.9+dfsg-1ubuntu4.29+esm12",
           "5.5.9+dfsg-1ubuntu4.29+esm13",
           "5.5.9+dfsg-1ubuntu4.29+esm14",
           "5.5.9+dfsg-1ubuntu4.29+esm15",
           "5.5.9+dfsg-1ubuntu4.29+esm16"
         ],
         "ecosystem_specific": {}
       },
       {
         "package": {
           "ecosystem": "Ubuntu:Pro:16.04:LTS",
           "name": "php7.0",
           "purl": "pkg:deb/ubuntu/php7.0@7.0.33-0ubuntu0.16.04.16+esm15?arch=source&distro=esm-infra/xenial"
         },
         "ranges": [
           {
             "type": "ECOSYSTEM",
             "events": [
               {
                 "introduced": "0"
               }
             ]
           }
         ],
         "versions": [
           "7.0.1-5",
           "7.0.1-6",
           "7.0.2-1",
           "7.0.2-3",
           "7.0.2-4",
           "7.0.2-5",
           "7.0.3-2",
           "7.0.3-3",
           "7.0.3-9ubuntu1",
           "7.0.4-5ubuntu1",
           "7.0.4-5ubuntu2",
           "7.0.4-7ubuntu1",
           "7.0.4-7ubuntu2",
           "7.0.4-7ubuntu2.1",
           "7.0.8-0ubuntu0.16.04.1",
           "7.0.8-0ubuntu0.16.04.2",
           "7.0.8-0ubuntu0.16.04.3",
           "7.0.13-0ubuntu0.16.04.1",
           "7.0.15-0ubuntu0.16.04.1",
           "7.0.15-0ubuntu0.16.04.2",
           "7.0.15-0ubuntu0.16.04.4",
           "7.0.18-0ubuntu0.16.04.1",
           "7.0.22-0ubuntu0.16.04.1",
           "7.0.25-0ubuntu0.16.04.1",
           "7.0.28-0ubuntu0.16.04.1",
           "7.0.30-0ubuntu0.16.04.1",
           "7.0.32-0ubuntu0.16.04.1",
           "7.0.33-0ubuntu0.16.04.1",
           "7.0.33-0ubuntu0.16.04.2",
           "7.0.33-0ubuntu0.16.04.3",
           "7.0.33-0ubuntu0.16.04.4",
           "7.0.33-0ubuntu0.16.04.5",
           "7.0.33-0ubuntu0.16.04.6",
           "7.0.33-0ubuntu0.16.04.7",
           "7.0.33-0ubuntu0.16.04.9",
           "7.0.33-0ubuntu0.16.04.11",
           "7.0.33-0ubuntu0.16.04.12",
           "7.0.33-0ubuntu0.16.04.14",
           "7.0.33-0ubuntu0.16.04.15",
           "7.0.33-0ubuntu0.16.04.16",
           "7.0.33-0ubuntu0.16.04.16+esm1",
           "7.0.33-0ubuntu0.16.04.16+esm2",
           "7.0.33-0ubuntu0.16.04.16+esm3",
           "7.0.33-0ubuntu0.16.04.16+esm4",
           "7.0.33-0ubuntu0.16.04.16+esm5",
           "7.0.33-0ubuntu0.16.04.16+esm6",
           "7.0.33-0ubuntu0.16.04.16+esm7",
           "7.0.33-0ubuntu0.16.04.16+esm8",
           "7.0.33-0ubuntu0.16.04.16+esm9",
           "7.0.33-0ubuntu0.16.04.16+esm10",
           "7.0.33-0ubuntu0.16.04.16+esm11",
           "7.0.33-0ubuntu0.16.04.16+esm12",
           "7.0.33-0ubuntu0.16.04.16+esm13",
           "7.0.33-0ubuntu0.16.04.16+esm14",
           "7.0.33-0ubuntu0.16.04.16+esm15"
         ],
         "ecosystem_specific": {}
       },
       {
         "package": {
           "ecosystem": "Ubuntu:Pro:18.04:LTS",
           "name": "php7.2",
           "purl": "pkg:deb/ubuntu/php7.2@7.2.24-0ubuntu0.18.04.17+esm8?arch=source&distro=esm-infra/bionic"
         },
         "ranges": [
           {
             "type": "ECOSYSTEM",
             "events": [
               {
                 "introduced": "0"
               }
             ]
           }
         ],
         "versions": [
           "7.2.1-1ubuntu2",
           "7.2.2-1ubuntu1",
           "7.2.2-1ubuntu2",
           "7.2.3-1ubuntu1",
           "7.2.5-0ubuntu0.18.04.1",
           "7.2.7-0ubuntu0.18.04.1",
           "7.2.7-0ubuntu0.18.04.2",
           "7.2.10-0ubuntu0.18.04.1",
           "7.2.15-0ubuntu0.18.04.1",
           "7.2.15-0ubuntu0.18.04.2",
           "7.2.17-0ubuntu0.18.04.1",
           "7.2.19-0ubuntu0.18.04.1",
           "7.2.19-0ubuntu0.18.04.2",
           "7.2.24-0ubuntu0.18.04.1",
           "7.2.24-0ubuntu0.18.04.2",
           "7.2.24-0ubuntu0.18.04.3",
           "7.2.24-0ubuntu0.18.04.4",
           "7.2.24-0ubuntu0.18.04.6",
           "7.2.24-0ubuntu0.18.04.7",
           "7.2.24-0ubuntu0.18.04.8",
           "7.2.24-0ubuntu0.18.04.9",
           "7.2.24-0ubuntu0.18.04.10",
           "7.2.24-0ubuntu0.18.04.11",
           "7.2.24-0ubuntu0.18.04.12",
           "7.2.24-0ubuntu0.18.04.13",
           "7.2.24-0ubuntu0.18.04.15",
           "7.2.24-0ubuntu0.18.04.16",
           "7.2.24-0ubuntu0.18.04.17",
           "7.2.24-0ubuntu0.18.04.17+esm1",
           "7.2.24-0ubuntu0.18.04.17+esm2",
           "7.2.24-0ubuntu0.18.04.17+esm3",
           "7.2.24-0ubuntu0.18.04.17+esm4",
           "7.2.24-0ubuntu0.18.04.17+esm5",
           "7.2.24-0ubuntu0.18.04.17+esm6",
           "7.2.24-0ubuntu0.18.04.17+esm7",
           "7.2.24-0ubuntu0.18.04.17+esm8"
         ],
         "ecosystem_specific": {}
       },
       {
         "package": {
           "ecosystem": "Ubuntu:Pro:20.04:LTS",
           "name": "php7.4",
           "purl": "pkg:deb/ubuntu/php7.4@7.4.3-4ubuntu2.29?arch=source&distro=esm-infra/focal"
         },
         "ranges": [
           {
             "type": "ECOSYSTEM",
             "events": [
               {
                 "introduced": "0"
               }
             ]
           }
         ],
         "versions": [
           "7.4.3-4build1",
           "7.4.3-4build2",
           "7.4.3-4ubuntu1",
           "7.4.3-4ubuntu1.1",
           "7.4.3-4ubuntu2.2",
           "7.4.3-4ubuntu2.4",
           "7.4.3-4ubuntu2.5",
           "7.4.3-4ubuntu2.6",
           "7.4.3-4ubuntu2.7",
           "7.4.3-4ubuntu2.8",
           "7.4.3-4ubuntu2.9",
           "7.4.3-4ubuntu2.10",
           "7.4.3-4ubuntu2.11",
           "7.4.3-4ubuntu2.12",
           "7.4.3-4ubuntu2.13",
           "7.4.3-4ubuntu2.15",
           "7.4.3-4ubuntu2.16",
           "7.4.3-4ubuntu2.17",
           "7.4.3-4ubuntu2.18",
           "7.4.3-4ubuntu2.19",
           "7.4.3-4ubuntu2.20",
           "7.4.3-4ubuntu2.22",
           "7.4.3-4ubuntu2.23",
           "7.4.3-4ubuntu2.24",
           "7.4.3-4ubuntu2.26",
           "7.4.3-4ubuntu2.28",
           "7.4.3-4ubuntu2.29"
         ],
         "ecosystem_specific": {}
       },
       {
         "package": {
           "ecosystem": "Ubuntu:22.04:LTS",
           "name": "php8.1",
           "purl": "pkg:deb/ubuntu/php8.1@8.1.2-1ubuntu2.22?arch=source&distro=jammy"
         },
         "ranges": [
           {
             "type": "ECOSYSTEM",
             "events": [
               {
                 "introduced": "0"
               },
               {
                 "fixed": "8.1.2-1ubuntu2.22"
               }
             ]
           }
         ],
         "versions": [
           "8.1.0~rc4-1ubuntu2",
           "8.1.0-1",
           "8.1.2-1ubuntu1",
           "8.1.2-1ubuntu2",
           "8.1.2-1ubuntu2.1",
           "8.1.2-1ubuntu2.2",
           "8.1.2-1ubuntu2.3",
           "8.1.2-1ubuntu2.4",
           "8.1.2-1ubuntu2.5",
           "8.1.2-1ubuntu2.6",
           "8.1.2-1ubuntu2.8",
           "8.1.2-1ubuntu2.9",
           "8.1.2-1ubuntu2.10",
           "8.1.2-1ubuntu2.11",
           "8.1.2-1ubuntu2.13",
           "8.1.2-1ubuntu2.14",
           "8.1.2-1ubuntu2.15",
           "8.1.2-1ubuntu2.17",
           "8.1.2-1ubuntu2.18",
           "8.1.2-1ubuntu2.19",
           "8.1.2-1ubuntu2.20",
           "8.1.2-1ubuntu2.21"
         ],
         "ecosystem_specific": {
           "binaries": [
             {
               "binary_name": "libapache2-mod-php7.4",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "libapache2-mod-php8.0",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "libapache2-mod-php8.1",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "libphp8.1-embed",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-bcmath",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-bz2",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-cgi",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-cli",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-common",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-curl",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-dba",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-enchant",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-fpm",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-gd",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-gmp",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-imap",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-interbase",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-intl",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-ldap",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-mbstring",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-mysql",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-odbc",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-opcache",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-pgsql",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-phpdbg",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-pspell",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-readline",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-snmp",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-soap",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-sqlite3",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-sybase",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-tidy",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-xml",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-xsl",
               "binary_version": "8.1.2-1ubuntu2.22"
             },
             {
               "binary_name": "php8.1-zip",
               "binary_version": "8.1.2-1ubuntu2.22"
             }
           ],
           "availability": "No subscription required"
         }
       },
       {
         "package": {
           "ecosystem": "Ubuntu:24.04:LTS",
           "name": "php8.3",
           "purl": "pkg:deb/ubuntu/php8.3@8.3.6-0ubuntu0.24.04.5?arch=source&distro=noble"
         },
         "ranges": [
           {
             "type": "ECOSYSTEM",
             "events": [
               {
                 "introduced": "0"
               },
               {
                 "fixed": "8.3.6-0ubuntu0.24.04.5"
               }
             ]
           }
         ],
         "versions": [
           "8.3.0-1",
           "8.3.0-1ubuntu1",
           "8.3.4-1",
           "8.3.4-1build1",
           "8.3.6-0maysync1",
           "8.3.6-0ubuntu0.24.04.1",
           "8.3.6-0ubuntu0.24.04.2",
           "8.3.6-0ubuntu0.24.04.3",
           "8.3.6-0ubuntu0.24.04.4"
         ],
         "ecosystem_specific": {
           "binaries": [
             {
               "binary_name": "libapache2-mod-php8.3",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "libphp8.3-embed",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-bcmath",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-bz2",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-cgi",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-cli",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-common",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-curl",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-dba",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-enchant",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-fpm",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-gd",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-gmp",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-imap",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-interbase",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-intl",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-ldap",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-mbstring",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-mysql",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-odbc",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-opcache",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-pgsql",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-phpdbg",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-pspell",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-readline",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-snmp",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-soap",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-sqlite3",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-sybase",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-tidy",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-xml",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-xsl",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             },
             {
               "binary_name": "php8.3-zip",
               "binary_version": "8.3.6-0ubuntu0.24.04.5"
             }
           ],
           "availability": "No subscription required"
         }
       },
       {
         "package": {
           "ecosystem": "Ubuntu:25.04",
           "name": "php8.4",
           "purl": "pkg:deb/ubuntu/php8.4@8.4.5-1ubuntu1.1?arch=source&distro=plucky"
         },
         "ranges": [
           {
             "type": "ECOSYSTEM",
             "events": [
               {
                 "introduced": "0"
               },
               {
                 "fixed": "8.4.5-1ubuntu1.1"
               }
             ]
           }
         ],
         "versions": [
           "8.4.1-5",
           "8.4.2-1ubuntu1",
           "8.4.4-1",
           "8.4.5-1",
           "8.4.5-1ubuntu1"
         ],
         "ecosystem_specific": {
           "binaries": [
             {
               "binary_name": "libapache2-mod-php8.4",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "libphp8.4-embed",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-bcmath",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-bz2",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-cgi",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-cli",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-common",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-curl",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-dba",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-enchant",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-fpm",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-gd",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-gmp",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-interbase",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-intl",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-ldap",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-mbstring",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-mysql",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-odbc",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-opcache",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-pgsql",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-phpdbg",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-readline",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-snmp",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-soap",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-sqlite3",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-sybase",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-tidy",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-xml",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-xsl",
               "binary_version": "8.4.5-1ubuntu1.1"
             },
             {
               "binary_name": "php8.4-zip",
               "binary_version": "8.4.5-1ubuntu1.1"
             }
           ],
           "availability": "No subscription required"
         }
       }
     ],
     "references": [
       {
         "type": "REPORT",
         "url": "https://ubuntu.com/security/CVE-2025-6491"
       },
       {
         "type": "REPORT",
         "url": "https://www.cve.org/CVERecord?id=CVE-2025-6491"
       },
       {
         "type": "REPORT",
         "url": "https://github.com/php/php-src/security/advisories/GHSA-453j-q27h-5p8x"
       },
       {
         "type": "ADVISORY",
         "url": "https://ubuntu.com/security/notices/USN-7648-1"
       }
     ]
   }

The ``id`` field
----------------

We mentioned in :ref:`osv-data` the available vulnerability data. Each type
can be easily identified with the ``id`` field:

* **Ubuntu CVE Records:** The ``id`` is of the form ``UBUNTU-CVE-...``
* **Ubuntu Security Notices:** The ``id`` is of the form ``USN-...``
* **Livepatch Security Notices:** The ``id`` is of the form ``LSN-...``

.. note::
   **Why aren't Ubuntu CVE Records identified as CVE-...?**

   IDs in OSV need to be exclusive. The ``CVE-...`` id is already reserved for
   the data synced from the CVE Program. Therefore, Ubuntu CVE records have the
   ``UBUNTU-`` prefix.

The ``upstream`` field
----------------------

The OSV documentation describes it as: "The ``upstream`` field gives a list of
IDs of upstream vulnerabilities that are referred to by the vulnerability
entry."

For Ubuntu OSV data, this means:

* **Ubuntu CVE Records:** The upstream field contains the exact ``CVE-...``
  that matches the ``UBUNTU-CVE-...``. For example, ``UBUNTU-CVE-2025-6194``
  has:

  .. code-block:: json

     "upstream": [
       "CVE-2025-6491"
     ],

* **Ubuntu Security Notices:** The upstream field contains the list of Ubuntu
  CVE Records that were fixed in this USN. For example, ``USN-7548-1`` has:

  .. code-block:: json

     "upstream": [
       "UBUNTU-CVE-2023-52969",
       "UBUNTU-CVE-2023-52970",
       "UBUNTU-CVE-2023-52971",
       "UBUNTU-CVE-2025-30693",
       "UBUNTU-CVE-2025-30722"
     ],

* **Livepatch Security Notices:** Much like USNs, its ``upstream`` field
  contains a list of Ubuntu CVE Records fixed in that LSN. For example,
  ``LSN-0112-1`` has:

  .. code-block:: json

     "upstream": [
       "UBUNTU-CVE-2021-47506",
       "UBUNTU-CVE-2022-0995",
       "UBUNTU-CVE-2023-52664",
       "UBUNTU-CVE-2024-26689",
       "UBUNTU-CVE-2024-35864",
       "UBUNTU-CVE-2024-50302",
       "UBUNTU-CVE-2024-53063",
       "UBUNTU-CVE-2024-53150",
       "UBUNTU-CVE-2024-53168",
       "UBUNTU-CVE-2024-53197",
       "UBUNTU-CVE-2024-56551",
       "UBUNTU-CVE-2024-56593",
       "UBUNTU-CVE-2024-56595",
       "UBUNTU-CVE-2024-56598",
       "UBUNTU-CVE-2024-56653",
       "UBUNTU-CVE-2024-57798"
     ],

The ``severity`` field
----------------------

This field contains a list of severities of different types. It currently
supports CVSS entries and Ubuntu priorities. More severity types might be
added later, but for Ubuntu, those are the ones that matter to us and our
users.

.. note::
   Severity information is only available for Ubuntu CVE Records. This is
   because any USN or LSN can relate to one or more CVEs, and OSV currently
   doesn't have a standardized way to map the list of severities to their
   respective CVEs. Therefore, we recommend always evaluating USNs and LSNs
   in conjunction with the corresponding Ubuntu CVE records.

Ubuntu priority
^^^^^^^^^^^^^^^

If you aren't familiar with Ubuntu Priority, see `our explanation of it here
<https://ubuntu.com/security/cves/about#priority>`_.

The severity field is a list of items, where each item has a ``type`` and a
``score``. For Ubuntu priority, the ``type`` is ``Ubuntu`` and the ``score``
is a lowercase string matching one of our priorities:

* critical
* high
* medium
* low
* negligible

For example, for ``UBUNTU-CVE-2025-6491``:

.. code-block:: json

   "severity": [
     {
       "type": "Ubuntu",
       "score": "medium"
     }
   ],

CVSS severity
^^^^^^^^^^^^^

If you are familiar with CVSS, you probably know that there are different
versions of it, V4 being the latest. OSV supports the following CVSS
``type``:

* CVSS_V2
* CVSS_V3
* CVSS_V4

For the ``score``, we have the actual CVSS vector string related to such
vulnerability.

For example, for ``UBUNTU-CVE-2025-6491`` we have:

.. code-block:: json

   "severity": [
     {
       "type": "CVSS_V3",
       "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H"
     }
   ],

The ``withdrawn`` field
-----------------------

We create some Ubuntu CVE records for new vulnerabilities that might later be
rejected by the CVE program (for example, if they aren't actual security
issues). In those cases, instead of removing the data, we use the
``withdrawn`` field to indicate that the CVE record has been removed.

This field gives the time the entry should be considered withdrawn, as an
RFC3339-formatted timestamp in UTC (ending in "Z"). If the field is missing,
the entry hasn't been withdrawn.

The ``affected`` field
----------------------

The affected field is a list of objects where you will find the bulk of the
information regarding source packages and Ubuntu releases, as well as
vulnerable versions and patch status.

The ``package`` field
^^^^^^^^^^^^^^^^^^^^^

This field identifies which Ubuntu release is being reported (``ecosystem``
field), the source package name (``name``), and the package URL (``purl``
field). We will mostly focus on ``ecosystem`` and ``name`` fields, but if you
want to know more about package URL, check its `spec
<https://github.com/package-url/purl-spec>`_.

The Ubuntu ``ecosystem``
~~~~~~~~~~~~~~~~~~~~~~~~

As part of the list of affected packages, the ``ecosystem`` field helps
describe where that package entry is affected. For currently supported Ubuntu
releases, we use the following pattern:

``Ubuntu:YY.MM<:LTS>``

Here, ``YY.MM`` relates to the Ubuntu release number and ``:LTS`` is a suffix
to specify if the release is an LTS or not.

* Ubuntu 24.04 LTS (Noble Numbat) is represented as:

  .. code-block:: json

     "ecosystem": "Ubuntu:24.04:LTS",

* Ubuntu 25.04 (Plucky Puffin) is represented as:

  .. code-block:: json

     "ecosystem": "Ubuntu:25.04",

For fixes distributed via :ref:`esm`, we add a positional ``:Pro:`` entry to
the ecosystem.

* Ubuntu 18.04 LTS (Bionic Beaver) is represented as:

  .. code-block:: json

     "ecosystem": "Ubuntu:Pro:18.04:LTS"

Ubuntu Pro includes more services besides ESM, like FIPS, Livepatch, and
others. Below is a current list of Ubuntu Pro services for which we have
vulnerability data:

* Ubuntu:Pro:14.04:LTS
* Ubuntu:Pro:16.04:LTS
* Ubuntu:Pro:18.04:LTS
* Ubuntu:Pro:20.04:LTS
* Ubuntu:Pro:22.04:LTS
* Ubuntu:Pro:24.04:LTS
* Ubuntu:Pro:22.04:LTS:Realtime:Kernel
* Ubuntu:Pro:24.04:LTS:Realtime:Kernel
* Ubuntu:Pro:FIPS:16.04:LTS
* Ubuntu:Pro:FIPS:18.04:LTS
* Ubuntu:Pro:FIPS:20.04:LTS
* Ubuntu:Pro:FIPS-updates:18.04:LTS
* Ubuntu:Pro:FIPS-updates:20.04:LTS
* Ubuntu:Pro:FIPS-updates:22.04:LTS
* Ubuntu:Pro:FIPS-preview:22.04:LTS

If you are still unsure if a fix was released under Pro, check the
``ecosystem_specific`` field, which describes when a Pro subscription is
required. For example:

.. code-block:: json

   "ecosystem_specific": {
     "availability": "Available with Ubuntu Pro: https://ubuntu.com/pro"
   }

The ``name`` field
~~~~~~~~~~~~~~~~~~

This field specifies the **source package name**. The Ubuntu Security Team
tracks vulnerabilities and patches them in source packages. Binary packages
(those that you install with ``apt-get``) are generated from building a source
package.

Source package names aren't as useful for users as binary package names.
Therefore, to simplify reading, as well as automation or scanning, we add the
list of binary packages and their versions under the ``ecosystem_specific``
field. For example, for ``php8.4``:

.. code-block:: json

   "ecosystem_specific": {
     "binaries": [
       {
         "binary_name": "libapache2-mod-php8.4",
         "binary_version": "8.4.5-1ubuntu1.1"
       },
       {
         "binary_name": "libphp8.4-embed",
         "binary_version": "8.4.5-1ubuntu1.1"
       },
       {
         "binary_name": "php8.4",
         "binary_version": "8.4.5-1ubuntu1.1"
       },
       ...
       {
         "binary_name": "php8.4-zip",
         "binary_version": "8.4.5-1ubuntu1.1"
       }
     ],
     "availability": "No subscription required"
   }

For LSNs, there's no particular source package patching involved. Since the
kernel is patched during runtime via a kernel module, we list a regular
expression for the kernel module instead. For example `LSN-0113-1
<https://github.com/canonical/ubuntu-security-notices/blob/main/osv/lsn/LSN-0113-1.json>`_:

.. code-block:: json

   "ecosystem_specific": {
     "availability": "Livepatch subscription required",
     "module_name_regex": "lkp_Ubuntu_4_4_0[_|\\d]+_(?:generic|lowlatency)_(\\d+)"
   }

The ``ranges`` field
^^^^^^^^^^^^^^^^^^^^

The ``ranges`` field specifies the ``type`` of versioning scheme being used in
an ecosystem and the events of when a vulnerability was ``introduced``,
``fixed``, and any type-specific fields.

Since Debian versioning is not yet a supported type in OSV, the ``type`` will
always be ``ECOSYSTEM``.

The Ubuntu Security Team doesn't currently track when a vulnerability was
first introduced. Instead, we focus on identifying which of the shipped source
package versions are vulnerable to such CVE. Therefore, the ``introduced``
field is always ``0``. Whenever the team patches a vulnerability, the source
package version is listed in ``fixed``.

For example, a ranges entry:

.. code-block:: json

   "ranges": [
     {
       "type": "ECOSYSTEM",
       "events": [
         {
           "introduced": "0"
         },
         {
         "fixed": "8.4.5-1ubuntu1.1"
         }
       ]
     }
   ],

The ``versions`` field
^^^^^^^^^^^^^^^^^^^^^^

This field contains a list of source package versions that are affected by the
vulnerability in scope for a given Ubuntu release. For example:

.. code-block:: json

   "versions": [
     "8.4.1-5",
     "8.4.2-1ubuntu1",
     "8.4.4-1",
     "8.4.5-1",
     "8.4.5-1ubuntu1"
   ],

Mapping Ubuntu CVE Tracker statuses in OSV
==========================================

Now that you have a better understanding of Ubuntu's OSV data, you might want
to know how to map the status from Ubuntu's CVE tracker (`Web
<https://ubuntu.com/security/cves>`_ and/or `git
<https://code.launchpad.net/ubuntu-cve-tracker>`_) to OSV.

For any given vulnerability (CVE), the Ubuntu Security Team tracks a source
package in the different Ubuntu releases that are supported. For any
combination of source package and Ubuntu release, we assign a status.

Here is a recap of the `statuses
<https://git.launchpad.net/ubuntu-cve-tracker/tree/README#n295>`_ in the git
version of the tracker:

* ``DNE``: Acronym for Does Not Exist. It means that the specific source
  package is not present (or supported) in that Ubuntu release.
* ``not-affected``: The source package (for the given release), while related
  to the CVE in some way, is not affected by the vulnerability. This can happen
  for many reasons, such as:
    * The vulnerable code isn't present in that version of the source package.
    * The source package is only vulnerable in a different OS.
    * The vulnerability is for older versions of the source package.
* ``needs-triage``: The Ubuntu Security Team hasn't evaluated the
  vulnerability yet.
* ``needed``: The package in scope is vulnerable to this CVE.
* ``released``: The vulnerability is patched in the specified version.
* ``ignored``: The Ubuntu Security Team isn't going to patch this
  vulnerability. This can happen for multiple reasons, such as:
    * The Ubuntu release is end-of-life.
    * The actual fix is hard to backport and can lead to regressions.
* ``pending``: The fix is currently ready and just awaiting publishing.
* ``deferred``: As of the date of investigation, the source package is known
  to be vulnerable but there is no fix available upstream.
* ``in-progress``: This is a rather new field and hasn't been used so far. Its
  intent is to show when a vulnerability fix is actively being worked on.

Now let's map the statuses from ``git`` to the `Web statuses
<https://ubuntu.com/security/cves/about#statuses>`_, as the latter has a more
human-readable and simplified status. We also show how this appears in the OSV
``affected`` field.

For a given Ubuntu release and source package:

.. csv-table::
   :header: "git tracker", "Web tracker", "OSV"
   :widths: auto

   "DNE", "Not in release", "Won't be listed under affected"
   "not-affected", "Not affected", "Won't be listed under affected"
   "needs-triage", "Needs evaluation", "Listed under affected and fixed is not set"
   "needed", "Vulnerable", "Listed under affected and fixed is not set"
   "released", "Fixed", "Listed under affected and fixed is set"
   "ignored", "Ignored", "Listed under affected and fixed is not set"
   "pending", "Vulnerable, work in progress", "Listed under affected and fixed is not set"
   "deferred", "Vulnerable, fix deferred", "Listed under affected and fixed is not set"
   "in-progress", "Vulnerable, work in progress", "Listed under affected and fixed is not set"

.. note::
   We recommend that users and partners use one of our data formats (OSV, OVAL,
   VEX) instead of trying to consume the information directly from the Web
   tracker or git tracker, as those tend to change and can even be replaced
   over time.

Reporting issues in the data
============================

If you find any inconsistencies with Ubuntu's OSV data, send an email to
``security@ubuntu.com``. We will gladly analyze and fix any issues.

Downtimes in data generation
============================

Like any other service, we might need to take our data generation offline for
updates, server maintenance, and so forth. We will deliver those announcements
at the top of this `page <https://security-metadata.canonical.com/osv/>`_.
