#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .window import Window
from .commander import Commander
from .util import *

from time import sleep

class WindowController(object):

    def __init__(self, capture=False, **kwargs):
        """ WindowController objects get created at app.create_window. Keyword
        arguments are passed at that time, and each Window object inherits the
        properties and values defined in the config.yml. Every Window object
        should have: desired_height, desired_width, desired_x and desired_y. """

        # Unpack kwargs into self attributes
        for k, v in kwargs.items():
            self.__setattr__(k, v)

        # This just gives a Window access to the run command
        self.command = Commander()

        # If we are simply running the 'capture', command, don't start
        # a window flow. We still need this WindowController for its
        # Commander, though
        if capture == False:

            if verbose_mode(self.config):
                print('|  ---WindowController---: {}'.format(hex(id(self))))
                self.dump()

            self.window = Window(self.name, self.config, self)
            self.begin_window_flow()

            if verbose_mode(self.config):
                print('|  ----------------------')


    def begin_window_flow(self):

        # Spawn the window
        if hasattr(self, 'args'):
            self.window.spawn(self.args)
        else:
            self.window.spawn()

        # Give it a second
        while True:
            sleep(.1)
            if not self.config.last_window_id == self.new_window_id() and self.new_window_id() not in self.config.opened_windows:
                self.config.last_window_id = self.new_window_id()
                self.config.opened_windows.append(self.config.last_window_id) # keep list of all we've opened!
                break

        # Tell the Window the new ID
        self.window.set_id(self.config.last_window_id)

        # Position
        self.window.resize(name=self.name,
                           desired_width=self.desired_width,
                           desired_height=self.desired_height,
                           desired_x=self.desired_x,
                           desired_y=self.desired_y)


    def new_window_id(self):
        id = self.command.run(self.config.getid_sh)
        return id


    def dump(self):
        for attr in vars(self):
            print("|  | %s: %r" % (attr, getattr(self, attr)))
