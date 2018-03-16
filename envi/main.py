#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from time import sleep
import textwrap

from .window_controller import WindowController
from .config import Config
from .space import Space
from .util import bail

__version__ = '1.0.0'

config = None
args = None


def get_window_id(seconds: float):

    wc = WindowController(capture=True)
    config = Config()
    id = wc.command.run(config.getid_sh)
    return id


def focus_window_by_id(id):
    wc = WindowController(capture=True)
    config = Config()
    wc.command.run("wmctrl -a {winid} -i".format(winid=id))

def capture(seconds: float):

    # Passing capture=True prevents WindowController from attempting to
    # begin its 'window flow', which attempts to spawn windows that belong
    # to the specified space. Since no space has been specified, we don't
    # want that to happen. There's a better way to do this. I'll do it later.
    wc = WindowController(capture=True)

    config = Config()

    sleep(seconds)

    # Get window title and id
    # title = wc.command.run("xdotool getwindowfocus getwindowname")
    id = wc.command.run(config.getid_sh)

    # Get position
    tl_x = "xwininfo -all -int -id {} | grep Absolute | grep X | cut -d ':' -f2 | sed 's/ //g'".format(id)
    tl_y = "xwininfo -all -int -id {} | grep Absolute | grep Y | cut -d ':' -f2 | sed 's/ //g'".format(id)
    top_left_x = wc.command.run(tl_x)
    top_left_y = wc.command.run(tl_y)

    # Get dimensions
    w = "xwininfo -all -int -id {} | grep Width | cut -d ':' -f2 | cut -d ' ' -f2".format(id)
    h = "xwininfo -all -int -id {} | grep Height | cut -d ':' -f2 | cut -d ' ' -f2".format(id)
    width = wc.command.run(w)
    height = wc.command.run(h)

    # Display it nicely
    out = """
id:     {}
height: {}
width:  {}
x:      {}
y:      {} [ -28 = {} ]
""".format(id, height, width, top_left_x, top_left_y, str(int(top_left_y)-28))
    print(out)

    return id


def main():

    try:
      config = Config()
    except Exception as e:
      bail('config error: {}'.format(e), 1)

    # Was -v passed to space?
    if hasattr(args, 'verbose'):
      vb = getattr(args, 'verbose')
      if vb is True:
        config.verbose = True

    # envi list [...]
    if hasattr(args, 'thing_to_list'):
        import json

        if args.thing_to_list == 'spaces':
            for space in config.spaces:
                print(space)

        if args.thing_to_list == 'config':
            print(json.dumps(config.raw, sort_keys=True, indent=2))
        bail(None, 0)

    # envi space [...]
    if hasattr(args, 'space_name'):

        # Get the current window ID. Probably a terminal.
        # We want to check this against whatever the first application is.
        # Wait for this to change, then proceed..
        config.last_window_id = get_window_id(seconds=0)
        config.opened_windows.append(config.last_window_id)
        config.starting_window = config.last_window_id

        space = Space(args.space_name, config)
        for app in space.apps:
            app.create()

        focus_window_by_id(config.starting_window)

        bail(None, 0)

    # envi capture [...]
    if hasattr(args, 'capture_seconds'):
        capture(args.capture_seconds)
        bail(None, 0)


if __name__ == 'envi.main':

    parser = argparse.ArgumentParser(prog='envi',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     usage='%(prog)s [options…]',
                                     epilog='https://github.com/nvms/envi',
                                     add_help=False,
                                     description=textwrap.dedent('''\
                                     Automated window size and position tool.
                                     ----------------------------------------
                                       config location:
                                         ~/.config/envi/spaces.yml
                                     ----------------------------------------
                                     '''))
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(__version__))

    subparsers = parser.add_subparsers()

    space_parser = subparsers.add_parser('space')
    capture_parser = subparsers.add_parser('capture')
    list_parser = subparsers.add_parser('list')

    space_parser.add_argument('-v', '--verbose', action='store_true', help='turn verbose mode on')

    space_required = space_parser.add_argument_group('required')
    space_required.add_argument('space_name',
                                help='the name of the space')

    capture_required = capture_parser.add_argument_group('required')
    capture_required.add_argument('capture_seconds',
                                  type=float,
                                  help='the amount of time to wait before the window capture')

    list_required = list_parser.add_argument_group('required')
    list_required.add_argument('thing_to_list',
                               type=str,
                               help='list what?',
                               choices=['spaces', 'config'])

    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    main()
