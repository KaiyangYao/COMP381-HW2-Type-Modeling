package plang;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;

class PythonObjectTest {

    private PythonType fooType;
    private PythonType barType;
    private PythonObject foo;
    private PythonObject bar;

    /**
     * Equivalent Python:
     *
     *   class Foo:
     *     pass
     *
     *   class Bar:
     *     pass
     *
     *   foo = Foo()
     *   bar = Bar()
     */
    @BeforeEach
    void createTestTypeHierarchy() {
        fooType = new PythonType("Foo", null);
        barType = new PythonType("Bar", fooType);
        foo = fooType.instantiate();
        bar = barType.instantiate();
    }

    @Test
    void canCreateAndInstantiateTypes() {
        assertSame(fooType, foo.getType());
        assertSame(barType, bar.getType());
        assertNotSame(foo, bar);
    }

    // –––––– MRO tests ––––––

    @Test
    void typeMroIncludesSelf() throws Exception {
        assertEquals(
            Collections.singletonList(fooType),
            fooType.getMRO());
    }

    @Test
    void typeMroIncludesBaseClass() throws Exception {
        assertEquals(
            Arrays.asList(barType, fooType),
            barType.getMRO());
    }

    @Test
    void objectMroIncludesType() throws Exception {
        assertEquals(
            Arrays.asList(foo, fooType),
            foo.getMRO());
    }

    @Test
    void objectMroIncludesBaseClass() throws Exception {
        assertEquals(
            Arrays.asList(bar, barType, fooType),
            bar.getMRO());
    }

    // –––––– Attribute lookup tests ––––––

    @Test
    void findAttrsOnSelf() throws Exception {
        foo.set("color", new PythonString("greenish orange"));
        bar.set("flavor", new PythonString("ineffable"));

        assertEqualsPyStr("greenish orange", foo.get("color"));
        assertEqualsPyStr("ineffable", bar.get("flavor"));
    }

    @Test
    void exceptionWhenAttrNotFound() throws Exception {
        bar.set("flavor", new PythonString("ineffable"));

        PythonAttributeException error = assertThrows(
            PythonAttributeException.class,
            () -> {
                foo.get("flavor");
            } );
        assertSame(foo, error.getPyObject());
        assertEquals("flavor", error.getAttrName());
    }

    @Test
    void objectsSupportNullValues() throws Exception {
        foo.set("worries", null);
        assertEquals(null, foo.get("worries"));  // No exception!
    }

    @Test
    void findInheritedAttrs() throws Exception {
        // Equivalent Python:
        //
        //   Foo.socks = "rainbow"   # Type attributes...
        //   foo.socks               # ...show up on instances of the type...
        //   Bar.socks               # ...and on subtypes...
        //   bar.socks               # ...and on instances of subtypes too!

        fooType.set("socks", new PythonString("rainbow"));
        assertEqualsPyStr("rainbow", fooType.get("socks"));
        assertEqualsPyStr("rainbow", foo.get("socks"));
        assertEqualsPyStr("rainbow", barType.get("socks"));
        assertEqualsPyStr("rainbow", bar.get("socks"));
    }

    @Test
    void overrideInheritedAttrsInType() throws Exception {
        // Equivalent Python:
        //
        //   Foo.socks = "rainbow"
        //   Bar.socks = "polka dot"

        fooType.set("socks", new PythonString("rainbow"));
        barType.set("socks", new PythonString("polka dot"));

        assertEqualsPyStr("rainbow",   fooType.get("socks"));
        assertEqualsPyStr("rainbow",   foo.get("socks"));
        assertEqualsPyStr("polka dot", barType.get("socks"));
        assertEqualsPyStr("polka dot", bar.get("socks"));
    }

    @Test
    void overrideInheritedAttrsInInstance() throws Exception {
        // Equivalent Python:
        //
        //   Foo.socks = "rainbow"
        //   foo.socks = "chartreuse"

        fooType.set("socks", new PythonString("rainbow"));
        foo.set("socks", new PythonString("chartreuse"));

        assertEqualsPyStr("rainbow",    fooType.get("socks"));
        assertEqualsPyStr("chartreuse", foo.get("socks"));
        assertEqualsPyStr("rainbow",    barType.get("socks"));
        assertEqualsPyStr("rainbow",    bar.get("socks"));
    }

    // –––––– Helpers ––––––

    private void assertEqualsPyStr(String str, PythonObject pyobj) {
        if(str == null || pyobj == null) {
            assertEquals((Object) str, (Object) pyobj);
            return;
        }

        assertEquals(PythonString.class, pyobj.getClass());
        assertEquals(str, pyobj.toString());
    }
}
