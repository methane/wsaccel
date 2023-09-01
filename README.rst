WSAccell
=========

**NOTE**: AutobahnPython and ws4py are not actively maintained. So I will stop this project too.
Please migrate to `Tornado <https://www.tornadoweb.org/en/stable/>`_ or
`websockets <https://websockets.readthedocs.io/en/stable/intro.html>`_.


WSAccell is WebSocket accelerator for `AutobahnPython <https://autobahn.readthedocs.io/en/latest/>`_,
and `ws4py <https://github.com/Lawouach/WebSocket-for-Python>`_.

WSAccell replaces per-byte process in them with Cython version.

AutobahnPython beginning with version 0.6 automatically uses WSAccell if available.
Otherwise you can run-time patch supported WebSocket libraries using:

.. code-block:: python

    import wsaccel
    wsaccel.patch_autobahn()  # for autobahn.
    wsaccel.patch_ws4py()     # for ws4py.


test
----

wsaccel uses `pytest <https://pytest.org/>`_ for testing.

.. code-block:: console

    $ pip install pytest
    $ pytest tests
