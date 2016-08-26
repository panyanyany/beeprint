beeprint
===
make your debug printing more friendly

Features
===
- print dict elegantly
- auto wrap text, including English and Chinese
- outstanding mark to class and instance
- compatible with py2 py3

Contents
===
- [Examples](#examples)
- [Installation](#installation)
- [Settings](#settings)

Examples
===

Import beeprint as pp
---
```
from beeprint.printer import beeprint as pp
```

Short List
---

```
In [2]: alist = [1, 2, 3, 4, 5, 6]

In [3]: pp(alist)
[1, 2, 3, 4, 5, 6]
```

Complicated List
---
```
In [4]: clist = [1, [2], {'key': 'val'}]

In [5]: pp(clist)
[
  1,
  [2],
  {
    'key': 'val',
  },
]
```

Class Instance
---
```
In [6]: class NormalClassNewStyle(object): 
   ...:         def mth():pass
   ...:         static_props = 1
   ...:         lists = []
   ...:         dicts = {}
   ...:         tupl = (1,2)
   ...:     

In [7]: obj = NormalClassNewStyle()

In [8]: pp(obj)
instance(NormalClassNewStyle):
  dicts: {
  },
  lists: [],
  static_props: 1,
  tupl: (1, 2)
```

Long Text
---
```
In [27]: long_text_en = "The separation of the sky and the earth took eighteen thousand years-the yang which was light and pure rose to become the sky, and the yin which was heavy and murky（朦胧的） sank to form the earth. Between them was Pangu, who went through nine changes every day, his wisdom greater than that of the sky and his ability greater than that of the earth. Every day the sky rose ten feet higher, the earth became ten feet thicker, and Pangu grew ten feet taller."

In [28]: pp(long_text_en)
'The separation of the sky and the earth took eighteen thousand years-the yang which was light and pure rose to
 become the sky, and the yin which was heavy and murky（朦胧的） sank to form the earth. Between them was Pangu,
 who went through nine changes every day, his wisdom greater than that of the sky and his ability greater than that
 of the earth. Every day the sky rose ten feet higher, the earth became ten feet thicker, and Pangu grew ten feet
 taller.'

In [30]: long_text_cn = "据民间神话传说古时盘古生在黑暗团中，他不能忍受黑暗，用神斧劈向四方，逐渐使天空高远，大地辽阔。他为不使天地会重新合并，继续施展法术。每当盘古的身体长高一尺，天空就随之增高一尺，经过1.8万多年的努力，盘古变成 一位顶天立地的巨人，而天空也升得高不可及，大地也变得厚实无比。盘古生前完成开天辟地的伟大业绩，死后永远留给后人无穷 无尽的宝藏，成为中华民族崇拜的英雄。""

In [31]: pp(long_text_cn)
'据民间神话传说古时盘古生在黑暗团中，他不能忍受黑暗，用神斧劈向四方，逐渐使天空高远，大地辽阔。他为不使天地会重新合
 并，继续施展法术。每当盘古的身体长高一尺，天空就随之增高一尺，经过1.8万多年的努力，盘古变成一位顶天立地的巨人，而
 天空也升得高不可及，大地也变得厚实无比。盘古生前完成开天辟地的伟大业绩，死后永远留给后人无穷无尽的宝藏，成为中华民
 族崇拜的英雄。'
```

Long Text in Dict
---
```
In [33]: d = {'en': long_text_en, 'cn': long_text_cn}

In [34]: pp(d)
{
  'en': 'The separation of the sky and the earth took eighteen thousand years-the yang which was light and pure
         rose to become the sky, and the yin which was heavy and murky（朦胧的） sank to form the earth. Between
         them was Pangu, who went through nine changes every day, his wisdom greater than that of the sky and his
         ability greater than that of the earth. Every day the sky rose ten feet higher, the earth became ten feet
         thicker, and Pangu grew ten feet taller.',
  'cn': '据民间神话传说古时盘古生在黑暗团中，他不能忍受黑暗，用神斧劈向四方，逐渐使天空高远，大地辽阔。他为不使天地
         会重新合并，继续施展法术。每当盘古的身体长高一尺，天空就随之增高一尺，经过1.8万多年的努力，盘古变成一位顶
         天立地的巨人，而天空也升得高不可及，大地也变得厚实无比。盘古生前完成开天辟地的伟大业绩，死后永远留给后人无
         穷无尽的宝藏，成为中华民族崇拜的英雄。',
}
```

Complicated data
---
```
[
  1,
  1.1,
  'literal',
  'unicode',
  'literal中文',
  'unicode中文',
  [1, 2, 3, 4, 5, 6],
  [
    1,
    [2],
    {
      'key': 'val',
    },
  ],
  (1, 2),
  function(EmptyFunc),
  class(EmptyClassOldStyle),
  class(EmptyClassNewStyle),
  class(NormalClassOldStyle):
    static_props: 1
  class(NormalClassNewStyle):
    dicts: {
    },
    lists: [],
    static_props: 1,
    tupl: (1, 2)
  instance(NormalClassOldStyle):
    static_props: 1
  instance(NormalClassNewStyle):
    dicts: {
    },
    lists: [],
    static_props: 1,
    tupl: (1, 2)
  method(mth),
  method(mth),
  {
    'key': []
  },
  {
    'key': instance(NormalClassNewStyle):
      dicts: {
      },
      lists: [],
      static_props: 1,
      tupl: (1, 2)
  },
]
```

Installation
===
```shell
pip install beeprint
```

Settings
===

> more on [settings.py](./beeprint/settings.py)

