Disabling AppArmor
##################

:doc:`AppArmor <../security-features/privilege-restriction/apparmor>` is the
default Mandatory Access Control (MAC) system on Ubuntu. It enforces policies
for the running processes based on an allow-list of actions that they can take,
such as files that can be accessed, network connections that can established or
capabilities that the processes can hold.

If an application's profile restricts an action that the process should
legitimately take, the application may not function correctly, or as expected.
In such an instance, people or online forums might suggest `disabling AppArmor
altogether
<https://ubuntu.com/server/docs/how-to/security/apparmor/#disabling-or-re-enabling-apparmor>`_.
Ubuntu stronly advises against this, as it would disable the protections for all
the other applications installed, as well as for :doc:`snaps
<../security-features/privilege-restriction/snap-confinement>`.

Instead, you should take one or more of the following steps:

- Open a `bug report
  <https://documentation.ubuntu.com/project/contributors/qa-and-testing/report-a-bug/>`_.
- `Identify and correct
  <https://ubuntu.com/server/docs/how-to/security/apparmor/#checking-and-debugging-denies>`_
  the problem in the AppArmor profile.
- As a last resort, `disable only the problematic profile
  <https://ubuntu.com/server/docs/how-to/security/apparmor/#disabling-or-re-enabling-a-profile>`_,
  as long as you understand the risks that this action could expose you to.
