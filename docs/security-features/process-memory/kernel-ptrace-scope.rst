ptrace scope
------------

.. tab-set::
    
    .. tab-item:: 14.04

        TBA

    .. tab-item:: 16.04
    
        TBA
   
    .. tab-item:: 18.04
    
        TBA

    .. tab-item:: 20.04
    
        TBA

    .. tab-item:: 22.04
    
        TBA

    .. tab-item:: 24.04
    
        TBA

A troubling weakness of the Linux process interfaces is that a single user is able to examine the memory and running state of any of their processes. For example, if one application was compromised, it would be possible for an attacker to attach to other running processes (e.g. SSH sessions, GPG agent, etc) to extract additional credentials and continue to immediately expand the scope of their attack without resorting to user-assisted phishing or trojans.

In Ubuntu 10.10 and later, users cannot ptrace processes that are not a descendant of the debugger. The behavior is controllable through the /proc/sys/kernel/yama/ptrace_scope sysctl, available via Yama.

In the case of automatic crash handlers, a crashing process can specficially allow an existing crash handler process to attach on a process-by-process basis using prctl(PR_SET_PTRACER, debugger_pid, 0, 0, 0).

See test-kernel-security.py for regression tests. 

