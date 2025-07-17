Snap confinement
################

A snap's confinement level controls the degree of isolation it has from the
user's system. Application developers or packagers can adjust the confinement
level to specify in broad terms how much access to system resources an
application needs, either for normal use or during development.

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
access.

Configuration access
^^^^^^^^^^^^^^^^^^^^

Note that any unprivileged user can retrieve configuration values set for the
snap (values configured using ``sudo snap set``).

Interfaces
^^^^^^^^^^

To gain access to certain resources provided by other snaps or on the host
system, the snap ecosystem introduces the concept of interfaces. Interfaces
consist of:

* **Slots:** Used by snaps or the system (implicit slot) to expose resources.
* **Plugs:** Used by snaps to consume access to resources exposed by a slot.

See `Interfaces <https://snapcraft.io/docs/interfaces>`_ for more details.

Interface connections
"""""""""""""""""""""

By connecting a plug with a slot, the snap that defines the plug gets access to
the resource provided by the slot. Interface connections can occur manually or
automatically, depending on the function of the interface. Manual connections
require users to use the ``snap connect`` command. Snapd handles
auto-connections whenever you install or refresh a snap.

For example, the ``home`` interface connects automatically, but it excludes
hidden files and directories (those starting with a dot) by default.

See `Interface auto-connection mechanism
<https://snapcraft.io/docs/auto-connection-mechanism>`_ for more details.

Interface privileges
""""""""""""""""""""

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

Classic
-------

You declare classic confinement in ``snapcraft.yaml`` through ``confinement:
classic``. These snaps have no confinement and allow access to the system's
resources in much the same way traditional packages do. Because of this, manual
review is required to publish this type of snap. Since the host does not
isolate these types of snaps, they may run into binary incompatibilities at
runtime much like any other third-party package.

Note that Ubuntu Core systems **do not support** running ``classic`` snaps.

Devmode
-------

You declare devmode confinement in ``snapcraft.yaml`` through ``confinement:
devmode``. Developers use this level of confinement during snap development.
Devmode runs snaps similarly to strictly confined snaps. However, instead of
limiting access to host system resources, it produces debug output. This
enables developers to identify what access or interfaces the snap might need to
run as strictly confined.

To facilitate debugging, you can install snaps with ``strict`` confinement
using the ``--devmode`` argument (for example, ``snap install <snap_name>
--devmode``).


Confinement mechanisms
======================

AppArmor
--------

Snapd generates AppArmor profiles for each app (a particular way of invoking an
executable) and service (daemon managed by snapd) defined in a snap package.
Declaring interfaces in the snap allows the default AppArmor profile to be
extended. `This default profile
<https://github.com/canonical/snapd/blob/8105ec1a7395c7a0c0126a4fff66a063d326c3f1/interfaces/apparmor/template.go#L63>`_
defines a common set of rules applied to all snaps by default.

For example, when a snap plugs the camera interface, the system adds `this
profile
<https://github.com/canonical/snapd/blob/8105ec1a7395c7a0c0126a4fff66a063d326c3f1/interfaces/builtin/camera.go#L32>`_
to extend the default policy. Snapd regenerates the AppArmor profiles for a
snap whenever you connect or disconnect an interface.

AppArmor confinement specificities might differ depending on the kernel version
running on the host.

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

Device cgroups
--------------

For snaps using bases ``core24`` and later, snapd uses cgroups only to manage
access to device files through the `device controller
<https://docs.kernel.org/admin-guide/cgroup-v2.html#device-controller>`_
mechanism. The device controller implementation uses a BPF program of type
``BPF_PROG_TYPE_CGROUP_DEVICE`` attached to the cgroup.

Prior to ``core24``, the system manages access to device files using `device
filtering <https://docs.kernel.org/admin-guide/cgroup-v1/devices.html>`_. It
adds device filtering only when udev tags any devices for that snap. The
interfaces used by a snap (for example, `custom-device
<https://snapcraft.io/docs/custom-device-interface>`_) determine this. The
system generates udev rules in ``/etc/udev/rules.d/70-snap...`` and adds tags
to the devices (hardware) associated with the use of this interface. If a snap
has tagged devices, the system creates a cgroup in ``/sys/fs/cgroup/devices/``
to allow access to these devices and other common devices (for example,
``/dev/null``).

Snapd regenerates the device cgroups for a snap whenever you connect or
disconnect an interface.

Regarding the eBPF attachment: if systemd executes the process, the eBPF
program attaches to that cgroup. If systemd does not execute the process, the
system creates a transient scope for each process.

See :doc:`cgroups` for more details.

Capabilities and credentials
----------------------------

The ``snap-confine`` tool does not set the ``nonewprivs`` flag. Consequently,
the process keeps all credentials, including additional groups.

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

All processes from the same snap exist in the same mount namespace to ensure
isolation from separate snaps. When a snap refreshes, the system creates a new
mount namespace. These namespaces use shared mounts, meaning mount events
could propagate to the namespace of the init process (PID 1).

Traditional permissions
-----------------------

Processes inside the snap that try to access resources are restricted by the
typical file permissions on the system (owner, group, file ACLs, and so on).

See `Security overview
<https://snapcraft.io/docs/security-policies#p-2741-security-overview>`_ for
more details.
