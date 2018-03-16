#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml
import os
import io
import sys
from .util import bail

class Config(object):

    def __init__(self):
        self.filename = 'spaces.yml'
        self.tmp_walk = []
        self.spaces = []
        self.unpacked = []
        self.raw = {}
        self.opened_windows = [] # keep track of window ID's.. this is used in window_controller.py

        dir_path = os.path.join(os.path.expanduser('~'), '.config/envi/')
        self.getid_sh = os.path.join(dir_path, 'getid.sh')

        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
            except Exception as e:
                print(e)
                sys.exit(1)

        file_path = os.path.join(dir_path, self.filename)
        self.filepath = file_path
        if not os.path.exists(file_path):
            default = {
                'dev': {
                    'gnome-terminal': {
                        'x': 50,
                        'y': 50,
                        'width': 400,
                        'height': 200
                    },
                    'nautilus': {
                        'x': 450,
                        'y': 50,
                        'width': 800,
                        'height': 600
                    }
                }
            }
            try:
                with io.open(file_path, 'w', encoding='utf8') as f:
                    yaml.dump(default, f, default_flow_style=False, allow_unicode=True)
            except Exception as e:
                print(e)
                sys.exit(1)

        self.unpack()

    def unpack(self):
        data = None

        try:
            with open(self.filepath) as stream:
                try:
                    data = yaml.load(stream)
                except yaml.YAMLError as e:
                    msg = "error loading yaml: {}".format(e)
                    bail(msg, 1)
        except Exception as e:
            print(e)
            sys.exit(1)

        if data == None:
            return False

        self.raw = data
        self.walk(data)
        del self.tmp_walk

        for s in data.items():
            for x in s:
                if isinstance(x, dict):
                    self.spaces.append(s[0])

        return data


    def walk(self, d):
        for k, v in d.items():
            if isinstance(v, str) or isinstance(v, int) or isinstance(v, float):
                self.tmp_walk.append(k)
                line_text = "{}={}".format(".".join(self.tmp_walk), v)
                self.unpacked.append(line_text)
                self.tmp_walk.pop()
            elif v is None:
                self.tmp_walk.append(k)
                # hm
                self.tmp_walk.pop()
            elif isinstance(v, dict):
                self.tmp_walk.append(k)
                line_text = "{}".format(".".join(self.tmp_walk))
                self.unpacked.append(line_text)
                self.walk(v)
                self.tmp_walk.pop()
            else:
                print("type {} not recognized: {}.{}={}".format(type(v), ".".join(self.tmp_walk), k, v))

    def dump(self):
        print('Config: {}'.format(hex(id(self))))
        for attr in vars(self):
            print("  %s: %r" % (attr, getattr(self, attr)))
