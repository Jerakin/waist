Provide a convenient way to define dispatch depending on outside APIs or other factors.

# Installation

Waist requires Python 3.8 or higher.

```bash
pip install waist
```

# What's This?
Waist helps you define dispatch methods for externally dependent APIs.


```python
from waist import API

import bpy  # 3D software Blender API


# Set the API that we need to support.
api = API(".".join(bpy.app.version))


@api(">4")
def f():
    return "Do something that only works in versions before 4."

@api("==4.0.1")
def f():
    return "Something happened in 4.0.1 that needs specific fix."

@api()
def f():
    return ("Generic or default function that gets called if no suitable version spec is found." 
            "In this case if the version is 4 or above (but not 4.0.1)")

```
