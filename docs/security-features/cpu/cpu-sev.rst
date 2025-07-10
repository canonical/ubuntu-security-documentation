AMD Secure Encrypted Virtualization (SEV)
=========================================

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
