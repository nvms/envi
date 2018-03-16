#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .util import *
from .window import Window
from .window_controller import WindowController

class App(object):

    def __init__(self):
        pass


    def create(self):

        self.required_fields = ['width', 'height', 'x', 'y']

        # Make sure that width, height, x and y were provided
        # It's the least we need
        self.ensure_required()

        # Looks like we're validated.
        del self.required_fields

        # We send these values to the WindowController, which in turn
        # passes them along to the Window that it creates. I prefixed
        # them with 'desired_' so that it makes more sense later on.
        self.desired_height = self.height
        self.desired_width = self.width
        self.desired_x = self.x
        self.desired_y = self.y

        # Don't need these any more
        del self.height
        del self.width
        del self.x
        del self.y

        if verbose_mode(self.config):
            print('')
            print('---Application---')
            print('| ', self.name)

        self.wc = WindowController(**vars(self))

        if verbose_mode(self.config):
            print('-----------------')


    def ensure_required(self):

        # Do all of the required_fields exist in vars(self)?
        # https://docs.python.org/2/library/stdtypes.html
        # set <= other
        # Test whether every element in the set is in other.
        if not set(self.required_fields) <= set(vars(self)):
            msg = """{} is missing a required config property.
Required fields: {}""".format(self.name, self.required_fields)
            bail(msg, 1)
            del self.required_fields


    def dump(self):
        print('App: {}'.format(hex(id(self))))
        for attr in vars(self):
            print("  %s: %r" % (attr, getattr(self, attr)))
        print('')
