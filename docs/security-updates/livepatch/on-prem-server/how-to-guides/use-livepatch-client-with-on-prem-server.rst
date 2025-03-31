Use livepatch client with on-prem server
########################################

Network access
--------------

Machines running livepatch-client will need network access to the
on-prem server. HTTPS (:443) or HTTP (:80) is used, depending on how the
livepatch on-prem haproxy and the livepatch application’s url_template
setting are configured.

In addition to that, machines will require access to the Canonical snap
store to install the livepatch client snap:

-  Snapstore: api.snapcraft.io:443
-  Snapstore CDN: \*.snapcraftcontent.com:443

Generating the authorization token
----------------------------------

To configure this livepatch client to start pulling patches from the
on-prem livepatch server, an authorization token is necessary. To issue
it, run:

::

   $ livepatch-admin auth-token <id> <tier>

The tier parameter is one of the tiers available on the server. The
client will download patches as they become available in that tier. See
`this
page <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/reference/patch_management>`__
on how to manage tiers and patches in your on-prem server.

The id parameter bears no significance in an on-prem deployment. It can
be set to a value identifying the group of livepatch clients that will
be enabled using the same token (a single authorization token can be
used to enable multiple client instances).

Configuring livepatch client
----------------------------

To start applying livepatches to a machine, it is necessary to install
the livepatch client on it. Livepatch client is currently distributed as
a snap. On the machine run:

::

   $ sudo snap install canonical-livepatch

Once the client is installed, it needs to be configured to pull patches
from the on-prem server:

::

   $ canonical-livepatch config remote-server="http(s)://<hostname>"

The authorization token returned can be then used to attach any number
of machines to the on-prem livepatch server:

::

   $ canonical-livepatch enable <token>
