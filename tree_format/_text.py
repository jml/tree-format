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


FORK = u'\u251c'
LAST = u'\u2514'
VERTICAL = u'\u2502'
HORIZONTAL = u'\u2500'


def _format_tree(node, format_node, get_children):
    yield format_node(node)
    children = get_children(node)
    for child in children[:-1]:
        yield ''.join([FORK, HORIZONTAL, HORIZONTAL, ' ', format_node(child)])
    if children:
        yield ''.join([LAST, HORIZONTAL, HORIZONTAL, ' ', format_node(children[-1])])


def format_tree(node, format_node, get_children):
    return u'\n'.join(_format_tree(node, format_node, get_children)) + u'\n'


def print_tree():
    print format_tree()
