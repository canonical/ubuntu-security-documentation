Ubuntu security
===============

..  grid:: 1 1 2 2

   ..  grid-item:: **Prevent and mitigate security risks**

      :doc:`Expanded Security Maintenance <docs/esm/index>` proivdes security maintenance for the entire collection of software packages shipped with Ubuntu.

      :doc:`Livepatch <docs/livepatch/index>` shrinks the exploit window for critical and high severity Linux kernel vulnerabilities, by patching the 
      Linux kernel between security maintenance windows, while the system runs. 
 
   ..  grid-item:: **Harden your Ubuntu system**

      :doc:`AppArmor <docs/apparmor/index>` is a Linux Security Module implementation that restricts applications’ capabilities and permissions with profiles that are set per-program. 

      :doc:`Secure boot <docs/secureboot/index>` is a verification mechanism for ensuring that code launched by firmware is trusted. 

      :doc:`Firewall <docs/firewall/index>` allows you to monitorr and control network traffic based on configurable security rules.

      :doc:`Disk encryption <docs/encryption/index>` is a method of protecting data by converting it into code that cannot be deciphered easily by unauthorized people or processes.

.. grid:: 1 1 2 2
   :reverse:

   .. grid-item:: **Comply with security standards**

      :doc:`USG <docs/compliance/usg>` is a tool for hardening and auditing Ubuntu system for compliance with different security standards.

      :doc:`CIS benchmarks<docs/compliance/usg/cis>` 

      :doc:`DISA Strig <docs/compliance/usg/disa>`

      :doc:`FIPS <docs/compliance/fips>`

     

   .. grid-item:: **Manage security**

      :doc:`Ubuntu OVAL data <docs/oval/index>` is a structured, machine-readable dataset that can be used to evaluate and manage security risks related to any existing Ubuntu components.

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


  