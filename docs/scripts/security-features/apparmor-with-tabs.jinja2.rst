.. _apparmor:

`AppArmor <AppArmor>`__
~~~~~~~~~~~~~~~~~~~~~~~

.. tabs::

   {% for tab in histories["apparmor"] %}
   .. group-tab:: {{ tab.release.only_version() }}

      {{ tab.cell }}
   {% endfor %}

`AppArmor <https://help.ubuntu.com/community/AppArmor>`__ is a
path-based MAC. It can mediate:

-  file access (read, write, link, lock)
-  library loading
-  execution of applications
-  coarse-grained network (protocol, type, domain)
-  capabilities
-  coarse owner checks (task must have the same euid/fsuid as the object
   being checked) starting with Ubuntu 9.10
-  mount starting with Ubuntu 12.04 LTS
-  unix(7) named sockets starting with Ubuntu 13.10
-  DBus API (path, interface, method) starting with Ubuntu 13.10
-  signal(7) starting with Ubuntu 14.04 LTS
-  ptrace(2) starting with Ubuntu 14.04 LTS
-  unix(7) abstract and anonymous sockets starting with Ubuntu 14.10

`AppArmor <AppArmor>`__ is a core technology for application confinement
for `Ubuntu
Touch <https://wiki.ubuntu.com/SecurityTeam/Specifications/ApplicationConfinement>`__
and `Snappy for Ubuntu Core and
Personal <https://developer.ubuntu.com/en/snappy/guides/security-policy/>`__.

Example profiles are found in the apparmor-profiles package from
universe, and by-default shipped `enforcing
profiles <SecurityTeam/KnowledgeBase/AppArmorProfiles>`__ are being
built up:

<<Include(`SecurityTeam/KnowledgeBase/AppArmorProfiles <SecurityTeam/KnowledgeBase/AppArmorProfiles>`__,
, from="=== Supported profiles in main ===", to="===")>>

Starting with Ubuntu 16.10, `AppArmor <AppArmor>`__ can "stack" profiles
so that the mediation decisions are made using the intersection of
multiple profiles. This feature, combined with `AppArmor <AppArmor>`__
profile namespaces, allows `LXD <https://linuxcontainers.org/lxd/>`__ to
define a profile that an entire container will be confined with while
still allowing individual, containerized processes to be further
confined with profiles loaded inside of the container environment.

See
`test-apparmor.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-apparmor.py>`__
and
`test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`__
for regression tests.