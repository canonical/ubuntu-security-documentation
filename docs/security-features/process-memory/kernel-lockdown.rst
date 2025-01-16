Kernel Lockdown
---------------

.. tab-set::

   .. tab-item:: 14.04

        TBA

   .. tab-item:: 16.04
    
        TBA
   
   .. tab-item:: 18.04
    
        TBA

   .. tab-item:: 20.04
    
        Enabled in integrity mode.

   .. tab-item:: 22.04
    
        Enabled in integrity mode.

   .. tab-item:: 24.04
    
        Enabled in integrity mode.

Starting with Ubuntu 20.04, the Linux kernel's lockdown mode is enabled in integrity mode. This prevents the root account from loading arbitrary modules or BPF programs that can manipulate kernel datastructures. Lockdown enforcement is tied to UEFI secure boot.

