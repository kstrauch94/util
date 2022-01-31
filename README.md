Utility classes for time tracking and counting

To track the time a specific code snippet takes use:
```
import util

with util.Timer("function time"):
  function()
```

Alternatively, functions can be decorated:

```
import util

@util.Timer("function")
def function():
  ...
```

In the same manner, it is possible to Count how many time a function was called:

```
import util

@util.Count("function")
def function():
  ...
```

Or, you can use the Counter inside the code:

```
import util

def function():
  # do stuff
  
  util.Count.add("Stuff done"):
  
  ...
```

the add function from Count can also add more than just 1:

```
import util

def function(n):
  for i in range(n)
    # do stuff
  util.Count.add("Stuff done", n) # adds n to the counter of "Stuff done"
 
```
