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
            (if (<= 2 1)
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
                  (define count 0)
                  (lambda ()
                      (set count (+ count 1))
                      count)))

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
            (while (< x 5) $commenting test
                (set x (+ x 1)))
            x
        """
        result = self.run_code(code)
        self.assertEqual(result, 5)

    def test_modulus(self):
        self.assertEqual(self.run_code("(mod 10 3)"), 1)
        self.assertEqual(self.run_code("(mod 20 5)"), 0)

    def test_not_not_equal_operator(self):
        self.assertEqual(self.run_code("(!= 5 3)"), True)
        self.assertEqual(self.run_code("(!= 4 4)"), False)
        self.assertEqual(self.run_code("(!= (+ 1 2) 4)"), True)

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

    def test_head(self):
        self.assertEqual(self.run_code("(head (list 1 2 3))"), 1)
        self.assertEqual(self.run_code("(head (list))"), None)

    def test_tail(self):
        self.assertEqual(self.run_code("(tail (list 1 2 3))"), [2, 3])
        self.assertEqual(self.run_code("(tail (list 1))"), [])
        self.assertEqual(self.run_code("(tail (list))"), [])

    def test_append_lists(self):
        self.assertEqual(self.run_code("(append (list 1 2) (list 3 4))"), [1, 2, 3, 4])

    def test_append_strings(self):
        self.assertEqual(self.run_code('(append "hello" " world")'), "hello world")

    def test_append_type_error(self):
        with self.assertRaises(RuntimeError):
            self.run_code('(append (list 1 2) "not a list")')

    def test_reverse(self):
        self.assertEqual(self.run_code("(reverse (list 1 2 3))"), [3, 2, 1])
        self.assertEqual(self.run_code("(reverse (list))"), [])

    def test_reverse_type_error(self):
        with self.assertRaises(RuntimeError):
            self.run_code('(reverse "not a list")')

    def test_push(self):
        self.assertEqual(self.run_code("(push 0 (list 1 2 3))"), [0, 1, 2, 3])

    def test_push_type_error(self):
        with self.assertRaises(RuntimeError):
            self.run_code('(push 1 "not a list")')

    def test_empty_question(self):
        self.assertEqual(self.run_code("(empty? (list))"), True)
        self.assertEqual(self.run_code("(empty? (list 1 2))"), False)

    def test_empty_type_error(self):
        with self.assertRaises(RuntimeError):
            self.run_code('(empty? "not a list")')

    def test_read_line(self):
        code = """
            (define name "")
            (read-line name)
            name
        """
        result = self.run_code_with_input(code, "Alice\n")
        self.assertEqual(result, "Alice")

    def test_for_loop(self):
        result = self.run_code("""
            (define sum 0)
            (for i 0 4
                (set sum (+ sum 1))
            )
            sum
        """)
        self.assertEqual(result, 4)

    def test_get_seq_with_list(self):
        result = self.run_code("""
            (define xs (list 10 20 30))
            (get xs 1)
        """)
        self.assertEqual(result, 20)

    def test_get_seq_with_string(self):
        result = self.run_code("""
            (define s "hello")
            (get s 1)
        """)
        self.assertEqual(result, "e")

    def test_get_seq_out_of_bounds(self):
        with self.assertRaises(RuntimeError):
            self.run_code("""
                (define xs (list 1 2))
                (get xs 5)
            """)

    def test_get_seq_wrong_type(self):
        with self.assertRaises(RuntimeError):
            self.run_code("""
                (define x 123)
                (get x 0)
            """)

    def test_set_seq_variable(self):
        result = self.run_code("""
            (define data (list 1 2 3))
            (set data (list 7 8 9))
            data
        """)
        self.assertEqual(result, [7, 8, 9])

    def test_set_seq_string_variable(self):
        result = self.run_code("""
            (define txt "abc")
            (set txt "xyz")
            txt
        """)
        self.assertEqual(result, "xyz")

    def test_read_int_and_print_result(self):
        code = """
            (define n 0)
            (define m 0)
            (read-ints n m)
            (print (* m n))
        """
        original_stdout = sys.stdout
        try:
            sys.stdout = io.StringIO()
            self.run_code_with_input(code, "2 3")
            output = sys.stdout.getvalue().strip()
            self.assertEqual(output, "6")
        finally:
            sys.stdout = original_stdout

    def test_while_loop_two_statements(self):
        code = """
            (define x 0)
            (while (< x 5)
               (set x (+ x 2))
               (set x (- x 1))

                )
            x
        """
        result = self.run_code(code)
        self.assertEqual(result, 5)


if __name__ == "__main__":
    unittest.main()
