Customize DISA-STIG profiles
############################    

Not all rules can be applied without additional input from the operator. You can provide that input using a tailoring file, as demonstrated below. Furthermore, a tailoring file allows you to select the rules to comply or not comply against.

1. Generate a tailoring file:

.. code-block:: bash

    sudo usg generate-tailoring disa_stig tailor.xml

2. Edit the tailoring file and go through the rules shown as comments.

For example to set the remote auditd server (rule UBTU-20-010216), find the text:

.. code-block:: xml 

    <!-- UBTU-20-010216
    <xccdf:set-value idref="var_audispd_remote_server">logcollector</xccdf:set-value>

And replace the logcollector with the name of the server. To disable the rule, replace `selected=true` with `selected=false`.

3.  Audit using the new tailoring file:

.. code-block:: bash

    usg audit --tailoring-file tailor.xml

4. Fix using the new tailoring file:

.. code-block:: bash

    usg fix --tailoring-file tailor.xml