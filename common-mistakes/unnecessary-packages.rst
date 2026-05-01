Unnecessary packages
####################

Ubuntu comes with access to tens of thousands of packages through the Ubuntu
archive. This provides not just convenience, but also a trusted distribution
channel for your open source software. Nevertheless, security hardening guides
recommend keeping the install base at a minimum, as each software package has
the potential to increase the attack surface of your system.

We recommend that you handle such advice with care. It is safe to remove
packages that were previously manually-installed and are no longer needed.
However, removing packages that are part of the default installation could
result in unexpected loss of functionality, even when they are not strictly
required. We recommend that you start with the smallest default installation
that suits your needs and add packages on top of that.

This page provides a high-level overview of the package relationships in Ubuntu,
as inherited from Debian via the dpkg and APT package management systems. As the
end-user, it is your decision which packages to have installed, based on the use
cases of the system, as well as your risk tolerance. The example commands use
`APT patterns
<https://manpages.ubuntu.com/manpages/resolute/man7/apt-patterns.7.html>`_ and
the `apt <https://manpages.ubuntu.com/manpages/resolute/man8/apt.8.html>`_
utility, but other package management tools can be similarly used.

Package properties
==================

Ubuntu packages are referenced by name, but they also contain other metadata in
the form of fields, which makes the package management system powerful.

Essential and Priority
----------------------

There are two methods to annotate the relative importance of a package to a
Ubuntu system: the **Essential** and the **Priority** fields.

A small number of packages are marked **Essential**, as without them the package
management system will not work. This is a flag: a package is either
**Essential** or not. These package can be listed with:

.. code-block:: console

    apt list '?essential'

Packages also have a **Priority** field. Note that its use does not strictly
mirror that in Debian. We do not recommend that you use the **Priority** field
to determine which packages to have installed. The possible values are:

- **required**: these are necessary for the system to function. Without one, a
  system, including the package management, may become unusable.

- **important**: these generally form the foundation of a Linux system and
  provide the functionality which users expect to see.

- **standard**: these are generally part of the default Ubuntu installations and
  contain utilities for a fully-fledged experience.

- **optional** and **extra**: these form the vast majority of the Ubuntu
  packages and provide functionality which you may choose to enable via their
  manual installation; they are considered interchangeable for the purpose of
  this page.

Packages with a **Priority** of **required**, but which aren't **Essential** can
be listed with:

.. code-block:: console

    apt list '?priority(required) ?not(?essential)'

Packages that are **Essential** and those with a **Priority** of **required**
must not be uninstalled. While all other packages can be removed, the resulting
lack of functionality may be unexpected and we do not recommend that.

Dependencies
------------

Packages also declare relationships between each other. The dependency
relationships are the ones which dictate the presence of packages on a system
and are described here. `Other relationships
<https://www.debian.org/doc/debian-policy/ch-relationships.html>`_ are outside
the scope of this page. The dependency relationships are of multiple types and
are always declared by the package that requests the presence of another package:

- **Depends**: this is a strict dependency, without which a package cannot
  function.
- **Pre-Depends**: this is similar to a **Depends** relationship, but has
  implications for the order in which the package manager processes the various
  installation phases of the packages. For the purpose of this document, it can
  be treated identically.
- **Recommends**: this is strong recommendation, without which a large part of a
  package's functionality may be unavailable.
- **Suggests**: this is a soft recommendation, the presence of which will
  enhance of functionality of a package, but is not expected to be useful to a
  majority of users.

A package will exist on a system, either because its installation was requested
by a user or because it is a dependency of an installed package. A package does
not need to establish a dependency on an **Essential** package or one with a
**Priority** of **required**, as these are assumed to be installed.

**Recommends** dependencies are treated as necessary by default. This can be
disabled using the ``APT::Install-Recommends`` configuration option.

**Suggests** dependencies are not considered by default. They can be treated as
necessary using the ``APT::Install-Suggests`` configuration option.

Automatic packages
------------------

Packages which are installed automatically by APT as a dependency are marked as
**automatic**. These can be automatically removed once no other necessary
package depends on them. You can list them with:

.. code-block:: console

    apt list '?automatic'

Any package which is not **automatic** is considered a **manual** package. They
are either part of the default Ubuntu installation or were manually installed by
the user with dpkg or APT. To mark a package as manually installed, you can run:

.. code-block:: console

    sudo apt-mark manual PACKAGE

To mark a package as automatically installed, you can run:

.. code-block:: console

    sudo apt-mark auto PACKAGE

To automatically remove unnecessary dependencies, you can run:

.. code-block:: console

    sudo apt autoremove

Installed **Recommends** and **Suggests** can be automatically removed depending
on the ``APT::AutoRemove::RecommendsImportant`` and
``APT::AutoRemove::SuggestsImportant`` configuration options, both of which
default to ``true``. This means that, by default, **Recommends** and
**Suggests** will not be automatically removed.

Reducing installed packages
===========================

This section details actions you can take to reduce the number of installed
packages. You must choose the configuration appropriate for your requirements,
as the system may become unusable. We recommend that you choose a minimal
default installation that suits your needs, rather than removing packages
installed by default.

Avoiding Recommends and Suggests
--------------------------------

You can avoid the installation of **Recommended** or **Suggested** packages, as
well as automate the removal of such dependencies, using APT configuration:

.. code-block:: console

    sudo tee /etc/apt/apt.conf.d/99dependencies <<EOF
    APT::Install-Recommends "false";
    APT::Install-Suggests "false";
    APT::AutoRemove::RecommendsImportant "false";
    APT::AutoRemove::SuggestsImportant "false";
    EOF

Minimizing manual packages
--------------------------

Metapackages are packages which don't contain actual software, but depend on
other packages. For example, the ``ubuntu-server`` metapackage depends on a
number of utilities which form part of the standard Ubuntu Server installation.
Similarly, the ``linux-image-generic`` metapackage depends on the latest
non-`HWE <https://ubuntu.com/kernel/lifecycle>`_ generic kernel image available.

You can mark any installed direct or transitive dependencies of metapackages as
automatically installed using `apt-mark
<https://manpages.ubuntu.com/manpages/resolute/man8/apt-mark.8.html>`_:

.. code-block:: console

    sudo apt-mark minimize-manual
    sudo apt autoremove

Note that, depending on your ``APT::AutoRemove::RecommendsImportant`` and
``APT::AutoRemove::SuggestsImportant`` configuration options, this may or may
not result in the removal of packages which are non-strict (**Recommends** or
**Suggests**) dependencies and could therefore lead to unexpected loss of
functionality. We recommend that you always evaluate what packages are
automatically-removed.

Reviewing manual packages
-------------------------

You can review the packages marked as manually-installed and, if determined to
be unnecessary, mark them as automatically installed. Note that manual
packages could be part of the default installation or could be strict or
non-strict dependencies of other manual packages. The following command will
list manual packages with a **Priority** of ``optional`` or ``extra``.

.. code-block:: console

    apt-mark showmanual '?priority(optional) | ?priority(extra)'

Note that the Linux kernel packages have a **Priority** of **optional**, as do
the bootloaders or other important packages, and will show up in the output.
These are required for bare-metal or virtual machine installations. Therefore,
we do not recommend using the **Priority** field exclusively to determine which
packages can be removed or marked as automatically-installed.

Purging packages
----------------

By default, removal of a package will not delete its configuration files, as a
data-loss avoidance strategy, as these may have been customised by you. Only the
configuration files are kept and all of the other files are removed, therefore
these would not normally take up a lot of disk space or increase your system's
attack surface. To list the packages which are in this state, you can use:

.. code-block:: console

    apt list '?config-files'

To remove all of their files completely, run:

.. code-block:: console

    sudo apt purge '?config-files'

The ``autoremove`` command can also delete the configuration files in the same
step in which it removes packages:

.. code-block:: console

    sudo apt autoremove --purge

Obsolete packages
-----------------

Sometimes, a system may end up with an installed package that is not referenced
by any of the configured archives in the APT sources. This could happen during a
release upgrade (when a package is no longer available in the newer release),
due to the `manual installation of a .deb file <deb-download-untrusted>`_, or
due to changes to the APT sources.

These packages will not receive updates through APT and are known as
**obsolete**. They can be listed and removed (or purged):

.. code-block:: console

    apt list '?obsolete'
    sudo apt remove --purge '?obsolete'
