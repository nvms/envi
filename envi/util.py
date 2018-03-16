#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


def bail(msg, code=0):
    if not msg == None:
        print(msg)
    sys.exit(code)


def toast(msg):
    if not msg == None:
        print(msg)


def remove_text_inside_brackets(text, brackets="()[]"):
    count = [0] * (len(brackets) // 2) # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b: # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1)**is_close # `+1`: open, `-1`: close
                if count[kind] < 0: # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else: # character is not a [balanced] bracket
            if not any(count): # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars)


def unique_list(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def verbose_mode(config):
    if hasattr(config, 'verbose'):
        vb = getattr(config, 'verbose')
        if vb is True:
            return True
    return False