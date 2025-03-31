
Using Ubuntu’s OVAL data
========================

Using OpenSCAP
---------------

1. Download the compressed XML:

.. code-block:: bash

    wget https://security-metadata.canonical.com/oval/com.ubuntu.$(lsb_release -cs).usn.oval.xml.bz2

2. Uncompress the data:

.. code-block:: bash
    
    bunzip2 com.ubuntu.$(lsb_release -cs).usn.oval.xml.bz2

3. Use OpenSCAP to evaluate the OVAL and generate an html report:

.. code-block:: bash
    
    oscap oval eval --report report.html com.ubuntu.$(lsb_release -cs).usn.oval.xml

4. The output is generated in the file report.html, open it using your browser:

.. code-block:: bash
    
    xdg-open report.html

5. File naming convention:

.. code-block:: bash
    
    com.ubuntu.<example release name>.usn.oval.xml.bz2

Scanning an Official Cloud Image
--------------------------------

To scan an Ubuntu Official Cloud Image for known vulnerabilities, the manifest file and xml data can be used together. Unlike above where we were able to use the lsb_release command, you will need to manually enter the URL for the OVAL data.

.. Note:: In the example below we are using focal/20.04, you would replace ‘focal’ with the version you are inspecting.

1. Download an Ubuntu image:

.. code-block:: bash
    
    wget https://security-metadata.canonical.com/oval/oci.com.ubuntu.focal.usn.oval.xml.bz2
    bunzip2 oci.com.ubuntu.focal.usn.oval.xml.bz2

2. Download the manifest file for the image

.. code-block:: bash
    
    wget -O manifest https://cloud-images.ubuntu.com/releases/focal/release/ubuntu-20.04-server-cloudimg-amd64-root.manifest

3. Use OpenSCAP to evaluate the OVAL and generate an html report

.. code-block:: bash
    
    oscap oval eval --report report.html oci.com.ubuntu.focal.usn.oval.xml

4. The output is generated in the file report.html, open it using your browser

.. code-block:: bash
    
    xdg-open report.html

5. File naming convention:

.. code-block:: bash
    
    oci.com.ubuntu.<example release name>.usn.oval.xml.bz2

