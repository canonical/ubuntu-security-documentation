FIPS
####

Ubuntu supports running Linux FIPS 140 workloads through the Ubuntu Pro 3 subscription. These documentation pages provide technical information and clarifications about Ubuntu’s FIPS certification. For a high level summary see our main page on Ubuntu for FIPS 17.
Our approach in certifications

By default, Ubuntu comes with cryptographic packages based on the upstream sources and is not configured to adhere to any national standard. The system can be switched to a state that adheres to the FIPS standard, that we call the FIPS mode. The process of enabling FIPS is described in this page.

Although there is a global system switch for FIPS, the FIPS 140 17 standard covers specific binary packages. In Ubuntu we select a set of cryptographic packages from the main repository that form our cryptographic core set. This set of packages, includes the Linux kernel and OpenSSL and is tested and validated periodically for the FIPS 140-2 requirements on each Ubuntu LTS release. The FIPS validated packages are installed during the FIPS enablement. The complete list of validated packages along with their certificates is at this page 3
Tutorials

Keeping up to date
===================

A mailing list is used to announce patches and news related to the FIPS packages and certifications. To request to join the mailing list, please send “join” in the email body to ubuntu-certs-announce-request@lists.canonical.com. Announcements will be sent to the email address ubuntu-certs-announce@lists.canonical.com from an ``@canonical.com`` email address.

.. toctree::
   :maxdepth: 2

   fips-tutorials/index
   fips-howtos/index
   fips-explanations/index
   fips-references/index