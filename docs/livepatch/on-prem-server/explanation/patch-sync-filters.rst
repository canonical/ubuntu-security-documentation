Patch sync filters
##################

Livepatch on-prem enables users to synchronise with the hosted server,
and this synchronisation process is configurable.

The primary synchronisation filters are: - System architecture for
limiting patches via architecture. - Flavours for limiting the kernel
flavour. - Minimum kernel version, only allowing versions greater than
the minimum to be sychronised.

Set sync filters if you want to reduce the amount of space consumed by
Livepatch files and/or you know your client machines will be limited to
a certain set of kernel variants.

A full list of the available sync filters can be found in our
`config </t/configuration/48791#patch-sync>`__.
