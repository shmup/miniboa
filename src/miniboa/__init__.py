# -*- coding: utf-8 -*-
from .mbasync import TelnetServer

__version__ = "1.0.9"

__title__ = "miniboa"
__description__ = "Asynchronous, single-threaded, poll-based Telnet server"
__uri__ = "https://github.com/shmup/miniboa"
__doc__ = __description__ + " <" + __uri__ + ">"

__author__ = "Jared Miller"
__email__ = "jared@smell.flowers"

__license__ = "Apache 2"
__copyright__ = "Copyright (c) 2022 Jared Miller"

__all__ = ['TelnetServer', ]
