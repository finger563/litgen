import os, sys; _THIS_DIR = os.path.dirname(__file__); sys.path = [_THIS_DIR + "/.."] + sys.path

from litgen.internal import srcml
from litgen.internal import code_utils
import litgen


def read_file_content(filename):
    with open(filename, "r") as f:
        content = f.read()
    return content


def play_code():
    options = litgen.code_style_imgui()
    code = """
MY_API inline int8_t test_with_one_const_buffer(const int8_t* values, int count) {}
    """

    cpp_unit = srcml.code_to_cpp_unit(options, code)
    print(cpp_unit)

def play_imgui():
    options = litgen.code_style_imgui()
    source_filename = os.path.realpath(_THIS_DIR + "/../../../examples_real_libs/imgui/imgui.h")
    cpp_unit = srcml.file_to_cpp_unit(options, source_filename)
    # print(cpp_unit)

#test_code()

#test_imgui()

play_code()