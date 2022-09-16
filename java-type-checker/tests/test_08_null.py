# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest
import unittest


class TestNull(TypeTest):
    def test_00_null_is_object_type(self):
        self.assertEqual(True, JavaBuiltInTypes.NULL.is_object_type)

    def test_01_null_is_not_instantiable(self):
        self.assertEqual(False, JavaBuiltInTypes.NULL.is_instantiable)

    def test_02_null_is_subtype_of_all_object_types(self):
        self.assertSubtype(JavaBuiltInTypes.NULL, JavaBuiltInTypes.OBJECT)
        self.assertSubtype(JavaBuiltInTypes.NULL, Graphics.graphics_group)
        self.assertSubtype(JavaBuiltInTypes.NULL, Graphics.fillable)
        self.assertNotSubtype(JavaBuiltInTypes.OBJECT, JavaBuiltInTypes.NULL)
        self.assertNotSubtype(Graphics.graphics_group, JavaBuiltInTypes.NULL)
        self.assertNotSubtype(Graphics.fillable, JavaBuiltInTypes.NULL)

    def test_03_null_is_subtype_of_itself(self):
        self.assertSubtype(JavaBuiltInTypes.NULL, JavaBuiltInTypes.NULL)

    def test_04_null_is_not_subtype_of_primitives(self):
        self.assertNotSubtype(JavaBuiltInTypes.NULL, JavaBuiltInTypes.INT)
        self.assertNotSubtype(JavaBuiltInTypes.INT, JavaBuiltInTypes.NULL)

    # For example:
    #
    #     null   ← static type of this expression is the type NULL
    #
    def test_05_null_literal_static_type_is_null(self):
        self.assertEqual(
            JavaBuiltInTypes.NULL,
            JavaNullLiteral().static_type())

    def test_06_object_params_accept_null(self):
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

    def test_07_cannot_call_method_on_null(self):
        # For example:
        #
        #     null.hashCode();
        #
        self.assertCompileError(
            NoSuchJavaMethod,  # Think: why shouldn’t this be NullPointerException?
            "Cannot invoke method hashCode() on null",  # null provides a special error message
            JavaMethodCall(
                JavaNullLiteral(),
                "hashCode"))

    def test_08_cannot_pass_null_for_primitive(self):
        # For example:
        #
        #     Rectangle rect;
        #
        #     rect.setPosition(0.0, null);
        #
        rect = JavaVariable("rect", Graphics.rectangle)
        self.assertCompileError(
            JavaTypeMismatchError,
            "Rectangle.setPosition() expects arguments of type (double, double), but got (double, null)",
            JavaMethodCall(
                rect,
                "setPosition",
                JavaLiteral("0.0", JavaBuiltInTypes.DOUBLE),
                JavaNullLiteral()))


if __name__ == '__main__':
    unittest.main()
