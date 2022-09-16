# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
import unittest


class TestClassStructure(unittest.TestCase):

    def test_00_finds_method_by_name(self):
        method = Graphics.point.method_named("getX")
        self.assertEqual("getX", method.name)

    def test_01_finds_method_from_supertype(self):
        method = Graphics.point.method_named("hashCode")
        self.assertEqual("hashCode", method.name)

    def test_02_finds_method_from_indirect_supertype(self):
        method = Graphics.rectangle.method_named("hashCode")
        self.assertEqual("hashCode", method.name)

    def test_03_raises_no_such_method(self):
        with self.assertRaisesRegex(NoSuchJavaMethod, "ergleflopse"):
            Graphics.point.method_named("ergleflopse")


if __name__ == '__main__':
    unittest.main()
