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

    def run_code_with_input_and_output_capture(self, source, input_data):
        original_stdin = sys.stdin
        original_stdout = sys.stdout
        sys.stdin = io.StringIO(input_data)
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            self.run_code(source)
            return captured_output.getvalue().strip()
        finally:
            sys.stdin = original_stdin
            sys.stdout = original_stdout

    # https://codeforces.com/problemset/problem/1/A
    def test_problem1(self):
        code = """
            (begin
              (define n 0)
              (define m 0)
              (define a 0)
              
              (read-int n)
              (read-int m)
              (read-int a)
              
              (define tiles-n (+ (div (- n 1) a) 1))
              (define tiles-m (+ (div (- m 1) a) 1))
              (print(* tiles-n tiles-m))
            )
        """

        result = self.run_code_with_input_and_output_capture(code, "6\n6\n4\n")
        self.assertEqual(result, "4")

    # https://codeforces.com/problemset/problem/4/A
    def test_problem2(self):
        code = """
            (define x 0)
            (read-int x) $ this is here to check commenting
            (print (if (and (> x 2) (= (mod x 2) 0)) "yes" "no"))
        """

        result = self.run_code_with_input_and_output_capture(code, "8")
        self.assertEqual(result, "yes")

    # https://codeforces.com/problemset/problem/231/A
    def test_problem3(self):
        code = """
            (begin
              (define n 0)
              (read-int n)
              
              (define i 0)
              (define count 0)
              
              (define a 0)
              (define b 0)
              (define c 0)
              (define sum 0)

              (while (< i n)
                (begin
                  (read-int a)
                  (read-int b)
                  (read-int c)
                  (set sum (+ a b))
                  (set sum (+ sum c))
                  (if (>= sum 2)
                      (set count (+ count 1))
                      0
                  )
                  (set i (+ i 1))
                )
              )

              (print count)
            )
        """

        result = self.run_code_with_input_and_output_capture(code, "3\n1\n1\n0\n1\n1\n1\n1\n0\n0")
        self.assertEqual(result, "2")

    # https://codeforces.com/problemset/problem/50/A
    def test_problem4(self):
        code = """
            (begin
                (define m 0)
                (define n 0)
                
                (read-int m)
                (read-int n)
                
                (define area (* m n))
                (define result (div area 2))
                (print result)
            )
        """

        result = self.run_code_with_input_and_output_capture(code, "2\n4")
        self.assertEqual(result, "4")

    # https://codeforces.com/problemset/problem/158/A
    def test_problem5(self):
        code = """
            (begin
              (define n 0)
              (define k 0)
              
              (read-int n)
              (read-int k)

              (define scores (list))
              (define i 0)
              (define x 0)
              
              (while (< i n)
                (begin
                  (read-int x)
                  (set scores (append scores (list x)))
                  (set i (+ i 1))
                )
              )

              (define threshold (get scores (- k 1)))

              (define count 0)
              (define j 0)
              (define sc 0)
              (while (< j n)
                (begin
                  (set sc (get scores j))
                  (if (and (>= sc threshold) (> sc 0))
                    (set count (+ count 1))
                    0
                  )
                  (set j (+ j 1))
                )
              )

              (print count)
            )
        """

        result = self.run_code_with_input_and_output_capture(code, "8\n5\n10\n9\n8\n7\n7\n7\n5\n5")
        self.assertEqual(result, "6")

    # https://codeforces.com/problemset/problem/236/A
    def test_problem6(self):
        code = """
            (begin
              (define username "")
              (read-line username)
              
              (define letters "")
              (to-list username)
              (define unique "")
              (all-unique letters)
              (define count 0)
              (set count (length (to-list unique)))
              
              (if (= (mod count 2) 0)
                  (print "CHAT WITH HER!")
                  (print "IGNORE HIM!")
              )
            )
        """

        result = self.run_code_with_input_and_output_capture(code, "wjmzbmr")
        self.assertEqual(result, "CHAT WITH HER!")

    # https://codeforces.com/problemset/problem/734/A
    def test_problem7(self):
        code = """
            (begin
              (define n 0)
              (define s "")
              
              (read-int n)
              (read-line s)
            
              (define lst (to-list s))
              (define a-wins 0)
              (define d-wins 0)
              (define ch "")
              (define i 0)
              
              (while (< i n)
                (begin
                  (set ch (get lst i))
                  (if (= ch "A")
                      (set a-wins (+ a-wins 1))
                      (if (= ch "D")
                          (set d-wins (+ d-wins 1))
                          0
                      )
                  )
                  (set i (+ i 1))
                )
              )
            
              (if (> a-wins d-wins)
                  (print "Anton")
                  (if (> d-wins a-wins)
                      (print "Danik")
                      (print "Friendship")
                  )
              )
            )
        """

        result = self.run_code_with_input_and_output_capture(code, "6\nADAAAA")
        self.assertEqual(result, "Anton")

    # https://codeforces.com/problemset/problem/344/A
    def test_problem8(self):
        code = """
            (begin
              (define n 0)
              (read-int n)
            
              (define prev "")
              (define curr "")
              (define i 0)
              (define groups 0)
            
              (while (< i n)
                (begin
                  (read-line curr)
                  (if (!= curr prev)
                      (set groups (+ groups 1))
                      0
                  )
                  (set prev curr)
                  (set i (+ i 1))
                )
              )
            
              (print groups)
            )
        """

        result = self.run_code_with_input_and_output_capture(code, "4\n01\n01\n10\n10")
        self.assertEqual(result, "2")

    # https://codeforces.com/problemset/problem/59/A
    def test_problem9(self):
        code = """
            (begin
              (define s "")
              (read-line s)
            
              (define chars (to-list s))
              (define lower 0)
              (define upper 0)
              (define i 0)
              (define ch "")
              (define ch-code 0)
            
              (while (< i (length chars))
                (begin
                  (set ch (get chars i))
                  (set ch-code (get-ascii ch))
                  (if (>= ch-code 97)
                      (set lower (+ lower 1))
                      (set upper (+ upper 1))
                  )
                  (set i (+ i 1))
                )
              )
            
              (if (> upper lower)
                  (print (to-upper s))
                  (print (to-lower s))
              )
            )
        """

        result = self.run_code_with_input_and_output_capture(code, "HoUse")
        self.assertEqual(result, "house")

    # https://codeforces.com/problemset/problem/58/A
    def test_problem10(self):
        code = """
            (begin
              (define s "") 
              (read-line s)
            
              (define target "hello")
              (define i 0)
              (define j 0)
              (define len_s (length (to-list s)))
              (define len_t (length (to-list target)))
            
              (while (and (< i len_s) (< j len_t))
                (begin
                  (if (= (get (to-list s) i) (get (to-list target) j))
                      (set j (+ j 1))
                      0)
                  (set i (+ i 1))
                )
              )
            
              (if (= j len_t)
                  (print "yes")
                  (print "no")
              )
            )
            """

        result = self.run_code_with_input_and_output_capture(code, "ahhellllloou")
        self.assertEqual(result, "yes")


if __name__ == "__main__":
    unittest.main()
