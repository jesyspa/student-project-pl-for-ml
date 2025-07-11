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
            (set x 42)
            x
        """)
        self.assertEqual(result, 42)

    def test_update_variable(self):
        result = self.run_code("""
            (set x 1)
            (set x 99)
            x
        """)
        self.assertEqual(result, 99)

    def test_variable_shadowing(self):
        result = self.run_code("""
            (set x 10)
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
            (set x 100)
            (set make_adder (lambda (y) (lambda (z) (+ x y z))))
            (set add_all (make_adder 5))
            (add_all 2)
        """)
        self.assertEqual(result, 107)

    def test_list_creation(self):
        result = self.run_code("(list 1 2 3)")
        self.assertEqual(result, [1, 2, 3])

    def test_get_from_list(self):
        result = self.run_code("""
            (set items (list 10 20 30))
            (get items 1)
        """)
        self.assertEqual(result, 20)

    def test_length_of_list(self):
        result = self.run_code("""
            (set items (list 5 6 7 8))
            (length items)
        """)
        self.assertEqual(result, 4)

    def test_add_string_and_number(self):
        result = self.run_code('( + "Answer: " 42 )')
        self.assertEqual(result, "Answer: 42")

    def test_add_number_and_list(self):
        result = self.run_code("""
            (+ (list 1 2 3) 1)
        """)
        self.assertEqual(result, [2, 3, 4])

    def test_add_list_and_number_reverse(self):
        result = self.run_code("""
            (+ 10 (list 1 2 3))
        """)
        self.assertEqual(result, [11, 12, 13])

    def test_subtract_list_and_number(self):
        result = self.run_code("(- (list 10 20 30) 5)")
        self.assertEqual(result, [5, 15, 25])

    def test_subtract_number_and_list(self):
        result = self.run_code("(- 100 (list 10 20 30))")
        self.assertEqual(result, [90, 80, 70])

    def test_mult_list_and_number(self):
        result = self.run_code("(* (list 1 2 3) 3)")
        self.assertEqual(result, [3, 6, 9])

    def test_mult_number_and_list(self):
        result = self.run_code("(* 2 (list 10 20))")
        self.assertEqual(result, [20, 40])

    def test_div_number_and_list(self):
        result = self.run_code("(/ 100 (list 2 4 5))")
        self.assertEqual(result, [50.0, 25.0, 20.0])

    def test_div_list_and_number(self):
        result = self.run_code("(/ (list 20 40 60) 2)")
        self.assertEqual(result, [10.0, 20.0, 30.0])

    def test_true_and_false(self):
        result = self.run_code("""
            (set x true)
            (if x 123 456)
        """)
        self.assertEqual(result, 123)

        result = self.run_code("""
            (set x false)
            (if x 123 456)
        """)
        self.assertEqual(result, 456)


if __name__ == "__main__":
    unittest.main()
