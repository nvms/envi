#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from .config import Config
from .util import *
from .app import App
from .window_controller import WindowController


class Space(object):

    def __init__(self, name: str, config: Config):

        self.requested_space = name
        self.config = config
        self.data = {}
        self.appdict = {}
        self.apps = []
        self.settings = {}

        self.args = []
        self.args_parent_app = []

        found_in_config = False
        new_space = True

        # for line in self.config.unpacked:
        #     print(line)

        for line in self.config.unpacked:

            if '.' in line:

                # space.setting=val
                # Something that gets unpacked like that is meant
                # to be a SETTING specific to a space, like:
                #
                #  - What workspace does this belong on?
                if line.count('.') == 1:
                    try:
                        space, setting = line.split('.')
                    except Exception as e:
                        bail('you have a config error on this line: {}'.format(line), 1)

                    # Make sure we're looking at the right part of the config
                    if space == self.requested_space:
                        if "=" in line:
                            s, v = setting.split('=')
                            self.settings.update({s:v})

                        # We'll actually do something with these
                        # settings later. Not sure how to approach that
                        # yet.



                else:

                    prop = None

                    if space == self.requested_space:
                        found_in_config = True


                    # Does this application have an argument?
                    if "[" in line and "]" in line:
                        
                        # Get the arguments
                        args = line[line.find("[")+1:line.find("]")]

                        # Remove it from this line so that we can parse it normally
                        # If we don't, the packed version looks weird, like this:
                        #  - music.firefox[www.reddit.com].height=1426
                        #
                        # We won't parse that, but we will parse this:
                        #  - music.firefox.height=1426
                        line = remove_text_inside_brackets(line)

                        # No = in line, this must be an application line
                        if not "=" in line:
                            try:
                                space, app = line.split('.')
                            except Exception as e:
                                bail('you have a config error on this line: {}'.format(line), 1)
                        else:
                            # Parse the rest of the line.
                            # Get the parent app of these particular arguments
                            # and save the name of the app to args_parent_app
                            try:
                                space, app, prop = line.split('.')
                            except Exception as e:
                                bail('you have a config error on this line: {}'.format(line), 1)

                        # Save the argument only if we are requesting this space
                        if self.requested_space == space:
                            self.args.append(args)
                            self.args_parent_app.append(app)

                            # Now we need to uniqify these two lists
                            self.args = unique_list(self.args)
                            self.args_parent_app = unique_list(self.args_parent_app)

                        # So args[0] should contain the arguments for args_parent_app[0]
                        # etc, etc, etc

                    # No = in line, this must be an application line
                    if not "=" in line:
                        try:
                            space, app = line.split('.')
                        except Exception as e:
                            bail('you have a config error on this line: {}'.format(line), 1)
                    else:
                        # Back to parsing for app properties and values
                        try:
                            space, app, prop = line.split('.')
                        except Exception as e:
                            bail('you have a config error on this line: {}'.format(line), 1)

                    # This is used to know if we need to create a new dictionary
                    # that will be used to store the app data
                    if not space in self.data:
                        self.data[space] = {}

                    if space == self.requested_space:
                        if app not in self.data[space].keys():
                            self.data[space][app] = {}

                        if prop:
                            prop, val = prop.split('=')
                            self.data[space][app][prop] = val

                        # Check for arguments
                        if self.args_parent_app:
                            # Does this application have arguments?
                            for i, j in enumerate(self.args_parent_app):
                                if j == app:
                                    self.data[space][app]['args'] = self.args[i]

            else:
                if "=" in line:
                    # No '.' found on this line, but it has a "="
                    # This must be a global config variable.
                    # Add it to Config. It's not specific to a Space.
                    p, v = line.split('=')
                    self.config.__setattr__(p, v)

        # We never found the requested space.
        # Print a message and then bail.
        if not found_in_config:
            msg = """error
no space with the name '{}' exists in your config
spaces defined in config: {}""".format(self.requested_space, ' '.join(config.spaces))

            bail(msg, 1)

        for app in self.data[self.requested_space]:
            self.appdict[app] = {}
            a = App()
            a.__setattr__('name', app)
            a.__setattr__('config', self.config)
            for p, v in self.data[self.requested_space][app].items():
                self.appdict[app][p] = v
                a.__setattr__(p, v)
            self.apps.append(a)

        # Now that the App object has been created, and had its
        # attributes passed on to it, we don't need the data dict
        # any more. It has served its purpose.
        del self.data
        # This was just a throwaway dict. I could have done this better.
        del self.appdict

        # self.dump()


    def dump(self):
        print('Space: {}'.format(hex(id(self))))
        for attr in vars(self):
            print("  %s: %r" % (attr, getattr(self, attr)))
        print('')
