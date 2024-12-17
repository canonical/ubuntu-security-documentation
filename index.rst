Ubuntu security
===============

..  grid:: 1 1 2 2

   ..  grid-item:: **Prevent and mitigate security risks**

      :doc:`Expanded Security Maintenance <docs/esm/index>` - security maintenance for the entire collection of software packages shipped with Ubuntu.

      :doc:`Livepatch <docs/livepatch/index>` - livepatch shrinks the exploit window for critical and high severity Linux kernel vulnerabilities, by patching the 
      Linux kernel between security maintenance windows, while the system runs. 
 
   ..  grid-item:: **Harden your Ubuntu system**

      :doc:`AppArmor <docs/apparmor/index>` 

      :doc:`Secure boot <docs/secureboot/index>` 

      :doc:`Firewall management <docs/firewall/index>` 

      :doc:`Disk encryption <docs/encryption/index>` 

.. grid:: 1 1 2 2
   :reverse:

   .. grid-item:: **Comply with security standards**

      :doc:`USG <docs/compliance/usg>`

      :doc:`CIS <docs/compliance/usg/cis>`

      :doc:`DISA Strig <docs/compliance/usg/disa>`

      :doc:`FIPS <docs/compliance/fips>`

     

   .. grid-item:: **Manage security**

      :doc:`OVAL <docs/oval/index>` - use Ubuntu OVAL to evaluate and manage security risks related to any existing Ubuntu components

---------


.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Prevent and Mitigate

   docs/esm/index   
   docs/livepatch/index
   

.. toctree::
   :hidden: 
   :maxdepth: 1
   :caption: Automate / Harden

   docs/apparmor/index
   docs/secureboot/index
   docs/firewall/index
   docs/encryption/index


.. toctree::
   :hidden: 
   :maxdepth: 1
   :caption: Manage

   docs/oval/index

.. toctree::
   :hidden: 
   :maxdepth: 1
   :caption: Compliance automation

   docs/compliance/usg
   docs/compliance/fips


  