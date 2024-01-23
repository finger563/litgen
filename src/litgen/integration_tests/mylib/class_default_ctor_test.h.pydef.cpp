// ============================================================================
// This file was autogenerated
// It is presented side to side with its source: class_default_ctor_test.h
// It is not used in the compilation
//    (see integration_tests/bindings/pybind_mylib.cpp which contains the full binding
//     code, including this code)
// ============================================================================

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <pybind11/numpy.h>
#include "mylib_main/mylib.h"

namespace py = pybind11;

// <litgen_glue_code>  // Autogenerated code below! Do not edit!

// </litgen_glue_code> // Autogenerated code end


void py_init_module_mylib(py::module& m)
{
    // <litgen_pydef> // Autogenerated code below! Do not edit!
    ////////////////////    <generated_from:class_default_ctor_test.h>    ////////////////////

    { // <namespace A>
        py::module_ pyNsA = m.def_submodule("a", "");
        py::enum_<A::Foo>(pyNsA, "Foo", py::arithmetic(), "")
            .value("foo1", A::Foo::Foo1, "")
            .value("foo2", A::Foo::Foo2, "")
            .value("foo3", A::Foo::Foo3, "");


        auto pyNsA_ClassClassNoDefaultCtor =
            py::class_<A::ClassNoDefaultCtor>
                (pyNsA, "ClassNoDefaultCtor", " This struct has no default constructor, so a default named constructor\n will be provided for python")
            .def(py::init<>([](
            bool b = true, int a = int(), int c = 3, A::Foo foo = A::Foo::Foo1)
            {
                auto r = std::make_unique<A::ClassNoDefaultCtor>();
                r->b = b;
                r->a = a;
                r->c = c;
                r->foo = foo;
                return r;
            })
            , py::arg("b") = true, py::arg("a") = int(), py::arg("c") = 3, py::arg("foo") = A::Foo::Foo1
            )
            .def_readwrite("b", &A::ClassNoDefaultCtor::b, "")
            .def_readwrite("a", &A::ClassNoDefaultCtor::a, "")
            .def_readwrite("c", &A::ClassNoDefaultCtor::c, "")
            .def_readwrite("foo", &A::ClassNoDefaultCtor::foo, "")
            .def_readonly("s", &A::ClassNoDefaultCtor::s, "")
            ;
        { // <namespace N>
            py::module_ pyNsA_NsN = pyNsA.def_submodule("n", "");
            auto pyNsA_NsN_ClassS =
                py::class_<A::N::S>
                    (pyNsA_NsN, "S", "")
                .def(py::init<>()) // implicit default constructor
                ;


            py::enum_<A::N::EC>(pyNsA_NsN, "EC", py::arithmetic(), "")
                .value("a", A::N::EC::a, "");


            py::enum_<A::N::E>(pyNsA_NsN, "E", py::arithmetic(), "")
                .value("a", A::N::E_a, "");


            pyNsA_NsN.def("foo",
                py::overload_cast<A::N::EC>(A::N::Foo), py::arg("e") = A::N::EC::a);

            pyNsA_NsN.def("foo",
                py::overload_cast<A::N::E>(A::N::Foo), py::arg("e") = A::N::E_a);

            pyNsA_NsN.def("foo",
                py::overload_cast<A::N::E, A::N::S>(A::N::Foo), py::arg("e") = A::N::E_a, py::arg("s") = A::N::S());
        } // </namespace N>

    } // </namespace A>
    ////////////////////    </generated_from:class_default_ctor_test.h>    ////////////////////

    // </litgen_pydef> // Autogenerated code end
}
