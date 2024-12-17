Fetch patches
#############

The livepatch application is configured to fetch patch updates every 24
hours. This setting is
`configurable </t/configuration/48791#patch-sync>`__.

Patch snapshot downloads can also be manually triggered:

::

   $ livepatch-admin sync trigger --wait

We recommend triggering a patch snapshot download once the server is
successfully set up.

Verifying that server is up to date
===================================

To verify that the server is receiving the latest patches from the
livepatch server hosted by Canonical use the following command.

::

   $ livepatch-admin sync reports
