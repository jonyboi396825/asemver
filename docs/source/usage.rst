Usage
=====

There are different ways to use the asemver package. It includes
a ``Version`` class that can be used to make objects that represent
a semantic version, functions that work with strings that represent
semantic versions, and a CLI.

Version class
-------------

This usage guide will show how to use the common version object operations.

``+``, ``-`` operators
~~~~~~~~~~~~~~~~~~~~~~

To make a version class, use the ``parse_version()`` function:

.. code-block:: py

    from semver import parse_version
    version = parse_version("2.5.1-alpha.41+meta293")

    print(str(version))
    # '2.5.1-alpha.41+meta293'

    print(repr(version))
    # "Version(major=2, minor=5, patch=1, pre=Pre(string='alpha.41'), build=Build(string='meta293'))"

The main features of the ``Version`` class are the ``+`` and ``-`` operators.

The ``+`` operator *adds* to a ``Version`` object. For example, it can
`increment <https://semver.org/spec/v2.0.0.html#spec-item-6>`_ a certain
version position (major, minor, patch, rightmost dot-separated identifier
in the pre-release label if it is a number) or add a pre-release or build
label if they do not exist already.

.. code-block:: py

    from semver import parse_version, VPos

    version = parse_version("2.5.1")
    version + "-alpha.5"
    print(str(version))
    # '2.5.1-alpha.5'

    version = parse_version("2.5.1")
    version + "+build.129"
    print(str(version))
    # '2.5.1+build.129'

    version = parse_version("2.5.1")
    version + "+build.129" + "-alpha.5"
    print(str(version))
    # '2.5.1-alpha.5+build.129'

    version = parse_version("2.5.1-alpha.2")
    version + "-beta.56"  # error: pre-release label already exists

    version = parse_version("2.5.1+build.129")
    version + "+build.129"  # error: build label already exists

    version = parse_version("2.5.1-alpha.6+build.129")
    version + VPos.MAJOR
    print(str(version))
    # '3.0.0-alpha.6+build.129'

    version = parse_version("2.5.1-alpha.6+build.129")
    version + VPos.MINOR
    print(str(version))
    # '2.6.0-alpha.6+build.129'

    version = parse_version("2.5.1-alpha.6+build.129")
    version + VPos.PATCH
    print(str(version))
    # '2.5.2-alpha.6+build.129'

    version = parse_version("2.5.1-alpha.6+build.129")
    version + VPos.PRE
    print(str(version))
    # '2.5.1-alpha.7+build.129'

    version = parse_version("2.5.1")
    version + VPos.PRE  # error: no pre-release label

    version = parse_version("2.5.1-alpha")
    version + VPos.PRE  # error: no pre-release digit

The ``-`` operator *removes/subtracts* from a ``Version`` object. For example, it can
decrement a certain version position (major, minor, patch, rightmost dot-separated 
identifier in the pre-release label if it is a number) if it is non-zero or it can
remove a pre-release or build label if they exist.

.. code-block:: py

    from semver import parse_version, VPos, VRm

    version = parse_version("2.5.1-alpha.5")
    version - VRm.PRE
    print(str(version))
    # '2.5.1'

    version = parse_version("2.5.1+build.129")
    version - VRm.BUILD
    print(str(version))
    # '2.5.1'

    version = parse_version("2.5.1-alpha.5+build.129")
    version - VRm.PRE - VRm.BUILD
    print(str(version))
    # '2.5.1'

    version = parse_version("2.5.1")
    version - VRm.PRE  # error: pre-release label doesn't exist

    version = parse_version("2.5.1")
    version - VRm.BUILD  # error: build label doesn't exist

    version = parse_version("2.5.1-alpha.6+build.129")
    version - VPos.MAJOR
    print(str(version))
    # '1.5.1-alpha.6+build.129'

    version = parse_version("2.5.1-alpha.6+build.129")
    version - VPos.MINOR
    print(str(version))
    # '2.4.1-alpha.6+build.129'

    version = parse_version("2.5.1-alpha.6+build.129")
    version - VPos.PATCH
    print(str(version))
    # '2.5.0-alpha.6+build.129'

    version = parse_version("2.5.1-alpha.6+build.129")
    version - VPos.PRE
    print(str(version))
    # '2.5.1-alpha.5+build.129'

    version = parse_version("2.5.0-alpha.6+build.129")
    version - VPos.PATCH  # error: patch version is 0 so cannot decrement

    version = parse_version("2.5.1")
    version - VPos.PRE  # error: no pre-release label

    version = parse_version("2.5.1-alpha")
    version - VPos.PRE  # error: no pre-release digit

These operators can be chained together. Chains are evaluated from left to right.

.. code-block:: py

    from semver import parse_version, VPos, VRm
    version = parse_version("10.10.10")

    (
        version
        + VPos.MAJOR  # 11.0.0
        + VPos.MAJOR  # 12.0.0
        + VPos.MINOR  # 12.1.0
        + VPos.MAJOR  # 13.0.0
        + VPos.PATCH  # 13.0.1
        + VPos.PATCH  # 13.0.2
        + "+build1"  # 13.0.2+build1
        + "-pre.12"  # 13.0.2-pre.12+build1
        + VPos.MINOR  # 13.1.0-pre.12+build1
        - VPos.MAJOR  # 12.1.0-pre.12+build1
        + VPos.PATCH  # 12.1.1-pre.12+build1
        - VPos.PRE  # 12.1.1-pre.11+build1
    )

    print(str(version))
    # 12.1.1-pre.11+build1

    version - VRm.PRE - VRm.BUILD
    print(str(version))
    # 12.1.1

Comparison operators
~~~~~~~~~~~~~~~~~~~~

Comparisons are based on SemVer `spec item 11 <https://semver.org/#spec-item-11>`_.

Comparison operators (``>``, ``>=``, ``<``, ``<=``, ``!=``, ``==``) are supported
on all version objects. Note that build labels are ignored when comparing.

.. code-block:: py

    from semver import parse_version

    lhs = parse_version("0.2.0-pre.2+build12")
    rhs = parse_version("0.2.0-pre.2+build25")
    print(lhs == rhs)  # True
    print(lhs <= rhs)  # True
    print(lhs >= rhs)  # True
    print(lhs != rhs)  # False
    print(lhs < rhs)  # False
    print(lhs > rhs)  # False

    lhs = parse_version("0.4.0-pre.2+build12")
    rhs = parse_version("0.4.0")
    print(lhs == rhs)  # False
    print(lhs <= rhs)  # True
    print(lhs >= rhs)  # False
    print(lhs != rhs)  # True
    print(lhs < rhs)  # True
    print(lhs > rhs)  # False

    lhs = parse_version("5.3.1")
    rhs = parse_version("2.9.9")
    print(lhs == rhs)  # False
    print(lhs <= rhs)  # False
    print(lhs >= rhs)  # True
    print(lhs != rhs)  # True
    print(lhs < rhs)  # False
    print(lhs > rhs)  # True

More information
~~~~~~~~~~~~~~~~

More information on the ``Version`` class can be found in the
:doc:`API reference <../semver>`.

Special notes on functions
--------------------------

A list of functions and their functionalities can be found
in the :doc:`API Operations section <../semver>`. Included here are
special notes on functions.

1. ``add()`` is the same as using the ``+`` operator on a ``Version`` object. So

.. code-block:: py

    from semver import add, VPos

    version = add("2.5.2", "+build.5", VPos.PATCH, "-alpha.8", VPos.MAJOR, VPos.MINOR)
    print(version)
    # 3.1.0-alpha.8+build.5

is equivalent to

.. code-block:: py

    from semver import parse_version, VPos

    version = parse_version("2.5.2")
    version + "+build.5" + VPos.PATCH + "-alpha.8" + VPos.MAJOR + VPos.MINOR
    print(str(version))
    # 3.1.0-alpha.8+build.5

2. ``sub()`` is the same as using the ``-`` operator on a ``Version`` object. So

.. code-block:: py

    from semver import sub, VPos, VRm

    version = sub("3.6.2-alpha.53+build.5", VRm.PRE, VPos.MINOR, VPos.MAJOR, VRm.BUILD)
    print(version)
    # 2.5.2

is equivalent to

.. code-block:: py

    from semver import parse_version, VPos, VRm

    version = parse_version("3.6.2-alpha.8+build.5")
    version - VRm.PRE - VPos.MINOR - VPos.MAJOR - VRm.BUILD
    print(str(version))
    # 2.5.2

3. ``update()`` combines ``add()`` and ``sub()``. However, because both use the VPos
enum, when a VPos is passed into ``update()``, it uses the ``+`` operator (which bumps
the version number), instead of the ``-`` operator. So

.. code-block:: py

    from semver import update, VPos, VRm

    version = update("2.3.5", VPos.MAJOR, VPos.MINOR, "-alpha.43", "+build.23", VRm.PRE)
    print(version)
    # 3.1.0+build.23

is equivalent to

.. code-block:: py

    from semver import parse_version, VPos, VRm

    version = parse_version("2.3.5")
    version + VPos.MAJOR + VPos.MINOR + "-alpha.43" + "+build.23" - VRm.PRE
    print(str(version))
    # 3.1.0+build.23

CLI
---

Asemver offers a very simple CLI. Type ``asemver --help`` into the command line for help.

There are 4 subcommands:

* ``clean``: Type ``asemver - clean --help`` for help.
* ``compare``: Type ``asemver - compare --help`` for help.
* ``print``: Type ``asemver - print --help`` for help.
* ``valid``: Type ``asemver - valid --help`` for help.
