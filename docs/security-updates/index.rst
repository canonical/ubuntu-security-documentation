Security updates
################

..
  FIXME: may be useful to introduce documentation links to SRU and the updates
  pocket.

Ubuntu is a fixed-release Linux distribution. As such, Ubuntu releases receive
security updates during the support window in the form of backported patches.
This means that security updates will not generally introduce new functionality
and stability is achieved by maintaining backward compatibility. Please note
that some packages in Ubuntu will receive feature updates through the Stable
Release Update process, but this is orthogonal to the delivery of security
updates.

..
  FIXME: this might also be documented elsewhere. It would be good to also
  reference what LTS and interim releases are.

The level of security support depends on the component in which a
package resides (``Main``, ``Restricted``, ``Universe`` or ``Multiverse``). The
Ubuntu Security Team is responsible for preparing security updates for supported
Ubuntu releases and working with the community to sponsor community-prepared
security updates. The following table lists the security maintenance window for
Ubuntu releases.

.. list-table::
   :header-rows: 1
   
   * - Release type
     - Main / Restricted
     - Universe / Multiverse
   * - Interim (standard support)
     - 9 months
     - Community-supported
   * - LTS (standard support)
     - 5 years
     - Community-supported
   * - LTS (ESM support - with Ubuntu Pro)
     - 10 years
     - 10 years
   * - LTS (ESM + Legacy support - with Ubuntu Pro)
     - 12 years
     - FIXME


Delivery
========

Security updates are delivered through special-purpose pockets in the Ubuntu
archive. For standard support, the ``security`` pocket is used, available from
http://security.ubuntu.com/ubuntu with a suite name that follows the
``RELEASE-security`` naming convention. For example, the following APT
sources configuration in DEB822 format will configure the ``security`` pocket
on the ``Main`` and ``Universe`` components for Ubuntu 24.04 LTS Noble Numbat:

.. code-block:: none

   Types: deb
   URIs: http://security.ubuntu.com/ubuntu/
   Suites: noble-security
   Components: main universe
   Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg


Security updates available with a Ubuntu Pro subscription are delivered through
a different Archive pocket. The configuration is detailed in the `ESM
<esm/>`_ section


Vulnerability tracking
======================

The Ubuntu Security Team manages information about vulnerabilities in Ubuntu
packages through the `Ubuntu CVE Tracker (UCT)
<https://launchpad.net/ubuntu-cve-tracker>`_. Vulnerability data is imported
from various sources, including the CVE Program, allowing vulnerabilities to be
referenced through CVE IDs. UCT contains information about known
vulnerabilities, even when security updates are not yet available.
Vulnerabilities under an embargo are not included, as this is a public project,
but are added to UCT upon public disclosure. You can find more information and
associated data processing tools in the project's `Git repository
<https://git.launchpad.net/ubuntu-cve-tracker>`_.

Additionally, all vulnerability data available in UCT can be browsed in the `CVE
reports <https://ubuntu.com/security/cves>`_ section of the Ubuntu website.


Ubuntu Security Notices
=======================

Upon publication of security updates for packages in the Ubuntu Archive, the
Ubuntu Security Team publishes Ubuntu Security Notices (USNs) that contain
information about the vulnerability and affected packages. You can browse all
Ubuntu Security Notices on the `website <https://ubuntu.com/security/notices>`_
or subscribe to the `Ubuntu Security Announce mailing list
<https://lists.ubuntu.com/mailman/listinfo/ubuntu-security-announce>`_ to
receive email notifications whenever Ubuntu Archive security updates are made
available.


Vulnerability knowledge base
============================

Detailed technical information on high-impact, publicly-disclosed
vulnerabilites, including available mitigation steps, is published in the
`Vulnerability knowledge base <https://ubuntu.com/security/vulnerabilities>`_
section of the Ubuntu website.


Data feeds
==========

Information on the available security updates can be obtained in several
industry-standard machine-readable formats: OVAL, OSV and VEX. These data feeds
facilitate the integration of automated patching tools and vulnerability
management scanners by incorporating information on the vulnerabilities that
each security update addresses, including by referencing the Common
Vulnerabilities and Exposures (CVE) enumeration through CVE IDs. The data feeds
are freely available for all supported releases and their use documented in
the respective sections, below.

ESM
===

.. toctree::
   :maxdepth: 2

   esm/index   


Livepatch
=========

.. toctree::
   :maxdepth: 2

   livepatch/index

OVAL
====

.. toctree::
   :maxdepth: 2

   oval/index

OSV
====

.. toctree::
   :maxdepth: 2

   osv/index

VEX
====

.. toctree::
   :maxdepth: 2

   vex/index
