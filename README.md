WSAccell
=========

WSAccell is accelerator for [AutobahnPython](http://autobahn.ws/python) and [ws4py](https://github.com/Lawouach/WebSocket-for-Python).
WSAccell replaces per-byte process in them with Cython version.

```python
import wsaccell
wsaccell.patch_autobahn()  # patch for autobahn.
wsaccell.patch_ws4py()     # patch for ws4py.
```
