Provide a convenient way to define method dispatch depending on outside API version.

# Installation

Waist requires Python 3.8 or higher.

```bash
pip install waist
```

# What's This?
Waist helps you write code when you depend on external APIs.


```python
from waist import API

import bpy  # 3D software Blender API


# Set the API that we need to support.
# the `bpy.app.version` is a version tuple, we join it into a string first.
api = API(".".join(bpy.app.version))

class App:
    @api("<4")
    def f(self):
        return "Do something that only works in versions before 4."
    
    @api("==4.0.1")
    def f(self):
        return "Something happened in 4.0.1 that needs specific fix."
    
    @api()
    def f(self):
        return ("Generic or default function that gets called if no suitable version spec is found." 
                "In this case if the version is 4 or above (but not 4.0.1)")

```

# Why is this?
Isn't it just a _waist_ of time when you can simply do if/else?

Sure it could be expressed with if/else and that's easy to do like the examples below.
However, that's in my opinion harder to read.  


```python
import bpy


api = bpy.app.version


if api == (4, 0, 1):
    def _f(self):
        return "Something happened in 4.0.1 that needs specific fix."
        
elif api < (4,):
    def _f():
        return "Do something that only works in versions before 4."
        
else:
    def _f(self):
        return ("Generic or default function that gets called if no suitable version spec is found." 
            "In this case if the version is 4 or above (but not 4.0.1)")


class App:
    f = _f
```

Another alternative

```python
import bpy


api = bpy.app.version

class App:
    def f(self):
        if api == (4, 0, 1):
            return "Something happened in 4.0.1 that needs specific fix."
                
        elif api < (4,):
            return "Do something that only works in versions before 4."
                
        else:
            return ("Generic or default function that gets called if no suitable version spec is found." 
                    "In this case if the version is 4 or above (but not 4.0.1)")

```
