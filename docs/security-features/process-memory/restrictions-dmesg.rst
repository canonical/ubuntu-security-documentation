dmesg restrictions
------------------

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

When attackers try to develop "run anywhere" exploits for vulnerabilties, they frequently will use dmesg output. By treating dmesg output as sensitive information, this output is not available to the attacker. Starting with Ubuntu 12.04 LTS, /proc/sys/kernel/dmesg_restrict can be set to "1" to treat dmesg output as sensitive. Starting with 20.10, this is enabled by default. 

