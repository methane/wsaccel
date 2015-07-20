WSAccell
=========

.. image:: https://travis-ci.org/methane/wsaccel.svg?branch=master
    :target: https://travis-ci.org/methane/wsaccel

WSAccell is WebSocket accelerator for `AutobahnPython <http://autobahn.ws/python>`_,
and `ws4py <https://github.com/Lawouach/WebSocket-for-Python>`_.

WSAccell replaces per-byte process in them with Cython version.

AutobahnPython beginning with version 0.6 automatically uses WSAccell if available.
Otherwise you can run-time patch supported WebSocket libraries using:

.. code-block:: python

    import wsaccel
    wsaccel.patch_autobahn()  # for autobahn.
    wsaccel.patch_ws4py()     # for ws4py.

.. note::
    WSAccell also provides accelerator for Tornado.  But Tornado provides own speedup
    module for now.  So Tornado acceralator has been deprecated.


test
----

wsaccel uses `pytest <https://pytest.org/>`_ for testing.

.. code-block:: console

    $ pip install pytest
    $ py.test tests
