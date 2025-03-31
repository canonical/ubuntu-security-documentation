References
##########

Technical information - security, APIs, architecture, etc., related to Livepatch.

Networking
----------

Livepatch client requires Internet access in order to fetch kernel
patches from the server. 

- `Network requirements </client/reference/network-requirements>`__

Compatibility
-------------

Livepatch determines which kernel patch may be applied based on your
kernel version. 

- `Supported kernels </client/reference/supported-kernels>`__ 

Security and privacy
--------------------

Livepatch sends specific data about your system in order to patch your
kernel. 

- `Data sent </client/reference/data-sent>`__ 

- `Patch Security </client/reference/patch-security>`__

Kernel patching
---------------

Livepatch inserts modules into a running kernel, this has inherent risks
and the following can detail some of these risks and misunderstandings.

- `Patch Installation </client/reference/patch-installation>`__


.. toctree::
    :hidden:
    :maxdepth: 2
    
    network-requirements
    supported-kernels
    data-sent
    patch-security
    patch-installation
