asemver API reference
=====================

The package name is called ``semver``. Every class, function, enum,
and exception shown below can be imported directly from ``semver``:

.. code-block:: py

   from semver import <something>

Where ``<something>`` is a class, function, enum, or exception listed below.

semver.constants module
-----------------------

.. automodule:: semver.constants
   :members: VPos, VRm
   :undoc-members:
   :show-inheritance:

semver.exc module
-----------------

.. automodule:: semver.exc
   :members:
   :undoc-members:
   :show-inheritance:

semver.operations module
------------------------

.. automodule:: semver.operations
   :members:
   :undoc-members:
   :show-inheritance:

semver.version module
---------------------

.. automodule:: semver.version
   :members: parse_version
   :undoc-members:
   :show-inheritance:

   .. autoclass:: semver.version.Version
      :members:
      :special-members: __add__, __sub__, __lt__, __eq__
      :undoc-members:
      :show-inheritance: