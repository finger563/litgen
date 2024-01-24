# ============================================================================
# This file was autogenerated
# It is presented side to side with its source: brace_init_default_value.h
#    (see integration_tests/bindings/lg_mylib/__init__pyi which contains the full
#     stub code, including this code)
# ============================================================================
# ruff: noqa: B008
from typing import List, Dict

# type: ignore

# <litgen_stub> // Autogenerated code below! Do not edit!
####################    <generated_from:brace_init_default_value.h>    ####################


class FooBrace:
    int_values: List[int] = List[int](1, 2, 3)
    dict_string_int: Dict[str, int] = Dict[str, int]({"abc", 3})
    def __init__(self, int_values: List[int] = List[int](1, 2, 3)) -> None:
        """Auto-generated default constructor with named params"""
        pass


def fn_brace(foo_brace: FooBrace = FooBrace(), ints: List[int] = List[int](1, 2, 3)) -> int:
    pass
####################    </generated_from:brace_init_default_value.h>    ####################

# </litgen_stub> // Autogenerated code end!
