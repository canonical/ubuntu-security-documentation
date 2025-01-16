Read-only data sections
-----------------------

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

This makes sure that certain kernel data sections are marked to block modification. This helps protect against some classes of kernel rootkits. Enabled via the CONFIG_DEBUG_RODATA option.

See test-kernel-security.py for configuration regression tests.
