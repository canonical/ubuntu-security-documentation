Configure proxy for fetching patches
####################################

Livepatch on-prem server can fetch patches through an HTTP proxy. The
configuration steps vary depending on the deployment platform.

See our `patch-sync config </t/configuration/48791#patch-sync>`__ for
more details.

Juju deployments (latest charms)
--------------------------------

If Livepatch on-prem has been deployed using Juju, run the following
Juju configuration command:

.. code:: bash

   $ juju config livepatch \
       patch-sync.proxy.enabled=true \
       patch-sync.proxy.http=http://proxy.example.com \
       patch-sync.proxy.https=http://proxy.example.com

Juju deployments (deprecated charm)
-----------------------------------

If Livepatch on-prem has been deployed using Juju with our older
reactive charm (see our migration guide
`here </on-prem-server/reference/charm-migration>`__), run the following
Juju configuration command:

.. code:: bash

   $ juju config livepatch \
       http_proxy=http://proxy.example.com \
       https_proxy=http://proxy.example.com

Snap deployments
----------------

If Livepatch on-prem has been deployed using Snap, users can run the
following commands to configure a proxy:

.. code:: bash

   $ sudo snap set canonical-livepatch-server lp.patch-sync.proxy.enabled=true
   $ sudo snap set canonical-livepatch-server lp.patch-sync.proxy.http=http://proxy.example.com
   $ sudo snap set canonical-livepatch-server lp.patch-sync.proxy.https=http://proxy.example.com

You can see the applied configuration by running the following:

.. code:: bash

   $ sudo snap get canonical-livepatch-server lp.patch-sync.proxy
   Key                          Value
   lp.patch-sync.proxy.enabled  true
   lp.patch-sync.proxy.http     http://proxy.example.com
   lp.patch-sync.proxy.https    http://proxy.example.com
