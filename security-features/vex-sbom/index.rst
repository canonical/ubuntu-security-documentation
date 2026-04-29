Using an SBOM with Ubuntu VEX data
####################################

An SBOM (Software Bill of Materials) gives you an inventory of every software
package present in a container, system or application. Ubuntu's OpenVEX data 
gives you the vulnerability and patch status for every package in the Ubuntu
archive. Cross-referencing the two produces an accurate, up-to-date list of
open vulnerabilities for any Ubuntu-based system or workload.

This guide explains how to perform that cross-reference: how to obtain Ubuntu
VEX data, how to identify packages using Package URLs (PURLs), and how to match
them to find open vulnerabilities.


Why use Ubuntu VEX data rather than a generic vulnerability database?
===============================================

Generic vulnerability databases (such as the NVD or GitHub Advisory Database) report 
vulnerabilities at the level of the upstream software component. 
They may flag a vulnerability as affecting ``curl`` without accounting for whether
the version shipped in Ubuntu is actually vulnerable. 
The Ubuntu Security team regularly applies targeted patches,
backports fixes, or determines that upstream vulnerabilities do not affect the
Ubuntu build. Thus, the following scenarios are common:

* A vulnerability may be listed as "affected" in the NVD but "not affected" in Ubuntu
  because the vulnerable code path is absent from the Ubuntu package or has
  already been patched.
* A vulnerability may already be fixed in an Ubuntu security update whose status does not
  yet propagate to third-party databases. Those updates result in version bumps
  with `+ubuntuX.Y` suffixes, which are not recognized by generic databases.

Ubuntu's VEX data reflects the **actual, current status** of each vulnerability for each
specific Ubuntu package version as tracked by the Ubuntu CVE Tracker (UCT). It
is the most accurate single source for Ubuntu-specific vulnerability
intelligence, and avoids both false positives and false negatives compared to
generic databases.


Scope
=====

This guide covers vulnerability information for software installed from the
Ubuntu archive in Debian binary package (``.deb``) format, including:

* Packages installed via ``apt`` on Ubuntu systems.
* Packages included in Ubuntu-based container images.
* Packages included in snap builds that include Debian packages from the Ubuntu archive.
* Any software built from Ubuntu source packages.

VEX data is published for all supported Ubuntu releases. Non-Ubuntu packages
present in your SBOM (for example, packages from a third-party repository or
compiled from source) will not have matching entries in the Ubuntu VEX data.


Prerequisites
=============

To follow this guide you need:

* An SBOM in a machine-readable format such as CycloneDX JSON or SPDX JSON,
  **or** the name and installed version of the Ubuntu packages you want to
  check, along with the Ubuntu release information.
* The Ubuntu VEX data, obtained as described below.
* (Optional) A JSON parsing tool such as ``jq`` or Python 3 for querying the data.


Obtaining Ubuntu VEX data
==========================

Ubuntu's VEX data is published in OpenVEX JSON format. There are two official
sources:

* The `Canonical security metadata page
  <https://security-metadata.canonical.com/vex/>`_, which provides a
  compressed tarball of all vulnerability records, updated continuously as vulnerability
  assessments are made or changed.
* The `Ubuntu Security Notices GitHub repository
  <https://github.com/canonical/ubuntu-security-notices>`_, under the ``vex``
  directory, with an individual JSON file for each CVE.

Download and extract the tarball. The exact file name is listed on the metadata
page:

.. code-block:: bash

   wget https://security-metadata.canonical.com/vex/vex-all.tar.xz
   mkdir -p ubuntu-vex && tar -xf vex-all.tar.xz -C ubuntu-vex

Once extracted, the data is organised as one JSON file per CVE under
``vex/cve/<year>/``.

Due to the size of the `ubuntu-security-notices` repository, the most practical
solution for a local setup is to download the tarball and perform queries 
against the extracted JSON files. The rest of this guide assumes you have the
VEX data available locally through extraction from the tarball, 
but you can also query the GitHub repository directly if preferred.

Matching against an SBOM created at a point in time
-----------------------------------------------------

VEX data is updated continuously. If you are auditing an SBOM that was
generated at a specific point in the past, using the current VEX data may
report vulnerabilities that did not exist yet when the SBOM was created, or
miss vulnerabilities that have since been resolved. To reproduce the
vulnerability state as it was when the SBOM was generated, check out the
``ubuntu-security-notices`` repository at the corresponding commit.

Clone the repository (using ``--filter=blob:none`` to avoid downloading the
full history of large files):

.. code-block:: bash

   git clone --filter=blob:none \
     https://github.com/canonical/ubuntu-security-notices.git
   cd ubuntu-security-notices

Find the commit that was current at the time the SBOM was created. If the SBOM
records its creation timestamp, use it directly with ``git log``:

.. code-block:: bash

   git log --oneline --before="2024-11-01T00:00:00Z" -1

Check out the repository at that commit:

.. code-block:: bash

   git checkout <commit-hash>

The ``vex/`` directory now reflects the vulnerability data as it was at that
point in time. Run your cross-reference queries against ``vex/cve/`` as usual.

To return to the latest data afterwards:

.. code-block:: bash

   git checkout main

Identifying packages: working with PURLs
=========================================

Both Ubuntu's VEX data and modern SBOMs use `Package URLs (PURLs)
<https://github.com/package-url/purl-spec>`_ to uniquely identify packages.
A PURL for an Ubuntu Debian package takes the form:

.. code-block::

   pkg:deb/ubuntu/<name>@<version>?arch=<arch>&distro=<distro>

For example:

.. code-block::

   pkg:deb/ubuntu/curl@7.81.0-1ubuntu1.23?arch=amd64&distro=jammy  

The qualifiers (``?arch=…`` and ``&distro=…``) are optional in the PURL specification, and some
tools omit them. The version field must be **the full Debian version string**,
including the revision suffix (for example, ``-1ubuntu1.23``), to uniquely
identify the package build successfully.


Extracting PURLs from your SBOM
---------------------------------

If your SBOM already contains PURLs for Ubuntu packages, extract them before
matching against the VEX data.

**CycloneDX JSON** example component entry:

.. code-block:: json

   {
     "type": "library",
     "name": "curl",
     "version": "7.81.0-1ubuntu1.23",
     "purl": "pkg:deb/ubuntu/curl@7.81.0-1ubuntu1.23?arch=amd64&distro=jammy"
   }

Extract all Ubuntu package PURLs from a CycloneDX SBOM with ``jq`` or similar JSON query tool:

.. code-block:: bash

   jq -r '.. | objects | .purl? | select(. and startswith("pkg:deb/ubuntu/"))' \
     sbom.cdx.json

**SPDX JSON** example package entry:

.. code-block:: json

   {
     "SPDXID": "SPDXRef-curl",
     "name": "curl",
     "versionInfo": "7.81.0-1ubuntu1.23",
     "externalRefs": [
       {
         "referenceCategory": "PACKAGE-MANAGER",
         "referenceType": "purl",
         "referenceLocator": "pkg:deb/ubuntu/curl@7.81.0-1ubuntu1.23?arch=amd64&distro=jammy"
       }
     ]
   }

Extract all Ubuntu package PURLs from an SPDX SBOM with ``jq`` or similar JSON query tool:

.. code-block:: bash

   jq -r '.packages[].externalRefs[]? |
     select(.referenceType == "purl" and
            (.referenceLocator | startswith("pkg:deb/ubuntu/"))) |
     .referenceLocator' sbom.spdx.json


Constructing a PURL from SBOM fields when no PURL is present
--------------------------------------------------------------

If your SBOM contains Ubuntu packages without a ``purl`` external
reference, you can construct one from the standard package fields.
The minimum required fields are ``name`` and ``versionInfo``. Architecture
and distro allow a more precise PURL as there might be the same package version in two
different Ubuntu releases, or a specific architecture might be vulnerable while another is not.
However, those fields are optional for VEX matching (see `PURL matching considerations`_ below).

**SPDX JSON**

``name`` and ``versionInfo`` are top-level fields on every SPDX package
entry. To extract them for all packages that lack a PURL:

.. code-block:: bash

   jq -r '.packages[] |
     select(
       ((.externalRefs // []) |
        map(select(.referenceType == "purl")) |
        length) == 0
     ) |
     "\(.name)\t\(.versionInfo)"' sbom.spdx.json

Architecture is not a top-level SPDX field. It may appear in places like these:

* A CPE 2.3 external reference, in the ``target_hw`` position (the twelfth
  colon-delimited field):

  .. code-block:: json

     {
       "referenceCategory": "SECURITY",
       "referenceType": "cpe23Type",
       "referenceLocator": "cpe:2.3:a:haxx:curl:7.81.0-1ubuntu1.23:*:*:*:*:*:amd64:*"
     }

* A package annotation whose ``comment`` contains the architecture, for
  example ``arch=amd64``.

  .. code-block:: json

     {
       "annotationType": "OTHER",
       "annotator": "Tool: sbom-generator",
       "comment": "arch=amd64"
     }

The Ubuntu release codename (for example, ``jammy``) is not stored per-package
in SPDX. It is typically recorded in one of these locations:

* A top-level ``packages`` entry for the operating system itself, whose
  ``name`` is ``ubuntu`` and whose ``versionInfo`` contains the codename or
  version number.
* A document-level annotation on the SBOM.

**CycloneDX JSON**

``name`` and ``version`` are top-level fields on every CycloneDX component
entry. To extract them for all components that lack a ``purl`` field:

.. code-block:: bash

   jq -r '.components[] |
     select(.purl == null or .purl == "") |
     "\(.name)\t\(.version)"' sbom.cdx.json

Architecture in CycloneDX is stored in the ``properties`` array. Common
property names used by SBOM generators include ``arch``, ``dpkg:architecture``,
and ``syft:package:arch``. For example:

.. code-block:: json

   {
     "name": "curl",
     "version": "7.81.0-1ubuntu1.23",
     "properties": [
       { "name": "dpkg:architecture", "value": "amd64" }
     ]
   }

Extract the architecture from the ``dpkg:architecture`` property with ``jq``:

.. code-block:: bash

   jq -r '.components[] |
     select(.purl == null or .purl == "") |
     .name as $name |
     ((.properties // [])[] | select(.name == "dpkg:architecture") | .value) as $arch |
     "\($name)\t\($arch)"' sbom.cdx.json

The Ubuntu release codename is not stored per-component in CycloneDX. It is
typically found in one of these locations:

* The ``metadata.component`` object, which describes the subject of the SBOM
  (for example, the container image or system). Its ``name`` or ``version``
  field may contain the Ubuntu codename or version string.
* A component of ``type: operating-system`` in the ``components`` array,
  whose ``name`` is ``ubuntu`` and whose ``version`` contains the codename.

Extract the distro codename from an operating-system component with ``jq``:

.. code-block:: bash

   jq -r '.components[] |
     select(.type == "operating-system" and (.name | ascii_downcase | startswith("ubuntu"))) |
     .version' sbom.cdx.json

Once you have the name, version, architecture, and distro, assemble the PURL
in the form ``pkg:deb/ubuntu/<name>@<version>?arch=<arch>&distro=<distro>``.


Finding open vulnerabilities
=============================

With a list of PURLs and the Ubuntu VEX data, you can determine which vulnerabilities
affect your packages. The algorithm is:

#. For each PURL in your package list:

   a. Search the VEX data for statements where a product ``@id`` matches your
      PURL (ignoring the ``?arch=…`` qualifier if needed for robustness).
   b. From the matching statements, keep only those with status ``affected``
      or ``under_investigation``. These represent open vulnerabilities.
   c. Record the vulnerability name, status, and any available notes.

#. Report the collected vulnerabilities as the open vulnerability list.

.. _PURL matching considerations:

PURL matching considerations
-----------------------------

When comparing PURLs from your SBOM with those in the VEX data, keep in mind:

* **Qualifiers** (the ``?key=value`` part) are optional. Implementations
  should compare PURLs with qualifiers stripped unless explicitly filtering by
  architecture.
* **Case sensitivity:** The PURL scheme (``pkg``) and type (``deb``) are case-insensitive; the
  package name and version are case-sensitive.
* **Exact version match:** Each VEX statement records a specific package
  version. Using a different version string (for example, a shortened one)
  will not match.

Instead of handling these edge cases manually with string operations, the
upstream `packageurl-python <https://github.com/package-url/packageurl-python>`_
library provides spec-compliant parsing and normalisation. Install it with:

.. code-block:: bash

   python3 -m pip install packageurl-python

``PackageURL.from_string()`` parses any PURL string into its structured
components (``type``, ``namespace``, ``name``, ``version``, ``qualifiers``,
``subpath``), handling case normalisation and encoding according to the spec.

This makes it straightforward to compare two PURLs while intentionally
ignoring qualifiers:

.. code-block:: python

   from packageurl import PackageURL

   def purl_key(raw: str):
       """Return a comparable (type, namespace, name, version) tuple from a PURL string.

       Qualifiers and subpath are intentionally excluded so that
       ``pkg:deb/ubuntu/curl@7.81.0-1ubuntu1.23?arch=amd64&distro=jammy`` and
       ``pkg:deb/ubuntu/curl@7.81.0-1ubuntu1.23`` compare as equal.
       Returns None for unparseable PURLs.
       """
       try:
           p = PackageURL.from_string(raw)
           return (p.type, p.namespace or '', p.name, p.version)
       except ValueError:
           return None

The Python example below uses this approach.

Example: automated search with Python
---------------------------------------

The following Python function accepts either a list of PURLs 
(which can either be retrieved by an SBOM or be provided in a plaintext file),
and reports all open vulnerabilities from the Ubuntu VEX data directory.

.. code-block:: python

   #!/usr/bin/env python3
   """Cross-reference an SBOM or PURL list with Ubuntu VEX data.

   Requires: pip install packageurl-python
   """

   import json
   from pathlib import Path
   from packageurl import PackageURL


   def find_open_vulnerabilities(purls: list[str], vex_dir: str) -> list[dict]:
       """Return open vulnerabilities from VEX data matching the given PURLs."""
       targets = {purl_key(p) for p in purls} - {None}
       findings = []

       for vex_file in Path(vex_dir).rglob('*.json'):
           try:
               data = json.loads(vex_file.read_text())
           except (json.JSONDecodeError, OSError):
               continue

           for statement in data.get('statements', []):
               if statement.get('status') not in ('affected', 'under_investigation'):
                   continue

               for product in statement.get('products', []):
                   if purl_key(product.get('@id', '')) in targets:
                       vuln = statement.get('vulnerability', {})
                       findings.append({
                           'cve': vuln.get('name', 'unknown'),
                           'purl': product['@id'],
                           'status': statement['status'],
                           'notes': (
                               statement.get('status_notes')
                               or statement.get('action_statement')
                               or ''
                           ),
                       })
                       break  # No need to check other products in this statement

       return sorted(findings, key=lambda x: x['cve'])


Interpreting the results
=========================

Each result will then contain a CVE identifier, a status value from the Ubuntu CVE
Tracker, and (where available) advisory notes. The statuses relevant to open
vulnerabilities are:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Status
     - Meaning
   * - ``affected``
     - The package is confirmed vulnerable. Either a fix has not yet been
       released, or the Ubuntu Security team has decided not to fix the issue
       in this release.
   * - ``under_investigation``
     - The vulnerability has been acknowledged but the Ubuntu Security team
       has not yet completed its assessment for this specific package version.

For completeness, the statuses filtered out (because they represent resolved
vulnerabilities) are:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Status
     - Meaning
   * - ``fixed``
     - A security update has been released. Installing the update resolves the
       vulnerability.
   * - ``not_affected``
     - The package is not vulnerable, for example because the vulnerable code
       path is absent from the Ubuntu build, the upstream version is not affected,
       or the package does not exist in this release.


Severity information
---------------------

The OpenVEX specification does not include a standard severity field. Ubuntu's
VEX data encodes severity information within the ``status_notes`` or
``action_statement`` fields in a programmatically parsable format, following the
`Ubuntu Priority schema <https://ubuntu.com/security/cves/about#priority>`_
(critical, high, medium, low, negligible). Refer to
:ref:`Limitations of the standard <vex-limitations-of-the-standard>` in the
Ubuntu VEX data documentation for the exact encoding and how to extract
severity programmatically.


Example use cases
==================

A **security operations or compliance team** managing a fleet of Ubuntu systems
can export an SBOM from each host or image, cross-reference the package list
against the VEX data, and immediately identify which systems carry unpatched
vulnerabilities. Filtering by ``affected`` status and Ubuntu priority gives a
ranked remediation backlog without sifting through false positives from
generic scanners.

An **application security engineer** reviewing an Ubuntu-based container image
before a production release can run the same cross-reference against the image
SBOM to produce a precise list of open vulnerabilities, their severity, and their current
fix status.

A **security scanner developer** integrating Ubuntu support into a scanning tool
can replace or augment NVD lookups with Ubuntu VEX data to provide
Ubuntu-specific verdicts. Rather than flagging every vulnerability that touches an
upstream package name, the tool surfaces only those entries where Ubuntu's own
assessment confirms the package version in question is ``affected`` or
``under_investigation``.


Further information
====================

* `Ubuntu VEX data documentation <https://documentation.ubuntu.com/security/security-updates/vex/>`_
  — full reference for the VEX data format, available data types, and how
  vulnerability statuses are assigned.
* `Ubuntu security data feeds <https://documentation.ubuntu.com/security/security-updates/#data-feeds>`_
  — overview of all machine-readable security data published by Canonical,
  including VEX, OVAL, and OSV.
* `OpenVEX specification <https://openvex.dev/>`_ — the upstream specification
  that Ubuntu's VEX data conforms to.
* `vexctl <https://github.com/openvex/vexctl>`_ — the OpenSSF open source CLI
  for creating, applying, and filtering OpenVEX documents.
* `PURL specification <https://github.com/package-url/purl-spec>`_ — the
  Package URL standard used to identify packages in both SBOMs and VEX data.
* `CycloneDX <https://cyclonedx.org/>`_ — a widely used SBOM format with
  built-in support for VEX integration.
* `SPDX <https://spdx.dev/>`_ — the ISO-standardised SBOM format.
* `Ubuntu CVE Tracker <https://ubuntu.com/security/cves>`_ — the upstream
  source of the vulnerability data published in VEX format.
