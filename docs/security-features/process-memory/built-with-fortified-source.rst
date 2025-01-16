Built with Fortify Source
-------------------------

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

Programs built with "-D_FORTIFY_SOURCE=2" (and -O1 or higher), enable several compile-time and run-time protections in glibc:

* expand unbounded calls to "sprintf", "strcpy" into their "n" length-limited cousins when the size of a destination buffer is known (protects against memory overflows).
* stop format string "%n" attacks when the format string is in a writable memory segment.
* require checking various important function return codes and arguments (e.g. system, write, open).
* require explicit file mask when creating new files. 

See test-gcc-security.py for regression tests. 