Stack Protector
---------------

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

gcc's -fstack-protector provides a randomized stack canary that protects against stack overflows, and reduces the chances of arbitrary code execution via controlling return address destinations. Enabled at compile-time. (A small number of applications do not play well with it, and have it disabled.) The routines used for stack checking are actually part of glibc, but gcc is patched to enable linking against those routines by default.

See test-gcc-security.py for regression tests. 

