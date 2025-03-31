Resource requirements
#####################

The resource requirements for machines running livepatch on-prem
components (postgresql, haproxy, livepatch) depend on the amount of
machines being serviced by the deployment.

Minimal requirements are:

========== ====== ==== ====
Service    Memory CPUs Disk
========== ====== ==== ====
postgresql 4GB    1    50GB
haproxy    2GB    1    50GB
livepatch  2GB    1    50GB
========== ====== ==== ====

If postgresql is going to be used as the patchstore, we recommend
increasing disk allocated to posgresql to 100GB.

The bundle needs to be deployed on machines running Ubuntu focal.
