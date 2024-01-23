# ============================================================================
# This file was autogenerated
# It is presented side to side with its source: mix_adapters_class_test.h
#    (see integration_tests/bindings/lg_mylib/__init__pyi which contains the full
#     stub code, including this code)
# ============================================================================

# type: ignore
from typing import List, Tuple
import numpy as np

# <litgen_stub> // Autogenerated code below! Do not edit!
####################    <generated_from:BoxedTypes>    ####################
class BoxedBool:
    value: bool
    def __init__(self, v: bool = False) -> None:
        pass
    def __repr__(self) -> str:
        pass

class BoxedInt:
    value: int
    def __init__(self, v: int = 0) -> None:
        pass
    def __repr__(self) -> str:
        pass

class BoxedString:
    value: str
    def __init__(self, v: str = "") -> None:
        pass
    def __repr__(self) -> str:
        pass

####################    </generated_from:BoxedTypes>    ####################

####################    <generated_from:mix_adapters_class_test.h>    ####################
# More complex tests, where we combine litgen function adapters with classes and namespace
#
# The main intent of these tests is to verify that the generated code compiles.
# The corresponding python test file will not test all these functions
# (as they are in fact copy/pasted/adapted from other tests)
#

# <submodule some_namespace>
class some_namespace:  # Proxy class that introduces typings for the *submodule* some_namespace
    pass  # (This corresponds to a C++ namespace. All method are static!)

    class Blah:
        """struct Blah"""

        def toggle_bool_pointer(self, v: BoxedBool) -> None:
            """//, int vv[2])"""
            pass
        def toggle_bool_pointer_get_points(
            self, v: BoxedBool, vv_0: BoxedInt, vv_1: BoxedInt
        ) -> None:
            pass
        def modify_string(self, s: BoxedString) -> None:
            pass
        def change_bool_int(self, label: str, value: int) -> Tuple[bool, int]:
            pass
        def add_inside_buffer(self, buffer: np.ndarray, number_to_add: int) -> None:
            pass
        def templated_mul_inside_buffer(
            self, buffer: np.ndarray, factor: float
        ) -> None:
            pass
        def const_array2_add(self, values: List[int]) -> int:
            pass
        def c_string_list_total_size(
            self, items: List[str], output_0: BoxedInt, output_1: BoxedInt
        ) -> int:
            pass
        def __init__(self) -> None:
            """Auto-generated default constructor"""
            pass
    # <submodule some_inner_namespace>
    class some_inner_namespace:  # Proxy class that introduces typings for the *submodule* some_inner_namespace
        pass  # (This corresponds to a C++ namespace. All method are static!)
        """ namespace SomeInnerNamespace"""
        @staticmethod
        def toggle_bool_pointer(v: BoxedBool) -> None:
            """//, int vv[2])"""
            pass
        @staticmethod
        def toggle_bool_pointer_get_points(
            v: BoxedBool, vv_0: BoxedInt, vv_1: BoxedInt
        ) -> None:
            pass
        @staticmethod
        def modify_string(s: BoxedString) -> None:
            pass
        @staticmethod
        def change_bool_int(label: str, value: int) -> Tuple[bool, int]:
            pass
        @staticmethod
        def add_inside_buffer(buffer: np.ndarray, number_to_add: int) -> None:
            pass
        @staticmethod
        def templated_mul_inside_buffer(buffer: np.ndarray, factor: float) -> None:
            pass
        @staticmethod
        def const_array2_add(values: List[int]) -> int:
            pass
        @staticmethod
        def c_string_list_total_size(
            items: List[str], output_0: BoxedInt, output_1: BoxedInt
        ) -> int:
            pass
    # </submodule some_inner_namespace>

# </submodule some_namespace>
####################    </generated_from:mix_adapters_class_test.h>    ####################

# </litgen_stub> // Autogenerated code end!
