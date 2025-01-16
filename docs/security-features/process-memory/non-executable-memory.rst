Non-Executable Memory
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

Most modern CPUs protect against executing non-executable memory regions (heap, stack, etc). This is known either as Non-eXecute (NX) or eXecute-Disable (XD), and some BIOS manufacturers needlessly disable it by default, so check your BIOS Settings. This protection reduces the areas an attacker can use to perform arbitrary code execution. It requires that the kernel use "PAE" addressing (which also allows addressing of physical addresses above 3GB). The 64bit and 32bit -server and -generic-pae kernels are compiled with PAE addressing. Starting in Ubuntu 9.10, this protection is partially emulated for processors lacking NX when running on a 32bit kernel (built with or without PAE). After booting, you can see what NX protection is in effect:

* Hardware-based (via PAE mode):

    [    0.000000] NX (Execute Disable) protection: active

* Partial Emulation (via segment limits):

    [    0.000000] Using x86 segment limits to approximate NX protection

If neither are seen, you do not have any NX protections enabled. Check your BIOS settings and CPU capabilities. If "nx" shows up in each of the "flags" lines in /proc/cpuinfo, it is enabled/supported by your hardware (and a PAE kernel is needed to actually use it).

Starting in Ubuntu 11.04, BIOS NX settings are ignored by the kernel. 

