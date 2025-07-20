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

    def test_list_creation(self):
        result = self.run_code("(list 1 2 3)")
        self.assertEqual(result, [1, 2, 3])

    def test_get_from_list(self):
        result = self.run_code("""
            (define items (list 10 20 30))
            (get items 1)
        """)
        self.assertEqual(result, 20)

    def test_length_of_list(self):
        result = self.run_code("""
            (define items (list 5 6 7 8))
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

    def test_div_list_and_list(self):
        result = self.run_code("(/ (list 1 2 3) (list 1 2 3))")
        self.assertEqual(result, [1, 1, 1])

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

    def test_compare_list_with_number(self):
        result = self.run_code("(= (list 1 2 3) 3)")
        self.assertEqual(result, [False, False, True])

        result = self.run_code("(< (list 1 2 3) 5)")
        self.assertEqual(result, [True, True, True])

        result = self.run_code("(> 2 (list 1 3 2))")
        self.assertEqual(result, [True, False, False])

    def test_lambda_const_function(self):
        result = self.run_code("""
            (func const (x) (lambda (y) x))
            (define x 5)
            ((const 3) 7)
        """)
        self.assertEqual(result, 3)

    def test_head_function(self):
        result = self.run_code("""
            (head (list 10 23 2))
        """)
        self.assertEqual(result, 10)

    def test_tail_function(self):
        result = self.run_code("""
            (tail (list 1 2 3 4))
        """)
        self.assertEqual(result, [2, 3, 4])

    def test_append_function(self):
        result = self.run_code("""
            (define a (list 1 2))
            (define b (list 3 4))
            (append a b)
        """)
        self.assertEqual(result, [1, 2, 3, 4])

    def test_reverse_function(self):
        result = self.run_code("""
            (reverse (list "a" "b" "c"))
        """)
        self.assertEqual(result, ["c", "b", "a"])

    def test_cons_function(self):
        result = self.run_code("""
            (push 1 (list 2 3))
        """)
        self.assertEqual(result, [1, 2, 3])

    def test_empty_function(self):
        result1 = self.run_code("(empty? (list))")
        self.assertTrue(result1)

        result2 = self.run_code("(empty? (list 1 2 3))")
        self.assertFalse(result2)


if __name__ == "__main__":
    unittest.main()
