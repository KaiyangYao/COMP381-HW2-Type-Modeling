# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest
import unittest


class TestMethodTypeChecking(TypeTest):
    def test_00_simple_method_call_passes(self):
        # For example:
        #
        #     Point p;
        #
        #     p.getX()
        #
        self.assertNoCompileErrors(
            JavaMethodCall(
                JavaVariable("p", Graphics.point),
                "getX"))

    def test_01_flags_nonexistent_method(self):
        # For example:
        #
        #     Point p;
        #
        #     p.getZ()
        #
        self.assertCompileError(
            NoSuchJavaMethod,
            "Point has no method named getZ",
            JavaMethodCall(
                JavaVariable("p", Graphics.point),
                "getZ"))

    def test_02_flags_too_many_arguments(self):
        # For example:
        #
        #     Point p;
        #
        #     p.getX(0.0, 1.0)
        #
        self.assertCompileError(
            JavaArgumentCountError,
            "Wrong number of arguments for Point.getX(): expected 0, got 2",
            JavaMethodCall(
                JavaVariable("p", Graphics.point),
                "getX",
                JavaLiteral("0.0", JavaBuiltInTypes.DOUBLE),
                JavaLiteral("1.0", JavaBuiltInTypes.DOUBLE)))

    def test_03_flags_too_few_arguments(self):
        # For example:
        #
        #     Rectangle r;
        #
        #     r.setPosition(0.0)
        #
        self.assertCompileError(
            JavaArgumentCountError,
            "Wrong number of arguments for Rectangle.setPosition(): expected 2, got 1",
            JavaMethodCall(
                JavaVariable("r", Graphics.rectangle),
                "setPosition",
                JavaLiteral("0.0", JavaBuiltInTypes.DOUBLE)))

    def test_04_flags_wrong_argument_type(self):
        # For example:
        #
        #     Rectangle r;
        #
        #     r.setPosition(0.0, true)
        #
        self.assertCompileError(
            JavaTypeMismatchError,
            "Rectangle.setPosition() expects arguments of type (double, double), but got (double, boolean)",
            JavaMethodCall(
                JavaVariable("rect", Graphics.rectangle),
                "setPosition",
                JavaLiteral("0.0", JavaBuiltInTypes.DOUBLE),
                JavaLiteral("true", JavaBuiltInTypes.BOOLEAN)))

    def test_05_allows_subtypes_for_arguments(self):
        # For example:
        #
        #     Rectangle rect;
        #     Color red;
        #
        #     rect.setFillColor(red)
        #
        self.assertNoCompileErrors(
            JavaMethodCall(
                JavaVariable("rect", Graphics.rectangle),
                "setFillColor",
                JavaVariable("red", Graphics.color)))

    def test_06_supports_complex_expression_as_receiver(self):
        # For example:
        #
        #     Rectangle rect;
        #     rect.getSize().getWidth()
        #
        self.assertNoCompileErrors(
            JavaMethodCall(
                JavaMethodCall(
                    JavaVariable("rect", Graphics.rectangle),
                    "getSize"),
                "getWidth"))

    def test_07_cannot_call_methods_on_primitives(self):
        # For example:
        #
        #     int x;
        #
        #     x.hashCode()
        #
        self.assertCompileError(
            NoSuchJavaMethod,
            "Type int does not have methods",
            JavaMethodCall(
                JavaVariable("x", JavaBuiltInTypes.INT),
                "hashCode"))


if __name__ == '__main__':
    unittest.main()
