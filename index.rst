Ubuntu security
===============

..  grid:: 1 1 2 2

   ..  grid-item:: **Prevent and mitigate security risks**

      :doc:`Expanded Security Maintenance <esm/index>` - security maintenance for the entire collection of software packages shipped with Ubuntu.

      :doc:`Livepatch <livepatch/index>` - livepatch shrinks the exploit window for critical and high severity Linux kernel vulnerabilities, by patching the 
      Linux kernel between security maintenance windows, while the system runs. 
 
   ..  grid-item:: **Harden your Ubuntu system**

      :doc:`AppArmor <apparmor/index>` 

      :doc:`Secure boot <secureboot/index>` 

      :doc:`Firewall management <firewall/index>` 

      :doc:`Disk encryption <encryption/index>` 

.. grid:: 1 1 2 2
   :reverse:

   .. grid-item:: **Comply with security standards**

      :doc:`USG <compliance/usg>`

      :doc:`DISA Strig <compliance/disa-stig>`

      :doc:`FIPS <compliance/fips>`

      :doc:`Common Criteria <compliance/common-criteria>`

      :doc:`CIS <compliance/cis>`
     

   .. grid-item:: **Manage security**

      :doc:`OVAL <oval/index>` - use Ubuntu OVAL to evaluate and manage security risks related to any existing Ubuntu components

---------


.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Prevent and Mitigate

   esm/index   
   livepatch/index
   

.. toctree::
   :hidden: 
   :maxdepth: 1
   :caption: Automate / Harden

   apparmor/index
   secureboot/index
   firewall/index
   encryption/index


.. toctree::
   :hidden: 
   :maxdepth: 1
   :caption: Manage

   oval/index

.. toctree::
   :hidden: 
   :maxdepth: 1
   :caption: Comply

   compliance/usg
   compliance/fips

  