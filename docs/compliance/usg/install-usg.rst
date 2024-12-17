Install Ubuntu Security Guide
##############################

Prerequisites
=============

* An `Ubuntu One account <https://login.ubuntu.com/>`_ with the email address you used to purchase your subscription.

* An Ubuntu machine running Ubuntu server or desktop 20.04 LTS

.. NOTE:: Hardening an existing Ubuntu image with the USG may take a long time due to the filesystem checks.


Install the Pro client
======================

.. code-block:: bash

    sudo apt update
    sudo add-apt-repository universe
    sudo apt install ubuntu-advantage-tools


Attach the subscription
=======================

.. NOTE:: Skip this step if you are using an Ubuntu Pro instance from a public cloud marketplace.

1. Check the status of to the Pro client:

.. code-block:: bash

    sudo pro status

.. code-block:: bash
        
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

You will see an ouput similar to the following example with a link and a code:

.. code-block:: bash

    You should see output like this, giving you a link and a code:

    Initiating attach operation...

    Please sign in to your Ubuntu Pro account at this link:
    https://ubuntu.com/pro/attach
    And provide the following code: 123456

3. Follow the link and enter the code. 

4. Choose which subscription you want to attach to. By default, the Free Personal Token will be selected.

5. Click **Submit**.

The attachment process will continue in the terminal window, you shoul see a similar output:

.. code-block:: bash

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



Enable the USG
==============

Run the following commands to enable and install the USG:

.. code-block:: bash

    sudo pro enable usg
    sudo apt install usg


Transition from the previous compliance tooling
===============================================

The previous compliance tooling available in Ubuntu provided per-release scripts for CIS compliance. The following points map the old commands to the Ubuntu Security Guide syntax.

.. csv-table:: 
    :header: "Command", "Replacement"

    "/usr/share/ubuntu-scap-security-guides/cis-hardening/Canonical_Ubuntu_20.04_CIS-harden.sh", "usg fix"
    "/usr/share/ubuntu-scap-security-guides/cis-hardening/Canonical_Ubuntu_18.04_CIS-harden.sh", "usg fix"
    "/usr/share/ubuntu-scap-security-guides/cis-hardening/Canonical_Ubuntu_16.04_CIS_v1.1.0-harden.sh", "usg fix"
    "cis-audit", "usg audit"
    "Custom configuration with ruleset-params.conf", "Profile customization"