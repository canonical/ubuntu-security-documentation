Syscall Filtering
-----------------

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

Programs can filter out the availability of kernel syscalls by using the seccomp_filter interface. This is done in containers or sandboxes that want to further limit the exposure to kernel interfaces when potentially running untrusted software.

See test-kernel-security.py for regression tests. 


