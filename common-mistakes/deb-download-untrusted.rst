Downloading .debs from untrusted sources
########################################

Packages offer a convenient way to distribute software, but this ease of
distribution comes with risks. For example, a user might provide a direct
download link for a package on a public forum.

.. warning::
   **Security risk**

   We strongly discourage downloading and installing packages from untrusted
   sources. Doing so bypasses security protections and can lead to malware
   infections or system instability.


Lack of security verification
=============================

Unlike software from Ubuntu's official repositories (such as the Ubuntu
Archive), which includes packages vetted by the Ubuntu Security team, a package
file from an untrusted source likely hasn't undergone security screening. This
lack of verification means that attackers may have modified the software inside
the package.

When possible, always source packages from trusted sources rather than public
forums.


Potential for malware
=====================

Installing a package system-wide almost always requires ``root`` privileges. If
an attacker has modified a ``.deb`` file, granting ``root`` privileges
increases the risk of installing malware, ransomware, spyware, or keyloggers on
your system.

Whenever running a command with ``root`` privileges, always ensure you know
what the command is going to do and that the inputs come from trusted sources.


System instability and dependency issues
========================================

Software from trusted sources, such as the Ubuntu Archive, is built and tested
to work with other packages on your system. In contrast, a package from an
unknown or untrusted source might have been built for a different version of
Ubuntu or have conflicting dependencies.

Installing such a ``.deb`` can cause system instability due to these conflicts,
which in the worst case can render a system unusable.

To avoid dependency issues and ensure system stability, it's always best to
install packages from trusted sources, like Ubuntu's official repositories.
