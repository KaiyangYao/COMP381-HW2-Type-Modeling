# -*- coding: utf-8 -*-


class JavaType(object):
    """The base type for all Java types, including object types, primitives, and special types.

    Attributes:
        name (str): Name of this type. **Note:** Names are not necessarily unique.
    """

    is_object_type = False   #: Indicates whether members of this type are objects (bool)
    is_instantiable = False  #: Indicates whether `new` can create instances of this type (bool)

    def __init__(self, name, direct_supertypes=[]):
        self.name = name

    def is_subtype_of(self, other):
        """Returns True if and only if a value of this type can be used in a context that expects
        the given type.

        Subclasses must override this.
        """
        raise NotImplementedError(type(self).__name__ + " must override is_subtype_of()")

    def is_supertype_of(self, other):
        """Convenience counterpart to is_subtype_of().
        """
        return other.is_subtype_of(self)

    def method_named(self, method_name):
        """Returns the JavaMethod with the given name, which may come from a supertype.

        Raises:
            NoSuchJavaMethod if the type has no method with the give name (or no methods at all)
        """
        raise NoSuchJavaMethod("Type {0} does not have methods".format(self.name))


class JavaConstructor(object):
    """The declaration of a Java constructor.

    Note: This represents the constructor, not a *call* to the constructor. For example::

        class Foo {
          public Foo(int bar) {  // This is a JavaConstructor
            ...
          }
        }

        new Foo(34)              // This is a JavaConstructorCall

    Attributes:
        parameter_types (list of JavaType): Declared parameter types
    """
    def __init__(self, parameter_types=[]):
        self.parameter_types = parameter_types


class JavaMethod(object):
    """The declaration of a Java method.

    In this simplified model, methods do not have implementations.

    Note: This object represents the method itself, not a *call* to the method. For example::

        class Foo {
          public bar() {  // This is a JavaMethod
            ...
          }
        }

        Foo foo = ...;
        foo.bar()         // This is a JavaMethodCall

    Attributes:
        name (str): Name of this method
        parameter_types (list of JavaType): Declared parameter types
        return_type (JavaType): Method’s declared return type
    """
    def __init__(self, name, parameter_types=[], return_type=None):
        self.name = name
        self.parameter_types = parameter_types
        self.return_type = return_type


class JavaPrimitiveType(JavaType):
    """A primitive type such as int or double.

    Primitive types are not object types and do not have methods.
    """
    def is_subtype_of(self, other):
        return other == self


class JavaObjectType(JavaType):
    """
    Describes the API of a Java type whose values are objects, i.e. a class or interface.

    (This simplified type model does not draw a distinction between classes and interfaces, and
    assumes they are all instantiable. Other than instantiability, the distinction between
    interfaces, abstract classes, and concrete classes makes no difference to us here: we are only
    checking types, not compiling or executing code, so none of the methods have implementations.)

    Attributes:
        name (str): The name of this class
        direct_supertypes (list of JavaObjectType): types this class extends or implements
        constructor (JavaConstructor): Class’s constructor (we only allow one)
        methods (list of JavaMethod): Class's methods
    """

    is_object_type = True
    is_instantiable = True

    def __init__(self, name, direct_supertypes=None, constructor=JavaConstructor([])):
        super().__init__(name)
        self.name = name
        if direct_supertypes is None:
            self.direct_supertypes = [JavaBuiltInTypes.OBJECT]
        else:
            self.direct_supertypes = direct_supertypes
        self.constructor = constructor
        self.methods = {}

    def add_method(self, method):
        self.methods[method.name] = method

    def method_named(self, name):
        try:
            return self.methods[name]
        except KeyError:
            for supertype in self.direct_supertypes:
                try:
                    return supertype.method_named(name)
                except NoSuchJavaMethod:
                    pass
            raise NoSuchJavaMethod("{0} has no method named {1}".format(self.name, name))

    def is_subtype_of(self, other):
        if other == self:
            return True
        # The overarching supertype should be JavaBuiltInTypes.OBJECT, which has no direct_supertypes
        # and will break out the recursion.
        for supertype in self.direct_supertypes:
            if supertype.is_subtype_of(other):
                return True
        return False


class JavaVoidType(JavaType):
    """The Java type `void`.

    It is never legal to use the result of a method returning void inside a larger expression.
    Void is therefore subtype only of itself, and not any other type.
    """
    def __init__(self):
        super().__init__("void")

    def is_subtype_of(self, other):
        return other == self


class JavaNullType(JavaType):
    """The type of the value `null` in Java.

    Null acts as though it is a subtype of all object types. However, it raises an exception for any
    attempt to look up a method.
    """
    def __init__(self):
        super().__init__("null")
        self.is_object_type = True

    def is_subtype_of(self, other):
        return other.is_subtype_of(JavaBuiltInTypes.OBJECT)

    def method_named(self, name):
        raise NoSuchJavaMethod("Cannot invoke method {0}() on null".format(name))


class JavaTypeError(Exception):
    """Indicates a compile-time type error in an expression.
    """
    pass


class NoSuchJavaMethod(JavaTypeError):
    """Indicates a call to a nonexistent method on a Java object.
    """
    pass


class JavaBuiltInTypes:
    """The types that are built into the Java language itself.

    (We only include a few of Java's language-provided types.)
    """
    VOID    = JavaVoidType()

    BOOLEAN = JavaPrimitiveType("boolean")
    INT     = JavaPrimitiveType("int")
    DOUBLE  = JavaPrimitiveType("double")

    NULL    = JavaNullType()

    OBJECT = JavaObjectType(
        "Object",
        direct_supertypes=[]
    )
    OBJECT.add_method(JavaMethod("equals", parameter_types=[OBJECT], return_type=BOOLEAN))
    OBJECT.add_method(JavaMethod("hashCode", return_type=INT))
