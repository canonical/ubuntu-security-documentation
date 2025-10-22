How to connect to WiFi in FIPS mode
====================================

You can connect to WiFi networks on a FIPS-enabled machine, as long as the network is set up to be compatible with the FIPS 140-3 requirements. WiFi uses encryption, and on Ubuntu this is handled by the wpa_supplicant package, which is linked against the system OpenSSL library.

When operating in FIPS mode, only FIPS-approved algorithms can be used. In particular, the WPA2 security protocol for WiFi networks, as specified in IEEE 802.11i-2004, calls for Pre-Shared Key networks to compute a shared secret based on the SSID network name and the password, using the PBKDF2-SHA1 hash function, with the SSID being the salt. The minimum security parameters for PBKDF2 are specified in NIST SP800-132, with a minimum key-length of 8 characters and a minimum salt-length of 16 characters.

This means that for WPA2 networks the SSID must be at least 16 characters, and the password at least 8 characters (which is in accordance with the WPA2 specifications already).