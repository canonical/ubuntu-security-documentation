Install Ubuntu Security Guide
#############################


Prerequisites
=============

* An `Ubuntu One account <https://login.ubuntu.com/>`_ with the email address
  you used to purchase your subscription.
* An Ubuntu machine running Ubuntu Server or Desktop 20.04 LTS (Focal Fossa).

.. note::
   Hardening an existing Ubuntu image with USG can take a long time due to
   filesystem checks.


Install the Pro client
======================

.. code-block:: bash

   sudo apt update
   sudo add-apt-repository universe
   sudo apt install ubuntu-advantage-tools


Attach the subscription
=======================

.. note::
   Skip this step if you are using an Ubuntu Pro instance from a public cloud
   marketplace.

1. Check the status of the Pro client:

   .. code-block:: bash

      sudo pro status

   Output:

   .. code-block:: text

      SERVICE          AVAILABLE  DESCRIPTION
      anbox-cloud      yes        Scalable Android in the cloud
      esm-apps         yes        Expanded Security Maintenance for Applications
      esm-infra        yes        Expanded Security Maintenance for Infrastructure
      fips             yes        NIST-certified FIPS crypto packages
      fips-updates     yes        FIPS compliant crypto packages with stable security updates
      livepatch        yes        Canonical Livepatch service
      ros              yes        Security Updates for the Robot Operating System
      usg              yes        Security compliance and audit tools

      For a list of all Ubuntu Pro services, run 'pro status --all'

      This machine is not attached to an Ubuntu Pro subscription.
      See https://ubuntu.com/pro

2. Attach your machine to a subscription:

   .. code-block:: bash

      sudo pro attach

   You will see output similar to the following example with a link and a code:

   .. code-block:: text

      Initiating attach operation...

      Please sign in to your Ubuntu Pro account at this link:
      https://ubuntu.com/pro/attach
      And provide the following code: 123456

3. Follow the link and enter the code.

4. Choose which subscription you want to attach to. By default, the system
   selects the Free Personal Token.

5. Click **Submit**.

   The attachment process continues in the terminal window. You should see output
   similar to:

   .. code-block:: text

      Attaching the machine...
      Enabling default service esm-apps
      Updating Ubuntu Pro: ESM Apps package lists
      Ubuntu Pro: ESM Apps enabled
      Enabling default service esm-infra
      Updating Ubuntu Pro: ESM Infra package lists
      Ubuntu Pro: ESM Infra enabled
      Enabling default service livepatch
      Installing canonical-livepatch snap
      Canonical Livepatch enabled
      This machine is now attached to 'Ubuntu Pro - free personal subscription'

      SERVICE          ENTITLED  STATUS       DESCRIPTION
      anbox-cloud      yes       disabled     Scalable Android in the cloud
      esm-apps         yes       enabled      Expanded Security Maintenance for Applications
      esm-infra        yes       enabled      Expanded Security Maintenance for Infrastructure
      fips             yes       disabled     NIST-certified FIPS crypto packages
      fips-updates     yes       disabled     FIPS compliant crypto packages with stable security updates
      livepatch        yes       enabled      Canonical Livepatch service
      ros              yes       disabled     Security Updates for the Robot Operating System
      usg              yes       disabled     Security compliance and audit tools

      NOTICES
      Operation in progress: pro attach

      For a list of all Ubuntu Pro services, run 'pro status --all'
      Enable services with: pro enable <service>

          Account: <email>
      Subscription: Ubuntu Pro - free personal subscription


Enable USG
==========

Run the following commands to enable and install USG:

.. code-block:: bash

   sudo pro enable usg
   sudo apt install usg


Transition from previous compliance tooling
===========================================

Previous compliance tools available in Ubuntu provided per-release scripts for
CIS Benchmarks compliance. The following table maps the old commands to the Ubuntu
Security Guide syntax.

.. csv-table::
   :header: "Command", "Replacement"

   "/usr/share/ubuntu-scap-security-guides/cis-hardening/Canonical_Ubuntu_20.04_CIS-harden.sh", "usg fix"
   "/usr/share/ubuntu-scap-security-guides/cis-hardening/Canonical_Ubuntu_18.04_CIS-harden.sh", "usg fix"
   "/usr/share/ubuntu-scap-security-guides/cis-hardening/Canonical_Ubuntu_16.04_CIS_v1.1.0-harden.sh", "usg fix"
   "cis-audit", "usg audit"
   "Custom configuration with ruleset-params.conf", "Profile customization"
