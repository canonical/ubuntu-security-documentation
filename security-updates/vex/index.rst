Ubuntu VEX data
###############

The Ubuntu Security Team publishes vulnerability data conforming to the structured, human and machine-readable Vulnerability Exploitability eXchange (VEX) format for all supported Ubuntu releases. In particular, the Ubuntu VEX
data feed follows the `OpenVEX <https://openvex.dev/>`_ specification, maintained by `OpenSSF <https://openssf.org/>`_. OpenVEX is an open source, minimal, compliant, interoperable, and embeddable implementation of VEX, that Canonical chose for clarity and ease of use.

As with the other vulnerability data feeds, Ubuntu's VEX data can be used in vulnerability and patch management processes.

The VEX data describes the exploitability status of known, publicly disclosed vulnerabilities, focusing on clarifying whether these are exploitable in
specific configurations.

The goal of the data is to provide users with additional information on whether a product is impacted by a specific vulnerability in an included component and, if affected, whether there are actions recommended to remediate the threat. 
In many cases, a vulnerability in an upstream component will not be “exploitable” in the final product for various reasons, and this is the gap that VEX data covers.

Available VEX data
==================

The following types of vulnerability data are available in the VEX format:

* CVE records, which mirror the per-vulnerability information available in the `Ubuntu Security Tracker <https://ubuntu.com/security/cves>`_ and contain information for known, publicly-disclosed vulnerabilities, even if security updates are not yet available. 
  
* Ubuntu Security Notices (USNs), which contain `announcements <https://ubuntu.com/security/notices>`_ of available security updates and the
  vulnerabilities they address.

VEX data for Ubuntu releases is available from two official sources:

* The `Canonical security metadata page <https://security-metadata.canonical.com/vex/>`_, as a compressed tarball updated whenever changes to the vulnerability are made available.

* The `Ubuntu Security Notices GitHub repository <https://github.com/canonical/ubuntu-security-notices>`_, under the ``vex`` directory, with individual JSON files for each CVE record or USN.

Understanding VEX data
======================
The VEX format, although easy to parse, might still be difficult to interpret. The next sections cover the relevant details of the data we publish.

To facilitate understanding, consider the following OpenVEX data file of `CVE-2025-5994 <https://github.com/canonical/ubuntu-security-notices/blob/main/vex/cve/2025/CVE-2025-5994.json>`_:

.. code:: JSON

  {
    "metadata": {
      "@context": "https://openvex.dev/ns/v0.2.0",
      "@id": "https://github.com/canonical/ubuntu-security-notices/blob/main/vex/cve/2025/CVE-2025-5994",
      "author": "Canonical Ltd.",
      "timestamp": "2025-07-23T05:12:19.020044",
      "version": 3
    },
    "statements": [
      {
        "vulnerability": {
          "@id": "https://nvd.nist.gov/vuln/detail/CVE-2025-5994",
          "name": "CVE-2025-5994",
          "description": "A multi-vendor cache poisoning vulnerability named 'Rebirthday Attack' has been discovered in caching resolvers that support EDNS Client Subnet (ECS). Unbound is also vulnerable when compiled with ECS support, i.e., '--enable-subnet', AND configured to send ECS information along with queries to upstream name servers, i.e., at least one of the 'send-client-subnet', 'client-subnet-zone' or 'client-subnet-always-forward' options is used. Resolvers supporting ECS need to segregate outgoing queries to accommodate for different outgoing ECS information. This re-opens up resolvers to a birthday paradox attack (Rebirthday Attack) that tries to match the DNS transaction ID in order to cache non-ECS poisonous replies.",
          "aliases": [
            "https://www.cve.org/CVERecord?id=CVE-2025-5994",
            "https://nlnetlabs.nl/downloads/unbound/CVE-2025-5994.txt",
            "https://ubuntu.com/security/notices/USN-7666-1",
            "https://ubuntu.com/security/CVE-2025-5994"
          ]
        },
        "timestamp": "2025-07-17",
        "products": [
          {
            "@id": "pkg:deb/ubuntu/unbound@1.13.1-1ubuntu5.11?arch=amd64"
          },
          {
            "@id": "pkg:deb/ubuntu/unbound@1.19.2-1ubuntu3.5?arch=amd64"
          },
          {
            "@id": "pkg:deb/ubuntu/unbound@1.22.0-1ubuntu1.1?arch=amd64"
          },
        ],
        "status": "fixed",
        "status_notes": "This package (for the given release) was vulnerable, but an update has been uploaded and published."
      },
      {
        "vulnerability": {
          "@id": "https://nvd.nist.gov/vuln/detail/CVE-2025-5994",
          "name": "CVE-2025-5994",
          "description": "A multi-vendor cache poisoning vulnerability named 'Rebirthday Attack' has been discovered in caching resolvers that support EDNS Client Subnet (ECS). Unbound is also vulnerable when compiled with ECS support, i.e., '--enable-subnet', AND configured to send ECS information along with queries to upstream name servers, i.e., at least one of the 'send-client-subnet', 'client-subnet-zone' or 'client-subnet-always-forward' options is used. Resolvers supporting ECS need to segregate outgoing queries to accommodate for different outgoing ECS information. This re-opens up resolvers to a birthday paradox attack (Rebirthday Attack) that tries to match the DNS transaction ID in order to cache non-ECS poisonous replies.",
          "aliases": [
            "https://www.cve.org/CVERecord?id=CVE-2025-5994",
            "https://nlnetlabs.nl/downloads/unbound/CVE-2025-5994.txt",
            "https://ubuntu.com/security/notices/USN-7666-1",
            "https://ubuntu.com/security/CVE-2025-5994"
          ]
        },
        "timestamp": "2025-07-17",
        "products": [
          {
            "@id": "pkg:deb/ubuntu/unbound@1.4.22-1ubuntu4.14.04.3+esm2?arch=amd64"
          },
          {
            "@id": "pkg:deb/ubuntu/unbound@1.5.8-1ubuntu1.1+esm2?arch=amd64"
          },
          {
            "@id": "pkg:deb/ubuntu/unbound@1.6.7-1ubuntu2.6+esm3?arch=amd64"
          },
        ],
        "status": "under_investigation",
        "status_notes": "The vulnerability of this package (for the given release) is not known and needs to be evaluated."
      }
    ]
  }

Each CVE entry associated with a particular package and release has a status in the `Ubuntu CVE Tracker (UCT) <https://launchpad.net/ubuntu-cve-tracker>`_, and a relevant status in the `Ubuntu Security Webpage <https://ubuntu.com/security/cves>`_. The following table details how these statuses are translated into OpenVEX fields within the vulnerability metadata:

+---------------+--------------------------+------------------------------------------------------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| UCT Status    | Web tracker status       | Canonical explanation                                                              | OpenVEX status      | OpenVEX action_statement / justification / impact_statement / status_notes                                                                                                       |
+===============+==========================+====================================================================================+=====================+==================================================================================================================================================================================+
| not-affected  | Not affected             | Source code is not affected                                                        | not_affected        | justification: vulnerable_code_not_present. impact_statement: The package is not affected by this CVE. CVE notes / justification: [...]                                          |
+---------------+--------------------------+------------------------------------------------------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| DNE           | Not in release           | CVE entry for this package does not exist                                          | not_affected        | justification: component_not_present. impact_statement: The package does not exist in the archive for this release.                                                              |
+---------------+--------------------------+------------------------------------------------------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| needs-triage  | Needs evaluation         | CVE has not yet been evaluated                                                     | under_investigation | status_notes: Vulnerability assessment is pending.                                                                                                                               |
+---------------+--------------------------+------------------------------------------------------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| deferred      | Vulnerable, fix deferred | CVE fix is currently deferred as a patch is not available                          | under_investigation | status_notes: The vulnerability is known but remediation is deferred. CVE notes / justification: [...]                                                                           |
+---------------+--------------------------+------------------------------------------------------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| needed        | Vulnerable               | CVE needs to be patched                                                            | affected            | action_statement: The package is vulnerable and needs fixing.                                                                                                                    |
+---------------+--------------------------+------------------------------------------------------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ignored       | Ignored                  | Canonical Security Engineering team or upstream has ignored this CVE               | affected            | action_statement: This package is vulnerable to the CVE, the problem is understood, but the Ubuntu Security Team decided to not fix it. CVE notes / justification: [...]         |
+---------------+--------------------------+------------------------------------------------------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| released      | Fixed                    | Canonical Security Engineering team has fixed the CVE and released the new version | fixed               | status_notes: A fix has been published. Additional notes provided if the fix is part of Ubuntu Pro (e.g., esm-infra, esm-apps).                                                  |
+---------------+--------------------------+------------------------------------------------------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

The *CVE notes / justification* information is provided by the Ubuntu CVE Tracker and is being actively maintained by the Ubuntu Security Team.

When it comes to USN (Ubuntu Security Notices) VEX data, the documents will only state the CVE entries that were fixed as a result of the update. Thus, it is expected that every statement in a USN VEX document will have a **fixed** status.
The *status_notes* will indicate if the update is widely available, or if you need an Ubuntu Pro subscription.

Limitations of the standard
===========================

One limitation of the OpenVEX standard is the lack of a standard Severity field in the vulnerability metadata. This limits a user or system ingesting the data from knowing the severity and the prioritization of the remediation of the vulnerability without resorting to additional data sources.
Our workaround for this limitation is adding more information in the *status_notes* field to inform about the severity of a CVE (following the `Ubuntu Priority schema <https://ubuntu.com/security/cves/about#priority>`_) in a programmatically parsable manner.

Using VEX data
==============

As a standardized, machine-friendly format, the VEX data feed can be used by any vulnerability management tool that supports it. More specifically, OpenSSF maintains `vexctl <https://github.com/openvex/vexctl>`_, an open source tool to create, apply and attest OpenVEX documents.

OpenVEX can also act as a complimentary to SBOMs (Software Bill of Materials) by providing precise metadata about vulnerability status of products mentioned in them. For example, `cycloneDX <https://cyclonedx.org/>`_ SBOMs support the integration of OpenVEX data.

Reporting issues in the data
============================

If at any point you encounter inconsistencies with Ubuntu's VEX data, please report those by sending an email to **security@ubuntu.com**. We will gladly analyze and fix any issues.

Downtimes in data generation
============================

As any other service, we might need to take our data generation offline to perform updates or server maintenance. Those announcements will be delivered in the top of this `page <https://security-metadata.canonical.com/vex/>`_.