Snap confinement
################

A snap's confinement level controls the degree of isolation the snap processes
have from other processes on the user's system. Snap processes are created
either from apps defined by the snap (executables that the user invokes on the
command line or via the Desktop GUI) or from services defined by the snap
(background processes managed by systemd).

Application developers or packagers can adjust the confinement level to specify
in broad terms how much access to system resources an application needs, either
for normal use or during development.

Snaps use multiple confinement levels:

* Strict
* Classic
* Devmode

See `Snap confinement
<https://snapcraft.io/docs/snap-confinement#p-29237-confinement-levels>`_ for
more details.

To achieve confinement, snaps use multiple Linux isolation and confinement
mechanisms. These are:

* AppArmor
* Seccomp
* Device cgroups
* Capabilities
* Mount namespaces
* Traditional file permissions

See `Confinement and isolation mechanisms
<https://snapcraft.io/docs/security-policies#p-2741-confinement-and-isolation-mechanisms>`_
for more details.


Confinement types
=================

Strict
------

You declare strict confinement in ``snapcraft.yaml`` through ``confinement:
strict``. This level of confinement uses all the confinement mechanisms listed
above to ensure the snap executables and data are sandboxed with limited
access. Access to resources is managed through :ref:`interfaces`.

Classic
-------

You declare classic confinement in ``snapcraft.yaml`` through ``confinement:
classic``. These snaps have no confinement and allow access to the system's
resources in much the same way traditional packages do. Because of this, the
Snap Store Review Team must manually review the snap before publication. Since
snapd does not isolate these types of snaps, they may run into binary
incompatibilities at runtime much like any other third-party package.

Note that `Ubuntu Core <https://documentation.ubuntu.com/core/>`_ systems 
**do not support** running ``classic`` snaps.

Devmode
-------

You declare devmode confinement in ``snapcraft.yaml`` through ``confinement:
devmode``. Developers use this level of confinement during snap development.
Devmode runs snaps similarly to strictly confined snaps. However, instead of
limiting access to host system resources, it produces debug output. This
enables developers to identify what access or :ref:`interfaces` the snap might
need to run as strictly confined.

To facilitate debugging, you can install snaps that had been defined with
``strict`` confinement to use ``devmode`` instead, bypassing all confinement
rules, by adding the ``--devmode`` argument (for example, ``snap install
<snap_name> --devmode``).

.. warning::
   **Security risk**

   Running a snap in devmode disables its security confinement. Do this only
   for trusted snaps when debugging.


.. _interfaces:

Interfaces
==========

To gain access to certain resources provided by other snaps or on the host
system, the snap ecosystem introduces the concept of interfaces. Interfaces
consist of:

* **Slots:** Used by snaps or the system (implicit slot) to expose resources.
* **Plugs:** Used by snaps to consume access to resources exposed by a slot.

These are strictly enforced for "strict" confinement snaps. "Devmode" snaps
only raise warning messages if access to a resource is not granted via any
interface, and "classic" snaps do not apply interfaces at all.

See `Interfaces <https://snapcraft.io/docs/interfaces>`_ for more details.

Interface connections
---------------------

By connecting a plug with a slot, the snap that defines the plug gets access to
the resource provided by the slot. Interface connections can occur manually or
automatically, depending on the function of the interface or whether the snap
was granted auto-connect access to a slot by the Snap Store Review Team (see
`Process for aliases, auto-connections and tracks
<https://forum.snapcraft.io/t/process-for-aliases-auto-connections-and-tracks/455>`_).

Manual connections require users to use the ``snap connect`` command. If a snap
is allowed to auto-connect its plug to a slot, the snapd daemon automatically
grants access to the associated resources whenever you install or refresh a
snap.

Some interfaces are allowed to be auto-connected without a review by the Snap
Store Review Team. For example, the ``home`` interface connects automatically,
but it excludes hidden files and directories (those starting with a dot) by
default.

See `Interface auto-connection mechanism
<https://snapcraft.io/docs/auto-connection-mechanism>`_ for more details.

Interface privileges
--------------------

Some interfaces enable snaps to control or access sensitive or privileged areas
of a system. For example, the ``snapd-control`` interface enables a snap to
communicate with snapd to allow snap removal, installation, and so on. These
are known as "super-privileged" interfaces, and the system takes extra
security measures to restrict or permit access. Using them requires approval
from ``@reviewers`` (the store review team) on the `Snapcraft Forum
<https://forum.snapcraft.io/>`_ and necessitates overriding the default
store-set policy for that interface.

See `Super-privileged interfaces
<https://snapcraft.io/docs/super-privileged-interfaces>`_ for more details.


Confinement mechanisms
======================

The following mechanisms enforce confinement for strict snaps. They do not apply
to classic snaps, and devmode snaps only warn about resource access violations
without blocking them.

AppArmor
--------

Snapd generates AppArmor profiles for each app (a particular way of invoking an
executable) and service (daemon managed by snapd) defined in a snap package.
Declaring interfaces in the snap allows the default AppArmor profile to be
extended. The default profile defines a common set of rules applied to all
snaps by default; for example, in snapd version 2.60, this is defined `here 
<https://github.com/canonical/snapd/blob/release/2.60/interfaces/apparmor/template.go>`_.

For example, when a snap plugs the camera interface, the system adds a specific
profile fragment (for snapd version 2.60, this profile can be viewed `here
<https://github.com/canonical/snapd/blob/release/2.60/interfaces/builtin/camera.go>`_)
to extend the default policy. Snapd regenerates the AppArmor profiles for a snap
whenever you connect or disconnect an interface.

AppArmor confinement specificities might differ depending on the kernel version
running on the host. Certain AppArmor rules might not be enforced if an older
kernel version is running which doesn't support them.

See :doc:`apparmor` for more details.

Seccomp
-------

Snapd also generates Seccomp filters for each app in a snap. These allow for
syscall filtering for processes inside the snap. The system uses an eBPF filter
based on the syscall number and architecture. For specific syscalls, it also
inspects the arguments.

Like AppArmor profiles, you can extend these filters through the use of snap
interfaces. Snapd regenerates the Seccomp filters for a snap whenever you
connect or disconnect an interface.

See :ref:`seccomp-filtering` for more details.

Device access control
---------------------

Snapd implements device access control using mechanisms provided by control
groups (cgroups). The sandbox configures device access filters so that the
snap application can access only permitted devices.

The sandbox selects the exact implementation at runtime depending on whether
the host kernel supports `cgroup v2
<https://docs.kernel.org/admin-guide/cgroup-v2.html#device-controller>`_ or
`cgroup v1 <https://docs.kernel.org/admin-guide/cgroup-v1/devices.html>`_.
When using ``cgroup v2``, the sandbox attaches an eBPF device filter program
to the unique cgroup where the snap application executes. When using ``cgroup
v1``, the sandbox creates a unique group under the device controller hierarchy
and moves the application process to that group.

Snapd assigns devices to snaps as a result of interface connections. It
generates udev rules at ``/etc/udev/rules.d/70-snap.<per-snap-tag>.rules``
that assign a unique, snap-specific tag to every device logically permitted by
a given connected interface.

For snaps using bases ``core24`` and later, the sandbox configures every snap
application with device access control filters during startup. For snaps using
``core22`` and earlier bases, the sandbox only configures device access control
if interface connections have assigned devices to the snap.

The system always allows access to the following devices:

* ``/dev/null``
* ``/dev/zero``
* ``/dev/full``
* ``/dev/random``
* ``/dev/urandom``
* ``/dev/tty``
* ``/dev/console``
* ``/dev/ptmx`` and PTY

Whenever you connect or disconnect an interface from a snap, snapd regenerates
and reloads the udev rules for that snap. A udev integration helper ensures
that active sandboxes are updated.

See :doc:`cgroups` for more details.

Capabilities and credentials
----------------------------

The ``snap-confine`` tool launches the application with the user's credentials,
including any additional groups. It does not set the ``nonewprivs`` kernel
attribute (``PR_SET_NO_NEW_PRIVS``), allowing the process to potentially gain
new privileges during execution (for example, via setuid binaries), subject to
AppArmor confinement.

Generally, a process does not gain new capabilities when executing a snap.
However, a snap service might run as UID 0 (or a specific list of UIDs) with
capabilities, depending on the connected interfaces. AppArmor mediates access
to these capabilities.

Services
--------

Snaps can define services (daemons) that run in the background. These services
are managed by the system's service manager (typically ``systemd``). By
default, services start automatically when you install the snap and restart
whenever the snap is refreshed or updated.

Services operate under the snap's defined confinement level (Strict, Classic,
or Devmode). Snapd generates specific AppArmor profiles and Seccomp filters for
each service to enforce isolation. Unlike interactive applications, services
often run as the ``root`` user (or a dedicated system user), which means they
may hold effective capabilities. Access to these capabilities is strictly
controlled by the interfaces connected to the snap and mediated by AppArmor.

Mount namespaces
----------------

All processes from the same snap normally exist in the same mount namespace to
ensure isolation from separate snaps. When a snap refreshes, the system creates
a new mount namespace, but existing processes will continue to execute in the
old mount namespace. These namespaces use shared mounts, meaning mount events
could propagate bidirectionally between the namespace and the init process (PID
1).

Traditional permissions
-----------------------

Processes inside the snap that try to access resources are restricted by the
typical file permissions on the system (owner, group, file ACLs, and so on).

See `Security overview
<https://snapcraft.io/docs/security-policies#p-2741-security-overview>`_ for
more details.


General considerations
======================

Configuration access
--------------------

Note that any unprivileged user can retrieve configuration values set for the
snap (values configured using ``sudo snap set``).
