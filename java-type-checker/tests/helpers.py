import unittest
import sys


class TypeTest(unittest.TestCase):
    def assertSubtype(self, type0, type1):
        self.assertTrue(type0.is_subtype_of(type1))
        self.assertTrue(type1.is_supertype_of(type0))

    def assertNotSubtype(self, type0, type1):
        self.assertFalse(type0.is_subtype_of(type1))
        self.assertFalse(type1.is_supertype_of(type0))

    def assertCompileError(self, error, error_message, expr):
        try:
            with self.assertRaises(error) as exception_context:
                expr.check_types()
            self.assertEqual(error_message, str(exception_context.exception))
        except AssertionError:
            raise
        except Exception as actual_error:
            sys.stderr.write(
                "Got " + type(actual_error).__name__ + ", but expected " + error.__name__
                + "; did you raise the wrong exception type?")
            raise

    def assertNoCompileErrors(self, expr):
        expr.check_types()
