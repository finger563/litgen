// THIS FILE WAS GENERATED AUTOMATICALLY. DO NOT EDIT.

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/mylib.h                                                                          //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/api_marker.h included by mylib/mylib.h                                           //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#ifndef MY_API
#define MY_API  // MY_API could typically be __declspec(dllexport | dllimport)
#endif

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/basic_test.h included by mylib/mylib.h                                           //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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


/*
For info, below is the python pyi stub that is published for this file:

def my_sub(a: int, b: int) -> int:
    """ Subtracts two numbers: this will be the __doc__ since my_sub does not have an end-of-line comment"""
    pass


# Title that should be published as a top comment in python stub (pyi) and thus not part of __doc__
# (the end-of-line comment will supersede the top comment)
def my_add(a: int, b: int) -> int:
    """ Adds two numbers"""
    pass


# my_mul should have no user doc (but it will have a typing doc generated by pybind)
# (do not remove the next empty line, or this comment would become my_mul's doc!)

def my_mul(a: int, b: int) -> int:
    pass
*/

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/header_filter_test.h included by mylib/mylib.h                                   //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Here, we test that functions placed under unknown preprocessor conditions are not exported by default
// You could choose to add them anyway with:
//    options.srcml_options.header_guard_suffixes.append("OBSCURE_OPTION")

#ifdef OBSCURE_OPTION
MY_API int ObscureFunction() { return 42; }
#endif

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/c_style_array_test.h included by mylib/mylib.h                                   //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//
// C Style array tests
//


// Tests with const array: since the input numbers are const, their params are published as List[int],
// and the python signature will be:
// -->    def add_c_array2(values: List[int]) -> int:
// (and the runtime will check that the list size is exactly 2)
MY_API inline int const_array2_add(const int values[2]) { return values[0] + values[1];}


// Test with a modifiable array: since the input array is not const, it could be modified.
// Thus, it will be published as a function accepting Boxed values:
// -->    def array2_modify(values_0: BoxedUnsignedLong, values_1: BoxedUnsignedLong) -> None:
MY_API inline void array2_modify(unsigned long values[2])
{
    values[0] = values[1] + values[0];
    values[1] = values[0] * values[1];
}

struct Point2 // MY_API
{
    int x, y;
};

// Test with a modifiable array that uses a user defined struct.
// Since the user defined struct is mutable in python, it will not be Boxed,
// and the python signature will be:
//-->    def get_points(out_0: Point2, out_1: Point2) -> None:
MY_API inline void array2_modify_mutable(Point2 out[2]) { out[0] = {0, 1}; out[1] = {2, 3}; }

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/c_style_buffer_to_pyarray_test.h included by mylib/mylib.h                       //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <stdint.h>
#include <stddef.h>

//
// C Style buffer to py::array tests
//
// litgen is able to recognize and transform pairs of params whose C++ signature resemble
//     (T* data, size_t|int count)
// Where
//   * `T` is a *known* numeric type, or a templated type
//   * `count` name resemble a size
//        (see LitgenOptions.fn_params_buffer_size_names: List[str] = ["nb", "size", "count", "total", "n"])
//

// add_inside_buffer: modifies a buffer by adding a value to its elements
// Will be published in python as:
// -->    def add_inside_buffer(buffer: np.ndarray, number_to_add: int) -> None:
// Warning, the python function will accept only uint8 numpy arrays, and check it at runtime!
MY_API inline void add_inside_buffer(uint8_t* buffer, size_t buffer_size, uint8_t number_to_add)
{
    for (size_t i  = 0; i < buffer_size; ++i)
        buffer[i] += number_to_add;
}

// buffer_sum: returns the sum of a *const* buffer
// Will be published in python as:
// -->    def buffer_sum(buffer: np.ndarray, stride: int = -1) -> int:
MY_API inline int buffer_sum(const uint8_t* buffer, size_t buffer_size, size_t stride= sizeof(uint8_t))
{
    int sum = 0;
    for (size_t i  = 0; i < buffer_size; ++i)
        sum += (int)buffer[i];
    return sum;
}

// add_inside_two_buffers: modifies two mutable buffers
// litgen will detect that this function uses two buffers of same size.
// Will be published in python as:
// -->    def add_inside_two_buffers(buffer_1: np.ndarray, buffer_2: np.ndarray, number_to_add: int) -> None:
MY_API inline void add_inside_two_buffers(uint8_t* buffer_1, uint8_t* buffer_2, size_t buffer_size, uint8_t number_to_add)
{
    for (size_t i  = 0; i < buffer_size; ++i)
    {
        buffer_1[i] += number_to_add;
        buffer_2[i] += number_to_add;
    }
}

// templated_mul_inside_buffer: template function that modifies an array by multiplying its elements by a given factor
// litgen will detect that this function can be published as using a numpy array.
// It will be published in python as:
// -->    def mul_inside_buffer(buffer: np.ndarray, factor: float) -> None:
//
// The type will be detected at runtime and the correct template version will be called accordingly!
// An error will be thrown if the numpy array numeric type is not supported.
template<typename T> MY_API void templated_mul_inside_buffer(T* buffer, size_t buffer_size, double factor)
{
    for (size_t i  = 0; i < buffer_size; ++i)
        buffer[i] *= (T)factor;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/c_string_list_test.h included by mylib/mylib.h                                   //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include "string.h"

//
// C String lists tests:
//   Two consecutive params (const char *, int | size_t) are exported as List[str]
//
// The following function will be exported with the following python signature:
// -->    def c_string_list_total_size(items: List[str], output_0: BoxedInt, output_1: BoxedInt) -> int:
//
MY_API inline size_t c_string_list_total_size(const char * const items[], int items_count, int output[2])
{
    size_t total = 0;
    for (size_t i = 0; i < items_count; ++i)
        total += strlen(items[i]);
    output[0] = (int)total;
    output[1] = (int)(total + 1);
    return total;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/modifiable_immutable_test.h included by mylib/mylib.h                            //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <string>

//
// Modifiable immutable python types test
//

// litgen adapts functions params that use modifiable pointer or reference to a type
// that is immutable in python.
// On the C++ side, these params are modifiable by the function.
// We need to box them into a Boxed type to ensure that any modification made by C++
// is visible when going back to Python.
//
// Note: immutable data types in python are
//   - Int, Float, String (correctly handled by litgen)
//   - Complex, Bytes (not handled)
//   - Tuple (not handled)


/////////////////////////////////////////////////////////////////////////////////////////////
// Test Part 1: in the functions below, the value parameters will be "Boxed"
//
// This is caused by the following options during generation:
//     options.fn_params_replace_modifiable_immutable_by_boxed__regexes = [
//         r"^Toggle",
//         r"^Modify",
//      ]
/////////////////////////////////////////////////////////////////////////////////////////////


// Test with pointer: a pointer
// Will be published in python as:
// -->    def toggle_bool_pointer(v: BoxedBool) -> None:
MY_API void ToggleBoolPointer(bool *v)
{
    *v = !(*v);
}

// Test with nullable pointer
// Will be published in python as:
// -->    def toggle_bool_nullable(v: BoxedBool = None) -> None:
MY_API void ToggleBoolNullable(bool *v = NULL)
{
    if (v != NULL)
        *v = !(*v);
}

// Test with reference
// Will be published in python as:
// -->    def toggle_bool_reference(v: BoxedBool) -> None:
MY_API void ToggleBoolReference(bool &v)
{
    v = !(v);
}

// Test modifiable String
// Will be published in python as:
// -->    def modify_string(s: BoxedString) -> None:
MY_API void ModifyString(std::string* s) { (*s) += "hello"; }


/////////////////////////////////////////////////////////////////////////////////////////////
//
// Test Part 2: in the functions below, the python return type is modified:
// the python functions will return a tuple:
//     (original_return_value, modified_parameter)
//
// This is caused by the following options during generation:
//
//     options.fn_params_output_modifiable_immutable_to_return__regexes = [r"^Slider"]
/////////////////////////////////////////////////////////////////////////////////////////////


// Test with int param + int return type
// Will be published in python as:
// --> def slider_bool_int(label: str, value: int) -> Tuple[bool, int]:
MY_API bool SliderBoolInt(const char* label, int * value)
{
    *value += 1;
    return true;
}

// Will be published in python as:
// -->    def slider_void_int(label: str, value: int) -> int:
MY_API void SliderVoidInt(const char* label, int * value)
{
    *value += 1;
}

// Will be published in python as:
// -->    def slider_bool_int2(label: str, value1: int, value2: int) -> Tuple[bool, int, int]:
MY_API bool SliderBoolInt2(const char* label, int * value1, int * value2)
{
    *value1 += 1;
    *value2 += 2;
    return false;
}

// Will be published in python as:
// -->    def slider_void_int_default_null(label: str, value: Optional[int] = None) -> Tuple[bool, Optional[int]]:
MY_API bool SliderVoidIntDefaultNull(const char* label, int * value = nullptr)
{
    if (value != nullptr)
        *value += 1;
    return true;
}

// Will be published in python as:
// -->    def slider_void_int_array(label: str, value: List[int]) -> Tuple[bool, List[int]]:
MY_API bool SliderVoidIntArray(const char* label, int value[3])
{
    value[0] += 1;
    value[1] += 2;
    value[2] += 3;
    return true;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/overload_test.h included by mylib/mylib.h                                        //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//
// litgen is able to detect automatically the presence of overloads that require
// to use `py::overload_cast<...>` when publishing
//

//
// overload on free functions
//

MY_API int add_overload(int a, int b) { return a + b; } // type: ignore
MY_API int add_overload(int a, int b, int c) { return a + b + c; } // type: ignore

//
// overload on methods
//

struct FooOverload // MY_API
{
    MY_API int add_overload(int a, int b) { return a + b; } // type: ignore
    MY_API int add_overload(int a, int b, int c) { return a + b + c; } // type: ignore
};


/*
For info, below is the generated C++ code that will publish these functions:

     m.def("add_overload",
        py::overload_cast<int, int>(add_overload), py::arg("a"), py::arg("b"));
    m.def("add_overload",
        py::overload_cast<int, int, int>(add_overload), py::arg("a"), py::arg("b"), py::arg("c"));


    auto pyClassFooOverload = py::class_<FooOverload>
        (m, "FooOverload", "")
        .def(py::init<>()) // implicit default constructor
        .def("add_overload",
            py::overload_cast<int, int>(&FooOverload::add_overload), py::arg("a"), py::arg("b"))
        .def("add_overload",
            py::overload_cast<int, int, int>(&FooOverload::add_overload), py::arg("a"), py::arg("b"), py::arg("c"))
        ;
*/

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/enum_test.h included by mylib/mylib.h                                            //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// BasicEnum: a simple C-style enum
enum BasicEnum     // MY_API
{
    MyEnum_a = 1, // This is value a
    MyEnum_aa,    // this is value aa
    MyEnum_aaa,   // this is value aaa

    // Lonely comment

    // This is value b
    MyEnum_b,

    // This is c
    // with doc on several lines
    MyEnum_c = MyEnum_a | MyEnum_b,

    // MyEnum_count
};


// ClassEnumNotRegistered should not be published, as it misses the marker "// MY_API"
// By default, all enums, namespaces and classes are published,
// but you can decide to include only "marked" ones, via this litgen option:
//       options.srcml_options.api_suffixes = ["MY_API"]
//
// Note: Do not remove the empty line below, otherwise this comment would become part of
//       the enum's doc, and cause it to be registered (since it contains "MY_API")

enum class ClassEnumNotRegistered
{
    On,
    Off,
    Unknown
};


// ClassEnum: a class enum that should be published
enum class ClassEnum // MY_API
{
    On = 0,
    Off,
    Unknown
};


/*
For info, below is the python pyi stub that is published for this file:

class BasicEnum(Enum):
    """ BasicEnum: a simple C-style enum"""
    my_enum_a   # (= 1)  # This is value a
    my_enum_aa  # (= 2)  # this is value aa
    my_enum_aaa # (= 3)  # this is value aaa

    # Lonely comment

    # This is value b
    my_enum_b   # (= 4)

    # This is c
    # with doc on several lines
    my_enum_c   # (= BasicEnum.my_enum_a | BasicEnum.my_enum_b)

    # MyEnum_count


# ClassEnumNotRegistered should not be published, as it misses the marker "// MY_API"
# By default, all enums, namespaces and classes are published,
# but you can decide to include only "marked" ones, via this litgen option:
#       options.srcml_options.api_suffixes = ["MY_API"]
#
# Note: Do not remove the empty line below, otherwise this comment would become part of
#       the enum's doc, and cause it to be registered (since it contains "MY_API")



class ClassEnum(Enum):
    """ ClassEnum: a class enum that should be published"""
    on      # (= 0)
    off     # (= 1)
    unknown # (= 2)
*/

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/struct_test.h included by mylib/mylib.h                                          //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <vector>


// A superb struct
struct MyStruct            // MY_API
{
    MyStruct(int factor = 10, const std::string& message = "hello"): factor(factor), message(message) {}
    ~MyStruct() {}


    ///////////////////////////////////////////////////////////////////////////
    // Simple struct members
    ///////////////////////////////////////////////////////////////////////////
    int factor = 10, delta = 0;
    std::string message;


    ///////////////////////////////////////////////////////////////////////////
    // Stl container members
    ///////////////////////////////////////////////////////////////////////////

    // By default, modifications from python are not propagated to C++ for stl containers
    // (see https://pybind11.readthedocs.io/en/stable/advanced/cast/stl.html)
    std::vector<int> numbers;
    // However you can call dedicated modifying methods
    MY_API void append_number_from_cpp(int v) { numbers.push_back(v); }


    ///////////////////////////////////////////////////////////////////////////
    // Fixed size *numeric* array members
    //
    // They will be published as a py::array, and modifications will be propagated
    // on both sides transparently.
    ///////////////////////////////////////////////////////////////////////////

    int values[2] = {0, 1};
    bool flags[3] = {false, true, false};
    // points is a fixed size array, but not of a numeric type. It will *not* be published!
    Point2 points[2];


    ///////////////////////////////////////////////////////////////////////////
    // Simple methods
    ///////////////////////////////////////////////////////////////////////////

    // calc: example of simple method
    MY_API int calc(int x) { return x * factor + delta; }
    // set_message: another example of simple method
    MY_API void set_message(const std::string & m) { message = m;}

    // unpublished_calc: this function should not be published (no MY_API marker)
    int unpublished_calc(int x) { return x * factor + delta + 3;}

    ///////////////////////////////////////////////////////////////////////////

    ///////////////////////////////////////////////////////////////////////////

    // Instance() is a method that returns a pointer that should use `return_value_policy::reference`
    static MyStruct& Instance() { static MyStruct instance; return instance; }  // return_value_policy::reference
};

MY_API MyStruct* FooInstance() { return & MyStruct::Instance(); } // return_value_policy::reference


// StructNotRegistered should not be published, as it misses the marker "// MY_API"
// By default, all enums, namespaces and classes are published,
// but you can decide to include only "marked" ones, via this litgen option:
//       options.srcml_options.api_suffixes = ["MY_API"]
//
// Note: Do not remove the empty line below, otherwise this comment would become part of
//       the enum's doc, and cause it to be registered (since it contains "MY_API")

struct StructNotRegistered
{
    int a = 0;
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                       mylib/return_value_policy_test.h included by mylib/mylib.h                             //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////


struct MyConfig            // MY_API
{
    int sum = 0;

    // Instance() is a method that returns a pointer that should use `return_value_policy::reference`
    MY_API static MyConfig& Instance() // return_value_policy::reference
    {
        static MyConfig instance;
        return instance;
    }
};

MY_API MyConfig* MyConfigInstance() { return & MyConfig::Instance(); } // return_value_policy::reference
