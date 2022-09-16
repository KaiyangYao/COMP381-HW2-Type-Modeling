# -*- coding: utf-8 -*-

from java_type_checker import *

class Graphics:
    """
    Type declarations used by the unit tests. These are fake/imaginary types,
    loosely modeled after the kilt-graphics library from COMP 127/128.
    """

    # (Each of these comments shows the Java structure of the Python object model below.)
    
    # class Point {
    #     Point(double x, double y)
    #
    #     double getX()
    #     double getY()
    #
    #     Point add(Point p)
    # }

    point = JavaObjectType(
        "Point",
        constructor=JavaConstructor([JavaBuiltInTypes.DOUBLE, JavaBuiltInTypes.DOUBLE])
    )
    point.add_method(
        JavaMethod("getX",
            return_type=JavaBuiltInTypes.DOUBLE))
    point.add_method(
        JavaMethod("getY",
            return_type=JavaBuiltInTypes.DOUBLE))
    point.add_method(
        JavaMethod("add",
            parameter_types=[point],
            return_type=point))

    # class Size {
    #     Size(double width, double height)
    #
    #     double getWidth()
    #     double getHeight()
    # }

    size = JavaObjectType(
        "Size",
        constructor=JavaConstructor([JavaBuiltInTypes.DOUBLE, JavaBuiltInTypes.DOUBLE])
    )
    size.add_method(
        JavaMethod("getWidth",
            return_type=JavaBuiltInTypes.DOUBLE))
    size.add_method(
        JavaMethod("getHeight",
            return_type=JavaBuiltInTypes.DOUBLE))

    # class GraphicsObject {
    #     abstract double getX()
    #     abstract double getY()
    #
    #     abstract Point getPosition()
    #     abstract void setPosition(double x, double y)
    # }

    graphics_object = JavaObjectType(
        "GraphicsObject"
    )
    graphics_object.add_method(
        JavaMethod("getX",
            return_type=JavaBuiltInTypes.DOUBLE))
    graphics_object.add_method(
        JavaMethod("getY",
            return_type=JavaBuiltInTypes.DOUBLE))
    graphics_object.add_method(
        JavaMethod("getPosition",
            return_type=point))
    graphics_object.add_method(
        JavaMethod("setPosition",
            parameter_types=[JavaBuiltInTypes.DOUBLE, JavaBuiltInTypes.DOUBLE],
            return_type=JavaBuiltInTypes.VOID))

    # interface Paint {
    # }

    paint = JavaObjectType(
        "Paint"
    )

    # class Color implements Paint {
    #     Color(int r, int g, int b)
    # }

    color = JavaObjectType(
        "Color",
        direct_supertypes=[paint],
        constructor=JavaConstructor([int, int, int])
    )

    # interface Fillable {
    #     void setFillColor(Paint fillColor)
    #     Paint getFillColor()
    # }

    fillable = JavaObjectType(
        "Fillable"
    )
    fillable.add_method(
        JavaMethod("setFillColor",
            parameter_types=[paint],
            return_type=JavaBuiltInTypes.VOID))
    fillable.add_method(
        JavaMethod("getFillColor",
            return_type=paint))

    # interface Strokable {
    #     void setStrokeColor(Paint strokeColor)
    #     Paint getStrokeColor()
    # }

    strokable = JavaObjectType(
        "Strokable"
    )
    strokable.add_method(
        JavaMethod("setStrokeColor",
            parameter_types=[paint],
            return_type=JavaBuiltInTypes.VOID))
    strokable.add_method(
        JavaMethod("getStrokeColor",
            return_type=paint))

    # class Rectangle extends GraphicsObject implements Strokable, Fillable {
    # }

    rectangle = JavaObjectType(
        "Rectangle",
        direct_supertypes=[graphics_object, strokable, fillable],
        constructor=JavaConstructor([point, size])
    )
    rectangle.add_method(
        JavaMethod("getSize",
            return_type=size))

    # class GraphicsGroup extends GraphicsObject implements GraphicsObserver {
    #     void add(GraphicsObject gObject)
    #     GraphicsObject getElementAt(Point p)
    # }

    graphics_group = JavaObjectType(
        "GraphicsGroup",
        direct_supertypes=[graphics_object]
    )
    graphics_group.add_method(
        JavaMethod("add",
            parameter_types=[graphics_object],
            return_type=JavaBuiltInTypes.VOID))
    graphics_group.add_method(
        JavaMethod("getElementAt",
            parameter_types=[point],
            return_type=graphics_object))

    # class Window {
    #     Size getSize()
    # }

    window = JavaObjectType(
        "Window"
    )
    window.add_method(
        JavaMethod("getSize",
            return_type=size))
