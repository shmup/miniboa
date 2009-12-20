# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#   mudlib/usr/xterm.py
#   Copyright 2009 Jim Storch
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain a
#   copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#------------------------------------------------------------------------------

import re

"""Support for color and formatting for Xterm style clients."""


#--[ Caret Code to ANSI TABLE ]------------------------------------------------

_ANSI_CODES = (

    # Note: order here matters to keep '^b' from clobbering '^bb'
    ( '^kb', '\x1b[40m' ),          # black background
    ( '^rb', '\x1b[41m' ),          # red background
    ( '^gb', '\x1b[42m' ),          # green background
    ( '^yb', '\x1b[43m' ),          # yellow background
    ( '^bb', '\x1b[44m' ),          # blue background
    ( '^mb', '\x1b[45m' ),          # magenta background
    ( '^cb', '\x1b[46m' ),          # cyan background
    ( '^k', '\x1b[22;30m' ),        # black
    ( '^K', '\x1b[1;30m' ),         # bright black (grey)
    ( '^r', '\x1b[22;31m' ),        # red
    ( '^R', '\x1b[1;31m' ),         # bright red
    ( '^g', '\x1b[22;32m' ),        # green
    ( '^G', '\x1b[1;32m' ),         # bright green
    ( '^y', '\x1b[22;33m' ),        # yellow
    ( '^Y', '\x1b[1;33m' ),         # bright yellow
    ( '^b', '\x1b[22;34m' ),        # blue
    ( '^B', '\x1b[1;34m' ),         # bright blue
    ( '^m', '\x1b[22;35m' ),        # magenta
    ( '^M', '\x1b[1;35m' ),         # bright magenta
    ( '^c', '\x1b[22;36m' ),        # cyan
    ( '^C', '\x1b[1;36m' ),         # bright cyan
    ( '^w', '\x1b[22;37m' ),        # white
    ( '^W', '\x1b[1;37m' ),         # bright white
    ( '^d', '\x1b[39m' ),           # default (should be white on black)
    ( '^i', '\x1b[7m' ),            # inverse text on
    ( '^I', '\x1b[27m' ),           # inverse text off
    ( '^^', '\x1b[0m' ),            # reset all
    ( '^_', '\x1b[4m' ),            # underline on
    ( '^-', '\x1b[24m' ),           # underline off
    ( '^!', '\x1b[1m' ),            # bold on
    ( '^1', '\x1b[22m'),            # bold off
    ( '^s', '\x1b[2J'),             # clear screen
    ( '^l', '\x1b[2K'),             # clear to end of line
    )


#-------------------------------------------------------------Strip Caret Codes

def strip_caret_codes(text):

    """
    Strip out any caret codes from a string.
    """

    for token, throwaway in _ANSI_CODES:
        text = text.replace(token, '')
    return text


#----------------------------------------------------------------------Colorize

def colorize(text, ansi=True):

    """
    If the client wants ansi, replace the tokens with ansi sequences --
    otherwise, simply strip them out.
    """

    if ansi:
        for token, code in _ANSI_CODES:
            text = text.replace(token, code)
    else:
        text = strip_caret_codes(text)

    return text


#---------------------------------------------------------------------Word Wrap

def word_wrap(text, columns=78, indent=2, padding=1):

    """
    Given a block of text, breaks into a list of lines wrapped to
    length.  Should be a bit more efficient with telnet sending lines.
    """

    para_break = re.compile(r"(\n\s*\n)", re.MULTILINE)
    paragraphs = para_break.split(text)
    lines = []
    for para in paragraphs:
        if para.isspace():
            continue
        line = ' ' * ( padding + indent )
        for word in para.split():
            if (len(line) + 1 + len(word)) > columns:
                lines.append(line)
                line = ' ' * padding
            line += ' ' + word
        if not line.isspace():
            lines.append(line)
    return lines
