Symlink restrictions
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


A long-standing class of security issues is the symlink-based ToCToU race, most commonly seen in world-writable directories like /tmp/. The common method of exploitation of this flaw is crossing privilege boundaries when following a given symlink (i.e. a root user follows a symlink belonging to another user).

In Ubuntu 10.10 and later, symlinks in world-writable sticky directories (e.g. /tmp) cannot be followed if the follower and directory owner do not match the symlink owner. The behavior is controllable through the /proc/sys/kernel/yama/protected_sticky_symlinks sysctl, available via Yama.

See `test-kernel-security.py <https://git.launchpad.net/qa-regression-testing/tree/scripts/test-kernel-security.py>`_ for regression tests.
