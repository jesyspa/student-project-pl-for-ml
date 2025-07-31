import random
import os

OP = ["+", "-", "*", "/"]
NUM = [str(random.randint(1, 100)) for _ in range(50)]
exist_vars = []
var_pool = ["x", "y", "z", "a", "b", "c", "d", "e", "f"]
var_values = {}

def fresh_var():
    for v in var_pool:
        if v not in exist_vars:
            exist_vars.append(v)
            return v
    return f"n{len(exist_vars)}"

def generate_expr(depth=0):
    if depth >= 1 or (exist_vars and random.random() < 0.5):
        return random.choice(exist_vars + NUM)
    if random.random() < 0.3 or len(exist_vars) < 2:
        return random.choice(NUM)
    op = random.choice(OP)
    left = generate_expr(depth + 1)
    right = generate_expr(depth + 1)
    return f"({op} {left} {right})"

#function to prevent usage of a variable during its definition
def generate_expr_exc(exclude, depth=0):
    candidates = [v for v in exist_vars if v != exclude] + NUM
    if depth >= 1 or (candidates and random.random() < 0.5):
        return random.choice(candidates)
    if random.random() < 0.3 or len(candidates) < 2:
        return random.choice(NUM)
    op = random.choice(OP)
    left = generate_expr_exc(exclude, depth + 1)
    right = generate_expr_exc(exclude, depth + 1)
    return f"({op} {left} {right})"

def tokenize(expr: str):
    expr = expr.replace('(', ' ( ').replace(')', ' ) ')
    return expr.split()

def eval_tokens(tokens):
    def helper():
        token = tokens.pop(0)
        if token == '(':
            op = tokens.pop(0)
            left = helper()
            right = helper()
            tokens.pop(0)
            if op == '+': return left + right
            if op == '-': return left - right
            if op == '*': return left * right
            if op == '/':
                if right == 0:
                    return 0
                return int(left / right)
        elif token.isdigit():
            return int(token)
        else:
            return var_values.get(token, 0)
    return helper()

#function for later use to evaluate expressions
def expr_eval(expr: str):
    tokens = tokenize(expr)
    return eval_tokens(tokens)

def generate_define():
    var = fresh_var()
    expr = generate_expr_exc(var)
    if expr == var:
        expr = random.choice(NUM)
    val = expr_eval(expr)
    var_values[var] = val
    return f"(define {var} {expr})"

def generate_print():
    if random.random() < 0.1:
        return f"(print {random.randint(1, 100)})"
    if not exist_vars:
        return generate_define()
    expr = random.choice(exist_vars)
    return f"(print {expr})"

#a list with all statements generators
statements = [generate_define, generate_print]

def generate_statement():
    return random.choice(statements)()

def generate_program(num_stat=random.randint(3, 5)):
    global exist_vars, func_names, var_values
    exist_vars = []
    func_names = []
    var_values = {}
    return "\n".join(generate_statement() for _ in range(num_stat))

#num_samples can be changed later
def save_dataset(num_samples=5000):
    output_dir = "dataset"
    os.makedirs(output_dir, exist_ok=True)
    for i in range(num_samples):
        code = generate_program()
        with open(os.path.join(output_dir, f"sample_{i+1}.txt"), "w") as f:
            f.write(code)

if __name__ == "__main__":
    save_dataset()
