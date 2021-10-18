# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

import copy
import random
import xml.etree.ElementTree as ET

from collections.abc import Iterable


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


def Case():
    pass


def Cases():
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
    'case': Case,
    'cases': Cases,
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


def gen_random_var():
    return '__' + ''.join(
        random.choice('azertyuiopqsdfghjklmwxcvbn')
        for _ in range(20)
    )


def check_elements(widget, variables, simple=False):

    if simple:
        elements = [widget]
    else:
        elements = [widget.text.strip() if widget.text else '']

        for element in widget:
            elements.append(element)
            elements.append(element.tail.strip() if element.tail else '')

    childs = []

    parts = []
    part = ''
    in_comprehention = False
    in_text = False
    last_symbol_text = None
    deep = 0

    is_widget = True

    for element in elements:

        is_widget = not is_widget

        if is_widget:
            if in_comprehention:
                id__ = element.attrib.get('id')
                
                if not id__:
                    id__ = gen_random_var()

                part += (' __config_attrib_element(' + id__ + ', vars()) ')
                variables[id__] = element
            else:
                childs.append(element)
        else:
            for carac in element:

                if carac == '{' and not in_text:
                    if deep == 0:
                        in_comprehention = True
                        parts.append(part.strip())
                        part = ''
                    deep += 1
                elif carac == '}' and not in_text:
                    deep -= 1
                    if deep == 0:
                        in_comprehention = False
                        parts.append(part.strip())
                        part = ''
                elif carac == '"' or carac == "'":
                    if last_symbol_text == carac:
                        if in_text:
                            in_text = False
                            last_symbol_text = None
                        else:
                            in_text = True
                            last_symbol_text = carac
                    part += carac
                else:
                    part += carac

    parts.append(part.strip())
    part = ''

    text = ''
    is_eval = True

    for part in parts:

        is_eval = not is_eval

        if not part:
            continue
        
        if is_eval:
            result = eval('(' + part.replace('\n', ' ') + ')', variables)

            if simple:
                value = result
            elif isinstance(result, (str, int, float)):
                text += str(result)
            elif isinstance(result, Iterable):
                childs.extend(result)
            else:
                childs.append(result) 
        else:
            text += (
                (' ' if part[0] == ' ' else '') 
                + ' '.join(part.split()) 
                + (' ' if part[-1] == ' ' else '')
            )

            if simple:
                value = text

    if simple:
        return value
    else:
        return text, childs


def parser_in(widget_parent, node, variables):

    for child in node:

        widget = widgets.get(child.tag)

        if not widget:
            continue

        variables.update(child.attrib.pop('__local_vars', {}))

        child.attrib = {
            key: check_elements(value, variables, simple=True)
            for key, value in child.attrib.items()
        }

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

        
        if widget in (Style, Script):
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

        elif widget == Bind:
            widget(
                (child.text if child.text else ''),
                variables,
                child.attrib.get('key'),
                child.attrib.get('alias', '').split(' '),
            )
            continue

        text, childs = check_elements(child, variables)

        if widget in (Zone, Carousel):
            widget = widget(**child.attrib)

        elif widget in (Text, Text.Fish, Button, Scrolling):
            widget = widget(text, **child.attrib)

        elif widget == CheckButton:
            widget = widget(*text.split(';'), **child.attrib)

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
            widget = widget(textleft=text, **child.attrib)

        elif widget == Map:
            widget = widget([], **child.attrib)

        elif widget == Tile:
            if isinstance(widget_parent, (Map)):
                widget_parent.tile(
                    child.attrib.get('name'),
                    text,
                    child.attrib.get('collision') == 'true'
                )
            continue

        elif widget == Case:
            if isinstance(widget_parent, (Map)):
                widget_parent.add_case(
                    child.attrib.get('x'),
                    child.attrib.get('y'),
                    text
                )
            continue

        elif widget == Cases:
            matrix = {}

            for line in text.strip().split('\n'):
                for index, value in enumerate(line.strip().split()):
                    matrix.setdefault(index, []).append(value)

            for x, line in enumerate(list(matrix.values())):
                for y, value in enumerate(line):
                    widget_parent.add_case(
                        x,
                        y,
                        value
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
        elif isinstance(widget_parent, Carousel):
            widget_parent.add(
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


        parser_in(widget, childs, variables)


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

    def __config_attrib_element(element, local_vars):
        element = copy.deepcopy(element)
        element.attrib.update({'__local_vars': local_vars.copy()})
        return element
    variables['__config_attrib_element'] = __config_attrib_element

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