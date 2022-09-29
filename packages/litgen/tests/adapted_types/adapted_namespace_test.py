from codemanip import code_utils

import litgen
from litgen import LitgenOptions


# Other tests exist for namespace exist inside litgen_context_test.py
# (since namespaces store their code in the context most of the time)


def test_namespaces():
    options = LitgenOptions()
    options.namespace_root__regex = code_utils.make_regex_exact_word("Main")
    # In the code below:
    # - the namespace details should be excluded
    # - the namespace Main should not be outputted as a submodule
    # - the namespace Inner should be produced as a submodule
    # - occurrences of namespace Inner should be grouped
    code = code_utils.unindent_code(
        """
void FooRoot();
namespace details { void FooDetails(); }
namespace Main  // This namespace should not be outputted as a submodule
{
    // this is an inner namespace (this comment should become the namespace doc)
    namespace Inner
    {
        void FooInner();
    }

    // This is a second occurrence of the same inner namespace
    // The generated python module will merge these occurrences
    // (and this comment will be ignored, since the Inner namespace already has a doc)
    namespace Inner
    {
        void FooInner2();
    }
}
    """,
        flag_strip_empty_lines=True,
    )

    generated_code = litgen.generate_code(options, code)

    code_utils.assert_are_codes_equal(
        generated_code.stub_code,
        '''
        def foo_root() -> None:
            pass
        """This namespace should not be outputted as a submodule"""


        # <submodule Inner>
        class Inner: # Proxy class that introduces typings for the *submodule* Inner
            # (This corresponds to a C++ namespace. All method are static!)
            """ this is an inner namespace (this comment should become the namespace doc)"""
            def foo_inner() -> None:
                pass
            def foo_inner2() -> None:
                pass

        # </submodule Inner>
    ''',
    )

    code_utils.assert_are_codes_equal(
        generated_code.pydef_code,
        """
            m.def("foo_root",
                FooRoot);

            { // <namespace Inner>
                py::module_ pyNamespaceInner = m.def_submodule("Inner", "this is an inner namespace (this comment should become the namespace doc)");
                pyNamespaceInner.def("foo_inner",
                    Main::Inner::FooInner);
                pyNamespaceInner.def("foo_inner2",
                    Main::Inner::FooInner2);
            } // </namespace Inner>
    """,
    )
