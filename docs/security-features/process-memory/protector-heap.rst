Heap Protector
--------------

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

The GNU C Library heap protector (both automatic via ptmalloc and manual) provides corrupted-list/unlink/double-free/overflow protections to the glibc heap memory manager (first introduced in glibc 2.3.4). This stops the ability to perform arbitrary code execution via heap memory overflows that try to corrupt the control structures of the malloc heap memory areas.

This protection has evolved over time, adding more and more protections as additional corner-cases were researched. As it currently stands, glibc 2.10 and later appears to successfully resist even these hard-to-hit conditions.

See test-glibc-security.py for regression tests. 