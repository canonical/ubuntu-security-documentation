Block module loading
---------------------

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

In Ubuntu 8.04 LTS and earlier, it was possible to remove CAP_SYS_MODULES from the system-wide capability bounding set, which would stop any new kernel modules from being loaded. This was another layer of protection to stop kernel rootkits from being installed. The 2.6.25 Linux kernel (Ubuntu 8.10) changed how bounding sets worked, and this functionality disappeared. Starting with Ubuntu 9.10, it is now possible to block module loading again by setting "1" in /proc/sys/kernel/modules_disabled.

See test-kernel-security.py for regression tests. 

