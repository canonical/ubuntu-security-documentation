Kernel Address Space Layout Randomisation
-----------------------------------------

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

Kernel Address Space Layout Randomisation (kASLR) aims to make some kernel exploits more difficult to implement by randomizing the base address value of the kernel. Exploits that rely on the locations of internal kernel symbols must discover the randomized base address.

kASLR is available starting with Ubuntu 14.10 and is enabled by default in 16.10 and later.

Before 16.10, you can specify the "kaslr" option on the kernel command line to use kASLR.

Note: Before 16.10, enabling kASLR will disable the ability to enter hibernation mode. 


