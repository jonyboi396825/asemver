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
   
   $ pip install git+https://github.com/jonyboi396825/asemver


The dependencies are:

* Setuptools: For package installing into virtualenv or into user/root
* Wheel: For working with Python wheels (ZIPs of packages)
* Click: For the CLI

The source code can be found `here <https://github.com/jonyboi396825/asemver>`_.

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   semver
