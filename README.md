beeprint: Beautifully Print
===
pprint is good, but not clean. So beeprint do it.

Features
===
- print dict elegantly
- outstanding mark to class and instance
- compatible with py2 py3
- auto wrap text, including English and Chinese

Contents
===
- [Examples](#examples)
- [Installation](#installation)
- [Settings](#settings)

Examples
===

Short list
---
```
[1, 2, 3, 4, 5, 6]
```

Compliated list
---
```
[
  1,
  [2],
  {
    'key': 'val',
  },
]
```

Class Instance Formatted Display
---
```
instance(NormalClassNewStyle):
  dicts: {
  },
  lists: [],
  static_props: 1,
  tupl: (1, 2)
```

Long Text Auto Wrapping
---

> auto wrapped by terminal width

```
[
  '\nThe sky and the earth were at first one blurred entity like an egg. Pangu
   was born into it.\n \nThe separation of the sky and the earth took eighteen
   thousand years-the yang which was light and pure rose to become the sky,
   and the yin which was heavy and murky（朦胧的） sank to form the earth.
   Between them was Pangu, who went through nine changes every day, his wisdom
   greater than that of the sky and his ability greater than that of the
   earth. Every day the sky rose ten feet higher, the earth became ten feet
   thicker, and Pangu grew ten feet taller.\n \nAnother eighteen thousand
   years passed, and there was an extremely high sky, an extremely thick
   earth, and an extremely tall Pangu. After Pangu died, his head turned into
   the Five Sacred Mountains (Mount Tai, Mount Heng, Mount Hua, Mount Heng,
   Mount Song), his eyes turned into the moon and the sun, his blood changed
   into water in river and sea, his hair into grass.\n \nIn all, the universe
   and Pangu combine in one.\n',
  '\n据民间神话传说古时盘古生在黑暗团中，他不能忍受黑暗，用神斧劈向四方，逐渐
   使天空高远，大地辽阔。他为不使天地会重新合并，继续施展法术。每当盘古的身体
   长高一尺，天空就随之增高一尺，经过1.8万多年的努力，盘古变成一位顶天立地的巨
   人，而天空也升得高不可及，大地也变得厚实无比。盘古生前完成开天辟地的伟大业
   绩，死后永远留给后人无穷无尽的宝藏，成为中华民族崇拜的英雄。\n',
]
```

Long Text in Dict Auto Wrapping
---

> auto wrapped by terminal width

```
[
  {
    'english version': '\nThe sky and the earth were at first one blurred entity
                        like an egg. Pangu was born into it.\n \nThe separation
                        of the sky and the earth took eighteen thousand
                        years-the yang which was light and pure rose to become
                        the sky, and the yin which was heavy and murky（朦胧的）
                        sank to form the earth. Between them was Pangu, who went
                        through nine changes every day, his wisdom greater than
                        that of the sky and his ability greater than that of the
                        earth. Every day the sky rose ten feet higher, the earth
                        became ten feet thicker, and Pangu grew ten feet
                        taller.\n \nAnother eighteen thousand years passed, and
                        there was an extremely high sky, an extremely thick
                        earth, and an extremely tall Pangu. After Pangu died,
                        his head turned into the Five Sacred Mountains (Mount
                        Tai, Mount Heng, Mount Hua, Mount Heng, Mount Song), his
                        eyes turned into the moon and the sun, his blood changed
                        into water in river and sea, his hair into grass.\n \nIn
                        all, the universe and Pangu combine in one.\n',
  },
  {
    'simplify chinese versino': '\n据民间神话传说古时盘古生在黑暗团中，他不能忍
                                 受黑暗，用神斧劈向四方，逐渐使天空高远，大地辽
                                 阔。他为不使天地会重新合并，继续施展法术。每当
                                 盘古的身体长高一尺，天空就随之增高一尺，经过1.8
                                 万多年的努力，盘古变成一位顶天立地的巨人，而天
                                 空也升得高不可及，大地也变得厚实无比。盘古生前
                                 完成开天辟地的伟大业绩，死后永远留给后人无穷无
                                 尽的宝藏，成为中华民族崇拜的英雄。\n',
  },
]
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

