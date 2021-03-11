---
author: Simon Klug
title: Python Function Annotation
date: 2020-03-20
tags: Python, Programming, Tips, PEP, Code
---

Starting with Python 3.0 (and [PEP 3107 -- Function Annotations](https://www.python.org/dev/peps/pep-3107)) it is possible to annotate the arguments and return values of functions.

A function with an annotation might look like this.
```python
def split_into_first_and_last_name(name: str) -> list:
    return name.split()
```

The syntax is for function arguments is `argument[: type][="default_value"]` where type can be either a Python Data Type or a String describing the argument. There is no meaning in these annotations on default and no type checking is done. You can access them programmatically via `split_into_first_and_last_name.__annotations__` or use the `help()` function for the 


## Why use Function Annotations?
* You can use them for Documentation Purposes and Type Hinting. Therfore using function Annotations will help you to write clean code.
* You can use [mypy](https://github.com/python/mypy), [Pyright](https://github.com/Microsoft/pyright) (Microsoft), [pyre-check](https://github.com/facebook/pyre-check) (Facebook) or [pytype](https://github.com/google/pytype) (Google) to optionaly turn on static type checking (According to [PEP 484 -- Type Hints](https://www.python.org/dev/peps/pep-0484/)). To do so: 
    * Install mypy with `pip install mypy`
    * Try out your type annotated file with `mypy namesplitter.py`
    * If you are using the function wrong (e.g. `split_into_first_and_last_name(["Simon","Klug"])`) you get an error message `error: Argument 1 to "split_into_first_and_last_name" has incompatible type "List[str]"; expected "str"`
* Get better linting with an integration for your favourite editor or linter