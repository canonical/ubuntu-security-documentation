Devices
#######

This section documents security features that protect against malicious external devices. 
Peripherals, especially those connected via USB, present a unique security 
risk because they can act as more than just the device they appear to be. For example,
consider `BadUSB attacks <https://en.wikipedia.org/wiki/BadUSB>`_. In these attacks, a device like a
flash drive or a charging cable can secretly act as a keyboard to inject malicious commands
into your system without your knowledge. 

The following tools provide mechanisms to authorize and manage devices,
reducing the risk of such attacks by ensuring only trusted hardware can interact with your system.

bolt
====

Starting with Ubuntu 18.04 Bionic Beaver, the ``bolt`` package is available in ``main`` to provide a
desktop-oriented tool for using the Linux kernel's Thunderbolt authorization support. Bolt implements
the user-space component of the kernel's Thunderbolt security framework, designed to protect against
unauthorized Thunderbolt device access and potential security threats like direct memory access
(DMA) attacks.

The bolt daemon (``boltd``) runs as a system service and manages Thunderbolt device authorization
using the kernel's Thunderbolt security levels. When a new Thunderbolt device is connected, ``bolt`` can
automatically authorize trusted devices or prompt the user for authorization decisions, depending on
the configured security policy.

Bolt stores device information and policies in ``/var/lib/boltd/`` and integrates seamlessly with
desktop environments through D-Bus interfaces. GNOME Settings and other desktop applications can
interact with ``bolt`` to provide user-friendly device management interfaces.

Security levels
---------------

Bolt supports multiple Thunderbolt security levels that determine how devices are handled:

1. **none**: No security - all devices are automatically authorized (legacy mode)
2. **user**: User authorization required - devices must be manually approved
3. **secure**: Secure connection with challenge-response authentication
4. **dponly**: DisplayPort-only mode - only video output devices are allowed

Example workflow
----------------

The typical ``bolt`` workflow involves:

1. **Device Detection**: When a Thunderbolt device connects, the kernel detects it but doesn't authorize it
2. **Policy Check**: Bolt checks if the device is in its database and what policy applies
3. **User Interaction**: For unknown devices, ``bolt`` may prompt for user authorization through desktop notifications
4. **Authorization**: Approved devices receive authorization and become functional
5. **Enrollment**: Devices can be "enrolled" to remember authorization decisions for future connections

You can manage ``bolt`` through the command line using the ``boltctl`` utility.

.. code-block:: bash

    # List connected devices
    boltctl list

    # Show device details
    boltctl info <device-id>

    # Enroll a device (authorize and remember)
    boltctl enroll <device-id>

    # Authorize a device temporarily
    boltctl authorize <device-id>

Configuration
-------------

Bolt's main configuration is typically handled automatically, but advanced users can modify behavior
through:

- **Policy files**: Located in ``/etc/bolt/``
- **Device database**: Stored in ``/var/lib/bolt/``
- **Security level**: Usually configured through firmware/BIOS settings

You can learn more about ``boltctl`` through its
`official manpages <https://manpages.ubuntu.com/manpages/resolute/man1/boltctl.1.html>`_. 
You can also learn more about ``boltd`` through its
`official manpages <https://manpages.ubuntu.com/manpages/resolute/man8/boltd.8.html>`_


thunderbolt-tools
=================

Starting with Ubuntu 18.04 Bionic Beaver, the ``thunderbolt-tools`` package is available in
``universe`` to provide a server-oriented tool for using the Linux kernel's Thunderbolt
authorization support. Unlike ``bolt``, which focuses on desktop integration, ``thunderbolt-tools`` provides
low-level command-line utilities for Thunderbolt management in server and embedded environments
where desktop services may not be available.

The package includes several utilities for direct interaction with the kernel's Thunderbolt
subsystem, making it suitable for scripting, automation, and headless systems where fine-grained
control over Thunderbolt devices is required.

Key components
--------------

The ``thunderbolt-tools`` package provides:

1. **tbtadm**: The primary administrative tool for Thunderbolt management
2. **Kernel interface access**: Direct access to ``/sys/bus/thunderbolt/`` interfaces
3. **Security management**: Tools for configuring and managing Thunderbolt security policies

Example workflow
----------------

Here's how you might use ``thunderbolt-tools`` in a server environment:

.. code-block:: bash

    # Show Thunderbolt topology
    tbtadm topology

    # List all currently connected Thunderbolt devices
    tbtadm devices

    # Approve a specific device
    tbtadm approve <device-uuid>

    # Print ACLs
    tbtadm acl

Configuration approaches
------------------------

Unlike desktop-oriented ``bolt``, ``thunderbolt-tools`` requires more manual configuration:

1. **Direct sysfs manipulation**: Interacting with kernel interfaces in ``/sys/bus/thunderbolt/``
2. **Scripted authorization**: Creating custom scripts for device approval workflows
3. **Security policy enforcement**: Implementing organizational policies through automation
4. **Integration with system management**: Incorporating Thunderbolt management into larger infrastructure management tools

Use cases
---------

``thunderbolt-tools`` is particularly valuable for:

- **Server environments**: Managing Thunderbolt storage arrays or network adapters
- **Embedded systems**: Implementing custom Thunderbolt authorization logic
- **Automation scripts**: Building automated device management workflows
- **Security auditing**: Inspecting and logging Thunderbolt device connections
- **Custom implementations**: Developing specialized Thunderbolt management solutions

Security considerations
-----------------------

When using ``thunderbolt-tools`` in production environments:

- Implement strict device allowlists based on device identifiers
- Monitor device connection events through system logs
- Consider disabling Thunderbolt entirely if not needed for security-critical systems
- Use the highest appropriate security level supported by your hardware
- Regularly audit authorized devices and remove unused entries

Both ``bolt`` and ``thunderbolt-tools`` work with the same underlying kernel Thunderbolt security framework
but serve different use cases, ``bolt`` for desktop users seeking seamless integration, and
``thunderbolt-tools`` for administrators requiring direct control and scriptable interfaces.

You can learn more about ``tbtadm`` through its
`official manpages <https://manpages.ubuntu.com/manpages/resolute/man1/tbtadm.1.html>`_.


usbauth
=======

Starting with Ubuntu 18.04 Bionic Beaver, the ``usbauth`` package is available 
in ``universe`` to provide a straightforward tool for using the Linux kernel's 
`USB authorization <https://docs.kernel.org/usb/authorization.html>`_ feature.
This feature acts as a gatekeeper, allowing users to define exactly which USB
devices are permitted to connect to their system. By default, ``usbauth`` deauthorizes
all new USB devices, effectively blocking them until they're explicitly approved.

You can manage device configuration in the :file:`/etc/usbauth/usbauth.conf` file. Here,
you can create an allowlist of trusted devices using specific attributes like vendor
and product IDs (``idVendor`` and ``idProduct``), device class, or even unique serial
numbers. This approach provides strong protection against rogue USB devices. 

When you need to authorize a new device, you can temporarily disable the service, 
connect the device, use tools like ``lsusb`` to find its attributes, add it to your
:file:`/etc/usbauth/usbauth.conf` configuration file, and then re-enable the service.

Example workflow
----------------

Here's an example of what you might add in the 
:file:`/etc/usbauth/usbauth.conf` configuration file:

.. code-block:: text
   :caption: /etc/usbauth/usbauth.conf

   # Allow a specific keyboard model.
   allow 046d:c52b

   # Also allow any device that identifies as a Mass Storage device.
   allow class 08

Each rule in :file:`/etc/usbauth/usbauth.conf` consists of an action and a matcher. For
example, the file above can be broken down into the following componenets:

* ``allow``: This is the action. It instructs the system to authorize any USB device that matches the criteria that follow.
* ``046d:c52b``: This is the matcher. It specifically targets the device's ``VendorID:ProductID`` pair. This rule does not distinguish between two identical device models; it allows any device of that exact model to connect.
* ``class 08``: This is an alternative type of matcher. The ``class`` keyword tells ``usbauth`` to look at the device's function rather than its manufacturer ID. The 08 is the value, which is the official `USB Class Code for Mass Storage devices <https://www.usb.org/defined-class-codes>`_. This single rule would permit any flash drive, external hard drive, or card reader to connect, regardless of its vendor or product ID.

While these rules provide effective filtering, it's important to understand the limitations
these rules have for risk reduction. A malicious device can be programmed to lie about its
attributes, such as its device class, vendor, or product ID. This can allow a malicious
device to be allowed by existing rules. Because of this ``usbauth`` should be viewed as an 
effective way to reduce the risk external devices connected via USB pose to a user's system,
but it doesn't eliminate the risk entirely.

You can learn more about ``usbauth`` through its 
`official manpages <https://manpages.ubuntu.com/manpages/noble/en/man8/usbauth.8.html>`_.


usbguard
========

Starting with Ubuntu 16.10 Yakkety Yak, the ``usbguard`` package is available in
``universe`` to provide a framework for implementing USB device policies. It provides a 
higher degree of security by allowing rules to be created based on a combination of
device attributes, making it more resilient to devices that provide false information.

The primary tool is the ``usbguard`` command-line utility, which allows a user to generate
an initial policy, view currently connected devices, and manage rules. The ruleset is stored
in :file:`/etc/usbguard/rules.conf`. A typical workflow involves running 
``usbguard generate-policy > /etc/usbguard/rules.conf`` to create a baseline policy that 
allows all currently connected devices. From that point on, any new device will be blocked by
default.

When a new device is connected, the ``usbguard`` daemon logs the event, and a user can use 
``usbguard list-devices`` to see the blocked device. To permanently allow it, a user can use
``usbguard allow-device <id>`` and then append the new rule to their :file:`rules.conf` file 
to ensure it persists after a reboot. This makes ``usbguard`` a powerful and dynamic tool 
for managing USB security on a running system.

usbguard for Desktops
---------------------

While managing ``usbguard`` from the command-line is effective, it can be cumbersome
on a desktop system. To improve usability, the ``usbguard-notifier`` service is
available. This tool monitors the ``usbguard`` daemon and provides a desktop
notification whenever a device is blocked. This notification pop-up allows a user to
immediately authorize the device and add a permanent rule for it, transforming the
experience from a manual, command-line process into an interactive one. It is the
successor to older tools like ``usbguard-applet-qt``.

Example workflow
----------------

Here's an example of what you might add in the :file:`rules.conf`
file after running ``usbguard generate-policy > /etc/usbguard/rules.conf``:

.. code-block:: text
   :caption: /etc/usbguard/rules.conf

   allow id 046d:c52b name "Unifying Receiver" serial "4071-DE-AD-BE-EF" via-port "usb3-port2" with-interface { 03:01:01 03:01:02 }
   allow id 046d:082d name "HD Pro Webcam C920" serial "BADA55C0" via-port "usb3-port1" with-interface { 0e:01:00 0e:02:00 }
   allow id 1d6b:0002 name "Linux Foundation 2.0 root hub" serial "" via-port "" with-interface { 09:00:00 }

Each rule in :file:`/etc/usbguard/rules.conf` consists of a target and attributes.
For example, the file above can be broken down into the following components:

* ``allow``: This is the "target", meaning a device matching this rule will be authorized. Other targets are ``block`` and ``reject``.
* ``id 046d:c52b``: This is the ``VendorID:ProductID`` pair. This is a primary attribute for matching.
* ``name "Unifying Receiver"``: The human-readable device name. This is for a user's reference and is ignored by the matching engine.
* ``serial "4071-DE-AD-BE-EF"``: The device's unique serial number. If present, this makes the rule extremely specific to a single physical device.
* ``via-port "usb3-port2"``: The physical port the device is connected to. This can be used to enforce that a device is only allowed in a specific port.
* ``with-interface { 03:01:01 03:01:02 }`` This is often the most critical attribute for security. It specifies the exact functions (e.g., keyboard, mouse, mass storage) the device is allowed to have. This is powerful for managing composite devices, which present multiple functions at once. For example, a programmable keyboard might also act as a mass storage device to store its configuration. A strict rule can allow the keyboard interface (03:01:01) while blocking the mass storage interface (08:06:50), greatly reducing the attack surface.

By combining multiple attributes, especially the ``with-interface`` check, ``usbguard`` makes
it significantly more difficult for a malicious device to
bypass the guardrails put in place by ``usbguard``. This provides a substantial reduction in risk.

You can learn more about ``usbguard`` through its
`official manpages <https://manpages.ubuntu.com/manpages/noble/man1/usbguard.1.html>`_ or by
visiting the `project repository <https://usbguard.github.io/>`_. You can also learn more about
``usbguard-notifier`` through its 
`official manpages <https://manpages.ubuntu.com/manpages/noble/man1/usbguard-notifier.1.html>`_.
