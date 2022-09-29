# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest
import unittest


class TestVoid(TypeTest):
    def test_00_void_is_not_object_type(self):
        self.assertEqual(False, JavaBuiltInTypes.VOID.is_object_type)

    def test_01_void_is_not_instantiable(self):
        self.assertEqual(False, JavaBuiltInTypes.VOID.is_instantiable)

    def test_02_void_is_subtype_of_itself(self):
        self.assertSubtype(JavaBuiltInTypes.VOID, JavaBuiltInTypes.VOID)

    def test_03_void_is_not_subtype_of_anything_else(self):
        self.assertNotSubtype(JavaBuiltInTypes.VOID, JavaBuiltInTypes.OBJECT)
        self.assertNotSubtype(JavaBuiltInTypes.VOID, JavaBuiltInTypes.NULL)
        self.assertNotSubtype(JavaBuiltInTypes.VOID, JavaBuiltInTypes.BOOLEAN)
        self.assertNotSubtype(JavaBuiltInTypes.VOID, Graphics.rectangle)

    def test_04_nothing_is_subtype_of_void(self):
        self.assertNotSubtype(JavaBuiltInTypes.OBJECT, JavaBuiltInTypes.VOID)
        self.assertNotSubtype(JavaBuiltInTypes.NULL, JavaBuiltInTypes.VOID)
        self.assertNotSubtype(JavaBuiltInTypes.BOOLEAN, JavaBuiltInTypes.VOID)
        self.assertNotSubtype(Graphics.rectangle, JavaBuiltInTypes.VOID)

    def test_05_object_params_accept_null(self):
        # For example:
        #
        #     Rectangle rect;
        #
        #     rect.setFillColor(null);
        #
        self.assertNoCompileErrors(
            JavaMethodCall(
                JavaVariable("rect", Graphics.rectangle),
                "setFillColor",
                JavaNullLiteral()))

    def test_06_cannot_call_method_on_void(self):
        # For example:
        #
        #     Rectangle rect;
        #     Color red;
        #
        #     rect.setFillColor(red).hashCode();
        #
        self.assertCompileError(
            NoSuchJavaMethod,
            "Type void does not have methods",
            JavaMethodCall(
                JavaMethodCall(
                    JavaVariable("rect", Graphics.rectangle),
                    "setFillColor",
                    JavaVariable("red", Graphics.color)),
                "hashCode"))

    def test_07_cannot_instantiate_void(self):
        # For example:
        #
        #     new void();
        #
        self.assertCompileError(
            JavaIllegalInstantiationError,
            "Type void is not instantiable",
            JavaConstructorCall(
                JavaBuiltInTypes.VOID))

    def test_08_cannot_assign_void_return_value_to_variable(self):
        # For example:
        #
        #     Object x;
        #     Color red;
        #
        #     x = rect.setFill(red);
        #
        self.assertCompileError(
            JavaTypeMismatchError,
            "Cannot assign void to variable x of type Object",
            JavaAssignment(
                JavaVariable("x", JavaBuiltInTypes.OBJECT),
                JavaMethodCall(
                    JavaVariable("rect", Graphics.rectangle),
                    "setFillColor",
                    JavaVariable("red", Graphics.color))))

    def test_09_method_call_does_not_allow_void_passed_as_argument(self):
        # For example:
        #
        #     Rectangle rect;
        #     Color red;
        #
        #     rect.setFillColor(              // causes error here
        #         rect.setStrokeColor(red));  // setStrokeColor() returns void
        #
        self.assertCompileError(
            JavaTypeMismatchError,
            "Rectangle.setFillColor() expects arguments of type (Paint), but got (void)",
            JavaMethodCall(
                JavaVariable("rect", Graphics.rectangle),
                "setFillColor",
                JavaMethodCall(
                    JavaVariable("rect", Graphics.rectangle),
                    "setStrokeColor",
                    JavaVariable("red", Graphics.color))))


if __name__ == '__main__':
    unittest.main()
