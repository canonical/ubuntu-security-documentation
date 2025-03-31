Enable-client
#############

Livepatch is included in Ubuntu Pro (previously known as Ubuntu
Advantage). The recommended way to install it is using the Ubuntu Pro
client. The instructions below show how to enable livepatching and
install the client. Instructions can also be found in `this
tutorial <https://ubuntu.com/tutorials/enable-the-livepatch-service#1-overview>`__.

::

   # Attach your personal or enterprise subscription from ubuntu.com/pro
   $ sudo pro attach

   # Explicitly enable livepatch
   $ sudo pro enable livepatch

This will install the livepatch client, and enroll the system to the
Ubuntu livepatch service.
