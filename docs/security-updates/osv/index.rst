Ubuntu OSV data
***************

Ubuntu's Security Team publishes vulnerability data in the structured, human
and machine-readable `Open Source Vulnerability (OSV)
<https://ossf.github.io/osv-schema/>`_ format for all supported Ubuntu releases.
As with the other vulnerability data feeds, Ubuntu's OSV data can be used in
vulnerability and patch management processes.

.. _osv-data:

Available OSV data
==================

The following types of vulnerability data are available in the OSV format:

* Ubuntu CVE records, which mirror the per-vulnerability information available
  in the `Ubuntu Security Tracker <https://ubuntu.com/security/cves>`_ and
  contains information for known, publicly-disclosed vulnerabilities, even if
  security updates are not yet available.
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


Understanding Ubuntu's OSV Data
===============================

The OSV format, although easy to understand, might still be difficult to
understand what the data is telling you. Therefore the next sections will
go over the important details related to Ubuntu's data.

The ``id`` field
----------------

We metioned in :ref:`osv-data` the available vulnerability data. Each type
can easily be identified with the ``id`` field:

* Ubuntu CVE Records: the ``id`` is of the form ``UBUNTU-CVE-...``
* Ubuntu Security Notices: the ``id`` is of the form ``USN-...``
* Livepatch Security Notices: the ``id`` is of the form ``LSN-...``

.. NOTE::
   Why aren't Ubuntu CVE Records identified as ``CVE-...``?
   Because IDs in OSV need to be exclusive and the ``CVE-...`` id is already
   reserved for the data synced from the CVE Program. Therefore Ubuntu
   CVE records have the ``UBUNTU-`` prefix.

The ``upstream`` field
----------------------

The OSV documentation describes it as:
"The ``upstream`` field gives a list of IDs of upstream vulnerabilities that
are referred to by the vulnerability entry."

What does that actually mean for Ubuntu OSV data is that:

* Ubuntu CVE Records: the upstream field will contain the exact ``CVE-...``
  that matches the ``UBUNTU-CVE-...``. For example ``UBUNTU-CVE-2025-1234``
  will have:

  .. code-block:: JSON

     "upstream": [
       "CVE-2025-1234"
     ],

* Ubuntu Security Notices: the upstream field contain the list of Ubuntu
  CVE Records that were fixed in this USN. For example ``USN-7548-1`` will
  have:

  .. code-block:: JSON

     "upstream": [
       "UBUNTU-CVE-2023-52969",
       "UBUNTU-CVE-2023-52970",
       "UBUNTU-CVE-2023-52971",
       "UBUNTU-CVE-2025-30693",
       "UBUNTU-CVE-2025-30722"
     ],

* Livepatch Security Notices: much like USNs, its ``upstream`` field will
  contain a list of Ubuntu CVE Records that were fix in that LSN. For
  example ``LSN-0112-1``:

  .. code-block:: JSON

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
added later, but for Ubuntu, for now, those are the ones that matter to us
and our users.

.. NOTE::
   Severity information is only available in Ubuntu CVE Records. That is
   because any USN or LSN relates to one or more CVEs and OSV, currently,
   does not have a standardized way to map out of the list of severities
   which CVE it relates to. Therefore we recommend always looking USNs
   and/or LSNs with the corresponding Ubuntu CVE records.

Ubuntu priority
^^^^^^^^^^^^^^^

If you are unfamiliar with Ubuntu Priority, please check
`here <https://ubuntu.com/security/cves/about#priority>`_.

The severity field is pretty simple, it is a list of items, where each
item has a ``type`` and a ``score``. For Ubuntu priority, the ``type``
is ``Ubuntu`` and the ``score`` is a lowercase string matching one of
our priorities:

* critical
* high
* medium
* low
* negligible

For example:

.. code-block:: JSON

   "severity": [
     {
       "type": "Ubuntu",
       "score": "high"
     }
   ],

CVSS severity
^^^^^^^^^^^^^

If you are familiar with CVSS, you probably know there different versions
of it, being the V4 the latest. OSV supports the following CVSS ``type``:

* CVSS_V2
* CVSS_V3
* CVSS_V4

For the ``score`` we have the actual CVSS vector string related to such
vulnerability. For example:

.. code-block:: JSON

   "severity": [
     {
       "type": "CVSS_V4",
       "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N/E:P"
     },
   ]


The ``withdrawn`` field
-----------------------

Some Ubuntu CVE records might be created for new vulnerabilities and after
a while the vulnerability might be rejected by the CVE program since it is
not an actual security issue. In those cases, instead of removing the data
we use the ``withdrawn`` to indicate that such CVE record is removed.

This field gives the time the entry should be considered to have been
withdrawn, as an RFC3339-formatted timestamp in UTC (ending in "Z"). If the
field is missing, then the entry has not been withdrawn.

The ``affected`` field
----------------------

The affected field is a list of objects where you will find the bulk of
the information you are looking for in terms of source packages and
Ubuntu releases, as well as its vulnerable versions and it if was
patched/fixed.

The ``package`` field
^^^^^^^^^^^^^^^^^^^^^

Here in this field is where you will understand which Ubuntu release we are
reporting (``ecosystem`` field), the source package name (``name``) and the
package URL (``purl`` field). We will mostly focus on ``ecosystem`` and
``name`` fields, but if you want to know more about package URL check its
`spec <https://github.com/package-url/purl-spec>`_.

The Ubuntu ``ecosystem``
~~~~~~~~~~~~~~~~~~~~~~~~

As part of the list of affected packages, the ``ecosystem`` field is used to
help describe where that package entry is affected. For currently supported
Ubuntu releases we follow the below pattern:

``Ubuntu:YY.MM<:LTS>``

where ``YY.MM`` relates to the Ubuntu release number and ``:LTS`` is a suffix
to specify if the release is an LTS or not, e.g.:

* Ubuntu 24.04 LTS will be represented as:

.. code-block:: JSON

   "ecosystem": "Ubuntu:24.04:LTS",

* Ubuntu 25.04 will be represented as:

.. code-block:: JSON

   "ecosystem": "Ubuntu:25.04",

For fixes that are distributed via :ref:`esm`, we add a positional ``:Pro:``
entry to the ecosystem, e.g.:

* Ubuntu 18.04 LTS will be represented as:

  .. code-block:: JSON

     "ecosystem": "Ubuntu:Pro:18.04:LTS"

Ubuntu Pro includes more services besides ESM, like FIPS, Livepatch and
others. Below is a current list of Ubuntu Pro services which we have
vulnerability data for:

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

If you are still confused if a fix was released under Pro, we also have a
field under ``ecosystem_specific`` that describes when a Pro subscription
is required. For example:

.. code-block:: JSON

   "ecosystem_specific": {
     "availability": "Available with Ubuntu Pro: https://ubuntu.com/pro"
   }

The ``name`` field
~~~~~~~~~~~~~~~~~~

As mentioned previously, this field is where we specify the **source package
name**. The bold mention is on purpose, as the Ubuntu Security Team tracks
vulnerabilities and patch them in source packages. Binary packages (those that
you install with ``apt-get``) is what is generated from building a source
package.

Even though tracking source packages and having reports for them makes the
Ubuntu Security Team's life easier, for users, they care about binary
packages and to solve that we have a field under ``ecosystem_specific``
where we list all the binaries and their versions. For example, for the
source package ``tomcat9``:

.. code-block:: JSON

   "ecosystem_specific": {
     "binaries": [
       {
         "binary_name": "libtomcat9-java",
         "binary_version": "9.0.70-2ubuntu0.1"
       }
     ]
   }

The ``ranges`` field
^^^^^^^^^^^^^^^^^^^^

It specifies the ``type`` of versioning scheme being used in an ecosystem and
the events of when a vulnerability was ``introduced``, ``fixed``, and any
type-specific fields.

Since Debian versioning is not particularly a type supported in OSV yet, the
``type`` will always be ``ECOSYSTEM``.

For Ubuntu, the Ubuntu Security Team does not currently track when a
vulnerability was first introduced and instead focus on identifying out of
the shipped source package versions, which are vulnerable to such CVE.
Therefore, the ``introduced`` field is always ``0``. And whenever the team
patches a vulnerability, the source package version is listed in ``fixed``.

For example, a ranges entry:

.. code:: JSON

   "ranges": [
     {
       "type": "ECOSYSTEM",
       "events": [
         {
           "introduced": "0"
         },
         {
           "fixed": "9.0.70-2ubuntu0.1"
         }
       ]
     }
   ],

The ``versions`` field
^^^^^^^^^^^^^^^^^^^^^^

This field contains a list of versions of the source package that is affected
by the vulnerability in scope for a given Ubuntu Release. For example,

.. code-block:: JSON

   "versions": [
     "9.0.70-1ubuntu1",
     "9.0.70-2"
   ],

Mapping Ubuntu CVE Tracker statuses in OSV
==========================================

Now that you have a better understanding of Ubuntu's OSV data, you might
still be trying to understand how do you map the status you see in Ubuntu's
CVE tracker (`Web <https://ubuntu.com/security/cves>`_ and/or
`git <https://code.launchpad.net/ubuntu-cve-tracker>`_) to OSV.

For any given vulnerability (CVE), the Ubuntu Security Team will track a
source package in the different Ubuntu releases that are supported. For any
combination of source package and Ubuntu releases, then we assign a status.
First lets do a recap of the
`statuses <https://git.launchpad.net/ubuntu-cve-tracker/tree/README#n295>`_
we have in the git version of the tracker:

* DNE: acronym for Does Not Exist, it means that the specific source package
  is not present (or supported) in that Ubuntu Release

* not-affected: The source package (for the given release), while related to
  the CVE in some way, is not affected by the vulnerability. This can happen
  for many reasons, like:

  * the vulnerable code is not present in that version of the source package
  * the source package is only vulnerable in a different OS
  * the vulnerability is for older versions of the source package

* needs-triage: The Ubuntu Security Team has not evaluated the vulnerability
  yet

* needed: The package in scope is vulnerable to this CVE

* released: The vulnerability is patched in the specified version

* ignored: The Ubuntu Security Team is not going to patch this vulnerability,
  and this can happen for multiple reasons, but just to name a few:

  * Ubuntu release is end-of-life
  * the actual fix is hard to backport and can lead to regressions

* pending: The fix is currently ready and just awaiting publishing

* deferred: As of the date of investigation, the source package is known to
  be vulnerable but there is no fix available on upstream.

* in-progress: This is a rather new field and has not been used so far, but
  its intent is to show when a vulnerability fix is being actively being
  worked on


Now let's map the statuses from ``git`` to the
`Web statuses <https://ubuntu.com/security/cves/about#statuses>`_, as the
latter has a more human-readable and simplified status and also how this
shows up in OSV ``affected`` field. For a given Ubuntu release and source
package:

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

.. NOTE::
   We recommend users and partners to use one of our data formats (OSV, OVAL,
   VEX) instead of trying to consume the information directly from the Web
   tracker or git tracker as those tend to change and can even be replaced
   with time.
   
Reporting issues in the data
============================

If at any point you encounter inconsistencies with Ubuntu's OSV data, please
report those by sending and email to security@ubuntu.com. We will gladly
analyze and fix any issues.

Downtimes in data generation
============================

As any other service, we might need to take our data generation offline for
updates, or for server maintenance and so forth. Those announcements will be
delivered in the top of this `page <https://security-metadata.canonical.com/osv/>`_.
