cutf8validator
===============

Utf8Validator for AutobahnPython and WebSocket-For-Python implemented in Cython.

```python
import cutf8validator
cutf8validator.patch_autobahn()  # replace autobahn's Utf8Validator.
cutf8validator.patch_ws4py()     # replace ws4py's Utf8Validator.
```
