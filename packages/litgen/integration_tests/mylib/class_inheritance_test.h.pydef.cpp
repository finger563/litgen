// ============================================================================
// This file was autogenerated
// It is presented side to side with its source: class_inheritance_test.h
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
    ////////////////////    <generated_from:class_inheritance_test.h>    ////////////////////
    m.def("make_dog",
        make_dog, "Test that downcasting works: the return type is Animal, but it should bark!");

    { // <namespace Animals>
        py::module_ pyNsAnimals = m.def_submodule("Animals", "");
        auto pyNsAnimals_ClassAnimal =
            py::class_<Animals::Animal>
                (pyNsAnimals, "Animal", "")
            .def(py::init<const std::string &>(),
                py::arg("name"))
            .def_readwrite("name", &Animals::Animal::name, "")
            ;


        auto pyNsAnimals_ClassDog =
            py::class_<Animals::Dog, Animals::Animal>
                (pyNsAnimals, "Dog", "")
            .def(py::init<const std::string &>(),
                py::arg("name"))
            .def("bark",
                &Animals::Dog::bark)
            ;
    } // </namespace Animals>

    { // <namespace Home>
        py::module_ pyNsHome = m.def_submodule("Home", "");
        auto pyNsHome_ClassPet =
            py::class_<Home::Pet>
                (pyNsHome, "Pet", "")
            .def(py::init<>()) // implicit default constructor
            .def("is_pet",
                &Home::Pet::is_pet)
            ;


        auto pyNsHome_ClassPetDog =
            py::class_<Home::PetDog, Animals::Dog, Home::Pet>
                (pyNsHome, "PetDog", "")
            .def(py::init<const std::string &>(),
                py::arg("name"))
            .def("bark",
                &Home::PetDog::bark)
            ;
    } // </namespace Home>
    ////////////////////    </generated_from:class_inheritance_test.h>    ////////////////////

    // </litgen_pydef> // Autogenerated code end
}
