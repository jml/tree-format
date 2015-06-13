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

from operator import itemgetter
from textwrap import dedent

from testtools import TestCase

from .._text import (
    format_tree,
)


class TestFormatTree(TestCase):

    def format_tree(self, tree):
        return format_tree(tree, itemgetter(0), itemgetter(1))

    def test_single_node_tree(self):
        tree = ('foo', [])
        output = self.format_tree(tree)
        self.assertEqual(dedent(u'''\
        foo
        '''), output)

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
