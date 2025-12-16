Ubuntu archive integrity verification
#####################################

The Ubuntu Archive distributes packages over a variety of protocols and from
third-party mirrors. We decouple the authenticity of packages from the
distribution method used. This is achieved through cryptographic signatures
generated on systems independent of the distribution infrastructure. APT
automatically uses these signatures to verify the integrity of downloaded
software packages.

This architecture has several benefits:

* **Tampering protection**: It provides protection even in absence of 
  in-transit security through TLS.
* **Redistribution integrity**: You can verify the integrity of packages 
  even when they are redistributed by third parties.
* **Reduced attack surface**: The Ubuntu Archive can't distribute malicious
  software.

This verification scheme is inherited from Debian, Ubuntu's upstream distribution.
As such, most of the content in this section also applies to Debian installations. 
However, the infrastructure for distributing the official Ubuntu Archive and 
`Launchpad <https://launchpad.net/>`_ is completely independent of the Debian
infrastructure.

You should only configure trusted respositories as APT
`sources <https://manpages.ubuntu.com/manpages/man5/sources.list.5.html>`_.
There is no automatic mechanism to establish the trustworthiness of a
repository, with well-intentioned and malicious actors alike being able to set
up repositories compatible with APT or `PPAs on Launchpad
<https://help.launchpad.net/Packaging/PPA>`_.


Automatic verification
======================

Any frontend to APT will automatically apply the same validation rules,
including ``apt``, ``apt-get``, ``aptitude`` or any of the Ubuntu graphical
applications. You can manage this behavior through APT `configuration
<https://manpages.ubuntu.com/manpages/man5/apt.conf.5.html>`_ and its `sources
<https://manpages.ubuntu.com/manpages/man5/sources.list.5.html>`_.


Insecure settings
-----------------

There are a number of APT configuration settings that we don't recommended, as
they disable the verification checks described in this section. These can be
configured in ``/etc/apt/apt.conf`` (or the file specified in
``Dir::Etc::main``), ``/etc/apt/apt.conf.d/`` (or the path specified in
``Dir::Etc::Parts``), the file specified by the ``APT_CONFIG`` environment
variable, or directly passed on the command-line to a package manager.

.. warning::
   **Security risk**

   Pay particular attention to the following settings. You should only consider
   these acceptable in specific environments once you fully understand their
   implications:

   * The ``Trusted`` option for an APT sources entry, if set to ``yes``, as
     verification checks will be disabled.
   * ``APT::Get::AllowUnauthenticated``, if set to ``yes``.
   * ``Acquire::AllowInsecureRepositories``, if set to ``yes``.
   * ``Acquire::AllowDowngradeToInsecureRepositories``, if set to ``yes``.


Trust anchor
------------

Unless verification is disabled, APT validates each configured source against
a trust anchor, configured as a GPG keyring. A global trusted keyring serves
as a fallback and can be managed through ``apt-key``, but this functionality 
has been deprecated since Ubuntu 22.04 LTS (Jammy Jellyfish).

We recommend that you only configure the Ubuntu Archive trust anchor in the
global trusted keyring. Other repositories should reference individual keyrings
stored in ``/etc/apt/keyrings/`` (when configured by the system administrator) or
``/usr/share/keyrings/`` (when configured by a package) through the `sources
<https://manpages.ubuntu.com/manpages/man5/sources.list.5.html>`_ configuration.

Alternatively, you can embed the trust anchor in the sources configuration, as the
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

A configured repository that doesn't reference a trust anchor through the
``Signed-By`` option will use the global trusted keyring. The global trusted
keyring is bootstrapped by the ``ubuntu-keyring`` package, which is installed by
default. This package creates GPG keyrings containing the Ubuntu Archive signing
public keys under the ``/etc/apt/trusted.gpg.d/`` directory.
