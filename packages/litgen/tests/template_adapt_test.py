import litgen

import srcmlcpp
from srcmlcpp import CppType, srcmlcpp_main
from codemanip import code_utils


def _make_cpp_type(cpp_type_str: str) -> CppType:
    options = srcmlcpp.SrcmlcppOptions()
    r = srcmlcpp_main.code_to_cpp_type(options, cpp_type_str)
    return r


def test_specialize_or_exclude_tpl_type():
    options = litgen.LitgenOptions()
    options.class_template_options.add_specialization("^MyVec$", ["int *", "float"], [])

    cpp_type = _make_cpp_type("int")
    assert not options.class_template_options.shall_specialize_type(cpp_type)
    assert not options.class_template_options.shall_exclude_type(cpp_type)
    assert options.class_template_options.specialized_type_python_name(cpp_type, options.type_replacements) is None

    cpp_type = _make_cpp_type("MyVec<int *>")
    assert options.class_template_options.shall_specialize_type(cpp_type)
    assert not options.class_template_options.shall_exclude_type(cpp_type)
    assert (
        options.class_template_options.specialized_type_python_name(cpp_type, options.type_replacements)
        == "MyVec_int_ptr"
    )

    cpp_type = _make_cpp_type("MyVec<int*>")
    assert options.class_template_options.shall_specialize_type(cpp_type)
    assert not options.class_template_options.shall_exclude_type(cpp_type)
    assert (
        options.class_template_options.specialized_type_python_name(cpp_type, options.type_replacements)
        == "MyVec_int_ptr"
    )

    cpp_type = _make_cpp_type("MyVec<double>")
    assert not options.class_template_options.shall_specialize_type(cpp_type)
    assert options.class_template_options.shall_exclude_type(cpp_type)
    assert options.class_template_options.specialized_type_python_name(cpp_type, options.type_replacements) is None


def test_exclude_tpl_from_code():
    options = litgen.LitgenOptions()
    options.class_template_options.add_specialization("^MyPair$", ["int"], [])
    options.srcmlcpp_options.ignored_warning_parts.append("Excluding template type MyPair<double>")

    code = """
        template<typename T> struct MyPair
        {
            T v1, v2;
        };

        void Foo(MyPair<int> xs);        // Should be included in bindings, since MyPair<int> is handled
        void Foo2(MyPair<double> xs);    // Should be excluded from bindings, since MyPair<double> is unhandled

        struct FooStruct
        {
            MyPair<int> v1;               // Should be included in bindings
            MyPair<double> v2;            // Should be excluded from bindings
        };

        struct S
        {
            void FooS(MyPair<int> xs);     // Should be included in bindings
            void FooS2(MyPair<double> xs); // Should be excluded from bindings
        };
    """

    generated_code = litgen.generate_code(options, code)

    code_utils.assert_are_codes_equal(
        generated_code.stub_code,
        '''
        #  ------------------------------------------------------------------------
        #      <template specializations for class MyPair>
        class MyPair_int:  # Python specialization for MyPair<int>
            v1: int
            v2: int
            def __init__(self, v1: int = int(), v2: int = int()) -> None:
                """Auto-generated default constructor with named params"""
                pass
        #      </template specializations for class MyPair>
        #  ------------------------------------------------------------------------

        def foo(xs: MyPair_int) -> None:
            """ Should be included in bindings, since MyPair<int> is handled"""
            pass

        class FooStruct:
            v1: MyPair_int  # Should be included in bindings
            def __init__(self, v1: MyPair_int = MyPair_int()) -> None:
                """Auto-generated default constructor with named params"""
                pass

        class S:
            def foo_s(self, xs: MyPair_int) -> None:
                """ Should be included in bindings"""
                pass
            def __init__(self) -> None:
                """Auto-generated default constructor"""
                pass
        ''',
    )

    # print(generated_code.pydef_code)


def test_tpl_naming_with_replacements():
    options = litgen.LitgenOptions()
    options.type_replacements.add_last_replacement(r"ImGui([A-Z][a-zA-Z0-9]*)", r"\1")

    options.class_template_options.add_specialization("ImVector", ["ImGuiConfig"], [])

    code = """
    struct ImGuiConfig {};

    template<typename T>
    struct ImVector
    {
        T data;
    };

    struct Foo
    {
        ImVector<ImGuiConfig> Configs;
    };

    """

    generated_code = litgen.generate_code(options, code)
    code_utils.assert_are_codes_equal(
        generated_code.stub_code,
        '''
        class Config:
            def __init__(self) -> None:
                """Auto-generated default constructor"""
                pass

        #  ------------------------------------------------------------------------
        #      <template specializations for class ImVector>
        class ImVector_Config:  # Python specialization for ImVector<ImGuiConfig>
            data: Config
            def __init__(self, data: Config = Config()) -> None:
                """Auto-generated default constructor with named params"""
                pass
        #      </template specializations for class ImVector>
        #  ------------------------------------------------------------------------

        class Foo:
            configs: ImVector_Config
            def __init__(self, configs: ImVector_Config = ImVector_Config()) -> None:
                """Auto-generated default constructor with named params"""
                pass
        ''',
    )


def test_tpl_function_with_suffix():
    options = litgen.LitgenOptions()
    options.fn_template_options.add_specialization(
        "add", ["int"], add_suffix_to_function_name=True, cpp_synonyms_list_str=[]
    )
    code = """
    template<typename T> T add(T a, T b);
    """
    generated_code = litgen.generate_code(options, code)
    print(generated_code.stub_code)
    code_utils.assert_are_codes_equal(
        generated_code.stub_code,
        """
        #  ------------------------------------------------------------------------
        #      <template specializations for function add>
        def add_int(a: int, b: int) -> int:
            pass
        #      </template specializations for function add>
        #  ------------------------------------------------------------------------
        """,
    )
    # print("\n" + generated_code.pydef_code)
    code_utils.assert_are_codes_equal(
        generated_code.pydef_code,
        """
        m.def("add_int",
            add<int>, py::arg("a"), py::arg("b"));
        """,
    )


def test_tpl_with_pointer():
    options = litgen.LitgenOptions()
    options.class_template_options.add_specialization("ImVector", ["int*"], [])
    code = """
    template<typename T>
    struct ImVector
    {
        T* data;
    };

    void foo(ImVector<int *>xs = ImVector<int *>{});
    """
    generated_code = litgen.generate_code(options, code)
    code_utils.assert_are_codes_equal(
        generated_code.stub_code,
        '''
        #  ------------------------------------------------------------------------
        #      <template specializations for class ImVector>
        class ImVector_int_ptr:  # Python specialization for ImVector<int *>
            data: int
            def __init__(self) -> None:
                """Auto-generated default constructor"""
                pass
        #      </template specializations for class ImVector>
        #  ------------------------------------------------------------------------

        def foo(xs: ImVector_int_ptr = ImVector_int_ptr()) -> None:
            pass
    ''',
    )


def test_tpl_with_synonyms():
    options = litgen.LitgenOptions()
    options.class_template_options.add_specialization(
        name_regex="MyData", cpp_types_list_str=["int"], cpp_synonyms_list_str=["MyInt=int"]
    )
    code = """
        template<typename T> struct MyData { T data; };

        struct Foo
        {
            MyData<MyInt> values;
        };
        """
    generated_code = litgen.generate_code(options, code)
    # print(generated_code.stub_code)
    code_utils.assert_are_codes_equal(
        generated_code.stub_code,
        '''
        #  ------------------------------------------------------------------------
        #      <template specializations for class MyData>
        class MyData_int:  # Python specialization for MyData<int>
            data: int
            def __init__(self, data: int = int()) -> None:
                """Auto-generated default constructor with named params"""
                pass

        MyData_MyInt = MyData_int

        #      </template specializations for class MyData>
        #  ------------------------------------------------------------------------

        class Foo:
            values: MyData_MyInt
            def __init__(self, values: MyData_MyInt = MyData_MyInt()) -> None:
                """Auto-generated default constructor with named params"""
                pass
        ''',
    )
