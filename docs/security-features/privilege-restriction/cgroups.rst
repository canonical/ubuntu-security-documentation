Cgroups (Control Groups)
========================

Control Groups, commonly known as cgroups, are a powerful Linux kernel feature that allows for
the management and partitioning of system resources. At their core, cgroups enable a user to 
allocate, prioritize, and limit the usage of hardware resources (such as CPU, memory, disk I/O,
and network bandwidth) for a collection of processes. This capability is fundamental to the 
stability and security of a modern Ubuntu system, providing the foundation for technologies like
``systemd`` and containerization.


Core Concepts of Cgroups
------------------------

Cgroups operate on the key principles of organizational hierarchy and specific controllers representing system resources.

Hierarchy
^^^^^^^^^

Cgroups are organized in a tree-like hierarchy, similar to a filesystem. This structure allows
for fine-grained control, where resource limits set on a parent cgroup can be inherited by its
children and, recursively, all descendant cgroups.

Controllers (Subsystems)
^^^^^^^^^^^^^^^^^^^^^^^^
Each hierarchy is associated with one or more "controllers", which represent a specific type of
system resource. Key controllers include: 

- ``cpu``: Manages access to the CPU. It can be used to assign CPU shares (relative priority) or enforce a hard cap on CPU usage.
- ``memory``: Controls memory usage, allowing a user to set limits on how much memory a group of processes can consume and what happens when that limit is reached.
- ``blkio``: Manages block I/O, controlling read/write access to block devices like hard drives and SSDs.
- ``pids``: Limits the number of processes that can be created within a cgroup, providing a crucial defence against "fork bomb" attacks.
- ``network_cls``/``network_prio``: Used to tag network packets from processes within a cgroup, allowing for traffic shaping and prioritization.

More information about controllers can be found in `the kernel documentation <https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html>`_.


The Role of Cgroups in System Stability and Security
----------------------------------------------------

While often seen as a resource management tool, cgroups are a critical component of system
security and stability because they prevent misuse of system resources, enable containerization and management of system services.

Preventing Resource Exhaustion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The primary security benefit of cgroups is their ability to prevent any single process or service
from monopolizing system resources. A buggy application with a memory leak or a compromised service
attempting a denial-of-service attack cannot consume all available memory or CPU time if a cgroup
constrains it. This containment ensures that the rogue process will be terminated or throttled 
before it can crash the entire system, preserving the availability of other essential services.

Foundations of Containerization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Cgroups are the bedrock of container technologies like Docker and LXD. They provide the resource
isolation that makes containers viable. By placing each container into its own cgroup, the system
can guarantee that one container cannot access more than its allocated share of CPU or memory,
reducing the impact it can have on other containers or the host system.

Service Management with ``systemd``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On modern Ubuntu systems, ``systemd`` makes extensive use of cgroups to manage all system services.
Every service started by ``systemd`` is automatically placed into its own dedicated cgroup. This
provides several benefits: 

- When a service is stopped, ``systemd`` can reliably terminate the main process of its children
  by killing all tasks within the service's cgroup.
- ``systemd`` can accurately track the resource consumption of each service. Tools like 
  ``systemd-cgtop`` provides a real-time view of CPU, memory, and I/O usage, broken down by service.
- Administrators can easily apply resource limits directly to a service using:

  .. code-block:: sh
 
    sudo systemctl set-property postgresql.service MemoryMax=512M
  
Beyond memory, administrators can control a wide variety of resources. Below is a list of some
common properties that can be configured for a service:
  
- **CPU**

  - ``CPUQuota``: Sets a hard cap on the percentage of CPU time a service can use.
  - ``CPUWeight``: Sets a relative weight for CPU time, influencing its priority during contention.
  - ``AllowedCPUs``: Restricts the service to run only on specific CPU cores.

- **Memory**
  
  - ``MemoryMax``: Sets a hard limit on the amount of memory a service can use.
  - ``MemoryLow``: Sets a protected memory threshold; memory below this limit is not reclaimed.
  - ``MemoryHigh``: Sets a memory usage threshold where the system will begin to throttle the service's processes.

- **I/O**

  - ``IOReadBandwidthMax``/``IOWriteBandwidthMax``: Limits the maximum read/write bandwidth to block devices.
  - ``IOReadIOPSMax``/``IOWriteIOPSMax``: Limits the maximum read/write I/O operations per second.

- **Tasks & Resources**

  - ``TasksMax``: Limits the maximum number of concurrent tasks (processes or threads) a service can have.
  - ``LimitNOFILE``: Sets the maximum number of file descriptors a service can have open. 
  
.. NOTE:: While ``sudo`` isn't necessary when modifying user services, it is required for ``set-property`` to work for other services. 
   For a complete list of directives and their detailed explanations, refer to the Ubuntu `systemd.resource-control(5) <https://manpages.ubuntu.com/manpages/bionic/man5/systemd.resource-control.5.html>`_ manual page.

Running Ad-Hoc Processes in Cgroups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Beyond managing long-running services, users can use systemd wrappers to run any command
or script within a temporary, resource-controlled cgroup. This is ideal for 
resource-intensive and short-lived tasks like software compilation or data processing.

The primary tool for this is ``systemd-run``. It creates a transient service or scope unit,
runs a command inside it, and removes the unit when the command finishes.

For example, imagine a scenario where a user needs to run a large software build but want
to prevent it from consuming all CPU and memory, ensuring the desktop remains responsive.
Users can use ``systemd-run`` to place the build process into the ``user.slice`` with specific 
limits:

.. code-block:: sh

  systemd-run --unit=my-heavy-build --slice=user.slice --property="CPUWeight=100" --property="MemoryMax=4G" make -j$(nproc)

This command does the following:

- ``--unit=my-heavy-build``: Assigns a descriptive name to the transient unit.
- ``--slice=user.slice``: Places the unit into the slice reserved for user sessions, separating it from system services.
- ``--property="..."``: Applies resource controls on the fly. Here, we give it a lower CPU priority (``CPUWeight=100``) and cap its memory usage at 4 GB (``MemoryMax=4G``).
- ``make...``: The actual command to be executed within this controlled environment.

While ``systemd-run`` is a good choice for temporary tasks, users can also create persistent,
custom slices. This is done by creating a ``.slice`` unit file in :file:`/etc/systemd/system/`. For 
instance, a user could create a ``background-jobs.slice`` to group and manage all non-interactive
batch processing. For details on creating these files, consult the Ubuntu 
`systemd.slice(5) <https://manpages.ubuntu.com/manpages/bionic/man5/systemd.slice.5.html>`_ manual page.


Inspecting Cgroups on Ubuntu
----------------------------

There are several ways to see which cgroup a process belongs to, from high-level tools to
direct kernel interfaces.

Using ``systemctl``
^^^^^^^^^^^^^^^^^^^
One method to see which cgroup a process belongs to is to use the ``systemctl status`` 
command, which works for a service name or a process ID (PID).

.. code-block:: sh

   # Check the status of the Apache HTTP Server service
   systemctl status <service-name/pid>

The output will include a line showing its cgroup path. As an example, this may be the output
when checking ``apache2.service``:

.. code-block:: none

  ● apache2.service - The Apache HTTP Server
       Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset: enabled)
       Active: active (running) since Fri 2025-08-08 07:10:33 EDT; 3min 2s ago
     Main PID: 2305 (apache2)
        Tasks: 3 (limit: 4571)
       Memory: 15.1M
          CPU: 42ms
       CGroup: /system.slice/apache2.service
               ├─2305 /usr/sbin/apache2 -k start
               ├─9352 /usr/sbin/apache2 -k start
               └─9353 /usr/sbin/apache2 -k start

Users can get the same information by providing one of the PIDs directly, for example, using
the above output: 

.. code-block:: sh
  
  systemctl status 2305

Using the Proc Filesystem
^^^^^^^^^^^^^^^^^^^^^^^^^
For a direct, low-level view, users can inspect the virtual file :file:`/proc/<pid>/cgroup`.
This file shows the process's path in every active cgroup hierarchy.

.. code-block:: sh

  # Inspect the cgroup membership for PID 2305
  cat /proc/2305/cgroup

This command might produce a more complex output:

.. code-block:: none

  11:pids:/system.slice/apache2.service
  10:hugetlb:/
  9:perf_event:/
  8:net_cls,net_prio:/
  7:cpuset:/
  6:memory:/system.slice/apache2.service
  5:cpu,cpuacct:/system.slice/apache2.service
  4:devices:/system.slice/apache2.service
  3:blkio:/system.slice/apache2.service
  2:freezer:/
  1:name=systemd:/system.slice/apache2.service
  0::/system.slice/apache2.service

Unified vs. Legacy Cgroups
^^^^^^^^^^^^^^^^^^^^^^^^^^
One may wonder why ``systemctl`` shows one clean cgroup path while 
:file:`/proc/<pid>/cgroup` shows many. The reason is the coexistence of two cgroups
versions.

Modern systems use a single, unified hierarchy where all controllers (``cpu``, ``memory``,
``pids``, etc.) reside. ``systemd`` uses this unified hierarchy for service management. The
``systemctl`` output and the line in procfs starting with ``0::`` both show the process's
path in this single, modern tree.

Meanwhile, some systems may also run multiple legacy hierarchies to maintain backward
compatibility; where different controllers get their own separate trees. The other
numbered lines in the :file:`/proc/<pid>/cgroup` output show the process's path in each
of these separate legacy trees.

In short, ``systemctl status`` gives users the relevant, modern view for service management,
while :file:`/proc/<pid>/cgroup` gives users an exhaustive report of the process's position in
every active hierarchy, both new and old.

Browse the Cgroup Filesystem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Users can explore the cgroup hierarchy as a regular filesystem. The cgroup path from ``systemctl``
maps directory to a directory under :file:`/sys/fs/cgroup`.

.. code-block:: sh

  # List the contents of the Apache service's cgroup directory
  ls /sys/fs/cgroup/system.slice/apache2.service/

This reveals the kernel control files for the cgroup:

.. code-block:: none

  cgroup.controllers      cgroup.procs            cpu.max.burst                    cpuset.mems            cpu.weight.nice  memory.events        memory.oom.group     memory.swap.high        pids.events
  cgroup.events           cgroup.stat             cpu.pressure                     cpuset.mems.effective  io.max           memory.events.local  memory.peak          memory.swap.max         pids.events.local
  cgroup.freeze           cgroup.subtree_control  cpuset.cpus                      cpu.stat               io.pressure      memory.high          memory.pressure      memory.swap.peak        pids.max
  cgroup.kill             cgroup.threads          cpuset.cpus.effective            cpu.stat.local         io.prio.class    memory.low           memory.reclaim       memory.zswap.current    pids.peak
  cgroup.max.depth        cgroup.type             cpuset.cpus.exclusive            cpu.uclamp.max         io.stat          memory.max           memory.stat          memory.zswap.max
  cgroup.max.descendants  cpu.idle                cpuset.cpus.exclusive.effective  cpu.uclamp.min         io.weight        memory.min           memory.swap.current  memory.zswap.writeback
  cgroup.pressure         cpu.max                 cpuset.cpus.partition            cpu.weight             memory.current   memory.numa_stat     memory.swap.events   pids.current

These files are the direct interface to the kernel for managing resources. For instance, the
``cgroup.procs`` file lists all PIDs in this group.

.. code-block:: sh

  cat /sys/fs/cgroup/system.slice/apache2.service/cgroup.procs

.. code-block:: none

  2305
  9352
  9353

The other files correspond to the resource limits discussed above. When a user runs 
``systemctl set-property apache2.service MemoryMax=512M``, ``systemd`` is simply writing 
"536870912" (512 MB in bytes) into the ``memory.max`` file in this directory. This filesystem
interface is the underlying mechanism that makes all cgroup-based management possible.
