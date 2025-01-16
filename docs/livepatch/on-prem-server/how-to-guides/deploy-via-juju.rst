Deploy via Juju
###############

Prerequisites
=============

\```{note} :warning: This guide has been deprecated. Refer to our
`tutorials </on-prem-server/tutorial/index>`__ or `snap
how-to </on-prem-server/how-to-guides/deploy-via-snap>`__.

If you have an existing deployment using this document, see our
`migration guide </on-prem-server/reference/charm-migration>`__ to
update your deployment.

::


   We will deploy and configure the livepatch on-prem server using Juju and Charmed Operators. Juju is an Open Source Charmed Operator Framework that controls the whole lifecycle of an application - including machine applications. Please follow the [installation instructions](https://juju.is/docs/installing) for your system.

   The livepatch on-prem bundle needs to be deployed on machines running Ubuntu focal.

   You don’t need to have previous or advanced knowledge of Juju or Charmed Operators to follow this guide and deploy livepatch.

   ## Livepatch authorization token

   Since on-prem livepatch servers act as caching proxies for the livepatch service hosted by canonical, the subscription token is required to authorize the on-prem instance to pull patch information.

   To get your Ubuntu Pro subscription token, please go to https://ubuntu.com/pro.
   ![image1|690x373](upload://9IhZmAFso5ufkbB8QyboWUoROad.png) 

   # Deployment Steps

   ## 1. Initialize juju

   Once you have Juju CLI installed, you will need to bootstrap a Juju controller to your cloud. The [Juju documentation](https://juju.is/docs/clouds) has detailed instructions on how to do that for several clouds and machine types.

   See[ resources topic ](https://discourse.ubuntu.com/t/machine-resources-for-livepatch-on-prem/22548) for requirements for the virtual machines running livepatch on-premises services.

   ## 2. Deploying the bundle

   The bundle and charmed operators necessary to deploy livepatch server are available in the charmstore at

   https://charmhub.io/canonical-livepatch-onprem

   To start the deployment on a created juju model, run:

$ juju deploy ch:canonical-livepatch-onprem

::


   ## 3. Configuring livepatch

   After the deployment completes, verify the status of the model by running:

$ juju status

::


   The output should look like:
   ![screenshot_20210601_164245|648x159](upload://z8RLGfl4BdhI501OBguUgqlpaKY.png) 

   At this point the livepatch unit is expected to be in a blocked state with the message:
   "✘ sync_token not set"

   Provide the token (acquired by following instructions in the Livepatch authorization token section) by running:

$ juju config ubuntu-advantage token=“”

$ juju run-action livepatch/leader get-resource-token –wait

::

   The output should indicate the token has successfully been acquired:
   ![screenshot_20210601_164500|690x127](upload://fboev1KPeCS41ZI0OUD6Zsde1vC.png) 

   After that, provide the url_template setting as follows:

juju config livepatch
url_template=“http://10.94.227.82/v1/patches/{filename}”

::

   The url_template specifies the url where patch files can be downloaded by livepatch client agents. The url template should be of the form 'http(s)://{HOSTNAME}/v1/patches/{filename}'. The hostname is the only part that needs to be changed. The hostname can be just the ip address of the haproxy unit. If a DNS hostname is configured for the haproxy IP address, that can be used too.

   ### Deploying with a config overlay (Optional)

   These settings can be configured at deploy-time by using a juju bundle overlay:

$ juju deploy ch:canonical-livepatch-onprem –overlay config.yaml

::


   The overlay file should have the following content:

applications: livepatch: options: url_template: ubuntu-advantage:
options: token:

::


   ## 4. Setting up authentication

   To enable admin tool access to the livepatch server, authentication needs to be configured. The easiest way is to enable username/password authentication.

   Generate the password hash using:

$ sudo apt-get -y install whois

$ mkpasswd -m bcrypt admin123
$2b$05$BmmTKkhnl1w303GO.JZTtOS5BIqZS.BYZU2kJzRIYOFx6SuQ9A.yG

::

   Use the output of the previous command to configure livepatch. (note the 
single quotes used below to escape special characters when using a raw hash, 
and double quotes when passing it inline):

$ juju config livepatch
auth_basic_users=‘username:$2b$05$BmmTKk..IYOFx6SuQ9A.yG’

You can also combine this into a single command that prompts for the password:

   $ juju config livepatch auth.basic.users="admin:$(mkpasswd -m bcrypt)"

Or you can pass the password in, if you want to use this non-interactively:

   $ juju config livepatch auth.basic.users="admin:$(mkpasswd -m bcrypt admin123)"

::


   See [Administration Tool](https://discourse.ubuntu.com/t/livepatch-server-administration-tool/22551) topic for instructions on installing the administration tool and setting up authentication.

   Once this has been done, the livepatch admin tool can be used to authenticate:

$ export LIVEPATCH_URL=http(s)://{haproxy url}

$ livepatch-admin login -a [username:password]

::

   ## 5. Downloading patches

   The final step before attaching client machines to the server is to download patches from Canonical servers. This can be done using the admin tool. See the [Administration tool]() topic on how to install it.

   To download patches, run:

$ livepatch-admin sync trigger –wait

::


   # Enabling machine status reporting
   Each livepatch on-prem instance can optionally send information about the status of the machines it's serving back to Canonical. This functionality is opt-in.

   The information sent back about each machine includes:
   - Kernel version
   - CPU model
   - Architecture
   - Boot time and uptime
   - Livepatch client version
   - Obfuscated machine id
   - Status of the patch currently applied to the machine's kernel

   To enable this reporting, run the following juju command:

$ juju config livepatch sync_send_machine_reports=true \``\`

This can be disabled at any time by setting the flag to ``false``.
