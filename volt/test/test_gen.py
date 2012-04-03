# -*- coding: utf-8 -*-
"""
------------------
volt.test.test_gen
------------------

Tests for volt.gen.

:copyright: (c) 2012 Wibowo Arindrarto <bow@bow.web.id>
:license: BSD

"""


import unittest

from mock import patch

from volt.engine.core import Engine
from volt.gen import Generator
from volt.plugin.core import Plugin
from volt.test import INSTALL_DIR, USER_DIR, make_sessionconfig_mock


SessionConfig_mock = make_sessionconfig_mock()


@patch('volt.gen.CONFIG.VOLT.ROOT_DIR', USER_DIR)
@patch('volt.gen.CONFIG', SessionConfig_mock)
class GenCases(unittest.TestCase):

    def setUp(self):
        self.gen = Generator()

    @patch('volt.gen.path_import')
    def test_get_processor_class_unknown_type(self, path_import_mock):
        builtin_engine_name = 'volt.test.fixtures.install_dir.engine.builtins.in_install'
        path_import_mock.return_value = __import__(builtin_engine_name)
        self.assertRaises(AssertionError, self.gen.get_processor_class, \
                'in_install', 'foo', INSTALL_DIR)

    def test_get_processor_class_unknown_name(self):
        self.assertRaises(ImportError, self.gen.get_processor_class, \
                'foo', 'engines', INSTALL_DIR)

    def test_get_processor_class_builtin_engine(self):
        returned = self.gen.get_processor_class('in_install', 'engines', \
                INSTALL_DIR)
        self.assertEqual(returned.__name__, 'TestBuiltinEngine')
        self.assertTrue(issubclass(returned, Engine))

    def test_get_processor_class_user_engine(self):
        returned = self.gen.get_processor_class('in_user', 'engines', \
                INSTALL_DIR)
        self.assertEqual(returned.__name__, 'TestUserEngine')
        self.assertTrue(issubclass(returned, Engine))

    def test_get_processor_class_both_engine(self):
        returned = self.gen.get_processor_class('in_both', 'engines', \
                INSTALL_DIR)
        self.assertEqual(returned.__name__, 'TestUserEngine')
        self.assertTrue(issubclass(returned, Engine))

    def test_get_processor_class_builtin_plugin(self):
        returned = self.gen.get_processor_class('in_install', 'plugins', \
                INSTALL_DIR)
        self.assertEqual(returned.__name__, 'TestBuiltinPlugin')
        self.assertTrue(issubclass(returned, Plugin))

    def test_get_processor_class_user_plugin(self):
        returned = self.gen.get_processor_class('in_user', 'plugins', \
                INSTALL_DIR)
        self.assertEqual(returned.__name__, 'TestUserPlugin')
        self.assertTrue(issubclass(returned, Plugin))

    def test_get_processor_class_both_plugin(self):
        returned = self.gen.get_processor_class('in_both', 'plugins', \
                INSTALL_DIR)
        self.assertEqual(returned.__name__, 'TestUserPlugin')
        self.assertTrue(issubclass(returned, Plugin))
