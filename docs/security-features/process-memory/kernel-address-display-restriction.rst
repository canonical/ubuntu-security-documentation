Kernel Address Display Restriction
----------------------------------

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

When attackers try to develop "run anywhere" exploits for kernel vulnerabilities, they frequently need to know the location of internal kernel structures. By treating kernel addresses as sensitive information, those locations are not visible to regular local users. Starting with Ubuntu 11.04, /proc/sys/kernel/kptr_restrict is set to "1" to block the reporting of known kernel address leaks. Additionally, various files and directories were made readable only by the root user: /boot/vmlinuz*, /boot/System.map*, /sys/kernel/debug/, /proc/slabinfo

See test-kernel-security.py for regression tests. 

