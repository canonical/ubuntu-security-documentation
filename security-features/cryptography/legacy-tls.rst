Disable legacy TLS
------------------

Ubuntu 20.04 LTS (Focal Fossa) implemented a significant security enhancement by defaulting to **TLS v1.2 or higher** across all major TLS libraries. This change aligns with industry standards that phase out the insecure TLS 1.0 and 1.1 protocols, which contain known cryptographic vulnerabilities such as susceptibility to `POODLE <https://en.wikipedia.org/wiki/POODLE>`_, `BEAST <https://en.wikipedia.org/wiki/Transport_Layer_Security#BEAST_attack>`_, and `downgrade attacks <https://en.wikipedia.org/wiki/Downgrade_attack>`_.

----

Affected libraries and configuration changes
--------------------------------------------

The following TLS libraries have been updated with new security defaults:

**OpenSSL**
    - **Security Level**: Raised from ``SECLEVEL=1`` to ``SECLEVEL=2``
    - **Minimum TLS Version**: 1.2 (TLS 1.0/1.1 disabled)
    - **Disabled Algorithms**: SHA-1 signatures, RSA keys <2048 bits, DH keys <2048 bits
    - **Default Cipher String**: ``DEFAULT@SECLEVEL=2``

**GnuTLS**
    - **Priority String**: ``NORMAL:-VERS-ALL:+VERS-TLS1.3:+VERS-TLS1.2:+VERS-DTLS1.2:%PROFILE_MEDIUM``
    - **Disabled Protocols**: TLS 1.0 and 1.1 explicitly excluded
    - **Configuration File**: ``/etc/gnutls/config`` (if present)

**NSS (Network Security Services)**
    - **Minimum Protocol**: TLS 1.2 enforced internally
    - **Weak Ciphers**: Legacy cipher suites disabled by default

**Qt Framework**
    - **Effective Impact**: Cannot override OpenSSL security levels programmatically
    - **Behavior**: TLS 1.0/1.1 requests fail with socket error -1
    - **API Limitation**: Setting lower TLS versions breaks connectivity entirely

----

Legacy TLS re-enablement (not recommended)
-------------------------------------------

.. warning::
**Security risk**

   Re-enabling TLS 1.0/1.1 significantly reduces security and exposes systems to serious vulnerabilities. Only use as a temporary measure for critical legacy compatibility.

**OpenSSL System-wide Configuration**

1. Edit ``/etc/ssl/openssl.cnf`` and add at the very top (before any sections)::

    openssl_conf = default_conf

2. Add the following sections at the end of the file::

    [default_conf]
    ssl_conf = ssl_sect

    [ssl_sect]
    system_default = system_default_sect

    [system_default_sect]
    CipherString = DEFAULT@SECLEVEL=1

**OpenSSL Per-Application Override**

Use the ``OPENSSL_CONF`` environment variable to specify a custom configuration file, which uses the same format as ``/etc/ssl/openssl.cnf``::

    export OPENSSL_CONF=/path/to/custom-openssl.cnf

**GnuTLS Override**

1. Create ``/etc/gnutls/config``::

    [overrides]
    default-priority-string = NORMAL

2. Alternatively, use the ``GNUTLS_SYSTEM_PRIORITY_FILE`` environment variable to specify a configuration file in the same format as ``/etc/gnutls/config``::

    export GNUTLS_SYSTEM_PRIORITY_FILE=/path/to/gnutls-override-config

----

Common issues and troubleshooting
----------------------------------

Connection symptoms and solutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+-------------------------+-----------------------------+--------------------------------+
| Symptom                 | Possible Cause              | Solution                       |
+=========================+=============================+================================+
| Hanging connections     | DNS/network issues          | Check ``resolvectl query``     |
+-------------------------+-----------------------------+--------------------------------+
| Qt socket error -1      | SECLEVEL=2 restriction      | Application-level workaround   |
+-------------------------+-----------------------------+--------------------------------+
| Legacy app failures     | TLS version incompatibility | Temporary SECLEVEL=1 override  |
+-------------------------+-----------------------------+--------------------------------+

Diagnostic commands
~~~~~~~~~~~~~~~~~~~

Test TLS connectivity::

    # Test TLS 1.2 support
    openssl s_client -tls1_2 -connect example.com:443

    # Test TLS 1.3 support
    openssl s_client -tls1_3 -connect example.com:443

    # Check network connectivity
    mtr example.com
    resolvectl query example.com

----

Security implications and best practices
-----------------------------------------

**Risks of Re-enabling Legacy TLS**:
    - Exposure to POODLE, BEAST, CRIME attacks
    - Downgrade attack vulnerabilities
    - Compliance violations (PCI DSS, security standards)
    - Weak cryptographic primitives and key sizes

**Recommended Approach**:
    1. **Upgrade infrastructure** to support TLS 1.2+ instead of downgrading security
    2. Use **scoped overrides** (per-application) rather than system-wide changes
    3. Implement **temporary workarounds** only while planning proper upgrades
    4. Regular security auditing of systems requiring legacy protocol support

**Legacy Support Alternatives**:
    - Deploy SSL/TLS terminating proxies that can handle both old and new protocols
    - Implement application-level TLS handling with proper version negotiation
    - Use containerized environments with different security policies for legacy applications

----

Additional resources
--------------------

For comprehensive technical discussion and community troubleshooting, see the Ubuntu Discourse post: `Default to TLS v1.2 in all TLS libraries in 20.04 LTS <https://discourse.ubuntu.com/t/default-to-tls-v1-2-in-all-tls-libraries-in-20-04-lts/12464>`_.

This security enhancement reflects Ubuntu's commitment to secure-by-default configuration while maintaining backward compatibility through configuration options for critical legacy system support.

