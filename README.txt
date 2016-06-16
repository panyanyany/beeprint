beeprint: Beautifully Print
===
pprint is good, but not clean. So beeprint do it.

Features
===
- print dict elegantly
- format of sequential type is controllable
- outstanding mark to class and instance
- compatible with py2 py3 in same output

Examples
===

Complicated data
---
```
[
  1,
  1.1,
  's',
  'us',
  'a中文',
  'a中文',
  [1],
  (1, 2),
  function(EmptyFunc),
  class(EmptyClassOldStyle),
  class(EmptyClassNewStyle),
  class(NormalClassOldStyle):
    static_props: 1,
  class(NormalClassNewStyle):
    dicts: {
    },
    lists: [],
    static_props: 1,
  instance(NormalClassOldStyle):
    static_props: 1,
  instance(NormalClassNewStyle):
    dicts: {
    },
    lists: [],
    static_props: 1,
  method(mth),
  method(mth),
  {
    'key': [],
    'key2': {
    },
  },
]
```

