# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest


class TestNestedTypeChecking(TypeTest):
    def test_00_passes_deep_expression(self):
        # For example:
        #
        #     GraphicsGroup group0;
        #     GraphicsGroup group1;
        #     Rectangle rect;
        #
        #     group1.add(
        #         group0.getElementAt(
        #             rect.getPosition()));

        group0 = JavaVariable("group0", Graphics.graphics_group)
        group1 = JavaVariable("group1", Graphics.graphics_group)
        rect = JavaVariable("rect", Graphics.rectangle)

        self.assertNoCompileErrors(
            JavaMethodCall(
                group1,
                "add",
                JavaMethodCall(
                    group0,
                    "getElementAt",
                    JavaMethodCall(rect, "getPosition"))))

    def test_01_catch_type_error_in_assignment_rhs(self):
        # For example:
        #
        #     GraphicsObject gobj;
        #     GraphicsGroup group;
        #     Rectangle rect;
        #
        #     gobj = group.getElementAt(rect);

        gobj = JavaVariable("gobj", Graphics.graphics_object)
        group = JavaVariable("group", Graphics.graphics_group)
        rect = JavaVariable("rect", Graphics.rectangle)

        self.assertCompileError(
            JavaTypeMismatchError,
            "GraphicsGroup.getElementAt() expects arguments of type (Point), but got (Rectangle)",
            JavaAssignment(
                gobj,
                JavaMethodCall(group, "getElementAt", rect)))

    def test_02_method_call_children_get_type_checked_first(self):
        # For example:
        #
        #     Rectangle rect;
        #     GraphicsGroup group;
        #     Color red;
        #
        #     rect.setFillColor(           // Should not flag this “GraphicsObject ≠ Paint” error...
        #         group.getElementAt(red)); // ...because it detects this type error first

        rect = JavaVariable("rect", Graphics.rectangle)
        group = JavaVariable("group", Graphics.graphics_group)
        red = JavaVariable("red", Graphics.color)

        self.assertCompileError(
            JavaTypeMismatchError,
            "GraphicsGroup.getElementAt() expects arguments of type (Point), but got (Color)",
            JavaMethodCall(
                rect,
                "setFillColor",
                JavaMethodCall(
                    group,
                    "getElementAt",
                    red)))

    def test_03_catches_wrong_method_name_in_deep_expression(self):
        # For example:
        #
        #     GraphicsGroup group0;
        #     GraphicsGroup group1;
        #     Rectangle rect;
        #
        #     group1.add(
        #         group0.getElementAt(
        #             rect.getFunky()));  // error here

        group0 = JavaVariable("group0", Graphics.graphics_group)
        group1 = JavaVariable("group1", Graphics.graphics_group)
        rect = JavaVariable("rect", Graphics.rectangle)

        self.assertCompileError(
            NoSuchJavaMethod,
            "Rectangle has no method named getFunky",
            JavaMethodCall(
                group1,
                "add",
                JavaMethodCall(
                    group0,
                    "getElementAt",
                    JavaMethodCall(rect, "getFunky"))))


    def test_04_catches_wrong_arg_type_in_deep_expression(self):
        # For example:
        #
        #     GraphicsGroup group0;
        #     GraphicsGroup group1;
        #     Rectangle rect;
        #
        #     group1.add(
        #         group0.getElementAt(   // error in this method call...
        #             rect.getSize()));  // ...because of this arg

        group0 = JavaVariable("group0", Graphics.graphics_group)
        group1 = JavaVariable("group1", Graphics.graphics_group)
        rect = JavaVariable("rect", Graphics.rectangle)

        self.assertCompileError(
            JavaTypeMismatchError,
            "GraphicsGroup.getElementAt() expects arguments of type (Point), but got (Size)",
            JavaMethodCall(
                group1,
                "add",
                JavaMethodCall(
                    group0,
                    "getElementAt",
                    JavaMethodCall(rect, "getSize"))))

    def test_05_catches_type_error_in_method_call_receiver(self):
        # For example:
        #
        #     Window window;
        #
        #     window
        #         .getSize(37)  // error here
        #         .getWidth();
        #
        self.assertCompileError(
            JavaArgumentCountError,
            "Wrong number of arguments for Window.getSize(): expected 0, got 1",
            JavaMethodCall(
                JavaMethodCall(
                    JavaVariable("window", Graphics.window),
                    "getSize",
                    JavaLiteral("37", JavaBuiltInTypes.INT)),
                "getWidth"))
