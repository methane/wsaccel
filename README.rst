WSAccell
=========

WSAccell is WebSocket accelerator for `AutobahnPython <http://autobahn.ws/python>`_,
`ws4py <https://github.com/Lawouach/WebSocket-for-Python>`_ and
`Tornado <http://www.tornadoweb.org/>`_.

WSAccell replaces per-byte process in them with Cython version.

AutobahnPython beginning with version 0.6 automatically uses WSAccell if available.
Otherwise you can run-time patch supported WebSocket libraries using:

.. code-block:: python

    import wsaccel
    wsaccel.patch_autobahn()  # for autobahn.
    wsaccel.patch_ws4py()     # for ws4py.
    wsaccel.patch_tornado()   # for Tornado
