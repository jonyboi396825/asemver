Welcome to asemver's documentation!
===================================

Current release: |release|

This is an implementation of semantic versioning in Python. 
This will not be a standalone package on PyPI because there is 
already `another implementation <https://pypi.org/project/semver/>`_ 
of semantic versioning.

If anything, this package will only be used as a component of
a bigger project in a git submodule or installed using git.

The documentation is not going to be on readthedocs or GitHub
Pages and is only here for testing and clarity reasons.

Installation
------------

This package can be installed using pip and git:

.. code-block:: text
   
   $ pip install git+https://github.com/jonyboi396825/asemver@<version>

Replace ``<version>`` with |version| to install the latest stable version,
or with an earlier release number to install an earlier version.
See the `pip documentation <https://pip.pypa.io/en/stable/topics/vcs-support/>`_
for more info.

The dependencies are:

* Setuptools: For package installing into virtualenv or into user/root
* Wheel: For working with Python wheels (ZIPs of packages)
* Click: For the CLI

The source code can be found `here <https://github.com/jonyboi396825/asemver>`_.
The package can also be installed by cloning the source code or adding it
as a submodule.

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   semver
