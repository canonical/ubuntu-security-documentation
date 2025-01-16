/proc/$pid/maps protection
--------------------------

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

With ASLR, a process's memory space layout suddenly becomes valuable to attackers. The "maps" file is made read-only except to the process itself or the owner of the process. Went into mainline kernel with sysctl toggle in 2.6.22. The toggle was made non-optional in 2.6.27, forcing the privacy to be enabled regardless of sysctl settings (this is a good thing).

See test-kernel-security.py for regression tests. 

