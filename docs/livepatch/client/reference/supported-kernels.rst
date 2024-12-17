Supported kernels
##################

+------+----+------+-----------------------------------------+-------+
| Ub   | Ar | Ke   | Kernel Variants                         | Up    |
| untu | ch | rnel |                                         | grade |
| rel  |    | Ver  |                                         | and   |
| ease |    | sion |                                         | Reb   |
|      |    |      |                                         | oot\* |
+======+====+======+=========================================+=======+
| Ub   | 64 | 6.8  | aws, azure, gcp, generic, gke, ibm,     | every |
| untu | -b | (GA) | lowlatency                              | 13    |
| 2    | it |      |                                         | m     |
| 4.04 | x  |      |                                         | onths |
| LTS  | 86 |      |                                         |       |
+------+----+------+-----------------------------------------+-------+
| Ub   | s  | 6.8  | generic                                 | every |
| untu | 39 | (GA) |                                         | 13    |
| 2    | 0x |      |                                         | m     |
| 4.04 |    |      |                                         | onths |
| LTS  |    |      |                                         |       |
+------+----+------+-----------------------------------------+-------+
| Ub   | 64 | 6.8  | aws, azure, gcp, generic, gke, ibm,     | every |
| untu | -b | (    | lowlatency                              | 13    |
| 2    | it | HWE) |                                         | m     |
| 2.04 | x  |      |                                         | onths |
| LTS  | 86 |      |                                         |       |
+------+----+------+-----------------------------------------+-------+
| Ub   | 64 | 5.15 | aws, azure, fips, gcp, generic, gke,    | every |
| untu | -b | (GA) | ibm, lowlatency, oracle                 | 13    |
| 2    | it |      |                                         | m     |
| 2.04 | x  |      |                                         | onths |
| LTS  | 86 |      |                                         |       |
+------+----+------+-----------------------------------------+-------+
| Ub   | s  | 5.15 | generic                                 | every |
| untu | 39 | (GA) |                                         | 13    |
| 2    | 0x |      |                                         | m     |
| 2.04 |    |      |                                         | onths |
| LTS  |    |      |                                         |       |
+------+----+------+-----------------------------------------+-------+
| Ub   | 64 | 5.15 | aws, azure, gcp, generic, gke, ibm,     | every |
| untu | -b | (    | lowlatency, oracle                      | 13    |
| 2    | it | HWE) |                                         | m     |
| 0.04 | x  |      |                                         | onths |
| LTS  | 86 |      |                                         |       |
+------+----+------+-----------------------------------------+-------+
| Ub   | 64 | 5.4  | aws, aws-fips, azure, azure-fips, fips, | every |
| untu | -b | (GA) | gcp, gcp-fips, generic, gke, gkeop,     | 13    |
| 2    | it |      | ibm, lowlatency, oem, oracle            | m     |
| 0.04 | x  |      |                                         | onths |
| LTS  | 86 |      |                                         |       |
+------+----+------+-----------------------------------------+-------+
| Ub   | 64 | 5.4  | aws, azure, gcp, generic, gke, gkeop,   | every |
| untu | -b | (    | ibm, lowlatency, oracle                 | 13    |
| 1    | it | HWE) |                                         | m     |
| 8.04 | x  |      |                                         | onths |
| LTS  | 86 |      |                                         |       |
+------+----+------+-----------------------------------------+-------+
| Ub   | 64 | 4.15 | aws, aws-fips, azure, azure-fips, fips, | every |
| untu | -b | (GA) | gcp, gcp-fips, generic, gke,            | 13    |
| 1    | it |      | lowlatency, oem, oracle                 | m     |
| 8.04 | x  |      |                                         | onths |
| LTS  | 86 |      |                                         |       |
+------+----+------+-----------------------------------------+-------+
| Ub   | 64 | 4.15 | azure, generic, lowlatency              | every |
| untu | -b | (    |                                         | 13    |
| 1    | it | HWE) |                                         | m     |
| 6.04 | x  |      |                                         | onths |
| LTS  | 86 |      |                                         |       |
+------+----+------+-----------------------------------------+-------+
| Ub   | 64 | 4.4  | aws, fips, generic, lowlatency          | every |
| untu | -b | (GA) |                                         | 13    |
| 1    | it |      |                                         | m     |
| 6.04 | x  |      |                                         | onths |
| LTS  | 86 |      |                                         |       |
+------+----+------+-----------------------------------------+-------+
| Ub   | 64 | 4.4  | generic, lowlatency                     | every |
| untu | -b | (    |                                         | 13    |
| 1    | it | HWE) |                                         | m     |
| 4.04 | x  |      |                                         | onths |
| LTS  | 86 |      |                                         |       |
+------+----+------+-----------------------------------------+-------+

\*\ **Upgrade and Reboot Interval:** Security patches are only created
for a kernel for 9-13 months from the release date of the kernel. We
recommend updating and restarting your machine within this period to
continue receiving Livepatch updates.

GA is the kernel a release launched with, while `HWE or Hardware
Enablement <https://ubuntu.com/about/release-cycle#ubuntu-kernel-release-cycle>`__
kernels are a set of newer kernel that become available in the current
LTS release as these newer kernels are released with subsequent Ubuntu
versions, up until the next LTS release.

There will be Livepatch support for HWE kernels across a limited
combination of kernel flavour (variants), kernel version, and Ubuntu
release as detailed above.

See `this
page <https://ubuntu.com/security/livepatch/docs/livepatch/explanation/client_not_working>`__
to better understand why your kernel might not be supported.
