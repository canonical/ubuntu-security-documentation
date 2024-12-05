Getting started with FIPS
#########################

Prerequisites
-------------

* An `Ubuntu One account <https://login.ubuntu.com/>`_ with the email address you used to purchase your subscription.

* An Ubuntu machine running Ubuntu server or desktop 

Install the Pro client
======================

.. code-block:: bash

    sudo apt update
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


Enable FIPS
===========

.. WARNING:: Switching the system to contain the FIPS certified packages cannot be easily undone. Use a testing system for experimentation before trying on production.

We recommend enabling the :doc:`fips-updates <../fips-howtos/how-to-download-security-patches>` option that includes security fixes timely before the packages are re-certified. However, we provide the option to install the validated packages that are only updated on re-validation.

Enable FIPS including timely security updates
--------------------------------------------

#. Enable ``fips-updates``:
.. code-block:: bash

    sudo pro enable fips-updates

#. Verify that the system is attached to pro and has FIPS enabled:
.. code-block:: bash
    sudo pro status

Please proceed to the reboot section.

Strictly with the certified packages

    Enable FIPS.
    sudo pro enable fips
    Verify that the system is attached to pro and has FIPS enabled.
    sudo pro status
    Please proceed to the reboot section.

Reboot

The pro client will install the necessary packages for the FIPS mode, including the kernel and the bootloader. After this step you MUST reboot to put the system into FIPS mode. The reboot will boot into the FIPS-supported kernel and create the /proc/sys/crypto/fips_enabled entry which tells the FIPS certified modules to run in FIPS mode. If you do not reboot after installing and configuring the bootloader, FIPS mode is not yet enabled.

To verify that FIPS is enabled after the reboot check the /proc/sys/crypto/fips_enabled file and ensure it is set to 1. If it is set to 0, the FIPS modules will not run in FIPS mode. If the file is missing, the FIPS kernel is not installed, you can verify that FIPS has been properly enabled with the pro status command.
FIPS and livepatching

The Livepatch service is enabled by default while attaching the system to the Ubuntu Advantage service. Livepatch and the fips stream are not compatible, so it will be disabled. Livepatch is available on the fips-updates stream.