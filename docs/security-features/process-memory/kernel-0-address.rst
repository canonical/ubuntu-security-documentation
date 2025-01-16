0-address protection
--------------------

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

Since the kernel and userspace share virtual memory addresses, the "NULL" memory space needs to be protected so that userspace mmap'd memory cannot start at address 0, stopping "NULL dereference" kernel attacks. This is possible with 2.6.22 kernels, and was implemented with the "mmap_min_addr" sysctl setting. Since Ubuntu 9.04, the mmap_min_addr setting is built into the kernel. (64k for x86, 32k for ARM.)

See test-kernel-security.py for regression tests. 

