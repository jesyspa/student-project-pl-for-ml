import random
import os
from nelox.Expr import Variable, Literal, List
from nelox.nelox_token import Token
from nelox.token_type import TokenType
from dataset_generator.EnvStack import EnvStack

OP = ["+", "-", "*", "/"]
NUM = [random.randint(1, 100) for _ in range(50)]
var_pool = ["x", "y", "z", "a", "b", "c", "d", "e", "f"]
env = EnvStack()

def fresh_var():
    for v in var_pool:
        if not env.is_available(v):
            env.set_var(v)
            return v
    v = f"n{len(env.all_vars())}"
    env.set_var(v)
    return

def make_token(type_, lexeme):
    return Token(type_, lexeme, None, 0)

def make_op_token(op):
    return make_token(TokenType.IDENTIFIER, op)

def make_var_token(name):
    return make_token(TokenType.IDENTIFIER, name)

def generate_expr(depth=0):
    vars_available = env.all_vars()
    if depth >= 1 or (vars_available and random.random() < 0.5):
        return random.choice(
            [Variable(make_var_token(v)) for v in vars_available] +
            [Literal(n) for n in NUM]
        )

def generate_expr_exc(exclude, depth=0):
    candidates = [v for v in env.all_vars() if v != exclude]
    var_exprs = [Variable(make_var_token(v)) for v in candidates]
    literals = [Literal(n) for n in NUM]
    if depth >= 1 or (candidates and random.random() < 0.5):
        return random.choice(var_exprs + literals)
    if random.random() < 0.3 or len(candidates) < 2:
        return Literal(random.choice(NUM))
    op = random.choice(OP)
    return List([
        Variable(make_op_token(op)),
        generate_expr_exc(exclude, depth + 1),
        generate_expr_exc(exclude, depth + 1)
    ])

def pretty(expr):
    if isinstance(expr, Literal):
        return str(expr.value)
    if isinstance(expr, Variable):
        return expr.name.lexeme
    if isinstance(expr, List):
        return f"({' '.join(pretty(e) for e in expr.elements)})"

def generate_define():
    var = fresh_var()
    expr = generate_expr_exc(var)
    return f"(define {var} {pretty(expr)})"

def generate_print():
    if random.random() < 0.1:
        return f"(print {random.randint(1, 100)})"
    if not env.all_vars():
        return generate_define()
    return f"(print {random.choice(env.all_vars())})"

statements = [generate_define, generate_print]

def generate_statement():
    return random.choice(statements)()

def generate_program(num_stat=random.randint(3, 5)):
    env.reset()
    return "\n".join(generate_statement() for _ in range(num_stat))

def save_dataset(num_samples=5):
    output_dir = "dataset"
    os.makedirs(output_dir, exist_ok=True)
    for i in range(num_samples):
        code = generate_program()
        with open(os.path.join(output_dir, f"sample_{i+1}.txt"), "w") as f:
            f.write(code)

if __name__ == "__main__":
    save_dataset()
