# Ubuntu Security documentation
This repository contains in-depth technical documentation about platform-agnostic security features, their design, implementation, and security implications. The information here covers topics such as mechanisms for receiving security updates, privilege restrictions, cryptography, various features designed for protecting and hardening the system on different layers. It also includes information and technical guides about compliance automation available in Ubuntu.

Note that for practical guidance on working with your platform, you should consult platform-specific documentation such as [Ubuntu Server](https://documentation.ubuntu.com/server/) and [Ubuntu Core](https://documentation.ubuntu.com/core/).

## Community and support

This documentation is developed and maintained primarily by the [Ubuntu Security Team](https://launchpad.net/~ubuntu-security) 

To get in touch:

* email us security@ubuntu.com  
* join #ubuntu-security on the Libera Chat IRC
* join #security:ubuntu.com on Matrix

## Contribution guidelines

We welcome contributions! There are multiple ways you can help.

### Code of conduct

When contributing, you must abide by the [Ubuntu Code of Conduct].

### File a bug

If you notice any issues with documentation such as inconsistencies with formatting, typos, unclear or inaccurate language, do not hesitate to let us know and [file an issue](https://github.com/canonical/ubuntu-security-documentation/issues/new).

### Contribute directly to the documentation

You can contributes fixes and improvements yourself.

The project is written in [reStructuredText], built with [Sphinx], and hosted on Read the Docs. 

#### Configure your environment

You will need to have Python, `python3.12-venv`, and `make` packages.

```bash
sudo apt install make
sudo apt install python3
sudo apt install python3.12-venv
```

#### Build documentation locally

To build the documentation locally before submitting your changes, go to the root of the directory and run:

```bash
make run
```

The build will be served at http://127.0.0.1:8000

The build is dynamically updated, as you save, so you can make changes and monitor them live.

#### Submit a pull request

- **Title**: Summarize the change in a short, descriptive title.
- **Description**: Describe the purpose of your PR, the changes made and the reason(s). Include whether the change is minor (e.g. spelling/typos), major (e.g. adding steps, changing process) or structural (e.g. adding new sections, moving/reorganising structure). 

Every PR is automatically built so you and reviewers can preview the changes.

#### Wait for a review

A review is required from the Ubuntu Security team before your changes will be merged.

## License and copyright 

This work is licensed under the [Creative Commons Attribution-Share Alike 3.0 Unported License](http://creativecommons.org/licenses/by-sa/3.0/). 

<!-- LINKS --> 

[Ubuntu Code of Conduct]: https://ubuntu.com/community/ethos/code-of-conduct
[Sphinx]: https://canonical-starter-pack.readthedocs-hosted.com/latest/
[reStructuredText]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
