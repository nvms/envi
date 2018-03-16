#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shlex
from time import sleep
import subprocess
from subprocess import Popen, PIPE
from .util import *

class Window(object):

    def __init__(self, name, config, wc):
        self.name = name
        self.name = self.name.replace("*","")
        self.config = config
        self.wc = wc


    def dump(self):
        for attr in vars(self):
            print("|    | %s: %r" % (attr, getattr(self, attr)))


    def spawn(self, args=None):

        self.arg_string = self.name

        if args:
            self.arg_string = ' '.join([self.name, args])

        if verbose_mode(self.config):
            print('|    ---Window---: {}'.format(hex(id(self))))
            self.dump()

        self.wc.command.run(self.arg_string, spawner=True)


    def set_id(self, id):
        self.id = id


    def resize(self, name: str, desired_width: int, desired_height: int, desired_x: int, desired_y: int):

        self.name = name
        self.desired_width = int(desired_width)
        self.desired_height = int(desired_height)
        self.desired_x = int(desired_x)
        self.desired_y = int(desired_y)

        # wmctrl -i(by winid) -r [?] -e [gravity, x, y, w, h]
        cmd = "wmctrl -i -r {} -e '0, {}, {}, {}, {}'".format(self.id,
                                                              self.desired_x,
                                                              self.desired_y,
                                                              self.desired_width,
                                                              self.desired_height)
        self.wc.command.run(cmd)

