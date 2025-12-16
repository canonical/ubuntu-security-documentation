Disable legacy TLS
##################

Older versions of the Transport Layer Security (TLS) protocol, such as SSL 3.0,
TLS 1.0, and TLS 1.1, contain inherent vulnerabilities and don't provide the
necessary security you may expect when using such protocols.

Therefore, Ubuntu 20.04 LTS (Focal Fossa) and later releases proactively
disable these protocols, requiring more secure alternatives.

You can re-enable these protocols to communicate with legacy systems. For more
information, see `Default to TLS v1.2 in all TLS libraries in 20.04 LTS
<https://discourse.ubuntu.com/t/default-to-tls-v1-2-in-all-tls-libraries-in-20-04-lts/12464/8>`_.
