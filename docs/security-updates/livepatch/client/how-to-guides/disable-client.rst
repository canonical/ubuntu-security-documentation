Disable client
###############

In case the livepatch client needs to be disabled, there are several
ways of approaching this.

If you have access to the system, one way is to disable the livepatch
service: ``$ sudo snap stop --disable canonical-livepatch``

If direct access to the system is not available, livepatch client can be
disabled in two ways: - by setting a kernel command line parameter
``canonical_livepatch_mode`` - by writing the mode to the
``/var/local/canonical_livepatch_mode`` file

These two locations are only checked when the livepatch daemon is
started (usually at boot).

The mode value can be: - ``normal`` - the default operation mode, patch
information is refreshed regularly and new patches are applied. -
``no-apply`` - patch information is refreshed, but new patches are not
applied to the kernel. - ``no-refresh`` - patch information is not
refreshed. - ``stop`` - the livepatch daemon will not start.
