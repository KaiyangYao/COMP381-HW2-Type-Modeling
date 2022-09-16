# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest
import unittest


class TestAssignmentTypeChecking(TypeTest):

    def test_00_assignments_allow_same_type(self):
        self.assertNoCompileErrors(
            JavaAssignment(
                JavaVariable("x", JavaBuiltInTypes.INT),
                JavaLiteral("1", JavaBuiltInTypes.INT)))

    def test_01_assignments_do_not_allow_unrelated_type(self):
        self.assertCompileError(
            JavaTypeMismatchError,
            "Cannot assign boolean to variable x of type int",
            JavaAssignment(
                JavaVariable("x", JavaBuiltInTypes.INT),
                JavaLiteral("1", JavaBuiltInTypes.BOOLEAN)))

    def test_02_assignments_allow_rhs_subtype(self):
        self.assertNoCompileErrors(
            JavaAssignment(
                JavaVariable("f", Graphics.fillable),
                JavaVariable("r", Graphics.rectangle)))

    def test_03_assignments_does_not_allow_rhs_supertype(self):
        self.assertCompileError(
            JavaTypeMismatchError,
            "Cannot assign Fillable to variable r of type Rectangle",
            JavaAssignment(
                JavaVariable("r", Graphics.rectangle),
                JavaVariable("f", Graphics.fillable)))


if __name__ == '__main__':
    unittest.main()
