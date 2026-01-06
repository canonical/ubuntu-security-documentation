Customizing CIS Benchmarks profiles
###################################

Compliance with a benchmark isn't an all-or-nothing task. Each environment is
different, and options considered niche in one place might be essential in
another. Therefore, USG allows you to tailor the profile and remove unnecessary
rules, as well as customize rules that have multiple options available.


Setting variables
=================

1. Generate a tailoring file:

   .. code-block:: bash

      sudo usg generate-tailoring cis_level1_server tailor.xml

2. Edit the tailoring file and review the rules shown as comments. For example,
   to update the threshold on lockouts for failed password attempts:

   .. code-block:: xml

      <!--5.4.2 Ensure lockout for failed password attempts is configured (Automated)-->
      <set-value idref="xccdf_org.ssgproject.content_value_var_accounts_passwords_pam_faillock_deny">4</set-value>

3. Replace the value ``4`` with the number of your choosing and save the file.

4. Audit using the new tailoring file:

   .. code-block:: bash

      sudo usg audit --tailoring-file tailor.xml

5. Fix using the new tailoring file:

   .. code-block:: bash

      sudo usg fix --tailoring-file tailor.xml


Disable rules
=============

You can also disable certain rules. For example, if you are in an environment
where you require the ``jffs2`` filesystem, but you also need to comply with
the CIS level 1 for server (which prohibits it).

1. Generate a tailoring file:

   .. code-block:: bash

      sudo usg generate-tailoring cis_level1_server tailor.xml

2. Edit the tailoring file and find ``jffs2``.

   .. code-block:: xml

      <!-- 1.1.1.3 Ensure mounting of jffs2 filesystems is disabled (Automated) -->
      <xccdf:select idref="kernel_module_jffs2_disabled" selected="true"/>

   Replace ``selected="true"`` with ``selected="false"`` to stop enforcing the
   disablement of this filesystem.

3. Audit using the new tailoring file:

   .. code-block:: bash

      sudo usg audit --tailoring-file tailor.xml

4. Fix using the new tailoring file:

   .. code-block:: bash

      sudo usg fix --tailoring-file tailor.xml
