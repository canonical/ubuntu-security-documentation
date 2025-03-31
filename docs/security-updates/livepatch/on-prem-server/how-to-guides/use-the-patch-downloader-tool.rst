Use the patch downloader tool
#############################

The Canonical Livepatch downloader tool is a CLI application that
provides basic commands to query and download patch files.

Please note that this tool is not a replacement for the `Canonical
Livepatch client <https://snapcraft.io/canonical-livepatch>`__. Instead
it provides some basic patch download and query functionality which may
be particularly desirable in the following scenarios: - If the Livepatch
client cannot be used and patches must be inserted manually. - To
downloaded patches before transferring them into an airgapped on-premise
deployment of the Livepatch Server.

Using the Canonical Livepatch Downloader
----------------------------------------

Setup the Downloader
~~~~~~~~~~~~~~~~~~~~

Install the snap with

::

   sudo snap install canonical-livepatch-downloader

Enable the tool by running the following command with an Ubuntu Pro
token obtained from the `Ubuntu Pro
dashboard <https://ubuntu.com/pro/dashboard>`__, note that the token
must be entitled to Livepatch.

::

   canonical-livepatch-downloader enable <token>

Downloading single patches
~~~~~~~~~~~~~~~~~~~~~~~~~~

For this section we will list and download patches for a specific kernel
release. Using the host system’s kernel and assuming an ``amd64``
architecture.

::

   KERNEL_VERSION=$(cat /proc/version_signature  | cut -d ' ' -f 2)
   canonical-livepatch-downloader list --kernel=$KERNEL_VERSION --architecture=amd64

A sample output for a specific kernel version is provided below:

::

   $ canonical-livepatch-downloader list --kernel=5.15.0-107.117-generic --architecture=amd64
   - filename: livepatch-5.15.0-107.117-generic-107.1-amd64.tar.bz2
     hash: 696070a5dfb927bc9dcec809f7ba81c059e981a02829b44253e8ecf84d829fb5
   - filename: livepatch-5.15.0-107.117-generic-106.1-amd64.tar.bz2
     hash: 2b061466b553ca8805e7f278405031bf7607e088525dee5d21e19de513253df6
   - filename: livepatch-5.15.0-107.117-generic-105.1-amd64.tar.bz2
     hash: a73e702c795d1670066ac7209912434ae02006dc97a81b2b4bbdfebfbd15b7db
   - filename: livepatch-5.15.0-107.117-generic-104.1-amd64.tar.bz2
     hash: a603d9c7448d874625a95a2c06cbf554d3184868e803fb98b310a5722e9f359b

Next we will download the latest patch for your kernel.

::

   canonical-livepatch-downloader get-latest --kernel=$KERNEL_VERSION --architecture=amd64

An example output is provided below

::

   $ canonical-livepatch-downloader get-latest --kernel=5.15.0-107.117-generic --architecture=amd64
   Downloading patch 1/1
   Patch livepatch-5.15.0-107.117-generic-107.1-amd64 downloaded and extracted to /home/demo/snap/canonical-livepatch-downloader/common/patches/livepatch-5.15.0-107.117-generic-107.1-amd64

Note that the path the patch was downloaded to is shown. Unfortunately
the downloaded file path cannot currently be changed due to `snap
confinement <https://snapcraft.io/docs/snap-confinement>`__.

If a specific patch from the list is desired instead of the latest, use
the ``get-files`` command as follows.

::

   canonical-livepatch-downloader get-files livepatch-5.15.0-107.117-generic-105.1-amd64.tar.bz2

Syncing groups of patches
~~~~~~~~~~~~~~~~~~~~~~~~~

Syncing a group of patches is useful when you want to manually transfer
patches from into an airgapped environment.

To sync a group of patches we will utilise the ``list`` and
``get-files`` commands. Note that, again, because of snap confinement we
must place the output of the ``list`` command in a location that the
snap can access.

The list command provides filtering based on the following parameters: -
Architecture: Specify a fixed architecture string, e.g. “amd64” or
“s390x” - Flavour: Specify a kernel flavour, e.g. “generic”,
“lowlatency”, etc. - Kernel: A prefix match on kernel versions. E.g. 6.2
will match kernel versions 6.2.\* - Tier: Specify the tier from which to
download patches, defaults to “Proposed”. See
`here </client/explanation/what-are-livepatch-tiers>`__ for more info on
tiers.

The same flag cannot be passed multiple times. If multiple kernel
versions, flavours or architectures are desired, run the following
commands with each combination.

Assuming that we want to sync all patches for architecture ``amd64``,
kernel ``4.4.0-1100`` and flavour ``aws``:

::

   canonical-livepatch-downloader list --architecture=amd64 --flavour=aws --kernel=4.4.0-1100  > ~/snap/canonical-livepatch-downloader/common/patch-list.txt
   canonical-livepatch-downloader get-files -i ~/snap/canonical-livepatch-downloader/common/patch-list.txt

The output will indicate the download progress and specify the final
download location

::

   24/24 patches downloaded successfully.
   Patches downloaded and extracted to /home/demo/snap/canonical-livepatch-downloader/common/patches

Removing downloaded patches
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because patches are downloaded to
``~/canonical-livepatch-downloader/common/patches`` to remove all
downloads simply run

::

   rm -r ~/snap/canonical-livepatch-downloader/common/patches/*

Removing the Downloader
~~~~~~~~~~~~~~~~~~~~~~~

When removing the tool, Snap
`snapshots <https://snapcraft.io/docs/snapshots>`__ may result in the
removal taking a long time because a backup of the downloaded patches
are being made. To avoid this, uninstall the tool with the following
command to skip the creation of a snapshot.

::

   sudo snap remove canonical-livepatch-downloader --purge
