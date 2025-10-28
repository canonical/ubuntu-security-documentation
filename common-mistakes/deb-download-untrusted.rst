Downloading .debs from untrusted sources
########################################

While packages offer a convenient method to package and distribute software, 
this ease of distribution inherently comes with risks. As an example, 
consider a scenario where a user has provided a direct download link for a 
package on a public forum. Downloading and installing this package from such
a source is **discouraged** for several reasons.


Lack of security verification
=============================

Unlike software sourced from Ubuntu's official repositories (e.g., the Ubuntu
Archive), which includes packages vetted by the Ubuntu Security team, a package
file originating from an untrusted source, like a public forum, has likely 
undergone no security screening. This lack of verification means that bad 
actors may have made modifications to the software contained within the package. 

When possible, always source packages from trusted sources and not from untrusted
sources like public forums.


Potential for malware
=====================

Installing a package to make software available system-wide almost always requires
``root`` privileges. If a bad actor has modified a :file:`.deb` file for malicious
reasons, providing ``root`` privileges can elevate the risk that malware,
ransomware, spyware, or keyloggers are installed on your system. 

Whenever running a command with ``root`` privileges, always ensure you know what
the command is going to do, and that the inputs you are passing come from trusted
sources.


System instability and dependency issues
========================================

Software retrieved from trusted sources, such as the Ubuntu Archive, has been built
and tested to work seamlessly with other packages that may already be present on
a given system. In contrast, a package from an unknown or untrusted source might
have been built for a different version of Ubuntu or have conflicting dependencies.
The installation of such a :file:`.deb` can cause system instability due to these
conflicts, which in the worst case can render a system unusable. 

To avoid dependency issues and to ensure system stability, it is always best to 
retrieve and install packages from trusted sources, like Ubuntu's official 
repositories.
