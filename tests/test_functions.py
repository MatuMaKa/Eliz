# python -m unittest tests.test_functions -v

import unittest

from eliz.frontend.lexer import Lexer
from eliz.frontend.parser import Parser
from eliz.runtime.interpreter import Interpreter


class TestFunctions(unittest.TestCase):
    def run_eliz(self, source: str):
        tokens = Lexer(source).tokenize()
        program = Parser(tokens).parse()

        interpreter = Interpreter()
        interpreter.interpret(program)

    def test_function_with_return(self):
        source = """
        public fn add(a: Int, b: Int) {
            return a + b;
        }

        let result = add(5, 3);
        print(result);
        """

        self.run_eliz(source)

    def test_function_without_return(self):
        source = """
        public fn greet(name: String) {
            print("Hello, " + name);
        }

        greet("Eliz");
        """

        self.run_eliz(source)

    def test_nested_function_calls(self):
        source = """
        public fn add(a: Int, b: Int) {
            return a + b;
        }

        public fn multiply(a: Int, b: Int) {
            return a * b;
        }

        let result = add(multiply(2, 3), 4);
        print(result);
        """

        self.run_eliz(source)

    def test_wrong_argument_count(self):
        source = """
        public fn add(a: Int, b: Int) {
            return a + b;
        }

        add(5);
        """

        with self.assertRaises(Exception):
            self.run_eliz(source)


if __name__ == "__main__":
    unittest.main()
