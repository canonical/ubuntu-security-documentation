Configure cloud-enabled Livepatch
#################################


Cloud-Enabled livepatch is a feature that enables Livepatch to
intelligently roll out patches. Below are a set of CLI commands that
allow you to customise the configuration of your Livepatch client
config. For more info on Cloud-Enabled Livepatch see
`here </t/39163>`__.

Enable/disable
--------------

The Cloud-Enabled feature is enabled by default. To disable it, run:

::

   $ canonical-livepatch cloud-config --disable
   Successfully set cloud-config

You can re-enable the Cloud-Enabled feature via the following command:

::

   $ canonical-livepatch cloud-config --enable
   Successfully set cloud-config

Print current configuration
---------------------------

You can see your current Cloud-Enabled configuration, by running:

::

   $ canonical-livepatch status --format json
   {
     ...
     "Cloud-Enabled": {
       "cloud-enabled": true,
       "cloud": "aws",
       "region": "us-east-1",
       "az": "us-east-1a"
     }
     ...
   }

Override/reset configuration
----------------------------

Users may need to override their cloud/region/AZ settings. They can do
it by running such a command:

::

   $ canonical-livepatch cloud-config --set --cloud aws --region us-east-1 --az us-east-1a

If a user wishes to reset their cloud configuration, they may run:

::

   $ canonical-livepatch cloud-config --reset

This resets the Cloud-Enabled configuration back to the original state
and clears any overridden values. Note that resetting the configuration
does not disable or enable the Cloud-Enabled feature.
