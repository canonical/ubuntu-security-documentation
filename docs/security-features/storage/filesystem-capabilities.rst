Filesystem Capabilities
-----------------------

.. tab-set::

    .. tab-item:: 24.04

        TBA

    .. tab-item:: 22.04

        TBA

    .. tab-item:: 20.04

            TBA

    .. tab-item:: 18.04
        
        TBA
    
    .. tab-item:: 16.04

        TBA  

    .. tab-item:: 14.04

        TBA




The need for setuid applications can be reduced via the application of `filesystem capabilities <http://www.olafdietsche.de/linux/capability/>`_ using the xattrs available to most modern filesystems. This reduces the possible misuse of vulnerable setuid applications. The kernel provides the support, and the user-space tools are in main ("libcap2-bin").

Regression tests: `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_.
