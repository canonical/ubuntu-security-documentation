How to transition from the previous compliance tooling
=======================================================

The previous compliance tooling available in Ubuntu provided per-release scripts for CIS compliance. The following points map the old commands to the Ubuntu Security Guide syntax.


.. csv-table:: 
    "Command", "Replacement"
    "/usr/share/ubuntu-scap-security-guides/cis-hardening/Canonical_Ubuntu_20.04_CIS-harden.sh", "usg fix"
    "/usr/share/ubuntu-scap-security-guides/cis-hardening/Canonical_Ubuntu_18.04_CIS-harden.sh", "usg fix"
    "/usr/share/ubuntu-scap-security-guides/cis-hardening/Canonical_Ubuntu_16.04_CIS_v1.1.0-harden.sh", "usg fix"
    "cis-audit", "usg audit"
    "Custom configuration with ruleset-params.conf", "Profile customization"