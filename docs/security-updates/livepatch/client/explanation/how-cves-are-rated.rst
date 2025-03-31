How CVEs are rated
##################

We do not use an external rating system, but rate based on these
qualifications:

+----------------+-----------------------------------------------------+
| *negligible*   | Something that is technically a security problem,   |
|                | but is only theoretical in nature, requires a very  |
|                | special situation, has almost no install base, or   |
|                | does no real damage. These tend not to get backport |
|                | from upstreams, and will likely not be included in  |
|                | security updates unless there is an easy fix and    |
|                | some other issue causes an update.                  |
+----------------+-----------------------------------------------------+
| *low*          | Something that is a security problem, but is hard   |
|                | to exploit due to environment, requires a           |
|                | user-assisted attack, a small install base, or does |
|                | very little damage. These tend to be included in    |
|                | security updates only when higher priority issues   |
|                | require an update, or if many low priority issues   |
|                | have built up.                                      |
+----------------+-----------------------------------------------------+
| *medium*       | Something is a real security problem, and is        |
|                | exploitable for many people. Includes network       |
|                | daemon denial of service attacks, cross-site        |
|                | scripting, and gaining user privileges. Updates     |
|                | should be made soon for this priority of issue.     |
+----------------+-----------------------------------------------------+
| *high*         | A real problem, exploitable for many people in a    |
|                | default installation. Includes serious remote       |
|                | denial of services, local root privilege            |
|                | escalations, or data loss.                          |
+----------------+-----------------------------------------------------+
| *critical*     | A world-burning problem, exploitable for nearly all |
|                | people in a default installation of Ubuntu.         |
|                | Includes remote root privilege escalations, or      |
|                | massive data loss.                                  |
+----------------+-----------------------------------------------------+
