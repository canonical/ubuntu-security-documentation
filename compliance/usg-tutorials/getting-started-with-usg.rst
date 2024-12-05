Getting started with the Ubuntu Security Guide
##############################################

Security Technical Implementation Guides like the CIS benchmark or DISA-STIG have hundreds of configuration recommendations, so hardening and auditing a Linux system manually can be very tedious. Ubuntu Security Guide (USG) is a new tool available with Ubuntu 20.04 LTS that greatly improves the usability of hardening and auditing, and allows for environment-specific customizations. The following sections provide more information on hardening and auditing with usg.

In this tutorial, you will learn how to audit with the CIS benchmark or DISA-STIG on Ubuntu 20.04 LTS machines, while using an Ubuntu Pro subscription.

Prerequisites
-------------

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



#. Check the status of to the Pro client:

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

#. Attach your machine to a subscription:

.. code-block:: bash

    sudo pro attach

You will see an ouput similar to the following example with a link and a code:

.. code-block:: bash

    You should see output like this, giving you a link and a code:

    Initiating attach operation...

    Please sign in to your Ubuntu Pro account at this link:
    https://ubuntu.com/pro/attach
    And provide the following code: 123456

#. Follow the link and enter the code. 

#. Choose which subscription you want to attach to. By default, the Free Personal Token will be selected.

#. Click **Submit**.

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


Install CIS benchmarks
======================  

If you want to use `CIS benchmarks <https://ubuntu.com/security/certifications/docs/usg/cis/compliance>`_, install them: 

.. code-block:: bash
    
    sudo apt install usg-benchmarks-1


Run the USG
===========

You have successfully enabled USG tool and can now use it to audit or harden your Ubuntu machine. 

To audit use the following command replacing `<PROFILE>` with `cis_level1_server`, with `cis_level1_workstation`, or `disa_stig`, depending on the compliance target:

.. code-block:: bash
    
    sudo usg audit <PROFILE>

The output of this command will show the compliance status and will point to an HTML file with the audit report. 