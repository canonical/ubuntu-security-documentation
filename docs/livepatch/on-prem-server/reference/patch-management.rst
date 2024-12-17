Patch management
################

Livepatch patches are managed using tiers. Tiers are basically
containers that patches are put into. Each Livepatch client instance is
associated with a specific tier (via the token). After deployment the
server comes with a default tier list: edge, beta, candidate and stable.
This list can be modified using the Livepatch administration tool.

.. figure:: upload://a5BXTUhxJVYx45D4Bb4Av7VtVW3.png
   :alt: image2|624x428

   image2|624x428

The tiers form an ordered list. When the on-prem server pulls in patches
from Canonical’s servers, these patches are initially assigned to the
first tier in the list. The order of tiers in the output of the
Livepatch admin tool command is in the order of patch promotion. In this
example the ``edge`` tier is the initial tier patches will be assigned
to:

::

   livepatch-admin tier list

… should produce output like this:

::

   Tiers:
   - Name: edge
   - Name: updates
   - Name: stable
   - Name: <on-prem>

If no further validation of patches is necessary, all Livepatch client
instances can be associated with that tier and the patches will become
available to them as soon as they have been downloaded.

.. figure:: upload://z7xA042h7EvRf7fRFNqLGiGi9Mw.png
   :alt: image4|623x263

   image4|623x263

If, however, validation or a staggered rollout of patches is required,
the patch tiers can be used to implement that. In such a scenario, a
small portion of testing machines can be associated with the beta tier
and patches can be promoted to higher tiers once they have been
validated.

.. figure:: upload://hJiubhhVct8K28ljnzbxYhdyjza.png
   :alt: image3|624x526

   image3|624x526

To promote a patch to a different tier, use the command:

::

   livepatch-admin patch promote <patch-version> <tier>

The patch version here is the numerical patch version (e.g. 57.1).

Promoting all patches in a tier
-------------------------------

To promote all patches in one tier to another, there is a shortcut
command ``promote-all``:

::

   livepatch-admin patch promote-all <from-tier> <to-tier>

This tool is useful during the initial setup of **Livepatch on-prem**,
when all patches are imported into the edge tier and other tiers are
empty. By running:

.. code:: text

   livepatch-admin patch promote-all edge stable

…you can make the contents of all the tiers from edge to stable
identical.
