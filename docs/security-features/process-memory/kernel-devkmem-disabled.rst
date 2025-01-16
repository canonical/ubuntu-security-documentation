/dev/kmem disabled
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

There is no modern user of /dev/kmem any more beyond attackers using it to load kernel rootkits. CONFIG_DEVKMEM is set to "n". While the /dev/kmem device node still exists in Ubuntu 8.04 LTS through Ubuntu 9.04, it is not actually attached to anything in the kernel.

See test-kernel-security.py for regression tests. 

