/dev/mem protection
-------------------

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

Some applications (Xorg) need direct access to the physical memory from user-space. The special file /dev/mem exists to provide this access. In the past, it was possible to view and change kernel memory from this file if an attacker had root access. The CONFIG_STRICT_DEVMEM kernel option was introduced to block non-device memory access (originally named CONFIG_NONPROMISC_DEVMEM).

See test-kernel-security.py for regression tests. 

