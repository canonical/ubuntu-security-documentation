Built with RELRO
----------------

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

Hardens ELF programs against loader memory area overwrites by having the loader mark any areas of the relocation table as read-only for any symbols resolved at load-time ("read-only relocations"). This reduces the area of possible GOT-overwrite-style memory corruption attacks.

See test-gcc-security.py for regression tests. 