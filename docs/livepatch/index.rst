Livepatch
#########

`Canonical Livepatch <https://ubuntu.com/security/livepatch>`__ patches
high and critical linux kernel vulnerabilities removing the immediate
need to reboot to upgrade the kernel, instead allowing the downtime to
be scheduled. It is a part of the `Ubuntu
Pro <https://ubuntu.com/pro>`__ offering.

The ubuntu livepatch offering consists of the `client
application </client/index>`__, the livepatch service hosted by
Canonical and an optional `on-prem server </on-prem-server/index>`__.
The client runs on machines, periodically checks for available patches,
downloads, verifies and installs them.

Canonical livepatch is meant for critical infrastructure, where
unscheduled downtime is to be avoided. By applying live kernel patches
for high and critical kernel vulnerabilities, upgrades can be scheduled
at a suitable time.

If you’re using `Ubuntu Pro <http://ubuntu.com/pro>`__, then you’ll have
access to two additional Livepatch features.

1. Delayed updates for your `Livepatch clients </client/index>`__,,
   providing further security and protection.
2. Access to the `on-prem server </on-prem-server/index>`__.

`Livepatch Client </client/index>`__
------------------------------------

Livepatch is the client side software that runs on individual machines
and periodically checks for the availability of kernel patches. Once a
patch becomes available, it is downloaded, verified and applied to the
current kernel.

`Livepatch On-prem </on-prem-server/index>`__
---------------------------------------------

Complex enterprise environments often follow policies that require a
gradual roll-out of updates to reduce risk, or have high-security
isolated environments that need to be updated. Livepatch on-prem allows
an organization to define a rollout policy and remain in full control of
which machines will get updated and when. To keep your machines
up-to-date, the on-premises service regularly syncs with Livepatch
hosted by Canonical and obtains the latest patches. It then deploys the
patches gradually in as many stages as required.


.. toctree::
   :maxdepth: 2
   :hidden:
   
   client/index
   on-prem-server/index
   