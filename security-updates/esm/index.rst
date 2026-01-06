.. _esm:

Expanded Security Maintenance (ESM)
###################################

Ubuntu Pro extends the standard security maintenance scope for Ubuntu LTS
releases through the `Extended Security Maintenance (ESM)
<https://ubuntu.com/security/esm>`_ service. The product description defines
the duration and level of support.


Configuration
=============

You can enable ESM through the Pro client after attaching a Pro subscription, as
described in the `Pro Client Documentation
<https://documentation.ubuntu.com/pro/account-setup/>`_.

Ubuntu distributions deliver ESM security updates via the same mechanism as all
packages. You can use ``apt``, ``apt-get``, ``aptitude``, or any other APT
frontend to apply them. The Pro client manages the correct APT sources in
``/etc/apt/sources.list.d/``. Manage this according to the instructions in the
`Pro Client ESM Documentation
<https://documentation.ubuntu.com/pro/pro-client/enable_esm_infra/>`_.

We use special-purpose Archive pockets for ESM updates. The ``Infra`` pockets
cover packages in the ``Main`` component, while the ``Apps`` pockets cover
packages in the ``Universe`` component. Both are accessible from
https://esm.ubuntu.com.

The following is an APT sources configuration file in DEB822 format set up by
the Pro client for Ubuntu 24.04 LTS (Noble Numbat) with ESM Infra support:

.. code-block:: none

   # Written by ubuntu-pro-client
   Types: deb
   URIs: https://esm.ubuntu.com/infra/ubuntu
   Suites: noble-infra-security noble-infra-updates
   Components: main
   Signed-By: /usr/share/keyrings/ubuntu-pro-esm-infra.gpg

The following is an APT sources configuration file in DEB822 format set up by
the Pro client for Ubuntu 24.04 LTS (Noble Numbat) with ESM Apps support:

.. code-block:: none

   # Written by ubuntu-pro-client
   Types: deb
   URIs: https://esm.ubuntu.com/apps/ubuntu
   Suites: noble-apps-security noble-apps-updates
   Components: main
   Signed-By: /usr/share/keyrings/ubuntu-pro-esm-apps.gpg


Security notices
================

We communicate security updates delivered through ESM via standard `Ubuntu
Security Notices <../#ubuntu-security-notices>`_. Notices and associated
`CVE data <https://ubuntu.com/security/cves>`_ clearly mark updates available
only through Ubuntu Pro.


Repository pinning
==================

The Ubuntu Pro client automatically `pins the priority
<https://help.ubuntu.com/community/PinningHowto>`_ of packages distributed via
the ESM pockets to ``510``. This is slightly higher than the default priority
of ``500``.

This ensures the system prefers ESM updates over updates from standard pockets.
It avoids the risk of rolling back security fixes delivered through ESM via a
standard update that has a higher version number but doesn't contain the
ESM security fixes. This is particularly important when you enable the
``updates`` or ``backports`` pockets.

The client deploys this configuration in the following APT preferences files:

* ``/etc/apt/preferences.d/ubuntu-pro-esm-infra``
* ``/etc/apt/preferences.d/ubuntu-pro-esm-apps``
