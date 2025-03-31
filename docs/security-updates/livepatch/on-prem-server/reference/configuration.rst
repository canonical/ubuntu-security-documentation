Configuration
#############

This document provides the configuration options for the Livepatch
server.

``{note} The configuration below applies to the Livepatch Server operator charms and Server snap.  For our reactive charm (or if your deployment config doesn't match the below), please see [here](/on-prem-server/reference/charm-migration).``

Setting config
--------------

Depending on your deployment you may be using Juju + charms or a
standalone Snap to deploy the Livepatch server. How you setup config
will differ slightly between the two.

Default and example values are available on the respective
`machine <https://charmhub.io/canonical-livepatch-server/configurations?channel=ops1.x/stable>`__
and
`K8s <https://charmhub.io/canonical-livepatch-server-k8s/configurations>`__
charm config pages.

Juju
~~~~

The config values in the table below map directly to the config options
exposed by the Livepatch charms (except where otherwise stated).

Assuming the Livepatch server has been deployed with the alias
``livepatch``, to change a config value run:

::

   juju config livepatch <key>=<value>
   # E.g. to enable basic auth
   juju config livepatch auth.basic.enabled=true

See the `Juju docs <https://juju.is/docs/juju/juju-config>`__ for all
the ways you can apply config.

Snap
~~~~

The config values in the table below map directly to the config values
accepted by the Livepatch server snap. An additional value must be added
to all commands as shown below.

To change a config value run:

::

   sudo snap set canonical-livepatch-server lp.<key>=<value>
   # E.g. to enable basic auth
   sudo snap set canonical-livepatch-server lp.auth.basic.enabled=true

Config
------

The following sections describes what configuration values are
available.

Server config
~~~~~~~~~~~~~

The following config values determine the server’s behavior around
concurrency limits, log level, etc.

+-----------------------+-----------------------+-----------------------+
| Name                  | Description           | Value(s)              |
+=======================+=======================+=======================+
| ``server.log-level``  | Log level for the     | ``debug,              |
|                       | server                |  info, warn, error, d |
|                       |                       | panic, panic, fatal`` |
+-----------------------+-----------------------+-----------------------+
| ``                    | The template URL to   | ``string``            |
| server.url-template`` | redirect clients for  |                       |
|                       | patch downloads. For  |                       |
|                       | example:              |                       |
|                       | ``https://my-file-ser |                       |
|                       | ver.com/{filename}``. |                       |
+-----------------------+-----------------------+-----------------------+
| ``se                  | Listen address for    | ``url``               |
| rver.server-address`` | the server            |                       |
+-----------------------+-----------------------+-----------------------+
| ``serve               | Maximum number of API | ``integer``           |
| r.concurrency-limit`` | requests to serve     |                       |
|                       | concurrently.         |                       |
+-----------------------+-----------------------+-----------------------+
| `                     | The queue limit,      | ``integer``           |
| `server.burst-limit`` | roughly equals        |                       |
|                       | ``conc                |                       |
|                       | urrency-burst-limit`` |                       |
+-----------------------+-----------------------+-----------------------+
| ``server.is-leader``  | In multi-server       | ``bool``              |
|                       | deployments,          |                       |
|                       | determine if this is  |                       |
|                       | a leader unit. Not    |                       |
|                       | available for charmed |                       |
|                       | deployments.          |                       |
+-----------------------+-----------------------+-----------------------+
| ``server.is-hosted``  | Enable configuration  | ``bool``              |
|                       | blocks specific to    |                       |
|                       | Canonical’s hosted    |                       |
|                       | configuration for     |                       |
|                       | livepatch             |                       |
+-----------------------+-----------------------+-----------------------+

Admin Authentication
~~~~~~~~~~~~~~~~~~~~

| The following values configure authentication to the server’s admin
  endpoints.
| Besides basic auth, only Ubuntu SSO auth is supported.

Some notes on this section: - SSO Teams represent Launchpad teams. -
Basic auth can be a comma separated list, see
`here <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/how-to/administration_tool#password-authentication>`__
for more info. - Basic auth passwords *must* be bcrypt hashed.

+-----------------------+-----------------------+-----------------------+
| Name                  | Description           | Value(s)              |
+=======================+=======================+=======================+
| `                     | Whether or not to     | ``bool``              |
| `auth.basic.enabled`` | enable basic auth.    |                       |
+-----------------------+-----------------------+-----------------------+
| ``auth.basic.users``  | A comma separated     | ``<user               |
|                       | list of user objects. | 1>:<bcrypt hashed pas |
|                       |                       | sword>, <user2>:<bcry |
|                       |                       | pt hashed password>`` |
+-----------------------+-----------------------+-----------------------+
| ``auth.sso.enabled``  | Whether or not to     | ``bool``              |
|                       | enable Ubuntu SSO     |                       |
|                       | auth.                 |                       |
+-----------------------+-----------------------+-----------------------+
| ``auth.sso.teams``    | SSO Auth              | ``https://launchpad.n |
|                       | configuration         | et/~team-1,https://la |
|                       |                       | unchpad.net/~team-2`` |
+-----------------------+-----------------------+-----------------------+
| ``auth.sso.url``      | URL to access for SSO | ``login.ubuntu.com``  |
|                       | auth.                 |                       |
+-----------------------+-----------------------+-----------------------+
| ``                    | Public key for the    | ``string``            |
| auth.sso.public-key`` | auth server. Can be a |                       |
|                       | file path or the key. |                       |
+-----------------------+-----------------------+-----------------------+

Ubuntu Pro
~~~~~~~~~~

The following values configure how the server interacts with the Ubuntu
Pro backend (also called the contracts server) for authenticating
clients. This is useful for Canonical’s hosted Livepatch server and
airgapped deployments.

+-----------------------+-----------------------+-----------------------+
| Name                  | Description           | Value(s)              |
+=======================+=======================+=======================+
| ``contracts.enabled`` | Whether to connect to | ``bool``              |
|                       | the contracts service |                       |
+-----------------------+-----------------------+-----------------------+
| ``contracts.url``     | URL of the contracts  | ``string``            |
|                       | server                |                       |
+-----------------------+-----------------------+-----------------------+
| ``contracts.user``    | Basic auth user       | ``string``            |
+-----------------------+-----------------------+-----------------------+
| `                     | Basic auth pass       | ``string``            |
| `contracts.password`` |                       |                       |
+-----------------------+-----------------------+-----------------------+

Database
~~~~~~~~

The following values configure how the server interacts with its
database.

+-----------------------+-----------------------+-----------------------+
| Name                  | Description           | Value(s)              |
+=======================+=======================+=======================+
| ``databas             | Postgres connection   | ``string``            |
| e.connection-string`` | string (unavailable   |                       |
|                       | for charmed           |                       |
|                       | deployments, handled  |                       |
|                       | with Juju relations)  |                       |
+-----------------------+-----------------------+-----------------------+
| ``database.           | Max pool for          | ``int``               |
| connection-pool-max`` | connections           |                       |
+-----------------------+-----------------------+-----------------------+
| ``database.conn       | Max lifetime of       | ``int``               |
| ection-lifetime-max`` | connections           |                       |
+-----------------------+-----------------------+-----------------------+

Influx
~~~~~~

The following values configure how the server interacts with InfluxDB,
used for sending aggregated KPIs.

+-----------------------+-----------------------+-----------------------+
| Name                  | Description           | Value(s)              |
+=======================+=======================+=======================+
| ``influx.enabled``    | Whether to enable     | ``bool``              |
|                       | influx KPI reporting  |                       |
|                       | (hosted)              |                       |
+-----------------------+-----------------------+-----------------------+
| ``influx.url``        | URL of the Influx     | ``string``            |
|                       | server                |                       |
+-----------------------+-----------------------+-----------------------+
| ``influx.token``      | Auth token            | ``string``            |
+-----------------------+-----------------------+-----------------------+
| ``influx.bucket``     | Bucket to use         | ``string``            |
+-----------------------+-----------------------+-----------------------+
| ``                    | Org where bucket      | ``string``            |
| influx.organization`` | resides               |                       |
+-----------------------+-----------------------+-----------------------+

Patch Storage
~~~~~~~~~~~~~

| The following values configure how the server interacts with its patch
  storage.
| See our
  `how-to <https://ubuntu.com/security/livepatch/docs/livepatch_on_prem/how-to/storage/configure>`__
  on patch storage.

+-----------------------+-----------------------+-----------------------+
| Name                  | Description           | Value(s)              |
+=======================+=======================+=======================+
| `                     | File storage type to  | ``oneof: filesyste    |
| `patch-storage.type`` | use for on-prem       | m,swift,postgres,s3`` |
|                       | deployment patch      |                       |
|                       | syncs                 |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-stor          | File path to          | ``string``            |
| age.filesystem-path`` | directory to use for  |                       |
|                       | storage               |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-sto           | User of account       | ``string``            |
| rage.swift-username`` |                       |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-st            | Auth API key          | ``string``            |
| orage.swift-api-key`` |                       |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-sto           | Auth Url              | ``string``            |
| rage.swift-auth-url`` |                       |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-s             | Swift domain to       | ``string``            |
| torage.swift-domain`` | connect to            |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-s             | Swift tenacy          | ``string``            |
| torage.swift-tenant`` |                       |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-stor          | Swift container       | ``string``            |
| age.swift-container`` | bucket                |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-s             | Swift region          | ``string``            |
| torage.swift-region`` |                       |                       |
+-----------------------+-----------------------+-----------------------+
| ``                    | Postgres connection   | ``string``            |
| patch-storage.postgre | string (can be left   |                       |
| s-connection-string`` | blank in charmed      |                       |
|                       | deployments to use    |                       |
|                       | Juju relations)       |                       |
+-----------------------+-----------------------+-----------------------+
| ``patc                | S3 Bucket to store    | ``string``            |
| h-storage.s3-bucket`` | patches               |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-              | S3 endpoint           | ``string``            |
| storage.s3-endpoint`` |                       |                       |
+-----------------------+-----------------------+-----------------------+
| ``patc                | AWS Region for S3     | ``string``            |
| h-storage.s3-region`` |                       |                       |
+-----------------------+-----------------------+-----------------------+
| ``patc                | Whether to perform    | ``bool``              |
| h-storage.s3-secure`` | secure transfers      |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-st            | AWS Access key        | ``string``            |
| orage.s3-access-key`` |                       |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-st            | AWS Secret key        | ``string``            |
| orage.s3-secret-key`` |                       |                       |
+-----------------------+-----------------------+-----------------------+

Patch Cache
~~~~~~~~~~~

The following values configure the server’s patch cache.

+-----------------------+-----------------------+-----------------------+
| Name                  | Description           | Value(s)              |
+=======================+=======================+=======================+
| ``                    | Whether or not to     | ``bool``              |
| patch-cache.enabled`` | cache patches for     |                       |
|                       | quicker delivery      |                       |
+-----------------------+-----------------------+-----------------------+
| ``pa                  | TTL of patches in     | ``string``            |
| tch-cache.cache-ttl`` | cache                 |                       |
+-----------------------+-----------------------+-----------------------+
| ``pat                 | Maximum size of       | ``int``               |
| ch-cache.cache-size`` | caching for patches.  |                       |
+-----------------------+-----------------------+-----------------------+

Patch Sync
~~~~~~~~~~

The following values configure how the server syncs patches from an
upstream server.

+-----------------------+-----------------------+-----------------------+
| Name                  | Description           | Value(s)              |
+=======================+=======================+=======================+
| ``patch-sync.id``     | ID of unit (not       | ``string``            |
|                       | available in charmed  |                       |
|                       | deploymets)           |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-sync.min      | A minimum kernel      | ``string``            |
| imum-kernel-version`` | version of format     |                       |
|                       | “0.0.0” denoting the  |                       |
|                       | lowest kernel version |                       |
|                       | to download patches   |                       |
|                       | for. For example,     |                       |
|                       | “5.4.0” will sync     |                       |
|                       | “5.4.0” and up.       |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch               | Comma-separated list  | ``string``            |
| -sync.architectures`` | of kernel             |                       |
|                       | architectures to      |                       |
|                       | download patches for. |                       |
+-----------------------+-----------------------+-----------------------+
| `                     | Comma-separated list  | ``string``            |
| `patch-sync.flavors`` | of kernel flavors to  |                       |
|                       | download patches for. |                       |
+-----------------------+-----------------------+-----------------------+
| ``                    | Automatic sync        | ``string``            |
| patch-sync.interval`` | interval e.g. 12h     |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-sync.mac      | Define the way sync   | `                     |
| hine-count-strategy`` | reports the machine   | `oneof: unit,bucket`` |
|                       | counts, either by     |                       |
|                       | units or by buckets.  |                       |
|                       | On on-prem instances  |                       |
|                       | the counts are        |                       |
|                       | bucketed and the      |                       |
|                       | value reported is     |                       |
|                       | given by lower bound  |                       |
|                       | of the following      |                       |
|                       | buckets: ``[1-49]``,  |                       |
|                       | ``[50-99]``,          |                       |
|                       | ``[100-499]``,        |                       |
|                       | ``[500-999]``,        |                       |
|                       | ``[1000-1999]``,      |                       |
|                       | ``[2000-4999]``,      |                       |
|                       | ``[5000-9999]``,      |                       |
|                       | ``[10000, ∞]``        |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-sync.s        | Whether or not to     | ``bool``              |
| end-machine-reports`` | send machine reports  |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-sync.token``  | Token used to         | ``string``            |
|                       | authorise with an     |                       |
|                       | upstream Livepatch    |                       |
|                       | server.               |                       |
+-----------------------+-----------------------+-----------------------+
| ``patc                | The upstream server   | ``string``            |
| h-sync.upstream-url`` | to pull patches from. |                       |
+-----------------------+-----------------------+-----------------------+
| ``pa                  | Enable syncing tiers  | ``bool``              |
| tch-sync.sync-tiers`` | from upstream server. |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch               | Enable use of a proxy | ``bool``              |
| -sync.proxy.enabled`` | when syncing patches. |                       |
+-----------------------+-----------------------+-----------------------+
| ``pa                  | HTTP Proxy.           | ``string``            |
| tch-sync.proxy.http`` |                       |                       |
+-----------------------+-----------------------+-----------------------+
| ``pat                 | HTTPS Proxy.          | ``string``            |
| ch-sync.proxy.https`` |                       |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-              | Comma separated list  | ``string``            |
| sync.proxy.no-proxy`` | of addresses that     |                       |
|                       | should not go through |                       |
|                       | the proxy.            |                       |
+-----------------------+-----------------------+-----------------------+

Blocklist Cache
~~~~~~~~~~~~~~~

The following values configure the server’s patch blocklist cache.

+-----------------------+-----------------------+-----------------------+
| Name                  | Description           | Value(s)              |
+=======================+=======================+=======================+
| ``patc                | Whether or not to     | ``bool``              |
| h-blocklist.enabled`` | enable the blocklist  |                       |
|                       | cache.                |                       |
+-----------------------+-----------------------+-----------------------+
| ``patch-blockli       | How often to refresh  | ``string``            |
| st.refresh-interval`` | the blocklist cache.  |                       |
+-----------------------+-----------------------+-----------------------+

KPI Reports
~~~~~~~~~~~

| The following values configure how the server sends KPI reports. This
  requires Influx to be setup.
| KPIs include aggregated information on client machines e.g. the client
  version, patch status, etc.

+-----------------------+-----------------------+-----------------------+
| Name                  | Description           | Value(s)              |
+=======================+=======================+=======================+
| ``                    | Whether or not to     | ``bool``              |
| kpi-reports.enabled`` | enable KPI reporting. |                       |
+-----------------------+-----------------------+-----------------------+
| ``k                   | How often to submit   | ``string``            |
| pi-reports.interval`` | reports.              |                       |
+-----------------------+-----------------------+-----------------------+

Machine reports
~~~~~~~~~~~~~~~

The following values configure the server’s behavior with machine
reports. Machine reports are stored in Postgres and store information
when client’s check-in.

.. raw:: html

   <!---
   The config values for `event-bus` are intended for Canonical internal use only.
   # I've left the event-bus config options commented out since they are not relevant to users.
   -->

+-----------------------+-----------------------+-----------------------+
| Name                  | Description           | Value(s)              |
+=======================+=======================+=======================+
| ``machine-repor       | Whether or not to     | ``bool``              |
| ts.database.enabled`` | enable machine        |                       |
|                       | reporting to          |                       |
|                       | postgres. Reports are |                       |
|                       | stored in the         |                       |
|                       | server’s postgres     |                       |
|                       | store.                |                       |
+-----------------------+-----------------------+-----------------------+
| `                     | Retention for the     | ``int``               |
| `machine-reports.data | given reports.        |                       |
| base.retention-days`` |                       |                       |
+-----------------------+-----------------------+-----------------------+
| ``ma                  | Row limit for each    | ``int``               |
| chine-reports.databas | cleanup operation.    |                       |
| e.cleanup-row-limit`` |                       |                       |
+-----------------------+-----------------------+-----------------------+
| ``m                   | How often to perform  | ``string``            |
| achine-reports.databa | cleanups.             |                       |
| se.cleanup-interval`` |                       |                       |
+-----------------------+-----------------------+-----------------------+

.. raw:: html

   <!--- #Event bus config options
   | `machine-reports.event-bus.enabled` | Whether or not to enable machine reporting to a Kafka server. | `bool` |
   | `machine-reports.event-bus.brokers` | The Kafka broker(s) domain. Comma separated list. | `string` |
   | `machine-reports.event-bus.client-cert` | Client cert to auth via mTLS. | `string` |
   | `machine-reports.event-bus.client-key` | Client private key to auth via mTLS. | `string` |
   | `machine-reports.event-bus.ca-cert` | The root or intermediate CA to perform verification. | `string` |
   | `machine-reports.event-bus.kafka-version` | Eventbus kafka version. | `string` |
   -->

Cloud delay
~~~~~~~~~~~

The following values configure the server’s behavior with cloud-delays.

+-----------------------+-----------------------+-----------------------+
| Name                  | Description           | Value(s)              |
+=======================+=======================+=======================+
| ``                    | Enable the server to  | ``bool``              |
| cloud-delay.enabled`` | delay the release of  |                       |
|                       | patches to clients    |                       |
|                       | based on their        |                       |
|                       | cloud/region/az       |                       |
+-----------------------+-----------------------+-----------------------+
| ``cloud-delay.        | Default delay hours   | ``int``               |
| default-delay-hours`` | for                   |                       |
|                       | clouds/regions/azs    |                       |
|                       | without predefined    |                       |
|                       | delay hours           |                       |
+-----------------------+-----------------------+-----------------------+
