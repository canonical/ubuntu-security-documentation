Scale out
##########

There are several possible scenarios where scaling out a livepatch
deployment could be necessary:

1. High traffic due to large amount of machines being serviced
2. High availability setups

The livepatch on-prem deployment consists of 3 main components: the
``haproxy`` reverse-proxying requests, ``postgresql`` storing livepatch
data and ``livepatch server`` itself. Any one (or all) of these
components can be scaled out with additional units by running the
``juju`` command with the following syntax:

::

   juju add-unit <component> -n <number of units>

Where ``<component>`` is ``haproxy``, ``postgresql`` or ``livepatch``
and ``<number of units>`` is the number of additional units required.

.. figure:: upload://ydBPKHEv0bSYdpJZHTy8pjUDGps.png
   :alt: image5|622x350

   image5|622x350

Scaling out haproxy
-------------------

To deploy more than one ingress haproxy unit, run the following juju
command:

::

   $ juju add-unit haproxy -n 1

If more than one haproxy unit is being used, the DNS entry pointing to
the livepatch server should contain links to all the haproxy units.

Scaling out postgresql
----------------------

Scaling out postgresql will deploy additional follower units that can
take over in case the leader fails.

To deploy additional postgresql units, run the following juju command:

::

   $ juju add-unit postgrseql -n 1

Scaling out livepatch
---------------------

Deploying additional livepatch units will let them share the load of
handling machine requests. The filesystem patch storage type is not
compatible with a scaled out livepatch setup.

To deploy additional livepatch units, run the following juju commands:

::

   $ juju add-unit livepatch -n 1

Get new resource tokens
-----------------------

Once the units have been added, an additional command will have to be
run for each of the new units:

::

   juju run-action livepatch/{i} get-resource-token

Replace ``{i}`` with the number of each new livepatch unit in the
``juju status`` output.
