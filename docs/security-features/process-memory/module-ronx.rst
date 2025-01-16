Module RO/NX
------------

.. tab-set::

   .. tab-item:: 14.04

        TBA

   .. tab-item:: 16.04
    
        TBA
   
   .. tab-item:: 18.04
    
        TBA

   .. tab-item:: 20.04
    
        TBA

   .. tab-item:: 22.04
    
        TBA

   .. tab-item:: 24.04
    
        TBA

This feature extends CONFIG_DEBUG_RODATA to include similar restrictions for loaded modules in the kernel. This can help resist future kernel exploits that depend on various memory regions in loaded modules. Enabled via the CONFIG_DEBUG_MODULE_RONX option.

See test-kernel-security.py for configuration regression tests. 

