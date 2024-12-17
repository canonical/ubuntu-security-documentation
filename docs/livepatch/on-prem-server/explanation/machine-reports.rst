Machine reports
###############

Each machine running the Livepatch Client will periodically check in
with its configured server.

The machine checks for patches and sends machine status information. The
full list of information sent is documented
`here <https://ubuntu.com/security/livepatch/docs/livepatch/reference/data>`__.

Enabling Machine Reports
------------------------

See our `machine reports
config </t/configuration/48791#machine-reports>`__ to enable machine
reports and configure their retention period.

Generating Machine Reports
--------------------------

To generate machine reports use the Livepatch admin tool. See `our
how-to <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/how-to/administration_tool>`__
on setting up the admin tool.

You can create machine reports where you query machines by their tier,
last applied patch version or patch state.

``livepatch-admin report machines <tier> [<patch version> [<patch state]]``
