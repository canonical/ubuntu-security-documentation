Block kexec
-----------

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

Starting with Ubuntu 14.04 LTS, it is now possible to disable kexec via sysctl. CONFIG_KEXEC is enabled in Ubuntu so end users are able to use kexec as desired and the new sysctl allows administrators to disable kexec_load. This is desired in environments where CONFIG_STRICT_DEVMEM and modules_disabled are set, for example. When Secure Boot is in use, kexec is restricted by default to only load appropriately signed and trusted kernels. 

