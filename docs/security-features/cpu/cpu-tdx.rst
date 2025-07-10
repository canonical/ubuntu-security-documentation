Intel Trust Domain Extensions (TDX)
===================================

Intel Trust Domain Extensions (TDX) is a security technology that creates a hardware-isolated
environment called a Trust Domain. Like :doc:`AMD SEV <cpu-sev>`, it encrypts and isolates the
memory and CPU state of a virtual machine to protect it from the host hypervisor and other
software on the system. Support for TDX is a newer feature and requires both a modern Intel 
CPU and a recent Ubuntu kernel.

To see if your CPU supports TDX, check for the ``tdx`` flag in :file:`/proc/cpuinfo`:

.. code-block:: shell

    grep ^flags /proc/cpuinfo | head -n1 | egrep --color=auto ' tdx '

The presence of the ``tdx`` flag indicates CPU capability, but the feature must also be 
enabled in the BIOS. To see if the kernel initialized TDX, you can check the kernel's boot
messages:

.. code-block:: shell

    dmesg | grep "TDX initialized"

If you do not see this line, you must enable the feature in your system's BIOS. Look for ``Intel
Trust Domain Extensions (TDX)`` under the ``Advanced`` or ``Security`` sections. This option is
often dependent on other settings, so ensure that ``Intel Virtualization Technology (VT-x)`` and
``Total Memory Encryption (TME)`` are also enabled.

Because TDX support is still evolving in the Linux ecosystem, using it on Ubuntu requires 
up-to-date qemu-kvm and libvirt packages. As with :doc:`SEV <cpu-sev>`, a virtual machine must be
specifically configured at launch to operate as a protected Trust Domain.

More information about TDX can be viewed `here <https://www.intel.com/content/www/us/en/developer/tools/trust-domain-extensions/overview.html>`_.
