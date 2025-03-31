Air gapped livepatch and snap
#############################

Introduction
============

Livepatch on-prem is a self-hosted version of the Livepatch server,
enabling the delivery of patches to machines within network restricted
environments. For security reasons, administrators may prefer to deploy
Livepatch on-prem server in an air-gapped environment with restricted
Internet access.

This tutorial will deploy the Livepatch on-prem server as a Snap package
in an air-gapped environment.

How does Livepatch on-prem work in an air-gapped environment?
-------------------------------------------------------------

Generally, in order to perform authentication/authorisation of machines
and to fetch patches, the Livepatch on-prem server needs to communicate
with the main Livepatch server hosted by Canonical. In an air-gapped
environment, where such communication is not available, these functions
are handled using the following tools:

-  `Air-gapped Ubuntu Pro
   Server <https://discourse.charmhub.io/t/15278>`__ provides services
   related to Ubuntu Pro subscriptions in air-gapped environments.
   Livepatch on-prem can be integrated with this service to perform
   authentication/authorisation of machines and handle
   subscription-related functionality.
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

``{note} :information_source: When deploying air-gapped Livepatch on-prem using Snap, it is best to configure the patch storage to something independently accessible within your infrastructure, like the filesystem or an S3/Swift bucket, instead of PostgreSQL. This way, Livepatch administrators can independently download the latest patches via the Patch Downloader CLI tool and transfer them to the patch storage.``

Deployment steps
================

In this tutorial, we use `Multipass <https://multipass.run>`__ to create
Ubuntu virtual machines (VM) to deploy Livepatch and its dependencies on
it.

If not already installed, we can use the command below to install
Multipass:

.. code:: sh

   sudo snap install multipass

Also, we will need two Multipass virtual machines; one as the air-gapped
environment where the Livepatch on-prem server is going to be deployed,
and the other to simulate a normal environment (i.e., with access to the
Internet) to finalize the configurations for the air-gapped Ubuntu Pro
server.

Step 1: Create Multipass instances
----------------------------------

You can create the Multipass instances needed in this tutorial by
running the command below. This will create two instances, named
``pro-configuration`` and ``livepatch-deploy``.

.. code:: sh

   multipass launch jammy --name pro-configuration
   multipass launch jammy --name livepatch-deploy -d 10G

Step 2: Create configurations for the air-gapped Ubuntu Pro server
------------------------------------------------------------------

We first need an interactive shell in the ``pro-configuration``
instance:

.. code:: sh

   multipass shell pro-configuration

Once getting into the instance, we need to install the ``pro-airgapped``
configuration tool:

.. code:: sh

   sudo add-apt-repository ppa:yellow/ua-airgapped
   sudo apt update
   sudo apt install pro-airgapped

To create the configuration file, you will need your Ubuntu Pro
subscription token. You should copy your token from the Ubuntu Pro
`dashboard <https://ubuntu.com/pro/dashboard>`__, replace the
``<TOKEN>`` placeholder in the following command, and then run the
command:

.. code:: sh

   cat <<EOF > override.yml
   <TOKEN>:
     livepatch:
       directives:
         remoteServer: http://livepatch.test.com:8080
     livepatch-onprem:
       directives:
         remoteServer: http://livepatch.test.com:8080
   EOF

:literal:`{note} :information_source: Here we have set the Livepatch on-prem server hostname to \`livepatch.test.com\`. You can set it to any other value, but remember to replace it in the next steps.`

This will create a file named ``override.yml``. Now, we should use the
``pro-airgapped`` tool to make the final configuration file, which we
will use to set up the air-gapped environment. Note that the
``pro-airgapped`` tool needs Internet access to communicate with
upstream Canonical services to fetch your subscription details. By
running the following command the final configuration file will be
created as ``server-ready.yml``:

.. code:: sh

   cat override.yml | pro-airgapped > server-ready.yml

Now, we are done with this Multipass instance, and we should exit the
interactive shell:

.. code:: sh

   exit

Step 3: Transfer configuration to air-gapped environment
--------------------------------------------------------

Now, we need to transfer the air-gapped Ubuntu Pro configuration file,
``server-ready.yml``, to the isolated Multipass instance. To do this, we
have to transfer the file to the host machine and then to the isolated
instance.

.. code:: sh

   mulitpass transfer pro-configuration:server-ready.yml /tmp/server-ready.yml
   multipass transfer /tmp/server-ready.yml livepatch-deploy:server-ready.yml
   rm /tmp/server-ready.yml

Step 4: Deploy air-gapped Ubuntu Pro server
-------------------------------------------

Now it is time to deploy the air-gapped Ubuntu Pro server in the
air-gapped environment. To begin, we need an interactive shell in the
isolated Multipass instance:

.. code:: sh

   multipass shell livepatch-deploy

Next step is installing ``contracts-airgapped`` tool.

.. code:: sh

   sudo add-apt-repository ppa:yellow/ua-airgapped
   sudo apt update
   sudo apt install contracts-airgapped

:literal:`{note} :information_source: In a real air-gapped environment there will be no Internet access. So, one should use other methods, like local mirrors/packages, to install the dependencies via \`apt\` or \`snap\`. Setting up a fully isolated air-gapped environment is out of the scope of this tutorial. So, we simply install dependencies from the Internet.`

Once the installation is done, we need to run the air-gapped Ubuntu Pro
server with the configuration file we transferred to the instance in the
previous step:

.. code:: sh

   contracts-airgapped --input=./server-ready.yml

The air-gapped Ubuntu Pro server is now listening on TCP port ``8484``.

:literal:`{note} :information_source: This command runs the air-gapped Ubuntu Pro server in the foreground. We still need to work on this Multipass instance. So, you can either open a new shell to the instance or run it in the background by appending a \`&\` to the command.`

Step 5: Deploy Livepatch on-prem server
---------------------------------------

We should now deploy Livepatch on-prem server in the air-gapped
environment. For simplicity, we will reuse the same Multipass instance
we used for running the air-gapped Ubuntu Pro server.

Livepatch on-prem requires a PostgreSQL database to work. Here, we use
Docker Engine to spin up a PostgreSQL instance. Since the Multipass
instance we are in does not have Docker, you need to install it by
following the official
`instructions <https://docs.docker.com/engine/install/ubuntu/>`__. Once
Docker Engine is installed, you can create a PostgreSQL container by
using this command:

.. code:: sh

   docker run \
     --name postgresql \
     -e POSTGRES_USER=livepatch \
     -e POSTGRES_PASSWORD=testing \
     -p 5432:5432 \
     -d postgres:12.11

``{note} :information_source: Livepatch on-prem server requires PostgreSQL 12 or above.``

Now, we are ready to install Livepatch on-prem server:

.. code:: sh

   sudo snap install canonical-livepatch-server

Before configuring Livepatch on-prem to communicate with our PostgreSQL
database, we need to prepare the database:

.. code:: sh

   canonical-livepatch-server.schema-tool postgresql://livepatch:testing@localhost:5432/livepatch

Once the database preparation is done, we can configure Livepatch
on-prem database connection by the following command:

.. code:: sh

   sudo snap set canonical-livepatch-server lp.database.connection-string=postgresql://livepatch:testing@localhost:5432/livepatch

Next, the Livepatch on-prem server should be configured to communicate
with the air-gapped Ubuntu Pro server:

.. code:: sh

   sudo snap set canonical-livepatch-server \
     lp.contracts.enabled=true \
     lp.contracts.url=http://127.0.0.1:8484

Now, the Livepatch on-prem server is running and listening on TCP port
``8080``. To test it, you can use ``curl`` like this:

.. code:: sh

   curl http://localhost:8080
   # Canonical Livepatch Health service, version v1.14.3

:literal:`{note} :information_source: By default, Livepatch on-prem server uses filesystem to stores the patches. The directory is located at \`/var/snap/canonical-livepatch-server/common/patches\`. So, in a real-world setup, you can download the latest patches by using the Patch Downloader tool, transfer them to the mentioned path, and use the Admin tool to refresh patch information. Check out [this](/on-prem-server/how-to-guides/use-the-patch-downloader-tool) topic on how to use the Patch Downloader tool.`

Step 7: Set up Livepatch client
-------------------------------

In a real-world scenario, Livepatch clients run on different machines
than those serving the Livepatch on-prem server. Since network
configuration is out of the scope of this tutorial, we reuse the VM we
have used so far, to install and configure the Livepatch client.

Before proceeding with the Livepatch client, we should first instruct
the Ubuntu Pro client on the machine to communicate with the air-gapped
Ubuntu Pro server:

.. code:: sh

   sudo sed -i -e 's|contract_url:.*|contract_url: http://127.0.0.1:8484|g' /etc/ubuntu-advantage/uaclient.conf

You should also instruct the Ubuntu Pro client to refresh its internal
state for changes to take effect:

.. code:: sh

   sudo pro refresh

More than that, we still need to map ``livepatch.test.com`` to the
loopback interface IP address (i.e., ``127.0.0.1``):

.. code:: sh

   echo "127.0.0.1 livepatch.test.com" | sudo tee -a /etc/hosts

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
subscription token. You have already used the same token in an earlier
step. Replace the ``<TOKEN>`` placeholder below with the same token and
run the command:

.. code:: sh

   sudo pro attach <TOKEN>

This might fail because we did not fully set up the air-gapped Ubuntu
Pro server (e.g., apt repository mirrors). But for our purposes, it is
okay and we can continue with enabling Livepatch:

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

Since we used Multipass for this tutorial, we just need to delete the
created instances:

.. code:: sh

   multipass stop pro-configuration
   multipass delete --purge pro-configuration
   multipass stop livepatch-deploy
   multipass delete --purge livepatch-deploy

Summary
=======

In this tutorial, we deployed an air-gapped Livepatch on-prem server,
alongside an Ubuntu Pro server enabling air-gapped operations. Then, we
configured the Ubuntu Pro client and Livepatch client to communicate
with our air-gapped servers.
