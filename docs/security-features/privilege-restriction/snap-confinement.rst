Snap Confinement
================

A snap’s confinement level controls the degree of isolation it has from the user’s system. Application developers or packagers can adjust the confinement level to specify in broad terms how much access to system resources an application needs, either for normal use or during development.

There are multiple levels of snap confinement for snaps:

* Strict
* Classic 
* Devmode

See `Snap Confinement <https://snapcraft.io/docs/snap-confinement#p-29237-confinement-levels>`_ for more details.

In order to achieve confinement, snaps utilise multiple Linux isolation and confinement mechanisms. These are:

* AppArmor
* Seccomp
* Device cgroups
* Traditional permissions 

See `Confinement and isolation mechanisms <https://snapcraft.io/docs/security-policies#p-2741-confinement-and-isolation-mechanisms>`_ for more details.

Confinement Types 
#################

Strict
------

Strict confinement is declared in a snapcraft.yaml through ``confinement: strict``.
This level of confinement utilises all of the confinement mechanisms listed above to ensure the snap executables and data are sandboxed, with limited access.

Interfaces
^^^^^^^^^^

In order to gain access to certain resources on the host system, snap interfaces are used.
Interfaces enable resources from one snap to be shared with another and with the system.

See `Interfaces <https://snapcraft.io/docs/interfaces>`_ for more details.

Classic
-------

Classic confinement is declared in a snapcraft.yaml through ``confinement: classic``.
This level of confinement allows access to the system’s resources in much the same way traditional packages do. Because of this, manual review is required to publish this type of snap.

Devmode
-------

Devmode confinement is declared in a snapcraft.yaml through ``confinement: devmode``.
This level of confinement is used during the development of snaps. 
Devmode runs snaps similarly to strictly confined snaps, however, instead of limiting access to the host system resources, it produces a debug output to enable developers to identify what access or interfaces may be needed for the snap to run as strictly confined.

Confinement Mechanisms
######################

AppArmor
--------

AppArmor profiles are generated for each command in a snap and are used to restrict or allow certain capabilities for each command.
Declaring interfaces in the snap allows the default AppArmor to be extended.
For example, when a snap plugs the camera interface, `this profile <https://github.com/canonical/snapd/blob/master/interfaces/builtin/camera.go#L32>`_ is added to the default policy.

See :doc:`apparmor` for more details.

Seccomp
-------

Similarly to how AppArmor is used for snaps, Seccomp filters are also generated for each command in a snap.
These allow for processes inside the snap to have syscall filtering. Again, these can be extended through the use of snap interfaces.


Device cgroups
--------------

Cgroups are used in snaps to resource limit processes running inside the snap.
Udev rules are generated for each command in a snap.
When a depended interface is used by the snap, a device cgroup may be used in conjunction with the apparmor profile.
However, by default, no devices are tagged and the device cgroup is not used.
