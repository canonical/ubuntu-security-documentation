Report bugs
###########

Please file bugs at `the canonical-livepatch launchpad
project <https://bugs.launchpad.net/canonical-livepatch-client/+filebug>`__.
When you open a bug, please provide the output from the following
commands, so that we can troubleshoot your issue:

-  ``snap info canonical-livepatch``
-  ``canonical-livepatch status``
-  ``lsb_release -a``
-  ``uname -a``
-  ``journalctl -u snap.canonical-livepatch.canonical-livepatchd``

The output of ``journalctl`` can be long, so consider piping the output
into ``tail -100`` to only show recent issues.

**Note:** We recommend marking the bug as private if any of the output
contains personal information that you do not want publicly available
and searchable.
