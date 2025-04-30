Expanded Security Maintenance (ESM)
###################################

Ubuntu Pro extends the scope of the standard security maintenance provided to
Ubuntu LTS releases through the `Extended Security Maintenance (ESM)
<https://ubuntu.com/security/esm>`_ service. The duration and level of support
is defined in the product description.

Configuration
=============

ESM can be enabled through the Pro client once a Pro subscription is attached,
as described in the `Pro Client Documentation
<https://documentation.ubuntu.com/pro/account-setup/>`_.

ESM security updates are delivered through the same mechanism as all packages in
the Ubuntu distribution, allowing ``apt``, ``apt-get``, ``aptitude`` or any
other APT frontend to be used for applying them. The Pro client is responsible
for managing the correct APT sources in ``/etc/apt/sources.list.d/`` and can be
managed according to the instructions in the `Pro Client ESM Documentation
<https://documentation.ubuntu.com/pro/pro-client/enable_esm_infra/>`_.

Special-purpose Archive pockets are used for ESM updates: packages in the
``Main`` component are covered by the ``Infra`` pockets, while packages in the
``Universe`` component are covered by the ``Apps`` pockets, both of which are
accessible from https://esm.ubuntu.com.

The following is an APT sources configuration file in DEB822 format set up by
the Pro client for Ubuntu 24.04 LTS Noble Numbat with ESM Infra support:

.. code-block::

   # Written by ubuntu-pro-client
   Types: deb
   URIs: https://esm.ubuntu.com/infra/ubuntu
   Suites: noble-infra-security noble-infra-updates
   Components: main
   Signed-By: /usr/share/keyrings/ubuntu-pro-esm-infra.gpg


The following is an APT sources configuration file in DEB822 format set up by
the Pro client for Ubuntu 24.04 LTS Noble Numbat with ESM Apps support:

.. code-block::

   # Written by ubuntu-pro-client
   Types: deb
   URIs: https://esm.ubuntu.com/apps/ubuntu
   Suites: noble-apps-security noble-apps-updates
   Components: main
   Signed-By: /usr/share/keyrings/ubuntu-pro-esm-apps.gpg


Security notices
================

Security updates delivered through ESM are communicated through the standard
`Ubuntu Security Notices <../#ubuntu-security-notices>`_. Any updates that
are only available through Ubuntu Pro are clearly marked in the notices and
associated `CVE data <https://ubuntu.com/security/cves>`_.


Repository pinning
==================

The Ubuntu Pro client automatically `pins the priority
<https://help.ubuntu.com/community/PinningHowto>`_ of packages distributed via
the ESM pockets to ``510``, which is slightly higher than the default priority
of ``500``. This ensures that ESM updates are preferred over updates from the
standard pockets and avoids the risk that security fixes delivered through ESM
are rolled back through a standard update that has a higher package version
number than the one available through ESM pockets, but does not contain the ESM
security fixes. This is particularly important when the ``updates`` or
``backports`` pockets are enabled.

This configuration is deployed in the following APT preferences files:

* ``/etc/apt/preferences.d/ubuntu-pro-esm-infra``
* ``/etc/apt/preferences.d/ubuntu-pro-esm-apps``
