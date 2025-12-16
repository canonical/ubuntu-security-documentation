Software integrity
##################

Software artifacts distributed by Ubuntu use digital signatures and other
technical controls for integrity verification, protecting against the delivery
of forged replacements. These mechanisms usually run automatically, but we
recommend manual verification when you directly download artifacts using an
HTTP or FTP client (such as a browser).

.. warning::
   **Check your installation media**

   If you download installation media, you must perform an integrity check,
   even if you used a TLS-protected channel. The download workflow can't
   automatically perform this test for you.

This section documents the integrity protections employed for various types of
software artifacts. It's important to understand the configuration and the
established chain of trust to reduce the likelihood of malicious or
inadvertent tampering.


Ubuntu image integrity verification
===================================

.. toctree::
   :maxdepth: 2

   image-verification


Ubuntu archive integrity verification
=====================================

.. toctree::
   :maxdepth: 2

   archive-verification
