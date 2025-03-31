Setup TLS
#########

The security of livepatching depends not only on the signed kernel
modules but also on the secure TLS channel between the livepatch client
and the on-prem server. It is thus paramount to setup the necessary TLS
keys and certificates for the on-prem service to provide the necessary
security.

There are several ways to set up TLS for livepatch on-prem. One way is
to use a dedicated TLS terminating reverse proxy in front of the haproxy
service. Another way is to configure the appropriate TLS certificate and
key on the haproxy instance directly.

Configuring TLS for haproxy
---------------------------

These are the steps to configure TLS on the haproxy service directly:

1.Create a ``tls-overlay.yaml`` file with the following content:

::

   applications:
     haproxy:
       options:
         services: |
           - service_name: livepatch
             service_host: "0.0.0.0"
             service_port: 443
             service_options:
               - balance leastconn
               - cookie SRVNAME insert
               - 'acl restricted_api path_beg,url_dec -i /api/auth-tokens'
               - http-request deny if restricted_api
             server_options: maxconn 200 cookie S{i} check
             crts: [DEFAULT]
         ssl_cert: include-base64://./cert.pem
         ssl_key: include-base64://./key.pem

2. Rename the certificate and key files to ``cert.pem`` and ``key.pem``
   and place them in the same directory as the downloaded overlay file.
3. Run the following juju command

::

   $ juju deploy ch:canonical-livepatch-onprem --overlay ./tls-overlay.yaml

4. Run ``juju status`` to verify that the haproxy service is now
   exposing port 443 |screenshot_20210603_165758|690x55|

Configuring livepatch admin tool with TLS
-----------------------------------------

If the TLS certificate used for livepatch originates from a trusted CA,
there should be no further configuration necessary - the livepatch admin
tool will use the configured system certificates to verify the server’s
responses.

If, however, a self-signed certificate is used, the administration tool
will need to be configured to use the certificate. There are several
ways to do that.

Command line option
~~~~~~~~~~~~~~~~~~~

The command line option for the livepatch admin tool accepts either the
path to a certificate chain PEM file, or the contents of the certificate
chain:

::

   $ livepatch-admin --ca ./cert.pem login -a (...)

::

   $ livepatch-admin --ca "$(cat ./cert.pem)" login -a (...)

Environment variable
~~~~~~~~~~~~~~~~~~~~

The environment variable ``LIVEPATCH_CA_CRT`` can be set with either the
path to a certificate chain file or the contents of the certificate
chain:

::

   $ export LIVEPATCH_CA_CRT='/temp/cert.pem'

::

   $ export LIVEPATCH_CA_CRT="$(cat ./cert.pem)"

Configuring livepatch client with TLS
-------------------------------------

If a self-signed certificate is used for the livepatch on-prem service,
livepatch client instances will also need to be configured with that
certificate to be able to verify responses coming from the on-prem
server:

::

   $ sudo canonical-livepatch config ca-certs=@stdin < ./cert.pem

For more information on how to configure an HTTPS proxy on the Livepatch
Client, please check out
`this </client/how-to-guides/configure-proxy>`__ guide.

.. |screenshot_20210603_165758|690x55| image:: upload://nuS5aGmo44qwv5vagLczO0tnfog.png
