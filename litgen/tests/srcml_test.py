import os, sys; _THIS_DIR = os.path.dirname(__file__); sys.path = [_THIS_DIR + "/.."] + sys.path

import litgen.internal.srcml as srcml
import litgen.internal.code_utils as code_utils


def assert_code_unmodified_by_srcml(code: str):
    """
    We transform the code to xml (srcML), and assert that it can safely be translated back to the same code
    """
    root = srcml.code_to_srcml(code)
    code2 = srcml.srcml_to_code(root)
    assert code2 == code


def test_srcml_does_not_modify_code():
    assert_code_unmodified_by_srcml("int a = 1;")
    assert_code_unmodified_by_srcml("void foo(int x, int y=5){};")
    assert_code_unmodified_by_srcml("""
    #include <nonexistingfile.h>
    #define TRUC
    // A super nice function
    template<typename T> constexpr T add(const T& a, T b) { return a + b;}
    
    /* A dummy comment */
                            ;;TRUC;;TRUC; TRUC TRUC   ;;;; // and some gratuitous elements
    // A lambda
    auto fnSub = [](int a, int b) { return b - a;};
    """)


def test_parse_cpp_decl_statement():
    # Basic test
    code = "int a;"
    element = srcml.first_code_element_with_tag(code, "decl_stmt")
    cpp_decl_statement  = srcml.parse_cpp_decl_stmt(element)
    code_utils.assert_are_equal_ignore_spaces(cpp_decl_statement, """
        CppDeclStatement(cpp_decls=[
            CppDecl(cpp_type=CppType(name_cpp='int', specifiers=[], modifiers=[]), name_cpp='a', init_cpp='')])""")

    # Test with * and initial value
    code = "const int* a = 1;"
    element = srcml.first_code_element_with_tag(code, "decl_stmt")
    cpp_decl_statement  = srcml.parse_cpp_decl_stmt(element)
    code_utils.assert_are_equal_ignore_spaces(cpp_decl_statement, """
        CppDeclStatement(cpp_decls=[
            CppDecl(cpp_type=CppType(name_cpp='int', specifiers=['const'], modifiers=['*']), name_cpp='a', init_cpp='1')])""")

    # Test with several variables + modifiers
    code = "int a = 3, &b, *c;"
    element = srcml.first_code_element_with_tag(code, "decl_stmt")
    cpp_decl_statement  = srcml.parse_cpp_decl_stmt(element)
    code_utils.assert_are_equal_ignore_spaces(cpp_decl_statement, """
        CppDeclStatement(cpp_decls=[
            CppDecl(cpp_type=CppType(name_cpp='int', specifiers=[], modifiers=[]), name_cpp='a', init_cpp='3'), 
            CppDecl(cpp_type=CppType(name_cpp='int', specifiers=[], modifiers=['&']), name_cpp='b', init_cpp=''), 
            CppDecl(cpp_type=CppType(name_cpp='int', specifiers=[], modifiers=['*']), name_cpp='c', init_cpp='')])""")

    # Test with double pointer, which creates a double modifier
    code = "uchar **buffer;"
    element = srcml.first_code_element_with_tag(code, "decl_stmt")
    cpp_decl_statement  = srcml.parse_cpp_decl_stmt(element)
    code_utils.assert_are_equal_ignore_spaces(cpp_decl_statement, """
        CppDeclStatement(cpp_decls=[
            CppDecl(cpp_type=CppType(name_cpp='uchar', specifiers=[], modifiers=['*', '*']), name_cpp='buffer', init_cpp='')])""")

    # Test with a template type
    code = "std::map<int, std::string> x = {1, 2, 3};"
    element = srcml.first_code_element_with_tag(code, "decl_stmt")
    cpp_decl_statement  = srcml.parse_cpp_decl_stmt(element)
    code_utils.assert_are_equal_ignore_spaces(cpp_decl_statement, """
        CppDeclStatement(cpp_decls=[
            CppDecl(cpp_type=CppType(name_cpp='std::map<int, std::string>', specifiers=[], modifiers=[]), name_cpp='x', init_cpp='{1, 2, 3}')])""")


def test_parse_function_decl():
    # Basic test
    code = "int foo();"
    element = srcml.first_code_element_with_tag(code, "function_decl")
    function_decl  = srcml.parse_function_decl(element)
    assert str(function_decl) == "CppFunctionDecl(type=CppType(name_cpp='int', specifiers=[], modifiers=[]), name_cpp='foo', parameter_list=CppParameterList(parameters=[]))"

    # Test with params and default values
    code = "int add(int a, int b = 5);"
    element = srcml.first_code_element_with_tag(code, "function_decl")
    function_decl  = srcml.parse_function_decl(element)
    code_utils.assert_are_equal_ignore_spaces(
        str(function_decl), """
        CppFunctionDecl(type=CppType(name_cpp='int', specifiers=[], modifiers=[]), name_cpp='add', 
            parameter_list=CppParameterList(parameters=[
                CppParameter(decl=CppDecl(cpp_type=CppType(name_cpp='int', specifiers=[], modifiers=[]), name_cpp='a', init_cpp='')), 
                CppParameter(decl=CppDecl(cpp_type=CppType(name_cpp='int', specifiers=[], modifiers=[]), name_cpp='b', init_cpp='5'))
                ]))"""
        )

    # Test with template types
    code = """
    std::vector<std::pair<size_t, int>> enumerate(const std::vector<int>& xs);
    """
    element = srcml.first_code_element_with_tag(code, "function_decl")
    function_decl  = srcml.parse_function_decl(element)
    code_utils.assert_are_equal_ignore_spaces(function_decl, """
        CppFunctionDecl(type=CppType(name_cpp='std::vector<std::pair<size_t, int>>', specifiers=[], modifiers=[]), name_cpp='enumerate', 
            parameter_list=CppParameterList(parameters=[
                CppParameter(decl=CppDecl(cpp_type=CppType(name_cpp='std::vector<int>', specifiers=['const'], modifiers=['&']), name_cpp='xs', init_cpp=''))]))
        """)


    # Test with type declared after ->
    code = "auto divide(int a, int b) -> double;"
    element = srcml.first_code_element_with_tag(code, "function_decl")
    function_decl  = srcml.parse_function_decl(element)
    code_utils.assert_are_equal_ignore_spaces(function_decl, """
        CppFunctionDecl(type=CppType(name_cpp='double', specifiers=[], modifiers=[]), name_cpp='divide', 
            parameter_list=CppParameterList(parameters=[
                CppParameter(decl=CppDecl(cpp_type=CppType(name_cpp='int', specifiers=[], modifiers=[]), name_cpp='a', init_cpp='')), 
                CppParameter(decl=CppDecl(cpp_type=CppType(name_cpp='int', specifiers=[], modifiers=[]), name_cpp='b', init_cpp=''))]))    
        """)


    # Test with inferred type
    code = "auto minimum(int&& a, int b = 5);"
    element = srcml.first_code_element_with_tag(code, "function_decl")
    function_decl  = srcml.parse_function_decl(element)
    code_utils.assert_are_equal_ignore_spaces(function_decl, """
        CppFunctionDecl(type=CppType(name_cpp='auto', specifiers=[], modifiers=[]), name_cpp='minimum', 
            parameter_list=CppParameterList(parameters=[
                CppParameter(decl=CppDecl(cpp_type=CppType(name_cpp='int', specifiers=[], modifiers=['&&']), name_cpp='a', init_cpp='')), 
                CppParameter(decl=CppDecl(cpp_type=CppType(name_cpp='int', specifiers=[], modifiers=[]), name_cpp='b', init_cpp='5'))]))        
        """)


test_parse_function_decl()
