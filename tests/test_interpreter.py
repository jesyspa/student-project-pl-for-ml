import unittest
import io
import sys
from nelox.scanner import Scanner
from nelox.parser import Parser
from nelox.interpreter import Interpreter


class InterpreterTest(unittest.TestCase):

    def run_code(self, source):
        scanner = Scanner(source)
        parser = Parser(scanner)
        expressions = parser.parse()
        interpreter = Interpreter()
        return interpreter.interpret(expressions)

    def run_code_with_input(self, source, input_data):
        original_stdin = sys.stdin
        try:
            sys.stdin = io.StringIO(input_data)
            return self.run_code(source)
        finally:
            sys.stdin = original_stdin

    def test_simple_arithmetic(self):
        self.assertEqual(self.run_code("(+ 1 2)"), 3)
        self.assertEqual(self.run_code("(* 3 4)"), 12)
        self.assertEqual(self.run_code("(- 10 3)"), 7)
        self.assertEqual(self.run_code("(/ 8 2)"), 4.0)

    def test_set_variable(self):
        result = self.run_code("""
            (define x 42)
            x
        """)
        self.assertEqual(result, 42)

    def test_update_variable(self):
        result = self.run_code("""
            (define x 1)
            (set x 99)
            x
        """)
        self.assertEqual(result, 99)

    def test_variable_shadowing(self):
        result = self.run_code("""
            (define x 10)
            (func f (x) (+ x 1))
            (f 5)
        """)
        self.assertEqual(result, 6)

    def test_if_true_branch(self):
        result = self.run_code("""
            (if (> 5 3)
                1
                0)
        """)
        self.assertEqual(result, 1)

    def test_if_false_branch(self):
        result = self.run_code("""
            (if (< 2 1)
                1
                0)
        """)
        self.assertEqual(result, 0)

    def test_function(self):
        result = self.run_code("""
            (func square (x) (* x x))
            (square 6)
        """)
        self.assertEqual(result, 36)

    def test_lambda_simple(self):
        result = self.run_code("""
            ((lambda (a b) (+ a b)) 4 6)
        """)
        self.assertEqual(result, 10)

    def test_lambda_closure(self):
        result = self.run_code("""
            (define x 100)
            (define make_adder (lambda (y) (lambda (z) (+ x y z))))
            (define add_all (make_adder 5))
            (add_all 2)
        """)
        self.assertEqual(result, 107)

    def test_true_and_false(self):
        result = self.run_code("""
            (define x true)
            (if x 123 456)
        """)
        self.assertEqual(result, 123)

        result = self.run_code("""
            (define x false)
            (if x 123 456)
        """)
        self.assertEqual(result, 456)

    def test_lambda_counter(self):
        result = self.run_code("""
            (define make-counter
              (lambda ()
                (begin
                  (define count 0)
                  (lambda ()
                    (begin
                      (set count (+ count 1))
                      count)))))

            (define c (make-counter))
            (c)
            (c)
            (c)
        """)
        self.assertEqual(result, 3)

    def test_lambda_const_function(self):
        result = self.run_code("""
            (func const (x) (lambda (y) x))
            (define x 5)
            ((const 3) 7)
        """)
        self.assertEqual(result, 3)

    def test_read_int(self):
        code = """
            (define x 0)
            (read-int x)
            x
        """
        result = self.run_code_with_input(code, "12\n")
        self.assertEqual(result, 12)

    def test_while_loop(self):
        code = """
            (define x 0)
            (while (< x 5)
                (set x (+ x 1)))
            x
        """
        result = self.run_code(code)
        self.assertEqual(result, 5)

    def test_modulus(self):
        self.assertEqual(self.run_code("(mod 10 3)"), 1)
        self.assertEqual(self.run_code("(mod 20 5)"), 0)

    def test_not_equal_operator(self):
        self.assertEqual(self.run_code("(not-eq 5 3)"), True)
        self.assertEqual(self.run_code("(not-eq 4 4)"), False)
        self.assertEqual(self.run_code("(not-eq (+ 1 2) 4)"), True)

    def test_logical_not(self):
        self.assertEqual(self.run_code("(not true)"), False)
        self.assertEqual(self.run_code("(not false)"), True)
        self.assertEqual(self.run_code("(not 0)"), True)
        self.assertEqual(self.run_code("(not 1)"), False)

    def test_integer_division(self):
        self.assertEqual(self.run_code("(div 7 2)"), 3)
        self.assertEqual(self.run_code("(div 10 3)"), 3)
        self.assertEqual(self.run_code("(div 5 5)"), 1)

    def test_logical_and_or(self):
        self.assertEqual(self.run_code("(and true true)"), True)
        self.assertEqual(self.run_code("(and true false)"), False)
        self.assertEqual(self.run_code("(or false true)"), True)
        self.assertEqual(self.run_code("(or false (or false true))"), True)
        self.assertEqual(self.run_code("(and (> 3 2) (< 5 10))"), True)
        self.assertEqual(self.run_code("(or (= 1 2) (> 10 3))"), True)
        self.assertEqual(self.run_code("(and false false true)"), False)


if __name__ == "__main__":
    unittest.main()
