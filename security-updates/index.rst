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

The level of security support depends on the component in which a package
resides (``Main``, ``Restricted``, ``Universe`` or ``Multiverse``). The Ubuntu
Security Team is responsible for preparing security updates for supported
Ubuntu releases and working with the community to sponsor community-prepared
security updates. The following table lists the security maintenance window for
Ubuntu releases. You can read more about the Ubuntu release cycle `here
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
     - 12 years
     - 12 years
     - ✓

Ubuntu Pro is a subscription that provides access to several security-focused
features and services. You can read more about it in the `Ubuntu Pro
documentation </pro/services-overview/>`_.

Update Notifications
====================

Ubuntu users receive notifications when new updates are available as part of
the ``update-manager`` package (which is known as ``Software & Updates`` in the
desktop menu). Users can use it to configure the notifications, manage updates,
as well as manage automatic update settings (with more information in the
"Automatic security updates" section below)

For Ubuntu Server, users can choose to install ``update-notifier-common``,
which will notify about pending updates through the message of the day (motd)
upon logging into the system with the following commands:

.. code-block:: bash

   sudo apt-get update
   sudo apt-get -y install update-notifier-common

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
vulnerabilities, including available mitigation steps, is published in the
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

The Canonical Livepatch service provides security fixes for most major kernel
security issues without requiring a reboot.

* `Livepatch <https://ubuntu.com/security/livepatch/docs>`_

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

Automatic security updates
==========================

Starting with Ubuntu 16.04 LTS, unattended-upgrades is configured to
automatically apply security updates daily. Earlier Ubuntu releases can be
`configured
<https://ubuntu.com/server/docs/package-management#automatic-updates>`__ to
automatically apply security updates. Updates, by default, will be installed
after 24 hours for security updates or 7 days for normal updates.

Automatic updates can be managed through the internal ``Software & Updates``
graphical application available in the menu, or through the default
configuration file found in ``/etc/apt/apt.conf.d/50unattended-upgrades``,
which contains explanations for each option available to be modified. Through
the configuration file you are able to adjust more advanced options, such as
enabling automatic reboot when needed, along with the automatic reboot time, as
well as logging capabilities.

.. NOTE::

   Automatic updates through ``unattended-upgrades`` are only configured by
   default for archive and ESM repositories. In order to configure automatic
   updates for third party repositories and PPAs, editing the
   ``/etc/apt/apt.conf.d/50unattended-upgrades`` file is required.

The operations of ``unattended-upgrades`` are logged in
``/var/log/unattended-upgrades/unattended-upgrades.log``.
