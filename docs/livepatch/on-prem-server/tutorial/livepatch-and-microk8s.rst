Livepatch and microk8s
######################

Introduction
============

Livepatch on-prem is a self-hosted version of the Livepatch server,
enabling the delivery of patches to machines within network restricted
environments.

This tutorial will deploy the Livepatch On-prem server as a Kubernetes
application. We will deploy and configure the livepatch on-prem server
using Juju and Charmed Operators. Juju is an Open Source Charmed
Operator Framework that controls the whole lifecycle of an application.
While this is one option for deploying the on-prem server, another is to
deploy to virtual machines as described
`here <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/how-to/deployment>`__.

For this tutorial we will use Microk8s, a lightweight tool for creating
a local Kubernetes cluster.

You don’t need to have previous or advanced knowledge of Juju or Charmed
Operators to follow this guide and deploy livepatch.

Livepatch authorization token
-----------------------------

Since on-prem livepatch servers act as caching proxies for the livepatch
service hosted by Canonical, a subscription token is required to
authorise the on-prem instance to pull patch information.

To get your Ubuntu Pro subscription token, please go to
https://ubuntu.com/pro/dashboard, login to your Ubuntu SSO account and
use your free personal token for the remainder of this guide.

Deployment Steps
================

1. (Optional) Setup Multipass environment
-----------------------------------------

Multipass is a CLI tool to launch Ubuntu VMs from Windows, Linux and
MacOS. The remainder of this guide can be run from within a multipass VM
to avoid affecting the host machine.

Start by running the following commands to install and start a Multipass
VM, the optional section will define the VM’s memory/cpu/disk usage.

::

   $ sudo snap install multipass
   $ multipass launch jammy --name livepatch-deploy [-m 12g -c 4 -d 40G]
   $ multipass shell livepatch-deploy

2. Initialize Juju and microk8s
-------------------------------

Now we can install our dependencies, note that Juju 3.1 only works with
a strictly confined microk8s Snap.

::

   $ sudo snap install microk8s --channel=1.25-strict/stable
   $ sudo snap install juju --channel=3.1/stable

Once you have the Juju CLI installed, you will need to bootstrap a Juju
controller to your cloud (microk8s in this case). The `Juju
documentation <https://juju.is/docs/juju/get-started-with-juju>`__ has
detailed instructions on how to do that for several clouds and machine
types.

To begin,

::

   # Add the 'ubuntu' user to the MicroK8s group:
   $ sudo usermod -a -G snap_microk8s ubuntu
   # Give the 'ubuntu' user permissions to read the ~/.kube directory:
   $ sudo chown -f -R ubuntu ~/.kube
   # Create the 'microk8s' group:
   $ newgrp snap_microk8s
   # Enable the necessary MicroK8s addons:
   $ sudo microk8s enable hostpath-storage dns ingress
   # Set up a short alias for the Kubernetes CLI:
   $ sudo snap alias microk8s.kubectl kubectl

Next,

::

   # Since the Juju package is strictly confined, you also need to manually create a path:
   $ mkdir -p ~/.local/share
   $ juju bootstrap microk8s livepatch-demo-controller
   $ juju add-model livepatch

3. Deploying the bundle
-----------------------

The bundle and charmed operators necessary to deploy livepatch server
are available in the charmstore using the “k8s” track at

https://charmhub.io/canonical-livepatch-onprem

Livepatch On-Prem needs a place to store patches that it syncs from the
upstream. By default the above “k8s” bundle will store patches in
Postgres directly. Other options including S3 storage are available and
can be configured as described
`here <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/how-to/storage/configure>`__.

In order to ensure Postgres has enough space, see our `resources
topic <https://discourse.ubuntu.com/t/machine-resources-for-livepatch-on-prem/22548>`__
for requirements on virtual machines running livepatch on-prem. Although
this information relates to the deployment of Livepatch on virtual
machines, the storage requirements remain similar.

To start the deployment within the previously created juju model, run:

::

   $ juju deploy canonical-livepatch-onprem --channel=k8s/stable --trust

4. Configuring livepatch
------------------------

After the deployment completes, verify the status of the model by
running:

::

   $ juju status

The output should look like the following while the applications are
initialising:

.. figure:: https://lh5.googleusercontent.com/haNMs00cr4buv3xttS-HhQPeaMwMsw3sycR37Xc-sSAAmteOfYzC9i-3irPzi_q6osgVwdx3E-WCBAIym7r1pLvMBXCDSGgcVARsFDG3w9Po4zuI3e0FNxjvuE2SnuCjyvCOLMuoEUn9MI7W2NK4610
   :alt: \|624x116

   \|624x116

After initialisation, the livepatch unit is expected to be in a blocked
state with the message:

``"✘ patch-sync token not set, run get-resource-token action"``

Provide the token (acquired by following instructions in the Livepatch
authorization token section) by running:

::

   $ juju run livepatch/leader get-resource-token contract-token=<token> --wait 30s

The output should indicate the token has successfully been acquired:

.. figure:: https://lh4.googleusercontent.com/GzH_1cVxnKPqW-_rDbnKSxn7xsfDqwBvxUCG-dBJuEvaBQES3k_A6kc-rbvV5e-8kdKRpt7Vxhsz1JKCNYoMEC9UjXj_KQxKIF9FF_vnO7u1eTcHC67vAwfy7q9JDloXIwYFS6UKlKerJwTNdb6wP7U
   :alt: \|624x61

   \|624x61

After that, provide the url_template setting as follows:

::

   juju config livepatch server.url-template="http://10.1.236.9:8080/v1/patches/{filename}"

The url_template specifies the url where patch files can be downloaded
by livepatch clients. The url template should be of the form
‘http(s)://{HOSTNAME}/v1/patches/{filename}’. The hostname is the only
part that needs to be changed. When using microk8s, all pods and
services are exposed by default to the host so the hostname simplifies
to the ip address of the livepatch-server unit (this is the pod’s IP
address). This is useful for testing but not helpful in a production
setup. You should now be able to curl the Livepatch pod with

::

   $ curl 10.1.236.9:8080
   Canonical Livepatch Health service, version v1.13.1

To take this a step further we can configure the ``service-hostname``
config option of the nginx-ingress-integrator charm which will then set
up an ingress in the microk8s cluster. That can be tested as follows,

::

   $ juju config ingress service-hostname=livepatch.test.com
   $ kubectl get ingress -n livepatch
   NAME CLASS HOSTS ADDRESS PORTS AGE
   livepatch-test-com-ingress public livepatch.test.com 127.0.0.1 80 2m14s
   # Next we will edit our hosts file to make this address reachable locally
   $ echo '127.0.0.1 livepatch.test.com' | sudo tee -a /etc/hosts
   $ curl livepatch.test.com
   Canonical Livepatch Health service, version v1.13.1

Follow up on this by changing the url-template to match the ingress with

::

   juju config livepatch server.url-template="http://livepatch.test.com/v1/patches/{filename}"

To run this in a production environment, you will need to expose this
microk8s cluster publicly.

Deploying with a config overlay (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These settings can be configured at deploy-time by using a juju bundle
overlay:

::

   $ juju deploy ch:canonical-livepatch-onprem –channel=k8s/stable --overlay config.yaml

The overlay file should have the following content:

::

   applications:
     livepatch:
       options:
         url_template: <patch url template>
         external_hostname: <your-desired-hostname>

5. Setting up authentication
----------------------------

To enable admin tool access to the livepatch server, authentication
needs to be configured. This is done with username/password
authentication.

Generate the password hash using:

::

   $ sudo apt-get install apache2-utils
   $ htpasswd -bnBC 10 <username> <password>
   username:$2y$10$74ZpDgHaxnUQo.AJZk1cMuSRfef5oK5xq5o/GLbUH/Bbw6W2bmctm

The above is a ``username:<hashed-password>`` pair that was generated
from the pair “username:password” exactly. This should be changed for a
production workload.

Use the output of the previous command to configure livepatch:

::

   $ juju config livepatch auth.basic.enabled=true
   $ juju config livepatch auth.basic.users='username:$2y$10$74ZgHaxn...UH/Bbw6W2bmctm'

See `Administration
Tool <https://discourse.ubuntu.com/t/livepatch-server-administration-tool/22551>`__
topic for instructions on installing the administration tool and setting
up authentication.

Once this has been done, the livepatch admin tool can be used to
authenticate:

::

   $ export LIVEPATCH_URL=http(s)://{pod or ingress url}
   $ livepatch-admin login -a username:password

6. Downloading patches
----------------------

The final step before attaching client machines to the server is to
download patches from Canonical servers. This can be done using the
admin tool. See the `Administration tool <>`__ topic on how to install
it.

To download patches, run:

::

   $ livepatch-admin sync trigger --wait

To check for synced patches run:

::

   $ livepatch-admin storage patches

And to check for any sync failures run:

::

   $ livepatch-admin sync report

To limit which patches are downloaded see this
`document <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/how-to/set_patch_sync_filters>`__.

Enabling machine status reporting
=================================

Each livepatch on-prem instance can optionally send information about
the status of the machines it’s serving back to Canonical. This
functionality is opt-in.

The information sent back about each machine includes:

-  Kernel version
-  CPU model
-  Architecture
-  Boot time and uptime
-  Livepatch client version
-  Obfuscated machine id
-  Status of the patch currently applied to the machine’s kernel

To enable this reporting, run the following juju command:

::

   $ juju config livepatch patch-sync.send-machine-reports=true

This can be disabled at any time by setting the flag to ``false``.

7. Cleaning up
--------------

To clean up your Juju model you can run the following:

::

   $ juju destroy-model --no-prompt livepatch --destroy-storage

And to cleanup the Multipass VM:

::

   $ multipass delete --purge livepatch-deploy
