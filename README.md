# Pitwi

[![PyPI](https://img.shields.io/pypi/v/pitwi)](https://pypi.org/project/pitwi/)
[![GitHub issues](https://img.shields.io/github/issues/4surix/pitwi)](https://github.com/4surix/pitwi/issues)
[![Download](https://img.shields.io/pypi/dm/pitwi)](https://pypi.org/project/pitwi/)
![Version python](https://img.shields.io/pypi/pyversions/pitwi)

Module for terminal/console user interface.

# Aperçu

## Only Python :

```python
from pitwi import Root, Text

(
    Root(width = 45, height = 8)
    .add(Text('Puf', bg='white', fg='black'))
    .add(Text('Paf'), row=2, column=2)
    .run()
)
```

## Python + XML/CSS :

```xml
<root width="45" height="8">
	<style>
		#pwik {
			bg: white;
			fg: black;
		}
	</style>
	<text id="pwik">Puf</text>
	<text row="2" column="2">Paf</text>
</root>
```

```python
from pitwi import parser

parser.file('NAME_OF_YOUR_FILE.xml').run()
```