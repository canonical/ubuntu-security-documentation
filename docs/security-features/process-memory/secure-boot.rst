UEFI Secure Boot (amd64)
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

Starting with Ubuntu 12.04 LTS, UEFI Secure Boot was implemented in enforcing mode for the bootloader and non-enforcing mode for the kernel. With this configuration, a kernel that fails to verify will boot without UEFI quirks enabled. The Ubuntu 18.04.2 release of Ubuntu 18.04 LTS enabled enforcing mode for the bootloader and the kernel, so that kernels which fail to verify will not be booted, and kernel modules which fail to verify will not be loaded. This is planned to be backported for Ubuntu 16.04 LTS and Ubuntu 14.04 LTS (however only with kernel signature enforcement for Ubuntu 14.04 LTS, not kernel module signature enforcement). 

