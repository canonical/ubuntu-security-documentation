How to connect to Wi-Fi in FIPS mode
####################################

You can connect to Wi-Fi networks on a FIPS-enabled machine, provided the
network is compatible with FIPS 140-3 requirements. Wi-Fi uses encryption. On
Ubuntu, the ``wpa_supplicant`` package handles this, linking against the system
OpenSSL library.

When operating in FIPS mode, you can only use FIPS-approved algorithms.
Specifically, the WPA2 security protocol for Wi-Fi networks (specified in IEEE
802.11i-2004) requires Pre-Shared Key (PSK) networks to compute a shared
secret based on the SSID network name and the password. It uses the PBKDF2-SHA1
hash function, with the SSID as the salt. NIST SP800-132 specifies the minimum
security parameters for PBKDF2: a minimum key length of 8 characters and a
minimum salt length of 16 characters.

This means that for WPA2 networks, the SSID must be at least 16 characters
long, and the password must be at least 8 characters long (which aligns with
WPA2 specifications).
