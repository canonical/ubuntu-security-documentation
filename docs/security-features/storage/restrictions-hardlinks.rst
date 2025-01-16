Hardlink restrictions
-----------------------

.. tab-set::

    .. tab-item:: 24.04

        TBA

    .. tab-item:: 22.04

        TBA

    .. tab-item:: 20.04

            TBA

    .. tab-item:: 18.04
        
        TBA
    
    .. tab-item:: 16.04

        TBA  

    .. tab-item:: 14.04

        TBA


Hardlinks can be abused in a similar fashion to symlinks above, but they are not limited to world-writable directories. If /etc/ and /home/ are on the same partition, a regular user can create a hardlink to /etc/shadow in their home directory. While it retains the original owner and permissions, it is possible for privileged programs that are otherwise symlink-safe to mistakenly access the file through its hardlink. Additionally, a very minor untraceable quota-bypassing local denial of service is possible by an attacker exhausting disk space by filling a world-writable directory with hardlinks.

In Ubuntu 10.10 and later, hardlinks cannot be created to files that the user would be unable to read and write originally, or are otherwise sensitive. The behavior is controllable through the /proc/sys/kernel/yama/protected_nonaccess_hardlinks sysctl, available via Yama.

See `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_        for regression tests.
