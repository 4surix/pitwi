# encode: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------


boxs = []
index = 0


def add(box):
    if box not in boxs:
        boxs.append(box)


def rem(box):

    global index

    if box in boxs:
        if boxs.index(box) < index:
            index -= 1
        boxs.remove(box)


def next():

    global index

    boxs[index].inactive()

    index += 1

    if index >= len(boxs):
        index = 0

    boxs[index].active()