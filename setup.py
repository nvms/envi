#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup
from setuptools.command.install import install

PACKAGE = 'envi'
NAME = 'envi'
DESCRIPTION = 'Automated X window size and position tool.'
AUTHOR = 'nvms'
AUTHOR_EMAIL = 'jon@pye.rs'
VERSION = '1.0.0'

if (os.name == "posix") or (os.name == "nt"):
    print("sorry, envi is not compatible with this OS")
    sys.exit(1)

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config/envi/')

class EnviInstall(install):
    """ Custom setuptools install that ensures the config directory exists. """
    def run(self):

        if not os.path.exists(CONFIG_PATH):
            try:
                print('[envi] Creating config directory: {dir}'.format(dir=CONFIG_PATH))
                os.makedirs(CONFIG_PATH)
            except Exception as exc:
                print('[envi] ABORT! Failed to create config directory..')
                print('[envi] Do you not have permission to ~/.config for some reason?')
                print(exc)
                sys.exit(1)

        install.run(self)

        msg = """             _                           _   
 ___ ___ _ _|_|___ ___ ___ _____ ___ ___| |_ 
| -_|   | | | |  _| . |   |     | -_|   |  _|
|___|_|_|\_/|_|_| |___|_|_|_|_|_|___|_|_|_| 
                      ___ ___ ___ ___ ___ ___ 
                     |_ -| . | .'|  _| -_|_ -|
                     |___|  _|__,|___|___|___|
                         |_| 

[envi] Installed successfully.
[envi] Config location: {cfg_loc}
[envi] For usage information, vist: https://github.com/nvms/envi
""".format(cfg_loc=os.path.join(CONFIG_PATH, "spaces.yml"))

        print(msg)

OPTIONS = dict(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    cmdclass={
        'install': EnviInstall,
    },
    packages=['envi'],
    data_files=[
        (CONFIG_PATH, ['spaces.yml', 'getid.sh'])
    ],
    entry_points={
        'console_scripts': [
            'envi = envi.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications',
        'Topic :: Desktop Environment'
    ]
)

setup(**OPTIONS)
