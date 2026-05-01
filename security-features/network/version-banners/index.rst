Daemon version banners
======================

Network server daemons often advertise their installed version to clients as
part of their protocol. This functionality could be either mandatory, as part of
the protocol negotiation, or provided for convenience only. The text that
includes the server's version if often called a "version banner".

Having version banners enabled on a public service will effectively disclose the
software version of the server daemon to the world. Security guidelines and
security scanners may recommend disabling version banners for this reason.
However, disabling version banners has both advantages and disadvantages.

Advantages of disabling version banners
---------------------------------------

Threat actors often perform recognisance scans as a preliminary step to attacks.
Obtaining as much data as possible about the software stack of the target will
facilitate future actions. Version banners could leak information useful to a
threat actor to mount an attack.

Similarly, threat actors often run automatic scanners on Internet-facing
services searching for network servers with versions vulnerable to known
exploits. Even if the software is not vulnerable, the scanners may incorrectly
determine that they should attempt exploits, leading unnecessary alerts. These
automatic scanners might skip servers that do not expose their versions.

Disadvantages of disabling version banners
------------------------------------------

Disabling version banners is considered to be security by obscurity. If a
software version is vulnerable, the recommended approach is to patch it. The
vulnerability will remain exploitable, irrespective of the version being
advertised publicly. Additionally, it is often possible to derive with a certain
degree of confidence the version that a network daemon is based on probing and
observing its behaviour.

A network vulnerability management scanner often relies on the same version
banner that threat actors' scanners use. If these are disabled, the scanner may
no longer determine the correct version, which could lead to a large number of
false positives (the scanner reports vulnerabilities which the software is not
affected by). This could be especially problematic if a partial version can be
determined, but without the Ubuntu patch level, as explained below.


Version banners may not be precise
----------------------------------

Ubuntu, as a stable rather than rolling distribution, will not update packages
in a particular release to the newest version available from upstream. Instead,
security patches and bug fixes will be backported to the particular version that
was available when the Ubuntu release in question was first published.

For example, the OpenSSH server version available with the Ubuntu Noble Numbat
(24.04) release was 9.6p1. Vulnerabilities have since been identified and fixed
in subsequent versions: 9.8, 9.9p2, etc. In Ubuntu, these fixes were backported
to the 9.6p1 version. At the time of this writing, the latest version of OpenSSH
available in Noble is 9.6p1-3ubuntu13.16.

If a scanner were to rely on the upstream or a heuristically-guessed version,
such as 9.6p1, it would not be able to differentiate between the various Ubuntu
patch levels (9.6p1-3ubuntu13.16, 9.6p1-3ubuntu13.15, 9.6p1-3ubuntu13.14, etc.)
and would likely produce a large number of false positives.

The protocol may dictate that at least a partial version needs to be advertised
for negotiation. This would exacerbate the problem, as Ubuntu patch level would
be unlikely to be included in such an exchange (e.g. retaining only ``9.6`` in
the OpenSSH example above).

Service-specific configuration
------------------------------

.. toctree::
   :maxdepth: 1
   :glob:

   *
