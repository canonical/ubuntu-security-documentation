Security updates
################

Ubuntu is a fixed-release Linux distribution. As such, Ubuntu releases receive
security updates during the support window in the form of backported patches.
This means that security updates won't generally introduce new
functionality, and we achieve stability by maintaining backward compatibility.
Note that some packages in Ubuntu receive feature updates through the Stable
Release Update process, but this is independent of security updates.

The level of security support depends on the component in which a package
resides (``Main``, ``Restricted``, ``Universe`` or ``Multiverse``). The Ubuntu
Security Team prepares security updates for supported Ubuntu releases and works
with the community to sponsor community-prepared security updates. The
following table lists the security maintenance window for Ubuntu releases. You
can read more about the Ubuntu release cycle `here
<https://ubuntu.com/about/release-cycle>`_.

.. list-table::
   :header-rows: 1

   * - Support type
     - Main / Restricted
     - Universe / Multiverse
     - Ubuntu Pro required
   * - Interim
     - 9 months
     - Community support only (9 months)
     - ✕
   * - LTS
     - 5 years
     - Community support only (5 years)
     - ✕
   * - LTS + ESM infra only
     - 10 years
     - Community support only (5 years)
     - ✓
   * - LTS + ESM infra and apps
     - 10 years
     - 10 years
     - ✓
   * - LTS + ESM infra and apps + ESM Legacy
     - 15 years
     - 15 years
     - ✓

Ubuntu Pro is a subscription that provides access to several security-focused
features and services. You can read more about it `here <https://documentation.ubuntu.com/pro/>`_.


Delivery
========

We deliver security updates through special-purpose pockets in the Ubuntu
archive. For standard support, we use the ``security`` pocket, available from
http://security.ubuntu.com/ubuntu with a suite name that follows the
``RELEASE-security`` naming convention. For example, the following APT sources
configuration in DEB822 format configures the ``security`` pocket on the
``Main`` and ``Universe`` components for Ubuntu 24.04 LTS (Noble Numbat):

.. code-block:: none

   Types: deb
   URIs: http://security.ubuntu.com/ubuntu/
   Suites: noble-security
   Components: main universe
   Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

We deliver security updates available with an Ubuntu Pro subscription
through a different Archive pocket. The configuration is detailed in the `ESM
<esm/>`_ section.


Vulnerability tracking
======================

The Ubuntu Security Team manages information about vulnerabilities in Ubuntu
packages through the `Ubuntu CVE Tracker (UCT)
<https://launchpad.net/ubuntu-cve-tracker>`_. UCT imports vulnerability data
from various sources, including the CVE Program, allowing you to reference
vulnerabilities through CVE IDs. UCT contains information about known
vulnerabilities, even when security updates are not yet available. It
doesn't include vulnerabilities under an embargo, as this is a public
project, but adds them upon public disclosure. You can find more information
and associated data processing tools in the project's `Git repository
<https://git.launchpad.net/ubuntu-cve-tracker>`_.

Additionally, you can browse all vulnerability data available in UCT in the
`CVE reports <https://ubuntu.com/security/cves>`_ section of the Ubuntu
website.


Ubuntu Security Notices
=======================

Upon publication of security updates for packages in the Ubuntu Archive, the
Ubuntu Security Team publishes Ubuntu Security Notices (USNs) that contain
information about the vulnerability and affected packages. You can browse all
Ubuntu Security Notices on the `website
<https://ubuntu.com/security/notices>`_ or subscribe to the `Ubuntu Security
Announce mailing list
<https://lists.ubuntu.com/mailman/listinfo/ubuntu-security-announce>`_ to
receive email notifications whenever Ubuntu Archive security updates are made
available.

Vulnerability knowledge base
============================

We publish detailed technical information on high-impact, publicly disclosed
vulnerabilities, including available mitigation steps, in the `Vulnerability
knowledge base <https://ubuntu.com/security/vulnerabilities>`_ section of the
Ubuntu website.

Data feeds
==========

You can obtain information on available security updates in several
industry-standard, machine-readable formats: OVAL, OSV, and VEX. These data
feeds facilitate the integration of automated patching tools and vulnerability
management scanners by incorporating information on the vulnerabilities that
each security update addresses, including by referencing the Common
Vulnerabilities and Exposures (CVE) enumeration through CVE IDs. The data feeds
are freely available for all supported releases and their use is documented in
the respective sections below.

ESM
===

.. toctree::
   :maxdepth: 2

   esm/index

Livepatch
=========

The Canonical Livepatch service provides security fixes for most major kernel
security issues without requiring a reboot.

* `Livepatch <https://ubuntu.com/security/livepatch/docs>`_

OVAL
====

.. toctree::
   :maxdepth: 2

   oval/index

OSV
===

.. toctree::
   :maxdepth: 2

   osv/index

VEX
===

.. toctree::
   :maxdepth: 2

   vex/index

Automatic security updates
==========================

Starting with Ubuntu 16.04 LTS (Xenial Xerus), we configure
``unattended-upgrades`` to automatically apply security updates daily. You can
`configure
<https://ubuntu.com/server/docs/package-management#automatic-updates>`__
earlier Ubuntu releases to automatically apply security updates.
