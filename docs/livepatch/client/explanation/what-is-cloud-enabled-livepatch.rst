What is cloud-enabled Livepatch
###############################

Private and public clouds, like *AWS*, *Azure*, or *GCP*, allow their
users to deploy their high-availability (HA) workloads onto different
*Regions* and *Availability Zones* (AZs) so that unexpected downtimes or
physical outages in a data centre do not compromise their HA setups.

Designed as a safety mechanism for cloud users, Cloud-Enabled Livepatch
is a feature to ensure that the patches are delivered to different
regions or AZs based on a predefined schedule. In line with best
practices around phased rollouts of updates, Cloud-Enabled Livepatch
aims to minimise the risk of unexpected outages/transients due to
wide-scale updates.

The schedule of delays, maintained by the Canonical Livepatch team, is
carefully tailored to the needs of public cloud providers and their
priorities over various regions/AZs. However, Cloud-Enabled Livepatch is
not limited to public clouds. Private cloud owners who have deployed
Livepatch On-prem to manage their fleet, can also enable this feature
and configure it based on their own preferences.

The Cloud-Enabled Livepatch feature is enabled by default, and the users
do not need further configuration. Normally, the Livepatch client
extracts the host machine’s region/AZ information from the *cloud-init*
configuration file, if any. However, based on their specific
requirements, users have the option to override these settings, for
which they can check `this </t/39164>`__ document for detailed
instructions.

As an example, let us say an AWS user has deployed their workloads on
two different AZs; *us-east-1a* and *eu-central-1a*. When a new patch is
released, it will be first applied on the machines on one of the AZs,
*us-east-1a* for example, and then after a delay of several hours, on
the other AZ’s machines, *eu-central-1a*, will get the patch. However,
this is just an example and the priority of AZs could be different in
practice. The Livepatch team closely monitors the health status of the
client machines, if there is an issue applying the patch during the
initial rollout, the new patch will be blocklisted until the issue is
resolved and other AZs will be kept safe from the same issue.
