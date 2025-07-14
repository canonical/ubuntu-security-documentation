Direct downloading of .debs
###########################

A :file:`.deb` file, also known as a Debian package, is an archive that contains all
of the necessary files and information needed to install and run a piece of 
software. Ubuntu provides support for :file:`.deb` files, alongside snaps, Flatpaks,
and AppImages.

While :file:`.deb` files offer a convenient method to package and distribute software,
this ease of distribution inherently comes with risks. As an example, consider a
scenario where a user has provided a direct download link for a :file:`.deb` 
file on a public forum. Downloading and installing this file from such a source
is **discouraged** for several reasons.

Lack of verification
====================

Unlike software sourced from Ubuntu's official repositories (e.g., the Ubuntu
Archive), which includes packages vetted by the Ubuntu Security team, a :file:`.deb`
file originating from an untrusted source, like a public forum, has likely undergone
no security screening. This lack of verification means that bad actors may have
made modifications to the software contained within the :file:`.deb` file. 

When possible, always source :file:`.deb` files from trusted sources and not from 
untrusted sources like public forums.


Potential for malware
=====================

Installing a :file:`.deb` file to make software available system-wide almost always
requires ``root`` privileges. If a bad actor has modified a :file:`.deb` file for
malicious reasons, providing ``root`` privileges can elevate the risk that malware,
ransomware, spyware, or keyloggers are installed on your system. 

Whenever running a command with ``root`` privileges, always ensure you know what
the command is going to do, and that the inputs you are passing come from trusted
sources.


System instability and dependency issues
========================================

Software retrieved from trusted sources, such as the Ubuntu Archive, has been built
and tested to work seamlessly with other packages that may already be present on
a given system. In contrast, a :file:`.deb` file from an unknown or untrusted 
source might have been built for a different version of Ubuntu or have conflicting
dependencies. The installation of such a :file:`.deb` can cause system instability
due to these conflicts, which in the worst case can render a system unusable. 

To avoid dependency issues and to ensure system stability, it is always best to 
retrieve and install :file:`.deb` files from trusted sources, like Ubuntu's
official repositories.


No automatic security updates
=============================

Whenever installing software from Ubuntu's official repositories, that software will
automatically receive security patches and updates through the standard ``apt``
update process (contingent on the Ubuntu release being under active support, learn 
more `here <https://ubuntu.com/about/release-cycle>`_). If a standalone :file:`.deb`
is installed instead, this automatic security and update process is completely
bypassed. Updates need to be manually applied, potentially leaving a system 
vulnerable to exploitation.

To ensure you have the most secure version of software, it is highly recommended 
to source :file:`.deb` files from trusted sources that offer update paths through
the standard ``apt`` update process.
