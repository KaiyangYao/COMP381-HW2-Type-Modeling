package plang;

/**
 * A Python string, as opposed to a Java string.
 *
 * We need a special case for this so that Java code can get the string value back out and use it
 * in testing. Real Python uses similar special-case C implementations for its built-in types.
 */
public class PythonString extends PythonObject {
    public static final PythonType TYPE = new PythonType("str", null);
    private final String value;

    public PythonString(String value) {
        super(PythonString.TYPE);
        this.value = value;
    }

    @Override
    public String toString() {
        return value;
    }
}
