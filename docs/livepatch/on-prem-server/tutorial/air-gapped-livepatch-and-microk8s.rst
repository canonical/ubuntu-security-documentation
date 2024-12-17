Air-gapped Livepatch and microk8s
#################################

Introduction
============

Livepatch on-prem is a self-hosted version of the Livepatch server,
enabling the delivery of patches to machines within network restricted
environments. For security reasons, administrators may prefer to deploy
Livepatch on-prem server in an air-gapped environment with restricted
Internet access.

This tutorial will deploy the Livepatch on-prem server as a Kubernetes
application in an air-gapped environment. We will deploy and configure
the Livepatch on-prem server using Juju and Charmed Operators. Juju is
an Open Source Charmed Operator Framework that controls the whole
lifecycle of an application.

For this tutorial, we will use Microk8s, a lightweight tool for creating
a local Kubernetes cluster. You don’t need previous knowledge of Juju or
Charmed Operators to follow this guide and deploy Livepatch.

How does Livepatch on-prem work in an air-gapped environment?
-------------------------------------------------------------

Generally, in order to perform authentication/authorisation of machines
and also fetching latest patches, the Livepatch on-prem server needs to
communicate with the main Livepatch server hosted by Canonical. In an
air-gapped environment, where such communication is not available, these
functions have to be handled in an indirect way by using the following
tools:

-  `Air-gapped Ubuntu Pro
   Server <https://discourse.charmhub.io/t/15278>`__ is an on-prem
   deployable service that provides services related to Ubuntu Pro
   subscriptions in air-gapped environments. Livepatch on-prem can be
   integrated with this service to perform authentication/authorisation
   of machines and handle subscription-related functionalities.
-  `Patch
   Downloader <https://snapcraft.io/canonical-livepatch-downloader>`__
   is a CLI tool that can be used to download the latest patch files
   from the Livepatch server. In an air-gapped setup, the administrators
   of Livepatch on-prem should use this tool to fetch the latest patches
   and then upload them to the configured patch storage. You can check
   out `this </on-prem-server/explanation/patch-storage/index>`__ topic
   on how to configure various types of storage for Livepatch on-prem.
   `This </on-prem-server/how-to-guides/use-the-patch-downloader-tool>`__
   topic explains how to use the Patch Downloader tool to fetch patches.

``{note} :information_source: When deploying air-gapped Livepatch on-prem on MicroK8s, it is best to configure the patch storage to something independently accessible within your infrastructure, like an S3/Swift bucket, instead of PostgreSQL or filesystem. This way, Livepatch administrators can independently download the latest patches via the Patch Downloader CLI tool and transfer them to the patch storage.``

Deployment steps
================

In this tutorial, we use `Multipass <https://multipass.run>`__ to create
an Ubuntu virtual machine (VM) to deploy Livepatch and its dependencies
on it. If not already installed, we can use the command below to install
Multipass:

.. code:: sh

   sudo snap install multipass

Step 1: Create a VM
-------------------

Once Multipass is installed, you can create the VM for this tutorial by
running the command below. This will create a VM, named
``livepatch-deploy`` with the sufficient resources.

.. code:: sh

   multipass launch jammy --name livepatch-deploy --cpus 6 --memory 12G --disk 40G

Once the VM is created you need to open an interactive shell into it by
running:

.. code:: sh

   multipass shell livepatch-deploy

Step 2: Setup MicroK8s
----------------------

To deploy Livepatch on-prem and the air-gapped Ubuntu Pro server, we
would need Juju, MicroK8s, and LXD. The latter is already installed in
the VM, so we just need the other two. To install MicroK8s, you need to
use the following command:

.. code:: sh

   sudo snap install microk8s --channel=1.30-strict/stable

Once the installation is done, you need to apply the following
configurations to make it easier to use MicroK8s with the current user
and the ``kubectl`` CLI tool:

.. code:: sh

   sudo usermod -a -G snap_microk8s $USER
   mkdir -p ~/.kube
   chmod 0700 ~/.kube
   newgrp snap_microk8s

The next step is to enable some required addons on your MicroK8s
cluster. To do this, you need to run:

.. code:: sh

   sudo microk8s enable rbac
   sudo microk8s enable hostpath-storage
   sudo microk8s enable ingress

Now, to make sure MicroK8s is up and running, try:

.. code:: sh

   microk8s status --wait-ready

You should see an output like this, which means MicroK8s is ready to be
used.

.. code:: text

   microk8s is running
   ...

Step 3: Setup Juju
------------------

In this tutorial, we use Juju 3.5, which can be installed by running:

.. code:: sh

   sudo snap install juju --channel=3.5/stable

After the installation is done, we need to modify the MicroK8s client
configuration file so that the API address is accessible to the Juju
controllers we are going to create in the next steps. To do this, we
need to run the following:

.. code:: sh

   microk8s.config > /tmp/microk8s.config
   sudo cp /tmp/microk8s.config /var/snap/microk8s/current/credentials/client.config
   sudo snap restart microk8s

Now, we need to bootstrap two controllers; one on our MicroK8s cluster,
and one one LXD. We will use the MicroK8s controller to deploy Livepatch
on-prem, and the other to deploy the air-gapped Ubuntu Pro server.

To bootstrap a controller on LXD, we need to run:

.. code:: sh

   juju bootstrap localhost pro-demo-controller

This might take a while to complete. After it is done, we can use a
similar command to bootstrap a Juju controller on Microk8s:

.. code:: sh

   juju bootstrap microk8s livepatch-demo-controller

After the completion of the above commands, you can checkout the
available Juju controllers by running ``juju controllers`` which should
print out the list of controllers like this:

.. code:: sh

   $ juju controllers
   Controller                  Model      User   Access     Cloud/Region         Models  Nodes    HA  Version
   livepatch-demo-controller*  controller admin  superuser  microk8s/localhost        1      1     -  3.5.3  
   pro-demo-controller         controller admin  superuser  localhost/localhost       1      1  none  3.5.3  

Step 4: Deploy Livepatch on-prem
--------------------------------

First we need to create a Juju model to deploy Livepatch on-prem onto.
To do this we need to run:

.. code:: sh

   juju add-model livepatch

In order to deploy Livepatch on-prem, we can simply use the
``k8s/stable`` channel of the
`bundle <https://charmhub.io/canonical-livepatch-onprem?channel=k8s/stable>`__
charm. The bundle gives us all we need to deploy a working Livepatch
on-prem server.

.. code:: sh

   juju deploy canonical-livepatch-onprem --channel=k8s/stable --trust

Deploying the bundle takes a while to create the underlying
pods/containers and integrating them to each other. We can check out the
status of the model by running:

.. code:: sh

   juju status --watch 5s

Once the status of the ``livepatch`` application changes to *“patch-sync
token not set…”*, we are ready to continue.

``{note} :information_source: By default, the charm assumes an ordinary deployment of the Livepatch on-prem server (i.e., a non-air-gapped setup), and that is why it asks for a patch synchronisation token. Since this is an air-gapped deployment, you should ignore this message and proceed with integrating the charm with an air-gapped Ubuntu Pro server.``

Before continuing with the air-gapped Ubuntu Pro server, we need to make
sure the Livepatch on-prem server is accessible through a domain name.
Depending on IP addresses is not a reliable solution when referencing
applications deployed on Kubernetes from outside the cluster. The
standard practice is to use a Kubernetes ingress.

To create the ingress resource on our model and point it to the running
Livepatch server, we need to configure the ``nginx-ingress-integrator``
charm that is already deployed in our model under an application, named
``ingress``:

.. code:: sh

   juju config ingress service-hostname=livepatch.test.com

:literal:`{note} :information_source: Here, we used \`livepatch.test.com\` as the domain name, but this can be anything.`

After applying the command it takes a little time to create the
corresponding ``ingress`` resource on the MicroK8s cluster. As
mentioned, we can track the status of the Juju model by using
``juju status --watch 5s``.

Once the operation is finished, the ``ingress`` application status
message will show the IP address at which the ingress resource is
accessible with the ``livepatch.test.com`` domain name. Alternatively,
we can see the IP address of the ingress resource by running:

.. code:: sh

   microk8s kubectl get ingress -n livepatch

This will print out a single item like this:

::

   NAME                                    CLASS    HOSTS                ADDRESS     PORTS   AGE
   relation-6-livepatch-test-com-ingress   public   livepatch.test.com   127.0.0.1   80      4d3h

As you can see the IP address to access the ingress resource is
``127.0.0.1``. Note that depending on the network/MicroK8s
configuration, the IP can differ from the loopback interface address we
see in this case.

To finish this step, we need to add an entry to our VM’s ``/etc/hosts``
(mapping ``livepatch.test.com`` to ``127.0.0.1``) to make our Livepatch
on-prem server accessible to the air-gapped Ubuntu Pro server we are
going to deploy in the next step.

``{note} :information_source: Note that in a real-world scenario, the air-gapped Ubuntu Pro server might be deployed on another node/VM. So, the administrators might need to follow their procedures to enable communication between the deployments.``

You can use the command below to add the mentioned entry to the
``/etc/hosts`` file:

.. code:: sh

   echo "127.0.0.1 livepatch.test.com" | sudo tee -a /etc/hosts

Step 5: Deploy air-gapped Ubuntu Pro server
-------------------------------------------

To deploy the air-gapped Ubuntu Pro server, we are going to use the
```pro-airgapped-server`` <https://charmhub.io/pro-airgapped-server>`__
charm. Since this is a machine charm, we have to deploy it on a model on
LXD. The first step is to switch to our LXD controller and create a
model on that:

.. code:: sh

   juju switch pro-demo-controller
   juju add-model pro

After the model is created, we can deploy the ``pro-airgapped-server``
charm by running:

.. code:: sh

   juju deploy pro-air-gapped-server

You can watch the model status changes by running
``juju status --watch 5s``.

After the charm is deployed, it will be in a blocked state waiting for
an Ubuntu Pro token. You can find your Ubuntu Pro subscription token on
the Ubuntu Pro `dashboard <https://ubuntu.com/pro/dashboard>`__ page.
Copy your subscription token, replace the ``<TOKEN>`` placeholder in the
command below with your token, and run it:

.. code:: sh

   juju config pro-airgapped-server pro-tokens=<TOKEN>

After that, you need to provide the charm with your Livepatch on-prem
address. Assuming you are using the same ``livepatch.test.com`` domain,
you can run:

.. code:: sh

   juju config pro-airgapped-server entitlements-url-map='{"livepatch": {"remoteServer": "http://livepatch.test.com"},"livepatch-onprem": {"remoteServer": "http://livepatch.test.com"}}' 

Now, the ``pro-airgapped-server`` application status should be
``active``.

We should now create a Juju *application offer* to allow applications on
other Juju models/controllers (i.e., Livepatch on-prem server, in this
case) to integrate with the ``pro-airgapped-server`` application in the
current model. You can simply create an application offer by running:

.. code:: sh

   juju offer pro-airgapped-server:livepatch-server pro-offer

Before we finish this step, we need to take note of the IP address of
the ``pro-airgapped-server`` application. We will need it later when we
are going to set up Ubuntu Pro clients. To find the IP address, you can
just run ``juju status`` and copy the public IP address printed next to
the ``pro-airgapped-server/0`` unit.

Step 6: Enable air-gapped operation on Livepatch on-prem
--------------------------------------------------------

We should now switch back to the Juju model containing the Livepatch
on-prem and finish the integration with the ``pro-airgapped-server``
application. To switch to the corresponding model run:

.. code:: sh

   juju switch livepatch-demo-controller

To be able to consume the application offer we created in the previous
step, we need to call ``juju consume`` command:

.. code:: sh

   juju consume pro-demo-controller:pro.pro-offer

Now the application offer is ready to be integrated with:

.. code:: sh

   juju integrate livepatch pro-offer

When the integration is done, the status message on the ``livepatch``
application will change to *“url-template not set”*. This is about the
URL template that the Livepatch clients can use to download the patch
files.

To configure the URL template you can use the command below:

.. code:: sh

   juju config livepatch server.url-template="http://livepatch.test.com/v1/patches/{filename}"

:literal:`{note} :information_source: The \`{filename}\` placeholder should not be omitted or replaced.`

After some time, the Livepatch server should be up and running. You can
see this in the Juju model status as the ``livepatch`` application
status changes to ``active``. To test the running Livepatch on-prem
server we can use ``curl`` like this:

.. code:: sh

   $ curl http://livepatch.test.com
   Canonical Livepatch Health service, version v1.14.3

At this point, our Livepatch on-prem server is operating in air-gapped
mode and there is no communication with the upstream Livepatch server.
The next step is to set up Livepatch clients to speak with our on-prem
server.

Step 7: Set up Livepatch client
-------------------------------

In a real-world scenario, Livepatch clients run on different machines
than those serving the Livepatch on-prem server. Since network
configuration is out of the scope of this tutorial, we reuse the VM we
have used so far, to install and configure the Livepatch client.

Before proceeding with the Livepatch client, we should first instruct
the Ubuntu Pro client on the machine to communicate with the
``pro-airgapped-server`` we deployed on an LXD model. To do this replace
the ``<IP>`` placeholder in the command below with the IP of the
``pro-airgapped-server`` you copied in Step 5, and run the command:

.. code:: sh

   sudo sed -i -e 's|contract_url:.*|contract_url: http://<IP>:8484|g' /etc/ubuntu-advantage/uaclient.conf

You should also instruct the Ubuntu Pro client to refresh its internal
state:

.. code:: sh

   sudo pro refresh

With Ubuntu Pro client being configured, we are ready to install the
Livepatch client:

.. code:: sh

   sudo snap install canonical-livepatch

By default, the Livepatch client is configured to communicate with the
upstream Livepatch server. We need to change it so that the client
speaks to our Livepatch on-prem server:

.. code:: sh

   sudo canonical-livepatch config remote-server='http://livepatch.test.com'

Next, is to call ``pro attach`` and provide it with your Ubuntu Pro
subscription token. You have already used the same token when
configuring the ``pro-airgapped-server``. Replace the ``<TOKEN>``
placeholder below with the same token and run the command:

.. code:: sh

   sudo pro attach <TOKEN>

This might fail because we did not fully set up the
``pro-airgapped-server`` (e.g., apt repository mirrors). But for our
purposes, it is okay and we can continue with enabling Livepatch:

.. code:: sh

   sudo pro enable livepatch

This should finish successfully. We can now check the status of the
Livepatch client by running the following command:

.. code:: sh

   $ sudo canonical-livepatch status
   last check: 19 seconds ago
   kernel: 5.15.0-119.129-generic
   server check-in: succeeded

At this point, our Livepatch client is talking to our air-gapped
Livepatch on-prem server.

Cleaning up
===========

Since we used Multipass for this tutorial, we only need to delete the
created instance:

.. code:: sh

   multipass stop livepatch-deploy
   multipass delete --purge livepatch-deploy

Summary
=======

In this tutorial, we deployed an air-gapped Livepatch on-prem server,
alongside an Ubuntu Pro server enabling air-gapped operations. Then, we
configured the Ubuntu Pro client and Livepatch client to communicate
with our air-gapped servers.
