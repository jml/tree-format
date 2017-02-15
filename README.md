Python library to generate nicely formatted trees, like the UNIX `tree`
command.

## Example

Produce output like this:

```
foo
├── bar
│   ├── a
│   └── b
├── baz
└── qux
    └── c⏎
        d
```

using code like this:

```python
from operator import itemgetter

from tree_format import format_tree

tree = (
    'foo', [
        ('bar', [
            ('a', []),
            ('b', []),
        ]),
        ('baz', []),
        ('qux', [
            ('c\nd', []),
        ]),
    ],
)

print format_tree(
    tree, format_node=itemgetter(0), get_children=itemgetter(1))
```

## License

This is made available under the Apache Software License, version 2.0.

Copyright (c) 2015 - Jonathan M. Lange

## Testing

Run tests with:

```
python -m testtools.run discover
```

