Ubuntu archive integrity verification
#####################################


Packages in the Ubuntu Archive are distributed over a variety of protocols and
from third-party mirrors. The authenticity of packages is decoupled from the
distribution method used. This is achieved through cryptographic signatures that
are generated on systems independent of the distribution infrastructure. These
cryptographic signatures are automatically used by the package manager on Ubuntu
installations (APT) to verify the integrity of downloaded software packages.

This architecture has several benefits, including:

* providing tampering protection, even in the absence of in-transit security
  through TLS;
* the integrity of the packages can be verified, even when redistributed by
  third-parties;
* the attack surface is greatly reduced, as not even the Ubuntu Archive can
  distribute malicious software.

The verification scheme is inherited from Debian, which is Ubuntu's upstream
distribution. As such, most of the content in this section is also applicable to
Debian installations. The infrastructure for distributing the official Ubuntu
Archive, as well as `Launchpad <https://launchpad.net/>`_ are completely
independent of the Debian infrastructure.

It should be noted that only trusted repositories should be configured as APT
`sources <https://manpages.ubuntu.com/manpages/man5/sources.list.5.html>`_.
There is no automatic mechanism to establish the trustworthiness of a
repository, with well-intentioned and malicious actors alike being able to set
up repositories compatible with APT or `PPAs on Launchpad
<https://help.launchpad.net/Packaging/PPA>`_.

Automatic verification
======================

Any frontend to APT will automatically apply the same validation rules,
including ``apt``, ``apt-get``, ``aptitude`` or any of the Ubuntu graphical
applications. The behaviour can be managed through APT `configuration
<https://manpages.ubuntu.com/manpages/man5/apt.conf.5.html>`_ and its `sources
<https://manpages.ubuntu.com/manpages/man5/sources.list.5.html>`_.

Insecure settings
-----------------

There are a number of APT configuration settings which are not recommended, as
they disable the verification checks described in this section. These can be
configured in ``/etc/apt/apt.conf`` (or the file specified in
``Dir::Etc::main``), ``/etc/apt/apt.conf.d/`` (or the path specified in
``Dir::Etc::Parts``), the file specified by the ``APT_CONFIG`` environment
variable, or directly passed on the command-line to a package manager.

Particular attention should be payed to the following settings (these should
only be considered acceptable in particular environments, once their
implications are understood):

* The ``Trusted`` option for an APT sources entry, if set to ``yes``, as
  verification checks will be disabled.
* ``APT::Get::AllowUnauthenticated``, if set to ``yes``.
* ``Acquire::AllowInsecureRepositories``, if set to ``yes``.
* ``Acquire::AllowDowngradeToInsecureRepositories``, if set to ``yes``.

Trust anchor
------------

Unless verification is disabled, each configured APT source is validated against
a trust anchor, configured as a GPG keyring. A global trusted keyring is used as
a fallback and can be managed through ``apt-key``, but this functionality has
been deprecated since Ubuntu 22.04 Jammy Jellyfish. The recommendation is to
only configure the Ubuntu Archive trust anchor in the global trusted keyring,
with other repositories referencing individual keyrings stored in
``/etc/apt/keyrings/`` (when configured by the system administrator) or
``/usr/share/keyrings/`` (when configured by a package) through the `sources
<https://manpages.ubuntu.com/manpages/man5/sources.list.5.html>`_ configuration.
An alternative is to embed the trust anchor in the sources configuration, as the
following example demonstrates for a hypothetical PPA:

.. code-block:: none

    Types: deb
    URIs: https://ppa.launchpadcontent.net/ubuntu-security/demo/ubuntu/
    Suites: noble
    Components: main
    Signed-By: 
     -----BEGIN PGP PUBLIC KEY BLOCK-----
     .
     mQINBGbXMpEBEADdAP7i2KzwrStkf3qh64HZTeq2XbhhEIXbNLGn4sZDMtK1cHiH
     ...

A configured repository that does not reference a trust anchor through the
``Signed-By`` option will use the global trusted keyring. The global trusted
keyring is bootstrapped by the ``ubuntu-keyring`` package, which is installed by
default and creates GPG keyrings containing the Ubuntu Archive signing public
keys under the ``/etc/apt/trusted.gpg.d/`` directory.
