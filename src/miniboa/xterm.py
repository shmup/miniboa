# -*- coding: utf-8 -*-
"""
Support for color and formatting for Xterm style clients.
"""

import re

_PARA_BREAK = re.compile(r"(\n\s*\n)", re.MULTILINE)

# Caret contants for users to use.
BLACK = '^k'
BLACK_BACKGROUND = '^0'
BRIGHT_BLACK = '^K'

BLUE = '^b'
BLUE_BACKGROUND = '^4'
BRIGHT_BLUE = '^B'

CYAN = '^c'
CYAN_BACKGROUND = '^6'
BRIGHT_CYAN = '^C'

DEFAULT = '^d'

GREEN = '^g'
GREEN_BACKGROUND = '^2'
BRIGHT_GREEN = '^G'

MAGENTA = '^m'
MAGENTA_BACKGROUND = '^5'
BRIGHT_MAGENTA = '^M'

RED = '^r'
RED_BACKGROUND = '^1'
BRIGHT_RED = '^R'

WHITE = '^w'
BRIGHT_WHITE = '^W'

YELLOW = '^y'
YELLOW_BACKGROUND = '^3'
BRIGHT_YELLOW = '^Y'

BOLD_OFF = '^.'
BOLD_ON = '^!'
CLEAR_SCREEN = '^s'
CLEAR_TO_END_OF_LINE = '^l'
INVERSE_TEXT_OFF = '^i'
INVERSE_TEXT_ON = '^I'
RESET_ALL = '^~'
UNDERLINE_OFF = '^u'
UNDERLINE_ON = '^U'

# Caret Code to ANSI TABLE
_ANSI_CODES = (
    ('^k', '\x1b[22;30m'),    # black
    ('^K', '\x1b[1;30m'),    # bright black (grey)
    ('^r', '\x1b[22;31m'),    # red
    ('^R', '\x1b[1;31m'),    # bright red
    ('^g', '\x1b[22;32m'),    # green
    ('^G', '\x1b[1;32m'),    # bright green
    ('^y', '\x1b[22;33m'),    # yellow
    ('^Y', '\x1b[1;33m'),    # bright yellow
    ('^b', '\x1b[22;34m'),    # blue
    ('^B', '\x1b[1;34m'),    # bright blue
    ('^m', '\x1b[22;35m'),    # magenta
    ('^M', '\x1b[1;35m'),    # bright magenta
    ('^c', '\x1b[22;36m'),    # cyan
    ('^C', '\x1b[1;36m'),    # bright cyan
    ('^w', '\x1b[22;37m'),    # white
    ('^W', '\x1b[1;37m'),    # bright white
    ('^0', '\x1b[40m'),    # black background
    ('^1', '\x1b[41m'),    # red background
    ('^2', '\x1b[42m'),    # green background
    ('^3', '\x1b[43m'),    # yellow background
    ('^4', '\x1b[44m'),    # blue background
    ('^5', '\x1b[45m'),    # magenta background
    ('^6', '\x1b[46m'),    # cyan background
    ('^d', '\x1b[39;49m'), # default (should be white on black)
    ('^I', '\x1b[7m'),    # inverse text on
    ('^i', '\x1b[27m'),    # inverse text off
    ('^~', '\x1b[0m'),    # reset all
    ('^U', '\x1b[4m'),    # underline on
    ('^u', '\x1b[24m'),    # underline off
    ('^!', '\x1b[1m'),    # bold on
    ('^.', '\x1b[22m'),    # bold off
    ('^s', '\x1b[2J'),    # clear screen
    ('^l', '\x1b[2K'),    # clear to end of line
)


def strip_caret_codes(text):
    """
    Strip out any caret codes from a string.
    """
    # temporarily escape out ^^
    text = text.replace('^^', '\x00')
    for token, foo in _ANSI_CODES:
        text = text.replace(token, '')
    return text.replace('\x00', '^')


def colorize(text, ansi=True):
    """
    If the client wants ansi, replace the tokens with ansi sequences --
    otherwise, simply strip them out.
    """
    if ansi:
        text = text.replace('^^', '\x00')
        for token, code in _ANSI_CODES:
            text = text.replace(token, code)
        text = text.replace('\x00', '^')
    else:
        text = strip_caret_codes(text)
    return text


def word_wrap(text, columns=80, indent=4, padding=2):
    """
    Given a block of text, breaks into a list of lines wrapped to
    length.
    """
    paragraphs = _PARA_BREAK.split(text)
    lines = []
    columns -= padding
    for para in paragraphs:
        if para.isspace():
            continue
        line = ' ' * indent
        for word in para.split():
            if (len(line) + 1 + len(word)) > columns:
                lines.append(line)
                line = ' ' * padding
                line += word
            else:
                line += ' ' + word
        if not line.isspace():
            lines.append(line)
    return lines
