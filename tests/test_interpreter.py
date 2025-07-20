import unittest
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


if __name__ == "__main__":
    unittest.main()
