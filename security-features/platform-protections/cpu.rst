CPU features
############

Four CPU features on x86-based hardware aren't always available by default.
Many BIOS manufacturers disable these features in a conservative attempt to
help legacy operating systems that might perform strangely when these features
are available.

Ubuntu can fully utilize these features. This page describes where to find these
features in the BIOS and how to turn them on.

.. _non-exec:

Non-executable memory
---------------------

Most modern CPUs protect against executing non-executable memory regions (heap,
stack, and so on) to help block the exploitation of security vulnerabilities.
This feature is called "eXecute-Disable" (XD), "Non-eXecute" (NX), or "Execute
Disable Bit" (EDB), depending on your BIOS manufacturer.

The ``/proc/cpuinfo`` file contains information about the CPU, including a line
called "flags". The flags line lists all the features supported by the CPU. If
the ``nx`` flag is present in this line, the CPU supports the NX (Non-eXecute)
feature. To check if the file contains the flag, run:

.. code-block:: bash

   grep ^flags /proc/cpuinfo | head -n1 | grep -E --color=auto ' (pae|nx) '

Enabling NX depends on the device. In a Dell laptop BIOS, look under **Security
> CPU XD Support**; it should be set to **Enabled**. In an American Megatrends
BIOS, look under **CPU Features > Execute Disable Bit**; it should be set to
**Enabled**. Some BIOS manufacturers have released firmware updates to allow
enabling NX (for example, Lenovo IdeaPads), so make sure to install the latest
BIOS if the NX option is missing.

You can check if your hardware is expected to have NX available by running the
command:

.. code-block:: bash

   sudo /usr/sbin/check-bios-nx --verbose

Once enabled in the BIOS, the feature is automatically used if you're running a
64-bit kernel. If you're using a 32-bit kernel, you must install a ``-server``
or ``-generic-pae`` flavor. As a bonus, you get to address all your physical
RAM (since the PAE mode allows NX to work). If you run 32-bit kernels without
PAE, you will still have partial NX emulation. You must use PAE if you want
true NX support.

.. _sev:

AMD Secure Encrypted Virtualization (SEV)
-----------------------------------------

Available on modern AMD CPUs (typically from the EPYC and Ryzen Pro lines),
Secure Encrypted Virtualization (SEV) allows you to encrypt the memory of a
guest virtual machine. This protects the guest from the host hypervisor,
meaning that even the system administrator of the host machine cannot access
the memory of the running guest. You must enable this feature in the BIOS
before Ubuntu can use it.

First, check if your CPU reports the SEV capability by looking for the ``sev``
flag in ``/proc/cpuinfo``:

.. code-block:: bash

   grep ^flags /proc/cpuinfo | head -n1 | grep -E --color=auto ' sev '

If this flag is present, your CPU supports the feature. However, the BIOS might
still disable it. Check if the kernel successfully enabled SEV support during
boot with the following command:

.. code-block:: bash

   dmesg | grep "SEV is enabled"

If this command returns output, SEV is active. If not, you need to reboot into
your BIOS. In a typical BIOS, find the SEV setting under the **Advanced** tab,
often within a submenu like **AMD CBS** or **CPU Configuration**. You must
enable both **SVM Mode** (AMD's main virtualization feature) and **SEV
Control** (or a similar setting).

Once enabled in the BIOS, SEV isn't used automatically for all virtual
machines. KVM leverages the feature, and you must explicitly configure a
virtual machine to use it at launch time, typically through tools like
``libvirt``.

For more information, see `AMD SEV <https://www.amd.com/en/developer/sev.html>`_.

Intel Trust Domain Extensions (TDX)
-----------------------------------

Intel Trust Domain Extensions (TDX) is a security technology that creates a
hardware-isolated environment called a Trust Domain. Like `AMD SEV <sev_>`_, it
encrypts and isolates the memory and CPU state of a virtual machine to protect
it from the host hypervisor and other software on the system. Support for TDX
is a newer feature and requires both a modern Intel CPU and a recent Ubuntu
kernel.

To see if your CPU supports TDX, check for the ``tdx`` flag in
``/proc/cpuinfo``:

.. code-block:: bash

   grep ^flags /proc/cpuinfo | head -n1 | grep -E --color=auto ' tdx '

The presence of the ``tdx`` flag indicates CPU capability, but you must also
enable the feature in the BIOS. To see if the kernel initialized TDX, check the
kernel's boot messages:

.. code-block:: bash

   dmesg | grep "TDX initialized"

If you don't see this line, enable the feature in your system's BIOS. Look for
**Intel Trust Domain Extensions (TDX)** under the **Advanced** or **Security**
sections. This option often depends on other settings, so ensure that **Intel
Virtualization Technology (VT-x)** and **Total Memory Encryption (TME)** are
also enabled.

Because TDX is a new technology, enabling it is a complex task generally
intended for developers and testers on specialized hardware. Full support
requires specific versions of the Linux kernel, ``qemu``, and ``libvirt`` that
are not yet available in the standard Ubuntu 24.04 LTS (Noble Numbat)
repositories. This functionality is being actively developed and is targeted
for inclusion in future Ubuntu releases. For the latest information on TDX
availability and configuration, refer to official announcements from Canonical
and the Ubuntu Server team. As with `AMD SEV <sev_>`_, once supported, you must
specifically configure a virtual machine at launch to operate as a protected
Trust Domain.

For more information, see `Intel Trust Domain Extensions
<https://www.intel.com/content/www/us/en/developer/tools/trust-domain-extensions/overview.html>`_.

Virtualization
--------------

If your system supports hardware virtualization (Intel VT or AMD-V), you might
need to enable it in the BIOS before Ubuntu can use it. If you have no interest
in running virtual machines, it's safe to leave this disabled.

Unlike NX described `here <non-exec_>`_, the VT flag always shows up if your
CPU supports it, but the BIOS might still disable its ability to function.
First, check the ``/proc/cpuinfo`` flags, looking for ``vmx`` or ``svm``:

.. code-block:: bash

   grep ^flags /proc/cpuinfo | head -n1 | grep -E --color=auto ' (vmx|svm) '

If this exists, check if the kernel mentions the BIOS after loading the kvm
module:

.. code-block:: bash

   dmesg | grep "kvm: disabled by bios"

You can check if your hardware is expected to have VT available by running the
following command from the ``qemu-kvm`` package:

.. code-block:: bash

   /usr/sbin/kvm-ok

For details on using KVM with hardware virtualization, see the `KVM
Documentation <https://help.ubuntu.com/community/KVM>`_.

Additional references
---------------------

You can look up the expected features for a given CPU by manufacturer:

* `Intel <https://www.intel.com/content/www/us/en/ark.html>`_
* `AMD <https://www.amd.com/en/products/specifications.html>`_
