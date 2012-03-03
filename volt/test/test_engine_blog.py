# -*- coding: utf-8 -*-
"""
--------------------------
volt.test.test_engine_blog
--------------------------

Tests for volt.engine.blog.

:copyright: (c) 2012 Wibowo Arindrarto <bow@bow.web.id>

"""


import os
import unittest

from volt.engine import Pack, TextUnit
from volt.engine.blog import BlogEngine
from volt.test.mocks import SessionConfig_Mock


class TestBlogEngine(unittest.TestCase):

    def setUp(self):
        self.engine = BlogEngine(SessionConfig_Mock)

    def test_process_text_units(self):
        self.engine.CONFIG.BLOG.CONTENT_DIR = os.path.join(\
                self.engine.CONFIG.BLOG.CONTENT_DIR, 'engine_pass')
        self.engine.units = self.engine.process_text_units(self.engine.CONFIG.BLOG)

        self.assertEqual(len(self.engine.units), 5)
        for unit in self.engine.units:
            self.assertTrue(hasattr(unit, 'path'))
            self.assertTrue(hasattr(unit, 'permalink'))

    def test_process_packs(self):
        self.engine.CONFIG.BLOG.POSTS_PER_PAGE = 3
        packs = self.engine.process_packs(Pack, range(10))
        self.assertEqual(len(packs), 4)
        for pack in packs:
            if packs.index(pack) != 3:
                self.assertEqual(len(pack.units), 3)
            else:
                self.assertEqual(len(pack.units), 1)

        self.engine.CONFIG.BLOG.POSTS_PER_PAGE = 10
        packs = self.engine.process_packs(Pack, range(3))
        self.assertEqual(len(packs), 1)
        for pack in packs:
            self.assertEqual(len(pack.units), 3)

        self.assertRaises(TypeError, self.engine.process_packs, TextUnit, range(5))
