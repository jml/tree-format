# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Jonathan M. Lange <jml@mumak.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Library for formatting trees."""

import itertools


FORK = u'\u251c'
LAST = u'\u2514'
VERTICAL = u'\u2502'
HORIZONTAL = u'\u2500'


def _format_tree(node, format_node, get_children, prefix=''):
    children = get_children(node)
    next_prefix = u''.join([prefix, VERTICAL, u'   '])
    for child in children[:-1]:
        yield u''.join([prefix, FORK, HORIZONTAL, HORIZONTAL, u' ', format_node(child)])
        for result in _format_tree(child, format_node, get_children, next_prefix):
            yield result
    if children:
        last_prefix = u''.join([prefix, u'    '])
        yield u''.join([prefix, LAST, HORIZONTAL, HORIZONTAL, u' ', format_node(children[-1])])
        for result in _format_tree(children[-1], format_node, get_children, last_prefix):
            yield result


def format_tree(node, format_node, get_children):
    lines = itertools.chain(
        [format_node(node)],
        _format_tree(node, format_node, get_children),
        [u''],
    )
    return u'\n'.join(lines)


def print_tree(*args, **kwargs):
    print format_tree(*args, **kwargs)
