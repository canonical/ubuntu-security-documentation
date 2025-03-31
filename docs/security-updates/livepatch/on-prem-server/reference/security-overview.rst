Security overview
#################

This document provides an overview of Livepatch security measures,
focusing on areas related to authentication, transmission, and
cryptographic technologies.

Authentication
==============

We have multiple means of authentication, please see the following for
further detail.

The general structure of this document is to first describe the
different authentication flows, followed by an analysis of the various
technologies. ## Admin APIs These APIs are to be consumed by an admin
user via the Livepatch Admin Tool.

``{note} :information_source: Find more info on how to setup the admin-tool [here](https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/how-to/administration_tool).``

The flow is to login via either `SSO <#sso>`__ or `Basic
Auth <#basic-auth>`__ to get a `macaroon <#macaroons>`__. Then, use the
macaroon to authenticate requests.

Client APIs
-----------

These APIs are to be consumed by a Livepatch Client. The Livepatch
client is enabled with a token, and depending on the type we have two
different flows.

*Auth Token*: This is an `UUID <#UUID>`__ used to authenticate and
register a machine. After successful registration a machine token is
issued, which is then used to authenticate following requests. This is
an old-style token that is no longer used for new clients. *Resource
Token*: This is a `macaroon <#macaroons>`__ that is verified against the
Ubuntu Pro backend to authenticate requests. This token is passed to the
Livepatch Client by the Ubuntu Pro client when enabling Pro.

Server APIs
-----------

These APIs are to be consumed by an another Livepatch Server.

*Sync-token*: It is an `UUID <#UUID>`__ generated from Admin APIs used
to authenticate Livepatch Server to Livepatch Server. It is stored in
Postgresql and the verification is done by comparison.

Technologies
------------

SSO
~~~

Single Sign On for Ubuntu.com users. You can find a in-depth explanation
`here <https://help.ubuntu.com/community/SSO>`__.

Basic Auth
~~~~~~~~~~

Basic Authentication is a simple method for HTTP authentication, relying
on a username and password. It uses Base64 encoding to transmit
credentials. The authentication process involves extracting credentials
from the HTTP Authorization header, decoding them, and comparing the
provided password against a stored hash. The following Go packages are
used for implementing Basic Authentication:

-  ``encoding/base64``
-  ``crypto/subtle``
-  ``golang.org/x/crypto/bcrypt``

Macaroons
~~~~~~~~~

Macaroons are a tool for decentralised authentication similar to JSON
Web Tokens and use a combination of HMAC for cryptographic signatures
and symmetric encryption to encode the scope (or caveats) of what a
macaroon is entitled to.

These operations are performed using ``HMAC-SHA256`` and
``XSalsa20-Poly1305``. The following Go packages are used by the
underlying `macaroon package <gopkg.in/macaroon.v2>`__ for these
operations: - ``crypto/hmac`` - ``crypto/sha256`` -
``golang.org/x/crypto/nacl/secretbox``

Additionally, the higher-level `Macaroon Bakery
package <https://github.com/go-macaroon-bakery/macaroon-bakery>`__ is
used to interface with macaroons and introduces public key cryptography
to perform similar operations as mentioned above. This allows services
to trust macaroons generated externally.

These operations are performed using ``Ed25519`` and
``XSalsa20-Poly1305``. The following Go packages are used by the
underlying macaroon bakery package for these operations:

-  ``golang.org/x/crypto/nacl/box``
-  ``golang.org/x/crypto/curve25519``

UUID
~~~~

UUIDv4 is a 128-bit identifier format that uses random number generation
to create unique IDs. It’s represented as 32 hexadecimal digits in a
8-4-4-4-12 pattern. The algorithm generates 16 random bytes, sets
specific bits to indicate version 4, and converts the result to hex.

The following Go packages are used: - ``github.com/google/uuid``

TLS Communication
=================

TLS encryption is optional between the different Livepatch Server
components.

========================================= ========
communications                            TLS
========================================= ========
livepatch-server <-> livepatch-client     optional
livepatch-server <-> livepatch-admin-tool optional
livepatch-server <-> upstream-server      optional
livepatch-server <-> SSO server           enforced
livepatch-server <-> ua-contracts server  enforced
livepatch-server <-> Postgresql           optional
livepatch-server <-> S3                   optional
livepatch-server <-> Swift                optional
livepatch-server <-> InfluxDB             disabled
========================================= ========

It is implemented using Go’s standard library (``crypto/tls`` and
``crypto/x509``). The minimum supported version is TLS v1.2.

Encryption at rest
==================

Both Postgres `K8s Charm <https://charmhub.io/postgresql-k8s>`__ and
`Machine Charm <https://charmhub.io/postgresql>`__ do not support
encryption at rest.

Machine Reports
===============

When we send machine reports (you can find more information
`here <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/how-to/capture_machine_reports>`__)
we hash the machine-id with HMAC hashing algorithm.

The following Go packages are commonly used for implementing Basic
Authentication: - ``crypto/hmac``
