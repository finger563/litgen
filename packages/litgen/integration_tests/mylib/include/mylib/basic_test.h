#pragma once
#include "mylib/api_marker.h"

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

// Subtracts two numbers: this will be the function's __doc__ since my_sub does not have an end-of-line comment
MY_API int my_sub(int a, int b) { return a - b; }


// Title that should be published as a top comment in python stub (pyi) and thus not part of __doc__
// (the end-of-line comment will supersede this top comment)
MY_API inline int my_add(int a, int b) { return a + b; } // Adds two numbers


// my_mul should have no user doc (but it will have a typing doc generated by pybind)
// (do not remove the next empty line, or this comment would become my_mul's doc!)

MY_API int my_mul(int a, int b) { return a * b; }

// This should not be published, as it is not marked with MY_API
int my_div(int a, int b) { return a / b;}


// This is a generic function for python, accepting (*args, **kwargs) as arguments
MY_API int my_generic_function(pybind11::args args, const pybind11::kwargs& kwargs)
{
    int r = args.size() + 2 * kwargs.size();
    return r;
}


// Vectorizable functions example
//    Numeric functions (i.e. function accepting and returning only numeric params or py::array), can be vectorized
//    i.e. they will accept numpy arrays as an input.
//
// Auto-vectorization is enabled via the following options:
//     options.fn_namespace_vectorize__regex: str = r"^MathFunctions$"
//     options.fn_vectorize__regex = r".*"
//
namespace MathFunctions
{
    MY_API double vectorizable_sum(float x, double y)
    {
        return (double) x + y;
    }
}

// Ignored namespace example:
// By default, any namespace whose name contains "internal" or "detail" will be excluded.
// See LitgenOptions.namespace_exclude__regex
namespace Detail
{
    MY_API int foo() { return 42; }
}
