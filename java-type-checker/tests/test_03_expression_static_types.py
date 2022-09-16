# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest
import unittest


class TestExpressionStaticTypes(TypeTest):

    def test_00_variable_static_type_is_its_declared_type(self):
        # For example:
        #
        #     Point p;
        #
        #     p   ← static type of this expression is Point
        #
        self.assertEqual(
            Graphics.point,
            JavaVariable("p", Graphics.point).static_type())

    def test_01_literal_static_type_is_its_type(self):
        # For example:
        #
        #     3   ← static type of this expression is int
        #
        self.assertEqual(
            JavaBuiltInTypes.INT,
            JavaLiteral("3", JavaBuiltInTypes.INT).static_type())

    def test_02_assignment_static_type_is_lhs_type(self):
        # For example:
        #
        #     GraphicsObject g;
        #     Rectangle r;
        #
        #     g = r  ← static type of the expression is GraphicsObject (not Rectangle)
        #
        self.assertEqual(
            Graphics.graphics_object,
            JavaAssignment(
                JavaVariable("g", Graphics.graphics_object),
                JavaVariable("r", Graphics.rectangle)
            ).static_type())

    def test_03_method_call_static_type_is_method_return_type(self):
        # For example:
        #
        #     Point p;
        #
        #     p.getX()  ← static type is double, because the getX method of Point returns double
        #
        self.assertEqual(
            JavaBuiltInTypes.DOUBLE,
            JavaMethodCall(JavaVariable("p", Graphics.point), "getX").static_type())

if __name__ == '__main__':
    unittest.main()
