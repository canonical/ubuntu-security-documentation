Why Livepatch is not working on my machine
##############################################

UNSUPPORTED KERNELS
-------------------

Livepatch supports only kernels that have been released by the kernel
team to the updates pocket, i.e. officially-released kernels acquired
through APT using Canonical’s repository for system updates, or
Snap-based kernels released by Canonical to stable Snap channels.

While a livepatch *might* successfully apply to a kernel acquired from
other sources, only certain kernels released by Canonical are supported.
Kernels from other sources are not supported, including but not limited
to:

-  kernels acquired from the development (proposed) kernel PPA

-  kernels acquired from the kernel team’s build PPA

-  test kernels acquired from the kernel team’s development PPAs

-  personally-rebuilt kernels using the source debian package

-  personally-rebuilt kernels using snapcraft

-  kernels acquired from a Ubuntu-derived distribution

Please be aware that while it may be possible to build a kernel with the
same version markings as an officially-supported kernel, and to attempt
to load a Canonical-generated livepatch into that kernel, it will likely
not work, and can potentially crash your system or corrupt your data.

Also note that a kernel running unsigned, out-of-tree drivers will be
tainted, and the kernel will refuse to apply livepatches in this state.

A full list of supported kernels is available
`here <https://ubuntu.com/security/livepatch/docs/livepatch/reference/kernels>`__.

HWE vs GA Kernels
-----------------

Related to the above, detailing certain scenarios when a kernel may not
be supported, it felt necessary to add a dedicated section on HWE
(hardware enablement) versus GA (general availability) kernels.

Existing `blog
posts <https://canonical.com/blog/canonical-livepatch-gets-even-better-now-supporting-hardware-enablement-kernels>`__
and `official pages <https://ubuntu.com/kernel/variants>`__ detail what
exactly an HWE kernel is. Newer releases of LTS Ubuntu Desktop default
to the HWE kernel, meaning your machine will be running a kernel version
that will update alongside each Ubuntu release before settling on the
kernel released alongside the next LTS. Ubuntu Server installs continue
to remain on the GA kernel.

While Livepatch supports the GA kernel and the HWE that you eventually
settle on alongside the next LTS, it does not completely support the
interim kernels that are released every 6 months. This is why you might
see your machine running an LTS Ubuntu Desktop release, but still
encounter Livepatch messaging saying your kernel is not supported.

It is possible to switch from an HWE kernel to the GA if desired by
following the instructions
`here <https://wiki.ubuntu.com/Kernel/LTSEnablementStack>`__. One should
take care to backup data and other important information before making
such system level changes.

Finally, while prior to Ubuntu 22.04, Livepatch offered no support for
interim kernel versions, recently Livepatch has grown support for some
flavours of interim HWE kernels as described in our `blog
post <https://ubuntu.com/blog/canonical-livepatch-gets-even-better-now-supporting-hardware-enablement-kernels>`__.
Kernels for desktop users are the “generic” flavour, while kernels for
public clouds have their own unique flavours, supporting cloud specific
functionality. Livepatch is now supported on interim HWE kernels for
various public cloud flavours. Check your kernel flavour with
``uname -r``.

As above, a full list of GA and HWE kernels supported is available
`here <https://ubuntu.com/security/livepatch/docs/livepatch/reference/kernels>`__

SECUREBOOT
----------

If you are using secure boot with a kernel older than April 1 2021, you
will also need to import the livepatch public keys into your keyring. If
your kernel is newer, there is no need to import keys as the key is
included in the kernel, but doing so will not cause any harm.

Use the following command to import the livepatch key:

::


   sudo mokutil --import /snap/canonical-livepatch/current/keys/livepatch-kmod.x509

After this enter a password if necessary for MOK, then reboot.

Your BIOS will then guide you through enrolling a new key in MOK. At
this point you will be able to verify the module signatures.
