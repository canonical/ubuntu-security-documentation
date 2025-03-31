Logging and monitoring
######################

Monitoring of the Livepatch server can be most easily done by setting up
monitoring on one or more endpoints. Livepatch server exposes two
endpoints, in particular, ``/debug/info`` and ``/debug/status``, that
provide information on the server’s version and the server’s
database/related services, respectively. Any monitoring solution can
periodically check ``/debug/info`` as a liveliness check to ensure the
service is running.

The on-prem server also exposes Prometheus text-based formatted metrics
available from a /metrics endpoint which can be used to monitor the
system.

When deploying with Juju, debug logs from all deployed applications can
be obtained with the command ``juju debug-logs``. Increasing the
server’s log level can be configured with
``juju config livepatch log_level=<level>`` A full list of log levels
are available on the charm’s config
`page <https://charmhub.io/canonical-livepatch-server/configure#log_level>`__.

Further information on the use of juju for logging can be obtained from
Juju’s `documentation <https://juju.is/docs/olm/juju-debug-log>`__.
