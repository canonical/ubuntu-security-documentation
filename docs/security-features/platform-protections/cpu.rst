CPU features
============
Four CPU features on x86-based hardware are not always available by default out of the
box. Many BIOS manufacturers disable the features in a conservative attempt to help
legacy operating systems that may perform strangely when these features are available.

Ubuntu can fully utilize these features, and as such, these pages will attempt to describe
where to find these features in BIOS, and how to turn them on.


.. _non-exec:
Non-Executable Memory
---------------------

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
kernel mode that allows NX to work). In Ubuntu 9.10 Karmic Koala and later, if you run 32-bit
kernels without PAE, you will still have the partial NX emulation. It is required that you use
PAE if you want true NX support.

If you believe you are incorrectly getting the boot-time warning, please open a bug report
against the ``cpu-checker`` package, or disable the check by removing the motd module:

.. code-block:: shell

   sudo rm /etc/update-motd.d/20-cpu-checker


.. _sev:
AMD Secure Encrypted Virtualization (SEV)
-----------------------------------------

Available on modern AMD CPUs (typically from the EPYC and Ryzen Pro lines), Secure Encrypted
Virtualization (SEV) allows the memory of a guest virtual machine to be encrypted. This
protects the guest from the host hypervisor, meaning that even the system administrator of
the host machine cannot access the memory of the running guest. This feature must be enabled
in the BIOS before it can be used by Ubuntu.

First, check if your CPU reports the SEV capability by looking for the ``sev`` flag in
:file:`/proc/cpuinfo`:

.. code-block:: shell

    grep ^flags /proc/cpuinfo | head -n1 | egrep --color=auto ' sev '

If this flag is present, your CPU supports the feature. However, it may still be disabled by
the BIOS. You can check if the kernel successfully enabled SEV support during boot with the
following command:

.. code-block:: shell

   dmesg | grep "SEV is enabled"

If this command returns output, SEV is active. If not, you will need to reboot into your BIOS.
In a typical BIOS, the SEV setting is found under the ``Advanced`` tab, often within a submenu
like ``AMD CBS`` or ``CPU Configuration``. You will need to enable both ``SVM Mode`` (AMD's
main  virtualization feature) and ``SEV Control`` (or a similar setting).

Once enabled in the BIOS, SEV is not used automatically for all virtual machines. The feature
is leveraged by KVM, and you must explicitly configure a virtual machine to use it at launch
time, typically through tools like ``libvirt``.

More information about SEV can be viewed `here <https://www.amd.com/en/developer/sev.html>`_.


Intel Trust Domain Extensions (TDX)
-----------------------------------

Intel Trust Domain Extensions (TDX) is a security technology that creates a hardware-isolated
environment called a Trust Domain. Like `AMD SEV <sev_>`_, it encrypts and isolates the
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
up-to-date qemu-kvm and libvirt packages. As with `SEV <sev_>`_, a virtual machine must be
specifically configured at launch to operate as a protected Trust Domain.

More information about TDX can be viewed `here <https://www.intel.com/content/www/us/en/developer/tools/trust-domain-extensions/overview.html>`_.


Virtualization
--------------

If your system supports hardware virtualization (INTEL-VT or AMD-V), it may need to be enabled in
the BIOS before this feature will be available for use by Ubuntu. If you have no interest in
running virtual machines, this is safe to leave disabled.

Unlike NX described `here <non-exec_>`_, the VT flag will always show up if your CPU
supports it, but the BIOS may still be disabling its ability to function. First, check the
:file:`/proc/cpuinfo` flags, looking for ``vmx`` or ``svm``:

.. code-block:: shell

    grep ^flags /proc/cpuinfo | head -n1 | egrep --color=auto ' (vmx|svm) '

If this exists, then check if the kernel mentions the BIOS after loading the kvm module:

.. code-block:: shell

    dmesg | grep "kvm: disabled by bios"

On Ubuntu 9.10 Karmic Koala and later, you can check if your hardware is expected to have
VT available by running the following command from the ``qemu-kvm`` package:

.. code-block:: shell

    /usr/sbin/kvm-ok

For details on using KVM with hardware virtualization, see the `KVM Documentation <https://help.ubuntu.com/community/KVM>`_.


Additional References
---------------------
The expected features for a given CPU can be looked up by manufacturer:

- `Intel <https://www.intel.com/content/www/us/en/ark.html>`_
- `AMD <https://www.amd.com/en/products/specifications.html>`_
