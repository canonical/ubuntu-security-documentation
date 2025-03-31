Configure-proxy
################

Livepatch client users have the option to communicate with the Livepatch
server through a proxy. Livepatch supports communicating through HTTP,
HTTPS, or SOCKS5 proxies. To do so, there are a few configuration
parameters that should be assigned.

Check proxy configuration
-------------------------

To check the proxy configuration of the Livepatch client, run the
following command:

.. code:: bash

   $ canonical-livepatch config
   http-proxy: "http://proxy.example.com"
   https-proxy: "http://proxy.example.com"
   no-proxy: ""
   ca-certs: ""
   ...

Note that an empty string value (“”) means the corresponding parameter
is not set and system defaults will be used.

Using an HTTP/SOCKS5 proxy
--------------------------

To enable the usage of an HTTP proxy, run the following commands:

.. code:: bash

   $ sudo canonical-livepatch config http-proxy=http://proxy.example.com
   $ sudo canonical-livepatch config https-proxy=http://proxy.example.com

Users can also configure the Livepatch client to use a SOCKS5 proxy by
running these commands:

.. code:: bash

   $ sudo canonical-livepatch config http-proxy=socks5://proxy.example.com:1080
   $ sudo canonical-livepatch config https-proxy=socks5://proxy.example.com:1080

Although the client respects the standard Linux environment variables
used for proxy setup (i.e., ``HTTP_PROXY``, ``HTTPS_PROXY`` or
``NO_PROXY``), please note that for them to take effect, they should be
set in the Livepatch client daemon process environment. Therefore, it is
more straightforward for users to use the above configuration
parameters.

Using an HTTPS proxy
--------------------

When using an HTTPS proxy (not to be confused with proxying HTTPS
requests), users need to make sure they are including ``https://``
scheme when setting the above configuration parameters:

.. code:: bash

   $ sudo canonical-livepatch config http-proxy=https://proxy.example.com
   $ sudo canonical-livepatch config https-proxy=https://proxy.example.com

If a self-signed CA certificate is included in the HTTPS proxy’s TLS
certificate chain, the user should add the CA certificate to the trusted
certificates on the host machine by running the following commands
(assuming ``ca.crt`` is the CA certificate file):

.. code:: bash

   $ sudo apt-get install ca-certificates
   $ sudo cp ca.crt /usr/share/ca-certificates
   $ sudo dpkg-reconfigure ca-certificates

However, if a user does not want to install a self-signed CA certificate
as a system-wide trusted one, they can explicitly instruct Livepatch
client to trust the CA certificate:

.. code:: bash

   $ sudo canonical-livepatch config ca-certs=@stdin < ca.crt

Routing directly to Livepatch server
------------------------------------

If there is already a system-wide proxy set up (e.g., by ``HTTP_PROXY``
environment variable), the users can escape it for communication with
the Livepatch server by using the following configuration:

.. code:: bash

   $ sudo canonical-livepatch config no-proxy=canonical.com
