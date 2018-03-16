#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shlex
from subprocess import Popen, PIPE

class Commander(object):

    def __init__(self):
        pass

    def run(self, cmd, spawner=False):
        """ run chains Popens as needed """

        if spawner:
            command = 'nohup {} >/dev/null 2>&1 &'.format(cmd)
            os.system(command)
            return True

        if '|' in cmd:
            cmd_parts = cmd.split('|')
        else:
            cmd_parts = []
            cmd_parts.append(cmd)

        i = 0
        p = {}
        for part in cmd_parts:
            part = part.strip()
            if i == 0:
                p[i] = Popen(shlex.split(part), stdin=None, stdout=PIPE, stderr=PIPE)
            else:
                p[i] = Popen(shlex.split(part), stdin=p[i - 1].stdout, stdout=PIPE, stderr=PIPE)
            i = i + 1
        (output, err) = p[i - 1].communicate()
        exit_code = p[0].wait()

        return str(output.decode('utf-8')).strip()  # , str(err), exit_code
