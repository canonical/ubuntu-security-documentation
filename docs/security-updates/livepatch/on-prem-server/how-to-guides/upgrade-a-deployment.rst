Upgrade a deployment
####################

To upgrade the livepatch on-prem deployment, each application needs to
be upgraded separately:

::

   $ juju refresh haproxy

::

   $ juju refresh postgresql

::

   $ juju refresh ubuntu-advantage

::

   $ juju refresh livepatch

After upgrading the livepatch application, a schema upgrade may be
required. This will be indicated in the application’s status in juju
status. In such a case, run the command:

::

   $ juju run-action livepatch/leader schema-upgrade --wait

One can also restart the livepatch application with the following
command:

::

   $ juju run-action livepatch/<desired-unit> restart --wait

..

   Note: ``juju run-action`` has been renamed to ``juju run`` from Juju
   v3 See https://juju.is/docs/juju/manage-actions#heading–run-an-action
   for more details.
