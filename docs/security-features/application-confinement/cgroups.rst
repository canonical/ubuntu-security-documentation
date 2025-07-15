cgroups (Control Groups)
========================

Control Groups, commonly known as cgroups, are a powerful Linux kernel feature that allows for
the management and partitioning of system resources. At their core, cgroups enable a user to 
allocate, prioritize, and limit the usage of hardware resources (such as CPU, memory, disk I/O,
and network bandwidth) for a collection of processes. This capability is fundamental to the 
stability and security of a modern Ubuntu system, providing the foundation for technologies like
``systemd`` and containerization.


Core Concepts of cgroups
------------------------

cgroups operate on a few key principles: 

Hierarchy
^^^^^^^^^

cgroups are organized in a tree-like hierarchy, similar to a filesystem. This structure allows
for fine-grained control, where resource limits set on a parent ``cgroup`` can be inherited by its
children.

Controllers (Subsystems)
^^^^^^^^^^^^^^^^^^^^^^^^
Each hiearchy is associated with one or more "controllers", which represent a specific type of
system resource. Key controllers include: 

- ``cpu``: Manages access to the CPU. It can be used to CPU shares (relative priority) or enforce a hard cap on CPU usage.
- ``memory``: Controls memory usage, allowing a user to set limits on how much memory a group of processes can consume and what happens when that limit is reached.
- ``blkio``: Manages block I/O, controlling read/write access to block devices like hard drives and SSDs.
- ``pids``: Limits the number of processes that can be created within a cgroup, providing a crucial defence against "fork bomb" attacks.
- ``network_cls``/``network_prio``: Used to tag network packets from processes within a cgroup, allowing for traffic shaping and prioritization.

More information about controllers can be found `here <https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html>`_.


The Role of cgroups in System Stability and Security
----------------------------------------------------

While often seen as a resource management tool, cgroups are a critical component of system
security and stability.

Preventing Resource Exhaustion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The primary security benefit of cgroups is their ability to prevent any single process or service
from monopolizing system resources. A buggy application with a memory leak or a compromised service
attempting a denial-of-service attack cannot consume all available memory or CPU time if it is
constrained by a cgroup. This containment ensures that the rogue process will be terminated or
throttled before it can crash the entire system, preserving the availability of other essential
services.

Foundations of Containerization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
cgroups are the bedrock of container technologies like Docker, LXD, and Snap. They provide the
resource isolation that makes containers viable. By placing each container into its own cgroup,
the system can guarantee that one container cannot access more than its allocated share of CPU
or memory, effectively preventing it from interfering with other containers or the host system
itself.

Service Management with ``systemd``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On modern Ubuntu systems, ``systemd`` makes extensive use of cgroups to manage all system services.
Every service started by ``systemd`` is automatically placed into its own dedicated cgroup. This
provides several benefits: 

- When a service is stopped, ``systemd`` can reliably terminate the main process of its children
  by killing all tasks within the service's cgroup.
- ``systemd`` can accurately track the resource consumption of each service. Tools like 
  ``systemd-cgtop`` provide a real-time view of CPU, memory, and I/O usage, broken down by service.
- Administrators can easily apply resource limits directly to a service using:

  .. code-block:: sh
 
    sudo systemctl set-property <target-service> <property>

  For example, an admin can limit the memory available to a database server
  to prevent it from impacting the rest of the system under heavy load.



Inspecting cgroups on Ubuntu
----------------------------

Any interested user can directly explore their cgroup hierarchy, which is mounted as a virtual
filesystem at :file:`/sys/fs/cgroup`. To see the cgroup a specific service belongs to, a
``systemctl`` call can be executed:

.. code-block:: sh

   # Check the status of the Apache HTTP Server service
   systemctl status apache2.service

The output will include a line showing its cgroup path:

.. code-block:: sh

   /system.slice/apache2.service
   ├─2305 /usr/sbin/apache2 -k start
   ├─9352 /usr/sbin/apache2 -k start
   └─9353 /usr/sbin/apache2 -k start

The above demonstrates that the Apache HTTP Server daemon is running within its own slice of
system resources, managed by ``systemd`` and enforced by the kernel's cgroup controllers.
