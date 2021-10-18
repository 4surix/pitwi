# Pitwi

[![PyPI](https://img.shields.io/pypi/v/pitwi)](https://pypi.org/project/pitwi/)
[![GitHub issues](https://img.shields.io/github/issues/4surix/pitwi)](https://github.com/4surix/pitwi/issues)
[![Download](https://img.shields.io/pypi/dm/pitwi)](https://pypi.org/project/pitwi/)
![Version python](https://img.shields.io/pypi/pyversions/pitwi)

Librairy for create user interface in terminal/console with XML, CSS and Python.

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

## Weather

![weather](https://cdn.discordapp.com/attachments/557310650569850881/817915701620506694/syyhLr5L76.gif)

> [weather.xml](https://github.com/4surix/pitwi/blob/main/exemples/weather.xml)

## File explorer

![file_explorer](https://cdn.discordapp.com/attachments/557310650569850881/817915760570793994/phVuxs5gRt.gif)

> [file_explorer.xml](https://github.com/4surix/pitwi/blob/main/exemples/file_explorer.xml)

## Expression

![expression](https://cdn.discordapp.com/attachments/557310650569850881/899586259016622120/1D8NQnNvoe.gif)

> [calcul.xml](https://github.com/4surix/pitwi/blob/main/exemples/calcul.xml)

## Ramass'herbe

![ramassherbe](https://cdn.discordapp.com/attachments/557310650569850881/899586377082105876/Y6hB1XZP5J.gif)

> [rammassherbe.xml](https://github.com/4surix/pitwi/blob/main/exemples/ramassherbe.xml)

# Documentation

## Text :

The text is between an opening and closing tag. `<tag>text</tag>`  
  
The space in the beginning and the end are ignored.  
  
`<tag>   pantoufle  </tag>` == `<tag>pantoufle</tag>`  
  
The character `{` and `}` is used to use Python code online. Is same as f-string.  
  
`<tag>{f"Pomme {{poire}} fraise"}</tag>` == `<tag>Pomme {poire} fraise</tag>`  
  
The characters `<`, `>` is depreciated because XML not supported in text. Use escape character to use it. `<tag>Puik \<puf\> paf</tag>`  
  
## Colors :

```xml
<root>
    <style>
        object {
            item: color;
        }
    </style>
</root>
```

```xml
<root>
    <style>
        .exemple {
            color: white;
            fg: blue;
            bg: red;
            border-color: yellow;
            active-border-color: cyan;
        }
    </style>
</root>
```

### Dark

- black
- red
- green
- yellow
- blue
- magenta
- cyan
- silver

### Light

- gray
- pink
- lime
- banana
- marlin
- violet
- teal
- white