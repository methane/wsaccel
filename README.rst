WSAccell
=========

WSAccell is accelerator for `AutobahnPython <http://autobahn.ws/python>`_
and `ws4py <https://github.com/Lawouach/WebSocket-for-Python>`_
WSAccell replaces per-byte process in them with Cython version.

.. code-block:: python

    import wsaccell
    wsaccell.patch_autobahn()  # patch for autobahn.
    wsaccell.patch_ws4py()     # patch for ws4py.
