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

import doctest
from operator import itemgetter

from textwrap import dedent

from hypothesis import given
from hypothesis.strategies import integers, just, text, tuples, lists

from testtools import TestCase
from testtools.matchers import DocTestMatches

from .._text import (
    format_tree,
)


def generate_tree(depth):
    """Make a tree of the given depth.

    e.g.
    ('foo',
      [('bar',
        [('qux', []),
         ('baz', []),
        ]),
       ('shop',
        [('pet', [])]),
      ],
    )
    """
    if depth < 1:
        raise ValueError('Cannot make tree of depth {}'.format(depth))
    if depth == 1:
        return tuples(text(), just([]))
    else:
        return tuples(text(), lists(generate_tree(depth - 1), max_size=5))


def traverse_depth_first(tree, format_node, get_children):
    yield format_node(tree)
    for child in get_children(tree):
        for node in traverse_depth_first(child, format_node, get_children):
            yield node


class TestFormatTree(TestCase):

    def format_tree(self, tree):
        return format_tree(tree, itemgetter(0), itemgetter(1))

    @given(text())
    def test_single_node_tree(self, label):
        tree = (label, [])
        output = self.format_tree(tree)
        self.assertEqual(u'{}\n'.format(label), output)

    @given(integers(min_value=1, max_value=10).flatmap(generate_tree))
    def test_labels_appear_in_order(self, tree):
        output = self.format_tree(tree)
        index = 0
        dfs_nodes = traverse_depth_first(tree, itemgetter(0), itemgetter(1))
        for label in dfs_nodes:
            index = output[index:].find(label)
            self.assertNotEqual(-1, index)

    def test_single_level_tree(self):
        tree = (
            'foo', [
                ('bar', []),
                ('baz', []),
                ('qux', []),
            ],
        )
        output = self.format_tree(tree)
        self.assertEqual(dedent(u'''\
        foo
        ├── bar
        ├── baz
        └── qux
        '''), output)

    def test_multi_level_tree(self):
        tree = (
            'foo', [
                ('bar', [
                    ('a', []),
                    ('b', []),
                ]),
                ('baz', []),
                ('qux', []),
            ],
        )
        output = self.format_tree(tree)
        self.assertEqual(dedent(u'''\
        foo
        ├── bar
        │   ├── a
        │   └── b
        ├── baz
        └── qux
        '''), output)

    def test_multi_level_on_last_node_tree(self):
        tree = (
            'foo', [
                ('bar', []),
                ('baz', []),
                ('qux', [
                    ('a', []),
                    ('b', []),
                ]),
            ],
        )
        output = self.format_tree(tree)
        self.assertEqual(dedent(u'''\
        foo
        ├── bar
        ├── baz
        └── qux
            ├── a
            └── b
        '''), output)

    def test_acceptance(self):
        output = self.format_tree(ACCEPTANCE_INPUT)
        self.assertThat(
            output,
            DocTestMatches(
                ACCEPTANCE_OUTPUT,
                doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_NDIFF))


def d(name, files):
    return (name, files)


def f(name):
    return (name, [])


ACCEPTANCE_INPUT = \
    d(u'.', [
        f(u'cabal.sandbox.config'),
        f(u'config.yaml'),
        d(u'dist', [
            d(u'build', [
                d(u'autogen', [
                    f(u'cabal_macros.h'),
                    f(u'Paths_hodor.hs'),
                ]),
                d(u'hodor', [
                    f(u'hodor'),
                    d(u'hodor-tmp', [
                        d(u'Hodor', map(f, [
                            u'Actions.hi',
                            u'Actions.o',
                            u'CommandLine.hi',
                            u'CommandLine.o',
                            u'Commands.hi',
                            u'Commands.o',
                            u'Config.hi',
                            u'Config.o',
                            u'File.hi',
                            u'File.o',
                            u'Format.hi',
                            u'Format.o',
                            u'Functional.hi',
                            u'Functional.o',
                            u'Parser.hi',
                            u'Parser.o',
                            u'Types.hi',
                            u'Types.o',
                        ])),
                        f(u'Hodor.hi'),
                        f(u'Hodor.o'),
                        f(u'Main.hi'),
                        f(u'Main.o'),
                    ]),
                ]),
            ]),
            f(u'package.conf.inplace'),
            f(u'setup-config'),
        ]),
        d(u'Hodor', map(f, [
            u'Actions.hs',
            u'CommandLine.hs',
            u'Commands.hs',
            u'Config.hs',
            u'File.hs',
            u'Format.hs',
            u'Functional.hs',
            u'Parser.hs',
            u'Reports.hs',
            u'Types.hs',
        ])),
        f(u'hodor.cabal'),
        f(u'Hodor.hs'),
        f(u'LICENSE'),
        f(u'Main.hs'),
        f(u'notes.md'),
        f(u'Setup.hs'),
        d(u'Tests', map(f, [
            u'FormatSpec.hs',
            u'Generators.hs',
            u'ParserSpec.hs',
            u'TypesSpec.hs',
        ])),
        f(u'Tests.hs'),
        f(u'todo.txt'),
    ])


ACCEPTANCE_OUTPUT = u'''\
.
├── cabal.sandbox.config
├── config.yaml
├── dist
│   ├── build
│   │   ├── autogen
│   │   │   ├── cabal_macros.h
│   │   │   └── Paths_hodor.hs
│   │   └── hodor
│   │       ├── hodor
│   │       └── hodor-tmp
│   │           ├── Hodor
│   │           │   ├── Actions.hi
│   │           │   ├── Actions.o
│   │           │   ├── CommandLine.hi
│   │           │   ├── CommandLine.o
│   │           │   ├── Commands.hi
│   │           │   ├── Commands.o
│   │           │   ├── Config.hi
│   │           │   ├── Config.o
│   │           │   ├── File.hi
│   │           │   ├── File.o
│   │           │   ├── Format.hi
│   │           │   ├── Format.o
│   │           │   ├── Functional.hi
│   │           │   ├── Functional.o
│   │           │   ├── Parser.hi
│   │           │   ├── Parser.o
│   │           │   ├── Types.hi
│   │           │   └── Types.o
│   │           ├── Hodor.hi
│   │           ├── Hodor.o
│   │           ├── Main.hi
│   │           └── Main.o
│   ├── package.conf.inplace
│   └── setup-config
├── Hodor
│   ├── Actions.hs
│   ├── CommandLine.hs
│   ├── Commands.hs
│   ├── Config.hs
│   ├── File.hs
│   ├── Format.hs
│   ├── Functional.hs
│   ├── Parser.hs
│   ├── Reports.hs
│   └── Types.hs
├── hodor.cabal
├── Hodor.hs
├── LICENSE
├── Main.hs
├── notes.md
├── Setup.hs
├── Tests
│   ├── FormatSpec.hs
│   ├── Generators.hs
│   ├── ParserSpec.hs
│   └── TypesSpec.hs
├── Tests.hs
└── todo.txt
'''
