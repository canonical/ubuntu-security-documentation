Devices
#######

This section documents security features that provide protections for external devices.

bolt
====

Starting with Ubuntu 18.04, the bolt package has been available in main to provide a
desktop-oriented tool for using the Linux kernel's Thunderbolt authorization support. 


thunderbolt-tools
=================

Starting with Ubuntu 18.04, the thunderbolt-tools package has been available in
universe to provide a server-oriented tool for using the Linux kernel's Thunderbolt
authorization support. 


usbauth
=======

Starting with Ubuntu 18.04, the ``usbauth`` package has been available in universe
to provide a straightforward tool for using the Linux kernel's 
`USB authorization <https://docs.kernel.org/usb/authorization.html>`_ feature.
This mechanism acts as a gatekeeper, allowing a user to define exactly which USB
devices are permitted to connect to their system. By default, it will deauthorize
all new USB devices, effectively blocking them until they are explicitly approved.

Configuration is managed through the :file:`/etc/usbauth/usbauth.conf` file. Here,
a user can create an allowlist of trusted devices using specific attributes like vendor
and product IDs (``idVendor`` and ``idProduct``), device class, or even unique serial
numbers. This approach provides strong protection against rogue USB devices. When
a user needs to authorize a new device, they can temporarily disable the service, 
connect the device, use tools like ``lsusb`` to find its attributes, add it to their
:file:`/etc/usbauth/usbauth.conf` configuration file, and then re-enable the service.

Included below is an example of the content that may be included in the 
:file:`/etc/usbauth/usbauth.conf` configuration file:

.. code-block:: text
   :caption: /etc/usbauth/usbauth.conf

   # Allow a specific keyboard model.
   allow 046d:c52b

   # Also allow any device that identifies as a Mass Storage device.
   allow class 08

The above rules can be broken down into the following components:

* ``allow``: This is the action. It instructs the system to authorize any USB device that matches the criteria that follows.
* ``046d:c52b``: This is the matcher. It specifically targets the device's ``VendorID:ProductID`` pair. This rule does not distinguish between two identical keyboards; it allows any device of that exact model to connect.
* ``class 08``: This is an alternative type of matcher. The ``class`` keyword tells ``usbauth`` to look at the device's function rather than its manufacturer ID. The 08 is the value, which is the official `USB Class Code for Mass Storage devices <https://www.usb.org/defined-class-codes>`_. This single rule would permit any flash drive, external hard drive, or card reader to connect, regardless of its vendor or product ID.

You can learn more about ``usbauth`` through its `offical manpages <https://manpages.ubuntu.com/manpages/focal/man1/usbauth.1.html>`_.


usbguard
========

Starting with Ubuntu 16.10, the ``usbguard`` package has been available in universe 
to provide a robust framework for implementing USB device policies. It protects against
unauthorized USB devices by enforcing rules you define. When a USB device is plugged in,
``usbguard`` checks its attributes against the policy and decides whether to allow, block,
or reject it. In a similar vein to ``usbauth``, this is particularly effective at
preventing `BadUSB attacks <https://en.wikipedia.org/wiki/BadUSB>`_.

The primary tool is the ``usbguard`` command-line utility, which allows a user to generate
an initial policy, view currently connected devices, and manage rules. The ruleset is stored
in :file:`/etc/usbguard/rules.conf`. A typical workflow involves running usbguard 
``generate-policy > /etc/usbguard/rules.conf`` to create a baseline policy that allows all
currently connected devices. From that point on, any new device will be blocked by default.

When a new device is connected, the ``usbguard`` daemon logs the event, and a user can use 
``usbguard list-devices`` to see the blocked device. To permanently allow it, a user can use
``usbguard allow-device <id>`` and then append the new rule to their :file:`rules.conf` file 
to ensure it persists after a reboot. This makes ``usbguard`` a powerful and dynamic tool 
for managing USB security on a running system.

Included below is an example of the content that may be included in the :file:`rules.conf`
file after running ``generate-policy > /etc/usbguard/rules.conf``:

.. code-block:: text
   :caption: /etc/usbguard/rules.conf

   allow id 046d:c52b name "Unifying Receiver" serial "4071-DE-AD-BE-EF" via-port "usb3-port2" with-interface { 03:01:01 03:01:02 }
   allow id 046d:082d name "HD Pro Webcam C920" serial "BADA55C0" via-port "usb3-port1" with-interface { 0e:01:00 0e:02:00 }
   allow id 1d6b:0002 name "Linux Foundation 2.0 root hub" serial "" via-port "" with-interface { 09:00:00 }

The above rules can be broken down into the following components:

* ``allow``: This is the "target", meaning a device matching this rule will be authorized. Other targets are ``block`` and ``reject``.
* ``id 046d:c52b``: This is the ``VendorID:ProductID`` pair. This is a primary attribute for matching.
* ``name "Unifying Receiver"``: The human-readable device name. This is for a user's reference and is ignored by the matching engine.
* ``serial "4071-DE-AD-BE-EF"``: The device's unique serial number. If present, this makes the rule extremely specific to a single physical device.
* ``via-port "usb3-port2"``: The physical port the device is connected to. This can be used to enforce that a device is only allowed in a specific port.
* ``with-interface { 03:01:01 03:01:02 }`` This is the most critical part of the rule. It specifies the USB interfaces the device must have. In this case, ``03:01:01`` is a keyboard and ``03:01:02`` is a mouse, which is expected for a combo receiver. This prevents a device that shares the same Vendor/Product ID but has different functionality (like pretending to be a keyboard when it is not) from being authorized.

You can learn more about ``usbguard`` through its `official manpages <https://manpages.ubuntu.com/manpages/bionic/man1/usbguard.1.html>`_ or by visiting the `project repository <https://usbguard.github.io/>`_.
