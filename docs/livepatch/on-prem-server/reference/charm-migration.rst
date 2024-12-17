Charm migration
###############

The Juju framework offered a, now deprecated, way to write charms called
`reactive
charms <https://juju.is/docs/sdk/charm-taxonomy#heading--reactive>`__.
The modern framework is known as the `operator
framework <https://juju.is/docs/sdk/charm-taxonomy#heading--ops>`__.
Below we explain how to identify which type of charm you are running.

Run ``juju status`` and observe the charm name and channel. The output
will resemble the following. |livepatch-status|800x31|

**Machine Charm:** - Charm name =
`canonical-livepatch-server <https://charmhub.io/canonical-livepatch-server>`__
- Channel = ``latest/*`` - Reactive charm (deprecated) - Channel =
``ops1.x/*`` - Operator charm (recommended for new deployments)

**Kubernetes Charm:** - Charm name =
`canonical-livepatch-server-k8s <https://charmhub.io/canonical-livepatch-server-k8s>`__
- Channel = ``latest/*`` - Operator charm (recommended for new
deployments) - Only an operator charm is available for Livepatch on K8s.

Migrate deployment
------------------

Currently there is no way to migrate existing data to a new deployment.
Existing deployments will continue to function but will no longer
receive new features. It is recommended that new deployments use the
operator charms.

To migrate an existing reactive charm deployment, it is suggested that
you setup a new deployment and follow the steps below to migrate your
configuration.

Migrate Configuration
---------------------

The new Livepatch charms have different configuration keys.
Additionally, some options were removed in favour of a simpler
structure. To migrate your old config to the new one, you can use this
`script <https://github.com/canonical/livepatch-machine-charm/blob/main/scripts/migrate_config.py>`__.

To run the script:

::

   $ python3 ./converter.py -i input.yaml -o converted.yaml

Where the ``input.yaml`` is the old configuration that you want to
convert. To extract it from your deployment, you can use this command:

::

   $ juju config livepatch-server > input.yaml

The script would create/overwrite the output file specified by the
``-o`` parameter.

+------------+---------------+-----------------------------------------+
| **Old      | **New         | **Notes**                               |
| config**   | config**      |                                         |
+------------+---------------+-----------------------------------------+
| log_level  | ser           | Possible values:‘debug’, ‘info’,        |
|            | ver.log-level | ‘warn’, ‘error’.Default is ‘info’       |
+------------+---------------+-----------------------------------------+
| ur         | server        | Must be in the                          |
| l_template | .url-template | form:“http(s)://<                       |
|            |               | hostname>:<port>/v1/patches/{filename}” |
+------------+---------------+-----------------------------------------+
| p          | **NA**        |                                         |
| sql_dbname |               |                                         |
+------------+---------------+-----------------------------------------+
| psql_roles | **NA**        |                                         |
+------------+---------------+-----------------------------------------+
| blo        | patch-        | Make sure that patch-blocklist.enabled  |
| cklist_cac | blocklist.ref | is set to true                          |
| he_refresh | resh-interval |                                         |
+------------+---------------+-----------------------------------------+
| contract_  | contracts.url |                                         |
| server_url |               |                                         |
+------------+---------------+-----------------------------------------+
| contract_s | c             |                                         |
| erver_user | ontracts.user |                                         |
+------------+---------------+-----------------------------------------+
| cont       | contr         |                                         |
| ract_serve | acts.password |                                         |
| r_password |               |                                         |
+------------+---------------+-----------------------------------------+
| concurr    | server.conc   |                                         |
| ency_limit | urrency-limit |                                         |
+------------+---------------+-----------------------------------------+
| b          | serve         |                                         |
| urst_limit | r.burst-limit |                                         |
+------------+---------------+-----------------------------------------+
| is         | cloud-        |                                         |
| _cloud_del | delay.enabled |                                         |
| ay_enabled |               |                                         |
+------------+---------------+-----------------------------------------+
| c          | cloud         |                                         |
| loud_delay | -delay.defaul |                                         |
| _default_d | t-delay-hours |                                         |
| elay_hours |               |                                         |
+------------+---------------+-----------------------------------------+
| dbconn_max | da            |                                         |
|            | tabase.connec |                                         |
|            | tion-pool-max |                                         |
+------------+---------------+-----------------------------------------+
| dbconn_ma  | databa        |                                         |
| x_lifetime | se.connection |                                         |
|            | -lifetime-max |                                         |
+------------+---------------+-----------------------------------------+
| patch_sy   | patch         |                                         |
| nc_enabled | -sync.enabled |                                         |
+------------+---------------+-----------------------------------------+
| patch      | patch-ca      |                                         |
| _cache_ttl | che.cache-ttl |                                         |
+------------+---------------+-----------------------------------------+
| patch_     | patch-cac     |                                         |
| cache_size | he.cache-size |                                         |
+------------+---------------+-----------------------------------------+
| patc       | patch-        |                                         |
| h_cache_on | cache.enabled |                                         |
+------------+---------------+-----------------------------------------+
| http_proxy | patch-sy      | Make sure that                          |
|            | nc.proxy.http | **patch-sync.proxy.enabled** is set to  |
|            |               | true.                                   |
+------------+---------------+-----------------------------------------+
| h          | patch-syn     |                                         |
| ttps_proxy | c.proxy.https |                                         |
+------------+---------------+-----------------------------------------+
| no_proxy   | patch-sync.p  |                                         |
|            | roxy.no-proxy |                                         |
+------------+---------------+-----------------------------------------+
|            |               |                                         |
+------------+---------------+-----------------------------------------+
| e          | machine-rep   | Make sure:                              |
| vent_bus_c | orts.event-bu | machine-reports.event-bus.enabled is    |
| lient_cert | s.client-cert | set to true                             |
+------------+---------------+-----------------------------------------+
| event_bus_ | machine-re    |                                         |
| client_key | ports.event-b |                                         |
|            | us.client-key |                                         |
+------------+---------------+-----------------------------------------+
| event_b    | machine       |                                         |
| us_ca_cert | -reports.even |                                         |
|            | t-bus.ca-cert |                                         |
+------------+---------------+-----------------------------------------+
| event_b    | machine       |                                         |
| us_brokers | -reports.even |                                         |
|            | t-bus.brokers |                                         |
+------------+---------------+-----------------------------------------+
| aut        | a             | Make sure this is set to true:          |
| h_lp_teams | uth.sso.teams | auth.sso.enabled                        |
+------------+---------------+-----------------------------------------+
| auth_sso_  | auth.s        |                                         |
| public_key | so.public-key |                                         |
+------------+---------------+-----------------------------------------+
| auth_ss    | auth.sso.url  |                                         |
| o_location |               |                                         |
+------------+---------------+-----------------------------------------+
| auth_b     | aut           | Make sure that auth.basic.enable is set |
| asic_users | h.basic.users | to true                                 |
+------------+---------------+-----------------------------------------+
|            |               |                                         |
+------------+---------------+-----------------------------------------+
| swift_cont | pat           |                                         |
| ainer_name | ch-storage.sw |                                         |
|            | ift-container |                                         |
+------------+---------------+-----------------------------------------+
| swif       | pa            |                                         |
| t_auth_url | tch-storage.s |                                         |
|            | wift-auth-url |                                         |
+------------+---------------+-----------------------------------------+
| swif       | pa            |                                         |
| t_username | tch-storage.s |                                         |
|            | wift-username |                                         |
+------------+---------------+-----------------------------------------+
| sw         | p             |                                         |
| ift_apikey | atch-storage. |                                         |
|            | swift-api-key |                                         |
+------------+---------------+-----------------------------------------+
| swift_t    | patch-storage |                                         |
| enant_name | .swift-tenant |                                         |
+------------+---------------+-----------------------------------------+
| swift_r    | patch-storage |                                         |
| egion_name | .swift-region |                                         |
+------------+---------------+-----------------------------------------+
| swift_d    | patch-storage |                                         |
| omain_name | .swift-domain |                                         |
+------------+---------------+-----------------------------------------+
| patchstore | patch         | default: filesystem The available       |
|            | -storage.type | options are: - filesystem - swift -     |
|            |               | postgres - s3                           |
+------------+---------------+-----------------------------------------+
| st         | pat           | Path defaults to                        |
| orage_path | ch-storage.fi | /var/snap/ca                            |
|            | lesystem-path | nonical-livepatch-server/common/patches |
+------------+---------------+-----------------------------------------+
| sync_token | pat           |                                         |
|            | ch-sync.token |                                         |
+------------+---------------+-----------------------------------------+
| syn        | patch-sync    |                                         |
| c_upstream | .upstream-url |                                         |
+------------+---------------+-----------------------------------------+
| syn        | **NA**        |                                         |
| c_identity |               |                                         |
+------------+---------------+-----------------------------------------+
| sync_ups   | **NA**        | Upstream tier to download patch         |
| tream_tier |               | snapshots from. Default value is        |
|            |               | “updates”.                              |
+------------+---------------+-----------------------------------------+
| syn        | patch-        |                                         |
| c_interval | sync.interval |                                         |
+------------+---------------+-----------------------------------------+
| sync_tier  | **NA**        | Tier to assign downloaded patches to.   |
|            |               | Defaults to “edge”.                     |
+------------+---------------+-----------------------------------------+
| sy         | patch         |                                         |
| nc_flavors | -sync.flavors |                                         |
+------------+---------------+-----------------------------------------+
| sync_arc   | patch-sync.   |                                         |
| hitectures | architectures |                                         |
+------------+---------------+-----------------------------------------+
| sync_mi    | patch-s       |                                         |
| nimum_kern | ync.minimum-k |                                         |
| el_version | ernel-version |                                         |
+------------+---------------+-----------------------------------------+
| report     | machine-repor |                                         |
| _retention | ts.database.r |                                         |
|            | etention-days |                                         |
+------------+---------------+-----------------------------------------+
| rep        | ma            |                                         |
| ort_cleanu | chine-reports |                                         |
| p_interval | .database.cle |                                         |
|            | anup-interval |                                         |
+------------+---------------+-----------------------------------------+
| repo       | mac           |                                         |
| rt_cleanup | hine-reports. |                                         |
| _row_limit | database.clea |                                         |
|            | nup-row-limit |                                         |
+------------+---------------+-----------------------------------------+
| in         | influx.url    |                                         |
| fluxdb_url |               |                                         |
+------------+---------------+-----------------------------------------+
| infl       | influx.token  |                                         |
| uxdb_token |               |                                         |
+------------+---------------+-----------------------------------------+
| influ      | influx.bucket |                                         |
| xdb_bucket |               |                                         |
+------------+---------------+-----------------------------------------+
| i          | influx        |                                         |
| nfluxdb_or | .organization |                                         |
| ganization |               |                                         |
+------------+---------------+-----------------------------------------+
| s3_bucket  | patch-stor    |                                         |
|            | age.s3-bucket |                                         |
+------------+---------------+-----------------------------------------+
| s          | patch-storag  |                                         |
| 3_endpoint | e.s3-endpoint |                                         |
+------------+---------------+-----------------------------------------+
| s3_region  | patch-stor    |                                         |
|            | age.s3-region |                                         |
+------------+---------------+-----------------------------------------+
| s3_acc     | p             |                                         |
| ess_key_id | atch-storage. |                                         |
|            | s3-access-key |                                         |
+------------+---------------+-----------------------------------------+
| s3_        | p             |                                         |
| secret_key | atch-storage. |                                         |
|            | s3-secret-key |                                         |
+------------+---------------+-----------------------------------------+
| s3_secure  | patch-stor    |                                         |
|            | age.s3-secure |                                         |
+------------+---------------+-----------------------------------------+
| profil     | pro           |                                         |
| er_enabled | filer.enabled |                                         |
+------------+---------------+-----------------------------------------+
| pro        | profiler.s    |                                         |
| filer_serv | erver_address |                                         |
| er_address |               |                                         |
+------------+---------------+-----------------------------------------+
| profile    | prof          |                                         |
| r_hostname | iler.hostname |                                         |
+------------+---------------+-----------------------------------------+
| profiler_s | profile       |                                         |
| ample_rate | r.sample_rate |                                         |
+------------+---------------+-----------------------------------------+
| profiler_u | profile       |                                         |
| pload_rate | r.upload_rate |                                         |
+------------+---------------+-----------------------------------------+
| p          | profi         |                                         |
| rofiler_mu | ler.mutex_pro |                                         |
| tex_profil | file_fraction |                                         |
| e_fraction |               |                                         |
+------------+---------------+-----------------------------------------+
| profile    | p             |                                         |
| r_block_pr | rofiler.block |                                         |
| ofile_rate | _profile_rate |                                         |
+------------+---------------+-----------------------------------------+
| profiler   | pr            |                                         |
| _profile_a | ofiler.profil |                                         |
| llocations | e_allocations |                                         |
+------------+---------------+-----------------------------------------+
| pr         | profiler.     |                                         |
| ofiler_pro | profile_inuse |                                         |
| file_inuse |               |                                         |
+------------+---------------+-----------------------------------------+
| prof       | profiler.pr   |                                         |
| iler_profi | ofile_mutexes |                                         |
| le_mutexes |               |                                         |
+------------+---------------+-----------------------------------------+
| pro        | profiler.p    |                                         |
| filer_prof | rofile_blocks |                                         |
| ile_blocks |               |                                         |
+------------+---------------+-----------------------------------------+
| profile    | profiler.prof |                                         |
| r_profile_ | ile_goroutine |                                         |
| goroutines |               |                                         |
+------------+---------------+-----------------------------------------+

.. |livepatch-status|800x31| image:: upload://2uNc2yggCQnxXj7gfkmcBVE0j2H.png
