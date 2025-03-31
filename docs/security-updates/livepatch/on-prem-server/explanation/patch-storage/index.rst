Patch storage
=============

Livepatch server supports several different drivers for storing patch
files downloaded from livepatch.canonical.com:

1. Local filesystem
2. Swift
3. S3 (and compatible implementations, e.g. minio)
4. Postgresql

The filesystem patch store is easiest to deploy and suits most
configurations. However, if there is a need to scale out the livepatch
server such as have multiple livepatch servers running to handle the
load, the filesystem patch store should not be used.

In case there is a need to scale out livepatch on-prem, use the s3,
postgresql or swift patch stores. Any patch store should have enough
space for storing livepatches - currently at least 45GB for all patches,
see `this
guide <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/how-to/set_patch_sync_filters>`__
to filter patches sent to your on-prem instance to specific kernel
variants/architectures and lower this requirement.

See the `patch storage </t/configuration/48791#server-config>`__ config
for all available parameters.

.. toctree::
   :maxdepth: 2
   
   use-s3-for-patch-storage