Built with -fstack-clash-protection
-----------------------------------

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

Adds extra instructions around variable length stack memory allocations (via alloca() or gcc variable length arrays etc) to probe each page of memory at allocation time. This mitigates stack-clash attacks by ensuring all stack memory allocations are valid (or by raising a segmentation fault if they are not, and turning a possible code-execution attack into a denial of service).

See test-built-binaries.py for regression tests. 

