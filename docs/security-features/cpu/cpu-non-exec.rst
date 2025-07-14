Non-Executable Memory
#####################

Most modern CPUs protect against executing non-executable memory regions (heap, stack, etc)
to help block the exploitation of security vulnerabilities. This feature is called either 
"eXecute-Disable" (XD) or "Non-eXecute" (NX) or EDB (Execute Disable Bit), depending on
your BIOS manufacturer.

In reading the system's :file:`/proc/cpuinfo` file, the first flags line will include
``nx`` if the BIOS is not disabling the CPU feature, and the CPU is NX-capable.
Nearly all 64-bit CPUs are NX-capable. If the flags line contains ``pae``, usually the CPU
will support NX:

.. code-block:: shell
  
   grep ^flags /proc/cpuinfo | head -n1 | egrep --color=auto ' (pae|nx) '

In a Dell laptop BIOS, look under "Security" / "CPU XD Support": it should be set to "enabled".
In an American Megatrends BIOS, look under "CPU Features" / "Execute Disable Bit": it should
be set to "enabled". Some BIOS manufacturers have released firmware updates for their BIOS to
allow enabling NX (e.g. Lenovo IdeaPads) so make sure to install the latest BIOS if the NX 
option is missing.

In Samsung Netbooks (namely N140) use F2 to enter the BIOS, go to "Advanced", and set "EDB
(Execute Disable Bit)" to "enabled".

On Ubuntu 10.04 Lucid Lynx and later, you can check if your hardware is expected to have NX
available by running the command:

.. code-block:: shell

   sudo /usr/sbin/check-bios-nx --verbose

As far as making use of the CPU feature once it's not disabled in the BIOS, it will 
automatically be used if you’re running a 64-bit kernel. If you're using 32-bit, you can start
using it if you install the ``-server`` or ``-generic-pae`` flavor of the 32-bit kernel. As a 
bonus, you get to address all your physical RAM if you do this too (since the "PAE" mode is the
kernel mode that allows NX to work). In Ubuntu 9.10 and later, if you run 32-bit kernels
without PAE, you will still have the partial NX emulation. It is required that you use PAE if
you want true NX support.

If you believe you are incorrectly getting the boot-time warning, please open a bug report
against the ``cpu-checker`` package, or disable the check by removing the motd module:

.. code-block:: shell

   sudo rm /etc/update-motd.d/20-cpu-checker
