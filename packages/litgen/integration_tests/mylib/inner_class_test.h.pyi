# ============================================================================
# This file was autogenerated
# It is presented side to side with its source: inner_class_test.h
#    (see integration_tests/bindings/lg_mylib/__init__pyi which contains the full
#     stub code, including this code)
# ============================================================================

# type: ignore
import sys
from typing import Literal, List, Any, Optional, Tuple, Dict
import numpy as np
from enum import Enum, auto
import numpy

# <litgen_stub> // Autogenerated code below! Do not edit!
####################    <generated_from:inner_class_test.h>    ####################
# <submodule some_namespace>
class some_namespace:  # Proxy class that introduces typings for the *submodule* some_namespace
    pass  # (This corresponds to a C++ namespace. All method are static!)
    """ namespace SomeNamespace"""

    class ParentStruct:
        class InnerStruct:
            value: int

            def __init__(self, value: int = 10) -> None:
                pass
            def add(self, a: int, b: int) -> int:
                pass

        class InnerEnum(enum.Enum):
            zero = enum.auto()  # (= 0)
            one = enum.auto()  # (= 1)
            two = enum.auto()  # (= 2)
            three = enum.auto()  # (= 3)
        inner_struct: InnerStruct = InnerStruct()
        inner_enum: InnerEnum = InnerEnum.three
        def __init__(
            self,
            inner_struct: ParentStruct.InnerStruct = ParentStruct.InnerStruct(),
            inner_enum: ParentStruct.InnerEnum = ParentStruct.InnerEnum.three,
        ) -> None:
            """Auto-generated default constructor with named params"""
            pass

# </submodule some_namespace>
####################    </generated_from:inner_class_test.h>    ####################

# </litgen_stub> // Autogenerated code end!
