Devices
#######

This section documents security features that protect against malicious external devices. 
External peripherals, in particular those connected via USB, present a unique security 
risk because they can act as more than just the device they appear to be. For example,
consider BadUSB attacks <https://en.wikipedia.org/wiki/BadUSB>_, where a device like a
flash drive or charging cable can secretly emulate a keyboard to inject malicious commands
into a user's system. The tools below provide mechanisms to authorize and manage devices,
reducing the risk of such attacks by ensuring only trusted hardware can interact with a 
user's system.

bolt
====

Starting with Ubuntu 18.04 Bionic Beaver, the bolt package has been available in main to provide a
desktop-oriented tool for using the Linux kernel's Thunderbolt authorization support. 


thunderbolt-tools
=================

Starting with Ubuntu 18.04 Bionic Beaver, the thunderbolt-tools package has been available in
universe to provide a server-oriented tool for using the Linux kernel's Thunderbolt
authorization support. 


usbauth
=======

Starting with Ubuntu 18.04 Bionic Beaver, the ``usbauth`` package has been available 
in universe to provide a straightforward tool for using the Linux kernel's 
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

* ``allow``: This is the action. It instructs the system to authorize any USB device that matches the criteria that follow.
* ``046d:c52b``: This is the matcher. It specifically targets the device's ``VendorID:ProductID`` pair. This rule does not distinguish between two identical device models; it allows any device of that exact model to connect.
* ``class 08``: This is an alternative type of matcher. The ``class`` keyword tells ``usbauth`` to look at the device's function rather than its manufacturer ID. The 08 is the value, which is the official `USB Class Code for Mass Storage devices <https://www.usb.org/defined-class-codes>`_. This single rule would permit any flash drive, external hard drive, or card reader to connect, regardless of its vendor or product ID.

While these rules provide effective filtering, it's important to understand the limitations
these rules have for risk reduction. A malicious device can be programmed to lie about its
attributes, such as its device class, vendor, or product ID. This can allow a malicious
device to be allowed by existing rules, so while this ``usbauth`` is an effective way to
minimize the risk external devices connected via USB pose to a user's system, it does not
outright eliminate said risk.

You can learn more about ``usbauth`` through its 
`official manpages <https://manpages.ubuntu.com/manpages/noble/en/man8/usbauth.8.html>`_.


usbguard
========

Starting with Ubuntu 16.10 Yakkety Yak, the ``usbguard`` package has been available in
universe to provide a framework for implementing USB device policies. It provides a 
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

While managing ``usbguard`` from the command-line is effective, it can be cumbersome
on a desktop system. To improve usability, the ``usbguard-notifier`` service is
available. This tool monitors the ``usbguard`` daemon and provides a desktop
notification whenever a device is blocked. This notification pop-up allows a user to
immediately authorize the device and add a permanent rule for it, transforming the
experience from a manual, command-line process into an interactive one. It is the
successor to older tools like ``usbguard-applet-qt``.

Included below is an example of the content that may be included in the :file:`rules.conf`
file after running ``usbguard generate-policy > /etc/usbguard/rules.conf``:

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
* ``with-interface { 03:01:01 03:01:02 }`` This is often the most critical attribute for security. It specifies the exact functions (e.g., keyboard, mouse, mass storage) the device is allowed to have. This is powerful for managing composite devices, which present multiple functions at once. For example, a programmable keyboard might also act as a mass storage device to store its configuration. A strict rule can allow the keyboard interface (03:01:01) while blocking the mass storage interface (08:06:50), greatly reducing the attack surface.

By combining multiple attributes, especially the ``with-interface`` check, ``usbguard`` makes
it significantly more difficult, but not outright impossible, for a malicious device to
bypass the guardrails put in place by ``usbgaurd``, offering a substantial reduction in risk.

You can learn more about ``usbguard`` through its
`official manpages <https://manpages.ubuntu.com/manpages/noble/man1/usbguard.1.html>`_ or by
visiting the `project repository <https://usbguard.github.io/>`_. You can also learn more about
``usbguard-notifier`` through its 
`official manpages <https://manpages.ubuntu.com/manpages/noble/man1/usbguard-notifier.1.html>`_.
