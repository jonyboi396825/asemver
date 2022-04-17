# A Python implementation of semantic versioning

This is an implementation of semantic versioning in Python. 
This will not be a standalone package on PyPI because there is 
already [another implementation](https://pypi.org/project/semver/)
of semantic versioning.

If anything, this package will only be used as a component of
a bigger project in a git submodule or installed using git.

## Quick example

```py
from semver import parse_version
version = parse_version("2.5.1-alpha.41+meta293")

print(str(version))
# '2.5.1-alpha.41+meta293'

print(repr(version))
# "Version(major=2, minor=5, patch=1, pre=Pre(string='alpha.41'), build=Build(string='meta293'))"
```
