Network security
################

Network security for the on-premises Livepatch server encompasses
various topics.

Connection between the on-prem server and the hosted server
-----------------------------------------------------------

The connection between the on-prem server and the hosted server allows
TLS to ensure that communication is secure and the host is, in fact,
Canonical’s server.

Method of patch download when a sync is triggered.
--------------------------------------------------

Patches are downloaded with TLS encryption. When a sync is triggered,
the on-premises server makes a request to the hosted server (over TLS)
for any new patches, receiving patch locations and checksums for each
patch.

The on-premise server proceeds to download all new patches (from a
separate fileserver again with TLS) and verifies their contents using
the aforementioned checksum, before inserting the patch into the patch
store. This process is similar to how clients download patches.

Connection between clients and the on-prem server.
--------------------------------------------------

Connections between clients and the on-prem server can be secured with
TLS, but this is up to the administrator managing the deployment and the
network requirements. A how-to on this topic is
`available <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/how-to/tls>`__.

.. raw:: html

   <!--- uncomment when we have a security hardening doc
   ## Connection between the on-prem server and the database
   The connection between the server and database should be setup with TLS in a production environment. For more information on how to achieve this using the various deployment mechanisms, visit our security hardening doc.
   -->
