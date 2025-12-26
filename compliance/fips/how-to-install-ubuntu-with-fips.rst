How to install Ubuntu with FIPS mode enabled
============================================

Enabling FIPS during installation ensures that your system is compliant from the first boot. This process is supported in the Ubuntu Server (Subiquity) and Ubuntu Desktop installers for 22.04 LTS and later.

Prerequisites
-------------

Before starting the installation, ensure you have an **Ubuntu Pro token**. You can obtain a free token for personal use (up to 5 machines) at the `Ubuntu Pro website <https://ubuntu.com/pro/subscribe>`_.

Installation Steps
------------------

1. **Start the Installer**: Boot your machine using the Ubuntu installation media.
2. **Configure Basic Settings**: Follow the standard prompts for language, keyboard layout, and networking.
3. **Ubuntu Pro Screen**:
   - Proceed through the installer until you reach the **Ubuntu Pro** configuration screen.
   - Select **Connect this machine to Ubuntu Pro**.
   - You will be prompted to enter your token. You can type it manually or follow the on-screen instructions to activate via a QR code or URL.
4. **Enable FIPS**:
   - Once the machine is attached to your Pro subscription, the installer will display available services.
   - Locate the **FIPS** section and select **Enable FIPS-updates** (recommended for security patches) or **Enable FIPS** (strict certified versions).
5. **Complete Installation**: Finish the remaining installation steps (User setup, SSH configuration, etc.).
6. **Reboot**: After the installation completes, reboot the system.

Verification
------------

Once the system boots, you can verify that FIPS is active by running:

.. code-block:: bash

   cat /proc/sys/crypto/fips_enabled

A return value of ``1`` indicates that FIPS mode is successfully enabled.

Automated Installation (Autoinstall)
------------------------------------

If you are using **autoinstall** (cloud-init), you can enable FIPS by adding your token and the service to the ``user-data`` configuration:

.. code-block:: yaml

   #cloud-config
   ubuntu_pro:
     token: <YOUR_PRO_TOKEN>
     enable:
       - fips-updates