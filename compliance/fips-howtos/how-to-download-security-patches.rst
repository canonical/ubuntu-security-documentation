How to download security patches
################################

Each FIPS 140 certificate for a package can take several months to complete and is valid for 5 years. However, as vulnerabilities happen security-critical fixes may need to be included faster than a certification cycle. 

We provide two ways to consume validated packages: 

* a ``fips`` stream where the exact packages validated by NIST are present; 
* a ``fips-updates`` stream where the validated packages are present, but are updated with security fixes. ``fips-updates`` alows to access to the packages during the validation phase, enabling early application development and testing. 

Both streams are revalidated periodically during Ubuntu standard support phase.

How to switch from ``fips`` to ``fips-updates``
===============================================

If you are on a system with the ``fips`` stream enabled such as Ubuntu Pro FIPS, you can switch to the ``fips-updates`` stream with the following command:

.. code-block:: bash

    sudo pro enable fips-updates
