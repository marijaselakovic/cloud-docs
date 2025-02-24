.. _edge-disclaimer:

Introduction
============

.. NOTE::

    You must have `wget`_ and `jq`_ installed for the script to function.
    CrateDB Edge is currently in Pre-Release. CrateDB Edge and related services
    are provided on an "as is" basis and may change at any time. Crate.io
    provides no guarantees or warranty regarding the usability or performance
    of CrateDB Edge. The CrateDB Cloud Service Level Agreement (SLA) is
    expressly disclaimed for the use of CrateDB Edge and related services until
    further notice. By using CrateDB Edge, you agree to these terms and
    conditions.

    Should you find any errors, bugs, or functionality problems while using the
    CrateDB Edge Pre-Release, please let us know using the `contact page`_ or
    `support email`_.

.. rubric:: Table of contents

.. contents::
   :local:
   
.. _edge-prereqs:

Prerequisites
-------------

Certain hardware and software specifications must be met in order to make use
of CrateDB Edge. The most important of these is that you must provide a working
Kubernetes cluster, one that meets the following requirements:

.. rst-class:: open

* It must contain at least three nodes (for high availability).
  You can also run development workloads on a single-node cluster. Note,
  however, that you will only be able to provision single-node CrateDB
  clusters;

* Sufficient CPU per node to run the CrateDB Cloud software stack as well as
  sufficient compute to run the CrateDB instances desired. We recommend the use
  of a K8s autoscaler. For reference, the CrateDB Edge stack - without Grafana
  or Loki - requires about 2 CPUs and 2500 Mi of memory. We recommend at least
  4 CPUs per node for reliable performance.

* A Kubernetes version 1.20, 1.21, or 1.22;

* A storage class for persisting your data (SSD recommended). As outlined in
  the installation script, CrateDB Edge expects the storage classes
  ``crate-premium`` (SSD) and ``crate-standard`` (SSD or Spindle). Also ensure
  that you are able to set the field ``allowVolumeExpansion`` to ``true``.

* Unless you are experienced with operating Kubernetes clusters, we recommend
  to start with a dedicated Kubernetes cluster for CrateDB Edge. If you use an
  existing Kubernetes setup, be aware that the following components will be
  set up during installation of CrateDB Edge, which may interfere with your
  existing configuration:

  * cert-manager (version 1.6.1)
  * ingress-nginx (version 1.2.3)
  * Optionally, Grafana, Loki, or Promtail (via Helm).

Beyond this, using the CrateDB Cloud stack requires creating a CrateDB Cloud
account and an organization, which will become the owner of the Edge region in
which the cluster can be deployed. One must also access the CrateDB Cloud
Console in order to deploy the cluster itself, using the provided script. These
steps will be explained below.

Some Kubernetes knowledge, especially regarding networking and storage, is
recommended when using CrateDB Edge, especially when using it as-is. If you're
uncertain, you may benefit from using CrateDB Edge in combination with
:ref:`cloud providers or third-party tools <edge-providers>` as described
further down in this tutorial.

.. NOTE::
    A special note about bare metal Kubernetes clusters: CrateDB Edge should
    work on any bare metal cluster, but the CrateDB instances running within
    require a load balancer for outside access. If you do not have a load
    balancer (for example `MetalLB`_), you can still access the CrateDB
    clusters within, but you will need to figure out the node ports to use.


.. _edge-signup:

Sign up
-------

To use the CrateDB Cloud software, you must first sign up. Follow the steps
outlined in :ref:`this tutorial <sign-up>` to do so.


.. _edge-create-org:

Create an organization
----------------------

When you first log in to the CrateDB Cloud Console after having created an
appropriate account, you will arrive at the Organization overview page. Here
you will be prompted to create an organization.

.. image:: ../../_assets/img/free-trial-organization.png
   :alt: Create an organization

Fill out the name of the organization and click the *Create organization*
button. After a short moment, the organization will be created and you can
proceed. After you create your first organization, you will be taken to the
Dashboard tab of said organization.


.. _edge-create-custom:

Create a custom region
----------------------

In the Regions tab, it is possible to create a custom region. You will want to
do this if you are hosting your cluster locally and are not relying on existing
cloud providers to host your database infrastructure.

The Regions tab shows an overview of regions hosted by cloud providers as well
as the option to create your own.

.. image:: ../../_assets/img/cloud-regions.png
   :alt: CrateDB Console regions screen

To create a custom region, simply fill out a name for the region and click on
the *Create edge region* button.

Once you have done so, it will show your custom region.

.. image:: ../../_assets/img/cloud-custom-region.png
   :alt: CrateDB Console custom region screen

A preconfigured script will appear in the custom region field that you have
just created. To proceed, open your local CLI and follow the steps in the next
section of the tutorial. (You may want to keep the CrateDB Cloud Console open
in your browser in the meantime.)


.. _edge-script:

Apply the script
----------------

You can use the copy function provided in the custom region field to copy the
script into your own CLI. Simply paste it there and execute the script. The
script will check whether your local setup conforms to the prerequisites listed
above. If one or more prerequisites fail, the script will notify you of this,
and you will have to install them to proceed. (We recommend `Helm`_ for
tracking and installing dependencies on Kubernetes.)

.. NOTE::
    You must have `wget`_ and `jq`_ installed for the script to function.


Manifest and verification
'''''''''''''''''''''''''

Once you satisfy the prerequisites, the script will ask for your confirmation
to install CrateDB Edge. Type Y or y to continue. The script will then
download the manifest files for the CrateDB Edge service and apply them.

In the final stage, the script will loop over the services and check their
availability. It continues doing this until all required services have become
available. Note that this may take some time, which depends among other things
on how fast a certificate can be issued.


Help and parameters
'''''''''''''''''''

Use the ``--help`` parameter to find an overview of the available parameters
for the script.

The parameters are defined as follows:

.. code-block:: console

    Usage:
    cratedb-cloud-edge.sh <token> [options]

    Here <token> represents the installation token provided on region creation,
    and the [options] are the optional parameters as shown below.

    Options:
      --base-url: The URL the manifest should be fetched from
      -d, --debug: Displays a lot of debug information
      --dry-run: Will not apply the downloaded manifest file. This can be used
      for checking the manifest file (edge-manifest.yaml) before applying it.
      -m, --max-execution-time (600): Maximum time in seconds the script should
      run
      --run-prerequisites: Will only run the prerequisites check
      --run-validation: Will only run the post-install validation

Once the services are up and running, the script will report: "Successfully
validated installation". At this point, you can return to the CrateDB Cloud
Console.

In the CrateDB Cloud Console you can now deploy a cluster from within your
custom Edge region. Go to the Regions tab of the Organization overview to find
your custom region and deploy your cluster from there. This will take you to
the cluster configuration screen.

.. _edge-upgrade:

Upgrade the Edge Region
-----------------------

Components of a deployed Edge Region are not updated automatically. Because of
this, users should update their Edge Regions regularly to continue getting new
features, bugfixes, and security updates.

If your region is outdated, you will see a *Upgrade this Edge region* button
next to your region:

.. image:: ../../_assets/img/edge-region-upgrade.png
   :alt: CrateDB Console regions screen

Clicking it will show you a command that updates your Edge Region. Paste the
command into the environment where your Edge cluster is deployed to 
upgrade it.

.. _edge-config:

Configure the cluster
---------------------


Configuration
'''''''''''''

Next, go through the cluster configuration process. You will see that a
cluster can now be deployed to your custom region. You can move directly to the
cluster configuration. Configure your desired hardware values for CPU,
RAM, storage, and number of nodes.

.. image:: ../../_assets/img/cloud-edge-config.png
   :alt: Cluster configuration panels for CrateDB Edge

On the right the cluster scale overview shows the total hardware values for
the cluster. This is simply the number of nodes you have chosen, multiplied by
the values per node you have defined.

You can also define the backup location of your CrateDB Edge cluster. You
have the option of either using the default backup location for CrateDB Cloud,
which is managed by us, or use a custom backup location that is convenient to
you. This has to be an S3 bucket or a location with an equivalent
functionality. In the latter case, you can set the access key and secret here
as well. Clicking the the Test Connection button will check whether a
connection to your backup location can be established. Keep in mind that you
cannot proceed with a custom backup location unless the connection is
functional.

That's it. As you're using your own equipment in this case, no need to provide
the billing details.

Finish up
---------

You will now be returned to the CrateDB Cloud Console, but this time to the
Cluster overview page. A popup menu will remind you of the username and
password you selected for connecting to the cluster. Make sure you copy this
information to a safe place (e.g., a password manager), as it will not be
retrievable past this point.

You can use the Cluster overview page to access your cluster via the Admin UI
(see, however, the note below).

.. NOTE::
    If your Kubernetes cluster does not provide a load balancer with an
    external IP address, you will not be able to access your cluster from the
    CrateDB Cloud Console.


.. _edge-cloud-region:

Use a cloud provider region
---------------------------

Aside from creating your own custom region, it is also possible to use CrateDB
Edge in combination with an existing cloud provider. To deploy a cluster in
this way, follow the initial steps described above until you 
have :ref:`created an organization <edge-create-org>`. Then, go to the Regions
tab and instead of creating a custom region, choose a cloud provider from the
fields provided and click *Deploy cluster*. You will be referred to the
subscription plan screen. Select your desired plan and proceed to 
the :ref:`configuration wizard <edge-config>` as described above.


.. _edge-delete-region:

Delete a custom region
----------------------

In order to delete a custom region, click the trashcan icon at the bottom
right of the custom region panel. A confirmation dialog will appear warning
that deletion of a custom region disables access to CrateDB Cloud for that
region.

Deleting a custom region does not delete the resources inside that region. To
also delete the resources inside the region, run the script provided in the
deletion confirmation screen in your local CLI before confirming the deletion
in the console. This will uninstall CrateDB Edge from your local Kubernetes
cluster.

To finalize the deletion of the custom region, enter the name of your region
into the form.

.. image:: ../../_assets/img/cloud-edge-delete.png
   :alt: CrateDB Edge deletion confirmation screen
   :scale: 50%


.. _Admin UI: https://crate.io/docs/crate/admin-ui/en/latest/console.html
.. _Helm: https://helm.sh/docs/intro/quickstart/
.. _jq: https://stedolan.github.io/jq/
.. _MetalLB: https://metallb.universe.tf/
.. _contact page: https://crate.io/contact/
.. _Stripe: https://stripe.com
.. _support email: support@crate.io
.. _wget: https://www.gnu.org/software/wget/