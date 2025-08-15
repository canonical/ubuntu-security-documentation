Software integrity
##################

Software artifacts distributed by Ubuntu use digital signatures and other
technical controls for integrity verification, protecting against the delivery
of forged replacements. These mechanisms are normally employed automatically,
with manual verification recommended when artifacts are directly downloaded
using an HTTP or FTP client (e.g. a browser). In particular, downloading
installation media must be followed by an integrity check, even when performed
over a TLS-protected channel, as such a test cannot be automatically integrated
into the workflow.

This section documents the integrity protections employed for various types of
software artifacts. It is important to understand the configuration and the
established chain of trust, in order to reduce the likelihood of malicious or
inadvertent tampering.

Image integrity verification
============================

.. toctree::
   :maxdepth: 2

   image-verification

Archive integrity verification
=====================================

.. toctree::
   :maxdepth: 2

   archive-verification
