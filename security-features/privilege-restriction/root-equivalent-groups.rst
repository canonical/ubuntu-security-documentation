Root-Equivalent Groups
#######################

Root-equivalent groups are system groups that grant users powerful privileges similar to root. They exist to let trusted users manage logs, disks, containers, virtual machines, and other privileged functions without giving full sudo access. However, assigning these groups to an untrusted or compromised user can let them read sensitive data, manipulate system components, or escalate to full root control. Treat membership in these groups with the same caution as granting administrative access.


Ubuntu Groups: Root-Equivalent and High-Risk
=============================================

The "Default" column indicates whether the group exists in a standard Ubuntu Desktop installation. Groups marked "Yes" are created automatically, while "No" means they're added by installing additional software (like Docker).

Fully Root-Equivalent Groups
-----------------------------

These groups allow users to escalate to full root privileges with minimal effort. Membership in these groups should be treated with the same level of caution and security controls as granting direct root access.

+-------------------+-----------+-------------------------------------------------------------+------------------------------------------------------------------------+-------------------------------------------------------+
| Group             | Default?  | Purpose                                                     | Risk                                                                   | Example attack path                                   |
+===================+===========+=============================================================+========================================================================+=======================================================+
| root              | Yes       | The superuser group with full system privileges.            | Complete control over the system.                                      | N/A                                                   |
+-------------------+-----------+-------------------------------------------------------------+------------------------------------------------------------------------+-------------------------------------------------------+
| sudo              | Yes       | Allows running commands as root via sudo.                   | Can execute any command with full privileges.                          | Spawn a root shell or execute privileged commands.    |
+-------------------+-----------+-------------------------------------------------------------+------------------------------------------------------------------------+-------------------------------------------------------+
| disk              | Yes       | Direct access to raw disk block devices.                    | Can bypass filesystem permissions and read/write any file.             | Read password hashes or modify system files by        |
|                   |           |                                                             |                                                                        | accessing the raw disk device.                        |
+-------------------+-----------+-------------------------------------------------------------+------------------------------------------------------------------------+-------------------------------------------------------+
| lxd               | Yes       | Manages LXD containers and virtual machines.                | Privileged containers have full access to host resources.              | Launch a privileged container that mounts the host    |
|                   |           |                                                             |                                                                        | root filesystem with write access.                    |
+-------------------+-----------+-------------------------------------------------------------+------------------------------------------------------------------------+-------------------------------------------------------+
| docker            | No        | Manages Docker containers.                                  | Containers can mount and access any part of the host filesystem.       | Run a container that mounts the host root as a        |
|                   |           |                                                             |                                                                        | volume with full read-write access.                   |
+-------------------+-----------+-------------------------------------------------------------+------------------------------------------------------------------------+-------------------------------------------------------+
| libvirt           | No        | Manages virtual machines via libvirtd daemon.               | Storage pool operations execute with root privileges.                  | Create a storage volume pointing to sensitive files   |
|                   |           |                                                             |                                                                        | to read or overwrite them as root.                    |
+-------------------+-----------+-------------------------------------------------------------+------------------------------------------------------------------------+-------------------------------------------------------+


High-Risk but Not Root-Equivalent (REMOVE???)
------------------------------------------------------

These groups provide access to sensitive information or powerful capabilities but don't directly grant root access. They should still be treated as high-risk and membership should be minimized.

+-------------------+-----------+-------------------------------------------------------------+------------------------------------------------------------------------+-------------------------------------------------------+
| Group             | Default?  | Purpose                                                     | Risk                                                                   | Example attack path                                   |
+===================+===========+=============================================================+========================================================================+=======================================================+
| shadow            | Yes       | Read access to /etc/shadow                                  | Exposure of all user password hashes.                                  | Copy password hash file and use offline cracking      |
|                   |           |                                                             |                                                                        | tools to recover passwords.                           |
+-------------------+-----------+-------------------------------------------------------------+------------------------------------------------------------------------+-------------------------------------------------------+
| lpadmin           | Yes       | Manage printers via CUPS.                                   | Can execute arbitrary code as root through CUPS service.               | Install a malicious printer backend or filter that    |
|                   |           |                                                             |                                                                        | runs attacker code as root.                           |
+-------------------+-----------+-------------------------------------------------------------+------------------------------------------------------------------------+-------------------------------------------------------+
| adm               | Yes       | Read access to system log files.                            | Exposure of credentials, tokens, and security events.                  | Search authentication and application logs for        |
|                   |           |                                                             |                                                                        | leaked passwords, API keys, and tokens.               |
+-------------------+-----------+-------------------------------------------------------------+------------------------------------------------------------------------+-------------------------------------------------------+
| systemd-journal   | Yes       | Read the full systemd journal.                              | Access to service secrets, environment variables, and command          | Query journal for process environment variables,      |
|                   |           |                                                             | arguments containing sensitive data.                                   | command-line passwords, and authentication tokens.    |
+-------------------+-----------+-------------------------------------------------------------+------------------------------------------------------------------------+-------------------------------------------------------+
| input             | Yes       | Access to input devices like keyboards and mice.            | Complete keystroke logging capability.                                 | Read input event devices to capture all typed         |
|                   |           |                                                             |                                                                        | passwords, commands, and sensitive data.              |
+-------------------+-----------+-------------------------------------------------------------+------------------------------------------------------------------------+-------------------------------------------------------+
| wireshark         | No        | Raw packet capture on network interfaces.                   | Network traffic interception and credential sniffing.                  | Capture network packets to intercept unencrypted      |
|                   |           |                                                             |                                                                        | credentials and session tokens.                       |
+-------------------+-----------+-------------------------------------------------------------+------------------------------------------------------------------------+-------------------------------------------------------+


Best Practices for Root-Equivalent Groups
==========================================

- **Treat as Root Access**: Apply the same security controls and approval processes for group membership as you would for direct root access.
- **Minimize Membership**: Only add users when absolutely necessary and remove access immediately when no longer needed.
- **Separate Accounts**: Use dedicated privileged accounts for administrative tasks rather than elevating user accounts.
- **Prefer Limited Access**: Use specific sudo rules or service-specific permissions instead of broad group membership when possible.
- **Regular Reviews**: Audit group memberships periodically to verify access is still required.
- **Monitor Changes**: Log all group membership changes and investigate unexpected modifications immediately.


How to Audit and Remediate
===========================

Audit (who has access)
-----------------------

- For a single user:

  .. code-block:: bash

     $ id <user>
     $ groups <user>

- Enumerate all local groups and users:

  .. code-block:: bash

     $ getent group


Remediate (remove access)
--------------------------

- Remove a user from a group:

  .. code-block:: bash

     $ sudo gpasswd -d <user> <group>

- Notes:
    - Group membership changes typically require the user to log out and back in (or start a new session) to take effect.
    - Be careful removing your own access on remote systems; you can lock yourself out.
