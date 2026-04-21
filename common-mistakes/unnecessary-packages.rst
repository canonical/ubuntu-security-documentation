Unnecessary packages
####################

Ubuntu comes with access to tens of thousands of packages through the Ubuntu
archive. This provides not just convenience, but also a trusted distribution
channel for your open source software. Nevertheless, security hardening guides
recommend keeping the install base at a minimum, as each software package has
the potential to increase the attack surface of your system.

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

There two methods to annotate the relative importance of a package to a Ubuntu
system: the **Essential** and the **Priority** fields.

A small number of packages are marked **Essential**, as without them the package
management system will not work. This is a flag: a package is either
**Essential** or not. These package can be listed with:

.. code-block:: console

    apt list '?essential'

Packages also have a **Priority** field, with a value of:

- **required**: these are necessary for the system to function. Without one, a
  system, including the package management, may become unusable.

- **important**: these form the foundation of a Linux system and provide the
  functionality which users expect to see.

- **standard**: these are part of the default Ubuntu installations and contain
  utilities for a fully-fledged experience.

- **optional**: these form the vast majority of the Ubuntu packages and provide
  functionality which you may choose to enable via their manual installation.

- **extra**: this priority is deprecated and should be considered similar to
  **optional**.

Packages with a **Priority** of **required**, but which aren't **Essential** can
be listed with:

.. code-block:: console

    apt list '?priority(required) ?not(?essential)'

Packages that are **Essential** and those with a **Priority** of **required**
must not be uninstalled. All other packages can be removed, but the resulting
lack of functionality may be unexpected.

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

To mark a package as either manually installed, you can run:

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
as the system may become unusable.

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

Removing based on Priority
--------------------------

You can mark packages as automatically installed based on their **Priority**
field. The ``autoremove`` function can then trigger the deinstallation of the
unnecessary ones. For example, to mark any installed package that is not
**Essential** or with a **Priority** of **required** or **important** as
automatically installed and then trigger autoremove:

.. code-block:: console

    sudo apt-mark auto '?installed ?not(?essential) ?not(?priority(required)) ?not(?priority(important))'
    sudo apt autoremove

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
