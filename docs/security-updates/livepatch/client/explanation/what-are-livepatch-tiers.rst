What are Livepatch tiers
########################

Livepatch delivers patches to “tiers”. A tier is a target audience for
the delivery of a patch. Your tier depends on whether you have a free or
paid subscription to `Ubuntu Pro <https://ubuntu.com/pro>`__. The
differences are outlined below.

+-------------------------------+---------------------------------------+
| Tier                          | Description                           |
+===============================+=======================================+
| Proposed                      | The initial tier where patches are    |
|                               | added before they are promoted to the |
|                               | next tiers.                           |
+-------------------------------+---------------------------------------+
| Internal                      | For internal Canonical use. Updates   |
|                               | are first tested then applied across  |
|                               | Canonical infrastructure to decrease  |
|                               | the odds of a faulty patch making it  |
|                               | to customer machines.                 |
+-------------------------------+---------------------------------------+
| Updates                       | For free users of Ubuntu Pro. Patches |
|                               | are delivered to these machines next. |
+-------------------------------+---------------------------------------+
| Stable                        | For paid users of Ubuntu Pro. Patches |
|                               | are delivered to these machines last. |
+-------------------------------+---------------------------------------+

Our kernel team closely monitors the patch health within internal before
promoting to updates and further monitoring is done before promoting the
patch to stable.

For finer-grained control over patch roll-out take a look at `Livepatch
On-Prem <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem>`__.
