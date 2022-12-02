// ============================================================================
// This file was autogenerated
// It is presented side to side with its source: basic_test.h
// It is not used in the compilation
//    (see integration_tests/bindings/pybind_mylib.cpp which contains the full binding
//     code, including this code)
// ============================================================================

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <pybind11/numpy.h>
#include "mylib/mylib_main/mylib.h"

namespace py = pybind11;

// <litgen_glue_code>  // Autogenerated code below! Do not edit!

// </litgen_glue_code> // Autogenerated code end


void py_init_module_mylib(py::module& m)
{
    // <litgen_pydef> // Autogenerated code below! Do not edit!
    ////////////////////    <generated_from:basic_test.h>    ////////////////////
    m.def("my_sub",
        my_sub,
        py::arg("a"), py::arg("b"),
        "Subtracts two numbers: this will be the function's __doc__ since my_sub does not have an end-of-line comment");

    m.def("my_add",
        my_add,
        py::arg("a"), py::arg("b"),
        "Adds two numbers");

    m.def("my_mul",
        my_mul, py::arg("a"), py::arg("b"));

    m.def("my_generic_function",
        my_generic_function, "This is a generic function for python, accepting (*args, **kwargs) as arguments");

    { // <namespace MathFunctions>
        py::module_ pyNsMathFunctions = m.def_submodule("math_functions", " Vectorizable functions example\n    Numeric functions (i.e. function accepting and returning only numeric params or py::array), can be vectorized\n    i.e. they will accept numpy arrays as an input.\n\n Auto-vectorization is enabled via the following options:\n     options.fn_namespace_vectorize__regex: str = r\"^MathFunctions$\"\n     options.fn_vectorize__regex = r\".*\"\n");
        pyNsMathFunctions.def("vectorizable_sum",
            MathFunctions::vectorizable_sum, py::arg("x"), py::arg("y"));
        pyNsMathFunctions.def("vectorizable_sum",
            py::vectorize(MathFunctions::vectorizable_sum), py::arg("x"), py::arg("y"));
    } // </namespace MathFunctions>
    ////////////////////    </generated_from:basic_test.h>    ////////////////////

    // </litgen_pydef> // Autogenerated code end
}
