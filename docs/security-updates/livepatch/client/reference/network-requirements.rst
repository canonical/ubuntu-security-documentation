Network requirements
####################

On firewalled machines, ``canonical-livepatch`` needs access to two
hostnames:

-  ``livepatch.canonical.com``, port 443
-  ``livepatch-files.canonical.com``, port 443

If livepatch client is enabled using Ubuntu Pro, additional access to
``contracts.canonical.com`` on port 443 will be required.

For snap installation, see `snap network
requirements <https://forum.snapcraft.io/t/network-requirements/5147>`__.

**Note:** Previously patches were served via HTTP until switching over
to HTTPS in ~Oct 2023.
