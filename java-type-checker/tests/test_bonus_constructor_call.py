# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest
import unittest


@unittest.skip('This is a bonus problem.')
class TestConstructorTypeChecking(TypeTest):
    def test_00_object_instantiation_static_type_is_the_instantiated_type(self):
        # new Point()  ← static type is Point
        self.assertEqual(
            Graphics.point,
            JavaConstructorCall(Graphics.point).static_type())

    def test_01_cannot_instantiate_primitives(self):
        # For example:
        #
        #     new int()
        #
        self.assertCompileError(
            JavaIllegalInstantiationError,
            "Type int is not instantiable",
            JavaConstructorCall(
                JavaBuiltInTypes.INT))

    def test_02_flags_wrong_number_of_constructor_arguments(self):
        # For example:
        #
        #     Point p;
        #
        #     new Rectangle(p)
        #
        self.assertCompileError(
            JavaArgumentCountError,
            "Wrong number of arguments for Rectangle constructor: expected 2, got 1",
            JavaConstructorCall(
                Graphics.rectangle,
                JavaVariable("p", Graphics.point)))

    def test_03_flags_wrong_constructor_argument_type(self):
        #
        # For example:
        #
        #     Point p;
        #
        #     new Rectangle(p, true)
        #
        self.assertCompileError(
            JavaTypeMismatchError,
            "Rectangle constructor expects arguments of type (Point, Size), but got (Point, boolean)",
            JavaConstructorCall(
                Graphics.rectangle,
                JavaVariable("p", Graphics.point),
                JavaLiteral("true", JavaBuiltInTypes.BOOLEAN)))
