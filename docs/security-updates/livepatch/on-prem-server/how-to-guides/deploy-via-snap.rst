Deploy via snap
###############

Canonical Livepatch Server enables the delivery of Livepatch’s to
Livepatch clients, allowing reboots of critical infrastructure to be
scheduled at a convenient time.

In this tutorial we will setup the Livepatch Server snap.

   Please note, the server snap is not designed for high-availability
   setups!

**Requirements** At minimum, the server requires a PostgreSQL (*At least
version 12*) instance to persist data. For the sake of simplicity, we
will use docker to illustrate this server setup. However, feel free to
use an existing instance if you have one available to you!

   **Note**: For a production environment take a look at this
   `tutorial <https://ubuntu.com/server/docs/databases-postgresql>`__ to
   install Postgres with persistent storage.

Run the following to start a PostgreSQL instance in Docker:

::

    docker run \
    --name postgresql \
    -e POSTGRES_USER=livepatch \
    -e POSTGRES_PASSWORD=testing \
    -p 5432:5432 \
    -d postgres:12.11

**Installing the snap** To install the server snap, simply run:

::

    sudo snap install canonical-livepatch-server

**Migrating the database** Within the snap is an internal tool used to
migrate a PostgreSQL database with the Livepatch Server schema, to
migrate your database run:

::

    canonical-livepatch-server.schema-tool \
    postgresql://livepatch:testing@localhost:5432/livepatch

**Pointing Livepatch at your database** All of the configuration for the
Livepatch Server snap is handled within the snap daemon, to update
Livepatch to target the DSN of your PostgreSQL instance, run:

::

    sudo snap \
    set canonical-livepatch-server \
    lp.database.connection-string=postgresql://livepatch:testing@localhost:5432/livepatch

**Validate the server is available** To check the server is running
successfully, you may run the following:

::

    sudo snap logs \
    canonical-livepatch-server.livepatch -n 100

If you’re a customer of Ubuntu Pro and have access to Livepatch
on-premise, you can enable on-premise within the snap the same as you
would for the charm.

**Obtain a Ubuntu Pro token** Given you are a customer of Ubuntu Pro,
you will have Livepatch On-Premise available to you.

You can obtain your token from: https://ubuntu.com/pro/dashboard

**Updating Livepatch to use your Ubuntu Pro token** As previously
stated, we can update the servers configuration through the snap daemon,
so let’s update the server to use this token and enable Livepatch
On-Premise:

::

    sudo snap set canonical-livepatch-server token=<Ubuntu Pro token>

**Managing the server** To manage Livepatch, we have an administrator
tool, also available as a snap. Install the administrator tool from:

::

    sudo snap install canonical-livepatch-server-admin

The administrator tool needs to know where your Livepatch server is
hosted, in an all-in-one setup within a single machine, this is simply
``http://localhost:8080``. Export an environment variable like so:

::

    export LIVEPATCH_URL=http://localhost:8080

Next, for the administrator tool to be able to login to the server, we
will require some form of basic authentication, also set in the snap
daemon. For the purpose of this tutorial, we have provided you one with
the username as ``admin`` and password as ``admin123``:

   Please note, special characters are escaped using single quotes and
   the password must be 'bcrypt' hashed

::

    sudo snap set canonical-livepatch-server \
       lp.auth.basic.users='admin:$2y$10$c25NVkdeIMqWdbgR4883YuE/s2CT1mCmGPm5Ma1XbUqGqM26ClTGe'

If you would like to generate your own password and hash, you can do so as 
follows:

::

    $ sudo apt-get -y install whois
    $ mkpasswd -m bcrypt admin123

You can also combine this into a single command that prompts for the password. 
Note that this uses double-quotes and not single quotes. 

   $ sudo snap set canonical-livepatch-server lp.auth.basic.users="admin:$(mkpasswd -m bcrypt)"

Or you can pass the password in, if you want to use this non-interactively:

   $ sudo snap set canonical-livepatch-server lp.auth.basic.users="admin:$(mkpasswd -m bcrypt admin123)"


Next, we need to manually enable basic authentication:

::

    sudo snap set canonical-livepatch-server lp.auth.basic.enabled=true

Finally, we can login with the administrator tool like so presuming you
have used the example user and password:

::

    canonical-livepatch-server-admin.livepatch-admin login -a admin:admin123

**Sychronising with hosted Livepatch** Now you have a running, fully
configured On-Premise Livepatch server, we can synchronise patches from
hosted Livepatch into your server. Run the following within your
administrator tool:

::

    canonical-livepatch-server-admin.livepatch-admin sync trigger 

To set the server to automatically sync patches from Canonical’s servers
every 12 hours, you can run the following commands,

::

    sudo snap set canonical-livepatch-server lp.patch-sync.enabled=true
    sudo snap set canonical-livepatch-server lp.patch-sync.interval=12h

The default configuration is set to store the patches on the local
filesystem of the server, you can also view the patches on the
filesystem here:

::

    ls /var/snap/canonical-livepatch-server/common/patches/

**Exposing the server** By default the Snap listens on localhost:8080
and so is not accessible to requests from external networks. To see
this, run the following command:

::

   $ sudo snap get canonical-livepatch-server lp.server.server-address
   localhost:8080

This can be changed to listen for all incoming connections on any port:

::

   sudo snap set canonical-livepatch-server lp.server.server-address=0.0.0.0:<port>

Follow this up with the following change to ensure your admin tool can
still access the server. If you would like to access the server from a
remote machine, change ``localhost`` to the IP address of the machine
running Livepatch-server On-prem:

::

   export LIVEPATCH_URL=http://localhost:<port>

**Final words** And now you have an On-Premise Livepatch server
configured to synchronise with hosted Livepatch!

For further reading please consult the *how-to* guides!
