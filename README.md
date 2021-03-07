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

## Weater

![weater](https://cdn.discordapp.com/attachments/557310650569850881/817915701620506694/syyhLr5L76.gif)

> [weater.xml](https://github.com/4surix/pitwi/blob/main/exemples/weather.xml)

## File explorer

![file_explorer](https://cdn.discordapp.com/attachments/557310650569850881/817915760570793994/phVuxs5gRt.gif)

> [file_explorer.xml](https://github.com/4surix/pitwi/blob/main/exemples/file_explorer.xml)