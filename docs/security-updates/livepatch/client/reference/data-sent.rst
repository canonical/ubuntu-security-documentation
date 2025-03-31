Data sent
#########

Livepatch client instances ping servers hosted by Canonical at a
configurable schedule (every hour by default) to check for the
availability of new patches. These requests contain the following
information:

-  system architecture
-  CPU model
-  kernel version
-  boot time and uptime
-  unique machine identifier, based on ``/etc/machine-id``
-  version of the currently applied livepatch (if any)
-  current state of the system (whether a livepatch has been applied or
   not)
-  time of the last server request
-  version of the client
