from codemanip import code_utils

import litgen
from litgen.litgen_generator import LitgenGeneratorTestsHelper
from litgen.options import LitgenOptions


def test_adapted_function_stub():
    options = LitgenOptions()
    options.original_location_flag_show = True
    options.fn_params_replace_buffer_by_array__regex = r".*"

    code = """
    // This is foo's doc:
    //     :param buffer & count: modifiable buffer and its size
    //     :param out_values: output double values
    //     :param in_flags: input bool flags
    //     :param text and ... : formatted text
    void Foo(uint8_t * buffer, size_t count, double out_values[2], const bool in_flags[2], const char* text, ...);
    """
    stub_code = LitgenGeneratorTestsHelper.code_to_stub(options, code)
    # logging.warning("\n>>>" + stub_code + "<<<")
    code_utils.assert_are_codes_equal(
        stub_code,
        '''
        ####################    <generated_from:BoxedTypes>    ####################
        class BoxedDouble:
            value: float
            def __init__(self, v: float = 0.) -> None:
                pass
            def __repr__(self) -> str:
                pass
        ####################    </generated_from:BoxedTypes>    ####################



        def foo(    # Line:7
            buffer: np.ndarray,
            out_values_0: BoxedDouble,
            out_values_1: BoxedDouble,
            in_flags: List[bool],
            text: str
            ) -> None:
            """ This is foo's doc:
                 :param buffer & count: modifiable buffer and its size
                 :param out_values: output double values
                 :param in_flags: input bool flags
                 :param text and ... : formatted text
            """
            pass
            ''',
    )


def test_adapted_function_pydef_simple():
    options = LitgenOptions()
    code = """
    int add(int a, int b) { return a + b; }
    """
    pydef_code = LitgenGeneratorTestsHelper.code_to_pydef(options, code)
    # logging.warning("\n>>>" + pydef_code + "<<<")
    code_utils.assert_are_codes_equal(
        pydef_code,
        """
        m.def("add",
            add, py::arg("a"), py::arg("b"));
        """,
    )


def test_implot_easy() -> None:
    options = LitgenOptions()
    options.srcmlcpp_options.functions_api_prefixes = "IMPLOT_API|IMPLOT_TMP"
    options.original_location_flag_show = True
    code = """
        // Sets the format of numeric
        // axis labels
        IMPLOT_API void SetupAxisFormat(ImAxis axis, const char* fmt);
    """
    generated_code = LitgenGeneratorTestsHelper.code_to_pydef(options, code)
    expected_code = """
        m.def("setup_axis_format",    // Line:4
            SetupAxisFormat,
            py::arg("axis"), py::arg("fmt"),
            " Sets the format of numeric\\n axis labels");
        """
    # logging.warning("\n" + generated_code)
    code_utils.assert_are_codes_equal(generated_code, expected_code)


def test_return_value_policy() -> None:
    options = LitgenOptions()
    code = """
        // Returns a widget
        Widget* Foo();  // py::return_value_policy::reference
    """
    generated_code = LitgenGeneratorTestsHelper.code_to_pydef(options, code)
    # logging.warning("\n" + generated_code)
    expected_code = """
        m.def("foo",
            Foo,
            " Returns a widget\\nreturn_value_policy::reference",
            pybind11::return_value_policy::reference);
        """
    code_utils.assert_are_codes_equal(generated_code, expected_code)


def test_implot_one_buffer() -> None:
    options = LitgenOptions()
    options.fn_params_replace_buffer_by_array__regex = r".*"
    options.srcmlcpp_options.functions_api_prefixes = "IMPLOT_API|IMPLOT_TMP"
    options.original_location_flag_show = True
    code = """
        // Plots a standard 2D scatter plot. Default marker is ImPlotMarker_Circle.
        IMPLOT_TMP void PlotScatter(const T* values, int count);
    """
    generated_code = LitgenGeneratorTestsHelper.code_to_pydef(options, code)
    expected_code = """
        m.def("plot_scatter",    // Line:3
            [](const py::array & values)
            {
                auto PlotScatter_adapt_c_buffers = [](const py::array & values)
                {
                    // convert py::array to C standard buffer (const)
                    const void * values_from_pyarray = values.data();
                    py::ssize_t values_count = values.shape()[0];

                    #ifdef _WIN32
                    using np_uint_l = uint32_t;
                    using np_int_l = int32_t;
                    #else
                    using np_uint_l = uint64_t;
                    using np_int_l = int64_t;
                    #endif
                    // call the correct template version by casting
                    char values_type = values.dtype().char_();
                    if (values_type == 'B')
                        PlotScatter(static_cast<const uint8_t *>(values_from_pyarray), static_cast<int>(values_count));
                    else if (values_type == 'b')
                        PlotScatter(static_cast<const int8_t *>(values_from_pyarray), static_cast<int>(values_count));
                    else if (values_type == 'H')
                        PlotScatter(static_cast<const uint16_t *>(values_from_pyarray), static_cast<int>(values_count));
                    else if (values_type == 'h')
                        PlotScatter(static_cast<const int16_t *>(values_from_pyarray), static_cast<int>(values_count));
                    else if (values_type == 'I')
                        PlotScatter(static_cast<const uint32_t *>(values_from_pyarray), static_cast<int>(values_count));
                    else if (values_type == 'i')
                        PlotScatter(static_cast<const int32_t *>(values_from_pyarray), static_cast<int>(values_count));
                    else if (values_type == 'L')
                        PlotScatter(static_cast<const np_uint_l *>(values_from_pyarray), static_cast<int>(values_count));
                    else if (values_type == 'l')
                        PlotScatter(static_cast<const np_int_l *>(values_from_pyarray), static_cast<int>(values_count));
                    else if (values_type == 'f')
                        PlotScatter(static_cast<const float *>(values_from_pyarray), static_cast<int>(values_count));
                    else if (values_type == 'd')
                        PlotScatter(static_cast<const double *>(values_from_pyarray), static_cast<int>(values_count));
                    else if (values_type == 'g')
                        PlotScatter(static_cast<const long double *>(values_from_pyarray), static_cast<int>(values_count));
                    else if (values_type == 'q')
                        PlotScatter(static_cast<const long long *>(values_from_pyarray), static_cast<int>(values_count));
                    // If we reach this point, the array type is not supported!
                    else
                        throw std::runtime_error(std::string("Bad array type ('") + values_type + "') for param values");
                };

                PlotScatter_adapt_c_buffers(values);
            },
            py::arg("values"),
            "Plots a standard 2D scatter plot. Default marker is ImPlotMarker_Circle.");
   """
    code_utils.assert_are_codes_equal(generated_code, expected_code)


def test_immvision() -> None:
    options = LitgenOptions()
    options.srcmlcpp_options.functions_api_prefixes = "IMMVISION_API"
    code = """
        // Display an image (requires OpenGL initialized)
        IMMVISION_API bool Image(const std::string& label_id, const cv::Mat& mat, ImageParams* params);
    """
    generated_code = LitgenGeneratorTestsHelper.code_to_pydef(options, code)
    expected_code = """
        m.def("image",
            Image,
            py::arg("label_id"), py::arg("mat"), py::arg("params"),
            "Display an image (requires OpenGL initialized)");
        """
    code_utils.assert_are_codes_equal(generated_code, expected_code)


def test_overloads() -> None:
    options = LitgenOptions()
    code = """
    std::string foo();
    std::string foo(int a);
    void blah();
    """
    generated_code = LitgenGeneratorTestsHelper.code_to_pydef(options, code)
    # logging.warning("\n" + generated_code)
    code_utils.assert_are_codes_equal(
        generated_code,
        """
        m.def("foo",
            py::overload_cast<>(foo));

        m.def("foo",
            py::overload_cast<int>(foo), py::arg("a"));

        m.def("blah",
            blah);
        """,
    )

    code = """
    struct Foo
    {
        std::string foo();
        std::string foo(int a);
        void blah();
    };
    """
    generated_code = LitgenGeneratorTestsHelper.code_to_pydef(options, code)
    # logging.warning("\n" + generated_code)
    code_utils.assert_are_codes_equal(
        generated_code,
        """
        auto pyClassFoo =
            py::class_<Foo>
                (m, "Foo", "")
            .def(py::init<>()) // implicit default constructor
            .def("foo",
                [](Foo & self) { return self.foo(); })
            .def("foo",
                py::overload_cast<int>(&Foo::foo), py::arg("a"))
            .def("blah",
                &Foo::blah)
            ;
        """,
    )


def test_type_ignore():
    options = LitgenOptions()
    code = """
    // Foo doc
    std::string foo(); // type: ignore
    """
    stub_code = LitgenGeneratorTestsHelper.code_to_stub(options, code)
    # logging.warning("\n" + stub_code)
    code_utils.assert_are_codes_equal(
        stub_code,
        """
    # Foo doc
    def foo() -> str:  # type: ignore
        pass
    """,
    )

    code = """
    std::string foo(); // type: ignore // Some more doc
    """
    stub_code = LitgenGeneratorTestsHelper.code_to_stub(options, code)
    # logging.warning("\n" + stub_code)
    code_utils.assert_are_codes_equal(
        stub_code,
        '''
    def foo() -> str:  # type: ignore
        """ Some more doc"""
        pass
    ''',
    )


def test_py_none_param():
    options = LitgenOptions()

    code = """
    void foo(Widget *a = nullptr);
    """
    pydef_code = LitgenGeneratorTestsHelper.code_to_pydef(options, code)
    # logging.warning("\n" + pydef_code)
    code_utils.assert_are_codes_equal(
        pydef_code,
        """
        m.def("foo",
            foo, py::arg("a") = py::none());
        """,
    )

    code = """
    void foo(Widget *a = NULL);
    """
    pydef_code = LitgenGeneratorTestsHelper.code_to_pydef(options, code)
    # logging.warning("\n" + pydef_code)
    code_utils.assert_are_codes_equal(
        pydef_code,
        """
        m.def("foo",
            foo, py::arg("a") = py::none());
        """,
    )

    code = """
    void foo(Widget *a = Widget(NULL));
    """
    pydef_code = LitgenGeneratorTestsHelper.code_to_pydef(options, code)
    # logging.warning("\n" + pydef_code)
    code_utils.assert_are_codes_equal(
        pydef_code,
        """
        m.def("foo",
            foo, py::arg("a") = Widget(NULL));
        """,
    )


def test_vectorization():
    code = """
    namespace MathFunctions
    {
        double vectorizable_sum(float x, double y)
        {
            return (double) x + y;
        }
    }
        """

    options = litgen.LitgenOptions()
    options.fn_namespace_vectorize__regex = r"^MathFunctions$"
    options.fn_vectorize__regex = r".*"
    options.fn_vectorize_prefix = "v_"
    options.fn_vectorize_suffix = "_v"

    generated_code = litgen.generate_code(options, code)

    code_utils.assert_are_codes_equal(
        generated_code.pydef_code,
        """
        { // <namespace MathFunctions>
            py::module_ pyNsMathFunctions = m.def_submodule("math_functions", "");
            pyNsMathFunctions.def("vectorizable_sum",
                MathFunctions::vectorizable_sum, py::arg("x"), py::arg("y"));
            pyNsMathFunctions.def("v_vectorizable_sum_v",
                py::vectorize(MathFunctions::vectorizable_sum), py::arg("x"), py::arg("y"));
        } // </namespace MathFunctions>
    """,
    )
    code_utils.assert_are_codes_equal(
        generated_code.stub_code,
        """
        # <submodule math_functions>
        class math_functions:  # Proxy class that introduces typings for the *submodule* math_functions
            pass  # (This corresponds to a C++ namespace. All method are static!)
            @staticmethod
            def vectorizable_sum(x: float, y: float) -> float:
                pass
            @staticmethod
            def v_vectorizable_sum_v(x: np.ndarray, y: np.ndarray) -> np.ndarray:
                pass

        # </submodule math_functions>
    """,
    )


def test_templated_function():
    code = """
        struct Foo
        {
            template<typename T>
            T SumVector(std::vector<T> xs, const T other_values[2]);
        };
        """
    options = litgen.LitgenOptions()
    options.fn_template_options.add_specialization(r"SumVector", ["int"])
    options.fn_params_replace_buffer_by_array__regex = r".*"

    generated_code = litgen.generate_code(options, code)

    code_utils.assert_are_codes_equal(
        generated_code.stub_code,
        '''
        class Foo:
            #  ------------------------------------------------------------------------
            #      <template specializations for function SumVector>
            def sum_vector(self, xs: List[int], other_values: List[int]) -> int:
                pass
            #      </template specializations for function SumVector>
            #  ------------------------------------------------------------------------
            def __init__(self) -> None:
                """Auto-generated default constructor"""
                pass
             ''',
    )
    code_utils.assert_are_codes_equal(
        generated_code.pydef_code,
        """
        auto pyClassFoo =
            py::class_<Foo>
                (m, "Foo", "")
            .def(py::init<>()) // implicit default constructor
            .def("sum_vector",
                [](Foo & self, std::vector<int> xs, const std::array<int, 2>& other_values) -> int
                {
                    auto SumVector_adapt_fixed_size_c_arrays = [&self](std::vector<int> xs, const std::array<int, 2>& other_values) -> int
                    {
                        auto r = self.SumVector<int>(xs, other_values.data());
                        return r;
                    };

                    return SumVector_adapt_fixed_size_c_arrays(xs, other_values);
                },     py::arg("xs"), py::arg("other_values"))
            ;
    """,
    )


def test_templated_function_with_rename():
    code = """template<class T> T foo();"""
    options = LitgenOptions()
    options.fn_template_options.add_specialization(
        function_name_regex=r".*",
        cpp_types_list=["int", "double"],
        naming_scheme=litgen.TemplateNamingScheme.snake_suffix,
    )
    generated_code = litgen.generate_code(options, code)
    code_utils.assert_are_codes_equal(
        generated_code.stub_code,
        """
        #  ------------------------------------------------------------------------
        #      <template specializations for function foo>
        def foo_int() -> int:
            pass


        def foo_double() -> float:
            pass
        #      </template specializations for function foo>
        #  ------------------------------------------------------------------------
    """,
    )


def test_qualified_param_types():
    # in the pydef code, "S s" should be transcribed to Ns::S
    code = """
    namespace Ns {
        struct S {};
        void f(S s = S());
        void f(int a);
    }
    """
    options = litgen.LitgenOptions()
    generated_code = litgen.generate_code(options, code)
    code_utils.assert_are_codes_equal(
        generated_code.pydef_code,
        """
        { // <namespace Ns>
            py::module_ pyNsNs = m.def_submodule("ns", "");
            auto pyNsNs_ClassS =
                py::class_<Ns::S>
                    (pyNsNs, "S", "")
                .def(py::init<>()) // implicit default constructor
                ;


            pyNsNs.def("f",
                py::overload_cast<Ns::S>(Ns::f), py::arg("s") = Ns::S());

            pyNsNs.def("f",
                py::overload_cast<int>(Ns::f), py::arg("a"));
        } // </namespace Ns>
    """,
    )


def test_qualified_param_types_with_adapted_params():
    # in the pydef code, "S s" should be transcribed to Ns::S
    code = """
    namespace Ns {
        struct S {};
        void f(S s[1]);
    }
    """
    options = litgen.LitgenOptions()
    generated_code = litgen.generate_code(options, code)
    code_utils.assert_are_codes_equal(
        generated_code.pydef_code,
        """
        { // <namespace Ns>
            py::module_ pyNsNs = m.def_submodule("ns", "");
            auto pyNsNs_ClassS =
                py::class_<Ns::S>
                    (pyNsNs, "S", "")
                .def(py::init<>()) // implicit default constructor
                ;


            pyNsNs.def("f",
                [](Ns::S & s_0)
                {
                    auto f_adapt_fixed_size_c_arrays = [](Ns::S & s_0)
                    {
                        Ns::S s_raw[1];
                        s_raw[0] = s_0;

                        Ns::f(s_raw);

                        s_0 = s_raw[0];
                    };

                    f_adapt_fixed_size_c_arrays(s_0);
                },     py::arg("s_0"));
        } // </namespace Ns>
        """,
    )
