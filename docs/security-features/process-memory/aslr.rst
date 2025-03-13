Address Space Layout Randomisation (ASLR)
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

ASLR is implemented by the kernel and the ELF loader by randomising the location of memory allocations (stack, heap, shared libraries, etc). This makes memory addresses harder to predict when an attacker is attempting a memory-corruption exploit. ASLR is controlled system-wide by the value of /proc/sys/kernel/randomize_va_space. Prior to Ubuntu 8.10, this defaulted to "1" (on). In later releases that included brk ASLR, it defaults to "2" (on, with brk ASLR).

See test-kernel-security.py for regression tests for all the different types of ASLR. 

Stack ASLR
~~~~~~~~~~

Each execution of a program results in a different stack memory space layout. This makes it harder to locate in memory where to attack or deliver an executable attack payload. This was available in the mainline kernel since 2.6.15 (Ubuntu 6.06).

VDSO ASLR
~~~~~~~~~

Each execution of a program results in a random vdso location. While this has existed in the mainline kernel since 2.6.18 (x86, PPC) and 2.6.22 (x86_64), it hadn't been enabled in Ubuntu 6.10 due to COMPAT_VDSO being enabled, which was removed in Ubuntu 8.04 LTS. This protects against jump-into-syscall attacks. Only x86 (maybe ppc?) is supported by glibc 2.6. glibc 2.7 (Ubuntu 8.04 LTS) supports x86_64 ASLR vdso. People needing ancient pre-libc6 static high vdso mappings can use "vdso=2" on the kernel boot command line to gain COMPAT_VDSO again. 

* https://lwn.net/Articles/184734/

* https://articles.manugarg.com/systemcallinlinux2_6.html

Libs/mmap ASLR
~~~~~~~~~~~~~~

Each execution of a program results in a different mmap memory space layout (which causes the dynamically loaded libraries to get loaded into different locations each time). This makes it harder to locate in memory where to jump to for "return to libc" to similar attacks. This was available in the mainline kernel since 2.6.15 (Ubuntu 6.06).

Exec ASLR
~~~~~~~~~

Each execution of a program that has been built with "-fPIE -pie" will get loaded into a different memory location. This makes it harder to locate in memory where to attack or jump to when performing memory-corruption-based attacks. This was available in the mainline kernel since 2.6.25 (and was backported to Ubuntu 8.04 LTS).

brk ASLR
~~~~~~~~

Similar to exec ASLR, brk ASLR adjusts the memory locations relative between the exec memory area and the brk memory area (for small mallocs). The randomization of brk offset from exec memory was added in 2.6.26 (Ubuntu 8.10), though some of the effects of brk ASLR can be seen for PIE programs in Ubuntu 8.04 LTS since exec was ASLR, and brk is allocated immediately after the exec region (so it was technically randomized, but not randomized with respect to the text region until 8.10).
