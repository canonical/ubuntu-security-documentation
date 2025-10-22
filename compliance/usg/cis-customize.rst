Customizing CIS profiles
########################

Compliance with a benchmark is not an all-or-nothing task. Each environment is different and options that are considered as niche in one place can be essential in another. As such, USG allows to tailor the profile and remove unnecessary rules, as well as customize the rules that have multiple options available.

Setting variables
=================

1. Generate a tailoring file

.. code-block:: bash

    $ sudo usg generate-tailoring cis_level1_server tailor.xml

2. Edit the tailoring file and go through the rules shown as comments. For example to update the threshold on lockouts for failed password attempts:

.. code-block:: 

    <!--5.4.2 Ensure lockout for failed password attempts is configured (Automated)-->
        <set-value idref="xccdf_org.ssgproject.content_value_var_accounts_passwords_pam_faillock_deny">4</set-value>

3. Replace the value ``4`` with the number of your choosing and save the file.

4. Audit using the new tailoring file

.. code-block:: bash

    usg audit --tailoring-file tailor.xml

5. Fix using the new tailoring file
    
.. code-block:: bash    
    
    usg fix --tailoring-file tailor.xml

Disabling / Removing rules
==========================

Let’s also examine how we can disable certain rules from applying. Let’s say that we are in an environment where we require the jffs2 filesystem, but we also need to comply with the CIS level 1 for server that prohibits it.

1. Generate a tailoring file:


.. code-block:: bash

    $ sudo usg generate-tailoring cis_level1_server tailor.xml

2. Edit the tailoring file and go through the rules shown as comments. Let try to find ``jffs2`` in that file.

.. code-block:: 
    
    <!-- 1.1.1.3 Ensure mounting of jffs2 filesystems is disabled (Automated) -->
    <xccdf:select idref="kernel_module_jffs2_disabled" selected="true"/>

By replacing the ``selected=true`` with ``selected=false`` we no longer enforce the disablement of this filesystem.

3. Audit using the new tailoring file:

.. code-block:: bash

    usg audit --tailoring-file tailor.xml

4. Fix using the new tailoring file:
    
.. code-block:: bash
    
    usg fix --tailoring-file tailor.xml
