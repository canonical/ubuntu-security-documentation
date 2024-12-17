Setup administration tool
#########################

To perform operations such as promoting patches to tiers and issuing
tokens for machines to attach to the livepatch server, an administration
tool is provided as a snap:

::

   $ sudo snap install canonical-livepatch-server-admin

For ease of use, it’s recommended to alias the admin command:

::

   $ sudo snap alias canonical-livepatch-server-admin.livepatch-admin livepatch-admin

Authentication
==============

There are two ways for the livepatch administration tool to authenticate
with the livepatch server:

-  Ubuntu SSO
-  Username/password

Password authentication
-----------------------

To configure password authentication, username/password hash pairs will
need to be generated using the ``htpasswd`` tool available in the
``apache2-utils`` package.

\`\`\ ``{note} The``\ apache2-utils\` package can be installed by using
the following commands:

::

   $ sudo apt-get update
   $ sudo apt-get install apache2-utils

::


   This will generate a username/password hash pair:

$ htpasswd -bnBC 10
username:$2y$10$74ZpDgHaxnUQo.AJZk1cMuSRfef5oK5xq5o/GLbUH/Bbw6W2bmctm

::

   Multiple such pairs can be provided as a comma-separated list:

$ juju config livepatch auth_basic_users=“:<password1,:”

::

   When logging in with the client, the username and password will need to be provided:

$ export LIVEPATCH_URL={haproxy URL or unit IP}

$ livepatch-admin login –auth :

::


   ## Ubuntu SSO authentication

   Ubuntu SSO authentication utilizes membership in public launchpad groups to gate access. The launchpad groups that will have administrator privileges are specified using charmed operator configuration:

$ juju config livepatch auth_lp_teams=‘https://launchpad.net/~’

::

   Multiple teams can be specified as a comma-separated list.

   When logging in, user interaction will be necessary:

$ export LIVEPATCH_URL={haproxy URL}

$ livepatch-admin login

To login please visit http://127.0.0.1:44035 \``\`
