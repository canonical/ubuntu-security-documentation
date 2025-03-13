.. Source: https://documentation.ubuntu.com/server/how-to/security/apparmor/

AppArmor
########

.. tab-set::

   .. tab-item:: 24.04
    
        3.0.7 

   .. tab-item:: 22.04
    
        3.0.7

   .. tab-item:: 20.04
    
        3.0.7

   .. tab-item:: 18.04
    
        3.0.4

   .. tab-item:: 16.04
    
        2.13.3

   .. tab-item:: 14.04

        -

`AppArmor <https://apparmor.net/>`__ is a  Linux Security Module implementation that restricts applications’ capabilities and permissions with **profiles** that are set per-program. It provides
mandatory access control (MAC) to supplement the more traditional UNIX model of discretionary access control (DAC).

It uses **profiles** of an application to determine what files and permissions the application requires. Some packages will install their own profiles, and additional profiles can be found in the
``apparmor-profiles`` package.

AppArmor controls:

- File access (read, write, link, lock)
- Library loading
- Application execution
- Coarse-grained network access (protocol, type, domain)
- Capabilities
- Coarse owner checks (starting with Ubuntu 9.10)
- Mount operations (starting with Ubuntu 12.04 LTS)
- Unix(7) named sockets (starting with Ubuntu 13.10)
- DBus API (starting with Ubuntu 13.10)
- Signal(7) (starting with Ubuntu 14.04 LTS)
- Ptrace(2) (starting with Ubuntu 14.04 LTS)
- Unix(7) abstract and anonymous sockets (starting with Ubuntu 14.10)

AppArmor is a core technology for `Ubuntu Touch <https://wiki.ubuntu.com/SecurityTeam/Specifications/ApplicationConfinement>`_ and `Snappy for Ubuntu Core <https://developer.ubuntu.com/en/snappy/guides/security-policy/>`_.

AppArmor regression tests 
--------------------------

- `test-apparmor.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-apparmor.py>`_
- `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_

AppArmor Unprivileged User Namespace Restrictions
=================================================

AppArmor can deny unprivileged applications the use of user namespaces, preventing them from gaining additional capabilities and reducing kernel attack surface. Applications requiring unprivileged namespaces must be explicitly allowed by their AppArmor profile. 


Further reading
---------------

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
   `Libera <https://libera.chat>`__. The ``\#ubuntu-security`` IRC
   channel may also be of use.