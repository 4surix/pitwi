# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

import xml.etree.ElementTree as ET


from .objects import *
from .ids import IDS
from . import binding
from . import colors as COLORS


STYLES = {}


def Style(data, variables):
    for id__, params in decode_css(data, variables).items():
        STYLES.setdefault(id__, {}).update(params)


def Script(data, variables):
    exec('if True:\n' + data, variables)


def Function(data, variables, args):
    return lambda *args__: (
        variables.update(zip(args, args__)),
        exec('if True:\n' + data, variables)
    )


def Bind(data, variables, key, alias):
    binding.add(key, lambda: exec('if True:\n' + data, variables))

    for alias in alias:
        if alias:
            binding.add(alias, lambda: exec('if True:\n' + data, variables))


def Tile():
    pass


def Ignore():
    pass


widgets = {
    'root': Root,
    'text': Text,
    'fish': Text.Fish,
    'border': Border,
    'button': Button,
    'carousel': Carousel,
    'checkButton': CheckButton,
    'entry': Entry,
    'menu': Menu,
    'scrolling': Scrolling,
    'zone': Zone,
    'area': Zone,
    'map': Map,
    'style': Style,
    'script': Script,
    'ignore': Ignore,
    'function': Function,
    'tile': Tile,
    'bind': Bind,
}

borders = {
    'tranparent': Borders.Tranparent,
    'simple': Borders.Simple,
    'double': Borders.Double,
    'corner': Borders.Corner,
    'footer': Borders.Footer,
    'header': Borders.Header,
}


def check_childtext(child, variables):

    if not child.text:
        return ''

    text = child.text.strip()

    parts = []
    begin = end = -1
    begin_index = end_index = 0

    while True:

        try: begin_index = text.index('{', begin_index)
        except ValueError:
            parts.append(text[end + 1 :])
            break
        else:
            if begin_index + 1 < len(text) and text[begin_index + 1] == '{':
                text = text[:begin_index] + '{' + text[begin_index + 2:]
            else:
                begin = begin_index
                parts.append(text[end + 1 : begin])
            begin_index += 1

        try: end_index = text.index('}', end_index)
        except ValueError:
            parts.append(text[end + 1 :])
            break
        else:
            if end_index + 1 < len(text) and text[end_index + 1] == '}':
                text = text[:end_index] + '}' + text[end_index + 2:]
            else:
                end = end_index
                parts.append(text[begin + 1 : end])
            end_index += 1

    text = ''
    is_eval = True

    for part in parts:

        is_eval = not is_eval

        if not part:
            continue
        
        if is_eval:
            text += str(eval(part.replace('\n', ' '), variables))
        else:
            text += (
                (' ' if part[0] == ' ' else '') 
                + ' '.join(part.split()) 
                + (' ' if part[-1] == ' ' else '')
            )

    return text


def parser_in(widget_parent, node, variables):

    for child in node:

        widget = widgets.get(child.tag)

        if not widget:
            continue


        style = STYLES.get(child.tag, {}).copy()

        id__ = child.attrib.get('id', '').replace('-', '_')
        class__ = child.attrib.get('class')

        if class__:
            for c__ in class__.split(' '):
                style.update(STYLES.get('.' + c__.replace('-', '_'), {}))

        if id__:
            style.update(STYLES.get('#' + id__, {}))

        border = style.get('border')

        if border:
            style['border'] = border.copy(color=style.get('border_color'))

        border = style.get('active_border')

        if border:
            style['active_border'] = border.copy(color=style.get('active_border_color'))

        child.attrib.update(style)


        if widget in (Zone, Carousel):
            widget = widget(**child.attrib)

        elif widget in (Text, Text.Fish, Button, Scrolling):
            widget = widget(check_childtext(child, variables), **child.attrib)

        elif widget == CheckButton:
            widget = widget(*check_childtext(child, variables).split(';'), **child.attrib)

        elif widget == Menu:
            widget = widget(**child.attrib)
            widget.config_buttons(
                zone = IDS.get(child.attrib.get('area-buttons')),
                style = {
                    key[7:]: value
                    for key, value in style.items() 
                    if 'button_' in key
                }
            )

        elif widget == Entry:
            widget = widget(textleft=check_childtext(child, variables), **child.attrib)

        elif widget == Map:
            matrix = {}
            for line in check_childtext(child, variables).strip().split('\n'):
                for index, value in enumerate(line.strip().split()):
                    matrix.setdefault(index, []).append(value)
            value = list(matrix.values())
            widget = widget(value, **child.attrib)

        elif widget in (Style, Script):
            widget((child.text if child.text else ''), variables)
            continue

        elif widget == Function:
            if isinstance(widget_parent, (Entry, Button)):
                widget_parent.function = widget(
                    (child.text if child.text else ''),
                    variables,
                    child.attrib.get('args', "").split(' ')
                )
            continue

        elif widget == Tile:
            if isinstance(widget_parent, (Map)):
                widget_parent.tile(
                    child.attrib.get('name'),
                    check_childtext(child, variables),
                    child.attrib.get('collision') == 'true'
                )
            continue

        elif widget == Bind:
            widget(
                (child.text if child.text else ''),
                variables,
                child.attrib.get('key'),
                child.attrib.get('alias', '').split(' '),
            )
            continue


        if id__:
            variables[id__] = widget


        if widget == Ignore or widget_parent == Ignore:
            pass

        elif isinstance(widget_parent, Menu):
            widget_parent.add(
                child.attrib.pop('value-button'), 
                widget
            )
        else:
            widget_parent.add(
                widget,
                row = int(child.attrib.get('row', 0)),
                column = int(child.attrib.get('column', 0)),
                spanrow = int(child.attrib.get('spanrow', 1)),
                spancolumn = int(child.attrib.get('spancolumn', 1))
            )


        parser_in(widget, child, variables)


def decode_css(data, variables):

    infos = {}

    value = ''

    in_text = False
    in_comment = False
    in_escape = False

    for carac in data:

        if carac == '\\':
            in_escape = True

        elif in_escape:
            value += '\\' + value
            in_escape = False

        elif carac == '"' or carac == "'":
            value += carac
            in_text = not in_text

        elif in_text:
            value += carac

        elif carac == '/':

            if value[-1] == '/':
                value = ''
                in_comment = not in_comment

            else:
                value += '/'

        elif in_comment:
            pass

        elif carac == '{':
            infos[value.strip().replace('-', '_')] = info = {}
            value = ''

        elif carac == '}':
            pass

        elif carac == ':':
            key = value.strip().replace('-', '_')
            value = ''

        elif carac == ';':
            info[key] = eval(value.strip(), variables)
            value = ''

        else:
            value += carac

    return infos


def text(data:str, variables=None):

    variables = variables if variables else {}

    variables.update({k: k for k in COLORS.FG})
    variables.update({k: k for k in COLORS.BG})
    variables.update(borders)
    variables['space'] = lambda value: ' ' * value
    variables['COLORS'] = COLORS

    base = ET.fromstring(
        data
        .replace("\\<", "&lt;")
        .replace("\\>", "&gt;")
    )

    root = Root(**base.attrib)

    variables['root'] = root

    parser_in(root, base, variables)

    return root


def file(path, variables=None):

    with open(path, encoding='utf-8') as file:
        data = file.read()

    return text(data, variables)