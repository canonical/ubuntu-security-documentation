Virtualization
##############

If your system supports hardware virtualization (INTEL-VT or AMD-V), it may need to be enabled in
the BIOS before this feature will be available for use by Ubuntu. If you have no interest in 
running virtual machines, this is safe to leave disabled.

Unlike NX described :doc:`here <cpu-non-exec>`, the VT flag will always show up if your CPU
supports it, but the BIOS may still be disabling its ability to function. First, check the 
:file:`/proc/cpuinfo` flags, looking for ``vmx`` or ``svm``:

.. code-block:: shell

    grep ^flags /proc/cpuinfo | head -n1 | egrep --color=auto ' (vmx|svm) '

If this exists, then check if the kernel mentions the BIOS after loading the kvm module:

.. code-block:: shell

    dmesg | grep "kvm: disabled by bios"

On Ubuntu 9.10 and later, you can check if your hardware is expected to have VT available by 
running the following command from the ``qemu-kvm`` package:

.. code-block:: shell

    /usr/bin/kvm-ok

For details on using KVM with hardware virtualization, see the `KVM Documentation <https://help.ubuntu.com/community/KVM>`_.


