package plang;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * The runtime state of an object in Python.
 */
public class PythonObject {
    private final Map<String,PythonObject> attrs = new HashMap<>();
    private final PythonType type;
    private List<PythonObject> mro;

    PythonObject(PythonType type) {
        this.type = type;
    }

    /**
     * The Python type (i.e. class) of this object.
     *
     * May be null if this object is itself a class. This is a simplification for this assignment;
     * in actual Python, _all_ objects have types, and the type of a class is `type`. That is itself
     * a class, so the type of `type` is `type`. Phew! Thank goodness we’re ignoring that.
     */
    public final PythonType getType() {
        return type;
    }

    /**
     * Return the list of objects we should search when asked for a given attribute, in the order
     * we should search them.
     *
     * The real Python implementation of the MRO is substantially more complicated, because
     * (1) Python supports multiple inheritance (i.e. classes can have multiple base classes), and
     * (2) the base of `type` is `object`, and the type of `object` is `type`, which creates a
     *     circular reference that Python resolves by special-casing both `object` and `type`.
     *
     * Once again, hooray for not having to deal with that.
     */
    public List<PythonObject> getMRO() {
        if(mro == null)
            mro = Collections.unmodifiableList(buildMRO());
        return mro;
    }

    /**
     * Constructs the MRO. Called only once, the first time we need the MRO; this class memoizes the
     * result (i.e. it remembers the list buildMRO() returned and keeps returning it).
     */
    protected List<PythonObject> buildMRO() {
        throw new UnsupportedOperationException("not implemented yet");
    }

    /**
     * Returns the value of the attribute with the given name for this object.
     *
     * @param attrName The name of the attribute to look for.
     * @return Its value if found.
     * @throws PythonAttributeException When there is no attribute on this object with that name.
     */
    public final PythonObject get(String attrName) throws PythonAttributeException {
        throw new UnsupportedOperationException("not implemented yet");
    }

    /**
     * Add or changes the value of an attribute on this object. Note that it sets the value for
     * _this_ object alone, even if the attribute already exists somewhere upstream in the attribute
     * resolution order.
     *
     * @param attrName The name of the attribute to set
     * @param value Its new value
     */
    public final void set(String attrName, PythonObject value) {
        throw new UnsupportedOperationException("not implemented yet");
    }

    @Override
    public String toString() {
        return "PythonObject<" + getType().getName() + ">" + attrs;
    }
}
