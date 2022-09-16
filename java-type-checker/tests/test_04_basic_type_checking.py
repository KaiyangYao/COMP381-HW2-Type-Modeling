# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest
import unittest


class TestBasicTypeChecking(TypeTest):

    def test_00_variables_never_have_type_errors(self):
        """It is never possible for a reference to a variable to have a type error. It might be used
        in a _context_ where the type of the variable is wrong, but then the type error happens
        in that context, somewhere up the tree. The variable reference itself — just saying `x` —
        can never be a type error.
        """
        self.assertNoCompileErrors(
            JavaVariable("p", Graphics.point))

    def test_01_literals_never_have_type_errors(self):
        """Similarly, just stating a literal such as 3 or "hello" can never be a type error per se.
        """
        self.assertNoCompileErrors(
            JavaLiteral("3.72", JavaBuiltInTypes.DOUBLE))


if __name__ == '__main__':
    unittest.main()
