Security hardening
###################

This page provides recommendations on how to setup Livepatch Server’s
deployment to improve security.

Infrastructure Setup
--------------------

Independently from the method you have chosen to deploy Livepatch Server
you should have:

+----------------------+---------------+-------------------------------+
| Component            | Exposure      | Notes                         |
+======================+===============+===============================+
| livepatch client API | livepatch     | Endpoints potentially exposed |
|                      | clients       | to internet.                  |
+----------------------+---------------+-------------------------------+
| livepatch server API | livepatch     | Endpoints potentially exposed |
|                      | clients       | to internet.                  |
+----------------------+---------------+-------------------------------+
| livepatch server     | livepatch     | Endpoints exposed to few      |
| Admin API            | admins        | authorized users.             |
+----------------------+---------------+-------------------------------+
| postgresql           | livepatch     | Service exposed to a          |
|                      | server        | segregated internal network.  |
+----------------------+---------------+-------------------------------+
| patch storage        | livepatch     | Service exposed to a          |
|                      | server        | segregated internal network.  |
+----------------------+---------------+-------------------------------+
| patch server         | livepatch     | Endpoints potentially exposed |
|                      | clients       | to internet.                  |
+----------------------+---------------+-------------------------------+

..

   You can follow this
   `guide <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/tutorial/Getting%20started%20with%20Livepatch%20and%20MicroK8s>`__
   on how to setup your infrastracture using Juju.

Authentication
--------------

   We discuss authentication in detail on this
   `page <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/reference/security>`__.
   In summary, admins use basic auth (username and password) to
   authenticate, while Livepatch client use on of the token-based
   mechanisms.

*Admin authentication*: when you `setup Livepatch Admin
Tool <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/how-to/administration_tool>`__
be sure to use a `strong
password <https://en.wikipedia.org/wiki/Password_strength>`__ and you
should protect hosts where the Livepatch Admin Tool is used.

*Client authentication*: when you register a client, a token is stored
on the machine running the client. Ensure only authorized users have
``sudo`` access to the host.

Communication
-------------

TLS is a key factor, especially for those components exposed to the
internet. Below we explain how to enable TLS for each component of
Livepatch.

Livepatch Server
~~~~~~~~~~~~~~~~

Livepatch server is the core component serving APIs. You should enable
TLS for the Livepatch Server to ensure integrity and confidentiality of
communication with Livepatch clients and the Livepatch Admin Tool.

To enable TLS for the charmed Livepatch Server, you can follow this
`guide <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/how-to/tls>`__.

Additionally, you should put in place networking rules to only allow
admin API access from specific IP addresses (ex. company internal
network).

PostgreSQL
~~~~~~~~~~

PostgreSQL is where state to operate Livepatch Server is stored. It
should be in a segregated network to prevent external access but TLS can
be enabled to ensure confidentiality and integrity.

To enable TLS for charmed Postgresql you can follow this
`guide <https://charmhub.io/postgresql-k8s/docs/t-enable-tls>`__.

   As of October 2024, you need to manually restart the Livepatch Server
   if you enable TLS on Postgres after having related Livepatch and
   Postgres charms.

Patch Storage
~~~~~~~~~~~~~

Patch storage is the place where the Livepatch Server stores the actual
patch files and it should be in a segregated network to prevent external
access. Still, TLS can be enabled to ensure confidentiality and
integrity. You can choose between multiple
`solutions <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/how-to/storage/configure>`__.

Patch Server
~~~~~~~~~~~~

Patch Server is the component in charge of serving the actual patch
files. It can be the Livepatch server itself, or an external service.
TLS is recommended to ensure confidentiality and integrity.

Another Livepatch Server
~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to chain multiple Livepatch Servers, as described in this
`guide <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/how-to/chain-servers>`__.
They exchange tiers and patch information, and TLS can be enabled to
ensure confidentiality and integrity.

To enable TLS for the charmed Livepatch Server, you can follow this
`guide <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/how-to/tls>`__.
