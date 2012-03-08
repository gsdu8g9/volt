# -*- coding: utf-8 -*-
"""
---------------------
volt.test.test_plugin
---------------------

Tests for the volt.plugin module.

:copyright: (c) 2012 Wibowo Arindrarto <bow@bow.web.id>
:license: BSD

"""


import unittest

from volt.plugins import Plugin


class TestPlugin(unittest.TestCase):

    def test_run(self):
        self.assertRaises(NotImplementedError, Plugin().run, )
