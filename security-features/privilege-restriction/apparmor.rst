.. Source: https://documentation.ubuntu.com/server/how-to/security/apparmor/

AppArmor
########
.. Source for versions: https://launchpad.net/apparmor/+packages
.. tab-set::

   .. tab-item:: 24.04
    
        4.0.1

   .. tab-item:: 22.04
    
        3.0.4

   .. tab-item:: 20.04
    
        2.13.3

   .. tab-item:: 18.04
    
        2.12

   .. tab-item:: 16.04
    
        2.10.95

   .. tab-item:: 14.04

        2.10.95

`AppArmor <https://apparmor.net/>`__ is a Linux Security Module implementation that restricts applications' capabilities and permissions and supplements the more traditional UNIX model of discretionary access control (DAC).

AppArmor uses **application profiles** to determine the permissions the application process has.

AppArmor is a core technology for Linux Security Module (LSM) on Ubuntu, as well as for `Snappy for Ubuntu Core <https://developer.ubuntu.com/en/snappy/guides/security-policy/>`_.

Discretionary Access Control (DAC) vs. Mandatory Access Control (MAC)
======================================================================

Discretionary Access Control (DAC) is an access control mechanism where an entity (for example, a user, a program, or a group) has specific permissions to perform certain actions (read, write, execute, and so on). It is considered to be the traditional Unix permission model.

Mandatory Access Control (MAC) is an access control mechanism where permissions are explicitly defined by a *policy*. A user or program cannot do more than is allowed by the policy confining it.

An example of MAC would be a system-wide policy that permits this file to be read but never edited.
An example of DAC would be a user that has permissions to read and edit a specific file.

AppArmor is a MAC system and operates on the principle of controlling permissions of applications.

AppArmor architecture 
=====================

AppArmor is an implementation of `Linux Security Module (LSM) <https://www.kernel.org/doc/html/latest/admin-guide/LSM/index.html>`_. It utilizes a *path-based control model* which means that AppArmor rules define permissions for programs based on file path patterns and these paths are used during runtime checks. 

Linux Security Module framework 
-------------------------------

The Linux Security Module (LSM) is a framework in the Linux kernel that allows different security models to hook into the kernel and enforce access control policies. A hook in the kernel is a place in the code where additional logic can be inserted. LSM hook points are predefined in the Linux kernel. They are built into the kernel source code and serve as the official extension points where security modules like AppArmor can plug in their logic.

AppArmor policy enforcement process
-----------------------------------

Once AppArmor policy is defined and AppArmor is initialized, it registers its access control functions by attaching them to predefined LSM hook points.

When a process inside kernel reaches these hook points, the kernel

* intercepts the operation

* looks up a currently active AppArmor profile for the process

* compares access permissions that the process requests with the permissions in AppArmor policy

* denies or allows the request based on the policy in the profile

AppArmor and ``systemd`` 
------------------------

On boot, AppArmor profiles are managed by ``systemd`` directly when it comes to early policy loading. ``systemd`` calls `apparmor_parser` to load AppArmor profiles from the compiled policy cache location `/etc/apparmor/earlypolicy/`.

When early policy is not configured, the rest of the policies are loaded from the default behavior by the AppArmor systemd unit file, typically named ``apparmor.service``, which specifies how AppArmor is started and reloaded. Note that the stop command is intentionally a no-op, because of how the reload command is implemented in `systemd` - typically by a stop followed by a start, and this could lead to tasks operating in an unconfined state after the start. To unload profiles, `aa-teardown` should be used.

See `AppArmor in systemd <https://gitlab.com/apparmor/apparmor/-/wikis/AppArmorInSystemd>`_ for more details.

AppArmor security profiles
==========================

An AppArmor profile is a text file that contains the access rules for an application. It starts with the name of the application followed by the set of rules specifying what it is allowed to do. A profile defines a policy which is compiled and loaded into the kernel. The kernel enforces policy on applications.

Enforcing vs. complain
----------------------

AppArmor profiles have two modes - enforcing and complain. Profiles loaded in enforcing mode enforce the policy and report policy violation attempts via ``syslog`` or ``auditd``. Profiles in complain mode do not enforce policy and only report policy violation attempts. 

Audit logs
----------

Whether the profile is in enforcing or in complain mode, AppArmor logs all access denials. These logs are typically written to the system log (e.g., ``/var/log/syslog`` or ``/var/log/audit/audit.log``).


The logs typically include:

* Process ID (PID)

* Name of the process
  
* Timestamp of the event
  
* Path to the resource the process attempted to access

* Request that was denied (e.g., file read, socket access)

* Profile name applied to the process

Types of confinements
---------------------

File
     AppArmor can limit access to specific files and directories, a process's ability to access files based on file ownership or the ability to mount filesystems. 

Network
     AppArmor can limit what a process can do with network resources, including restricting network access entirely or limiting access to specific protocols, ports, or domains.

Application execution
     AppArmor can limit a process's ability to load shared libraries, execute specific applications, send or receive signals. It can also restrict the use of ptrace. 

Process control
     AppArmor can limit the Linux capabilities a process can acquire, for example, it can prevent a process from getting high-privilege capabilities.

Inter-process communications
      AppArmor can limit which DBus interfaces a process can interact with as well as limit which processes can access named, abstract and anonymous Unix sockets.

To learn more about AppArmor profile language and its capabilities, see `A quick guide to AppArmor profile Language <https://gitlab.com/apparmor/apparmor/-/wikis/QuickProfileLanguage#a-quick-guide-to-apparmor-profile-language>`_


AppArmor unprivileged user namespace restrictions
=================================================

AppArmor can deny unprivileged applications the use of user namespaces, preventing them from gaining additional capabilities and reducing kernel attack surface. Applications requiring unprivileged namespaces must be explicitly allowed by their AppArmor profile. 


Useful resources
================

-  See the `AppArmor Administration
   Guide <http://www.novell.com/documentation/apparmor/apparmor201_sp10_admin/index.html?page=/documentation/apparmor/apparmor201_sp10_admin/data/book_apparmor_admin.html>`__
   for advanced configuration options.
-  For details using AppArmor with other Ubuntu releases see the
   `AppArmor Community
   Wiki <https://help.ubuntu.com/community/AppArmor>`__ page.
-  The `OpenSUSE AppArmor <http://en.opensuse.org/SDB:AppArmor_geeks>`__
   page is another introduction to AppArmor.
-  (https://wiki.debian.org/AppArmor) is another introduction and basic
   how-to for AppArmor.
-  A great place to get involved with the Ubuntu Server community and to
   ask for AppArmor assistance is the ``\#ubuntu-server`` IRC channel on
   `Libera <https://libera.chat>`__. The ``\#ubuntu-security`` IRC channel may also be of use.
