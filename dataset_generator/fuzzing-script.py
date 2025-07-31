import random
import os

OP = ["+", "-", "*", "/"]
NUM = [str(random.randint(1, 100)) for _ in range(50)]
exist_vars = []
var_pool = ["x", "y", "z", "a", "b", "c", "d", "e", "f"]

env_stack=[{}]
def current_env():
    return env_stack[-1]

def set_var(name, value):
    current_env()[name] = value

def get_var(name):
    for env in reversed(env_stack):
        if name in env:
            return env[name]
    return 0


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
    return op, left, right

def generate_expr_exc(exclude, depth=0):
    candidates = [v for v in exist_vars if v != exclude] + NUM
    if depth >= 1 or (candidates and random.random() < 0.5):
        return random.choice(candidates)
    if random.random() < 0.3 or len(candidates) < 2:
        return random.choice(NUM)
    op = random.choice(OP)
    left = generate_expr_exc(exclude, depth + 1)
    right = generate_expr_exc(exclude, depth + 1)
    return op, left, right

def eval_expr_tree(tree):
    if isinstance(tree, tuple):
        op, left, right = tree
        l_val = eval_expr_tree(left)
        r_val = eval_expr_tree(right)
        if op == '+': return l_val + r_val
        if op == '-': return l_val - r_val
        if op == '*': return l_val * r_val
        if op == '/': return int(l_val / r_val) if r_val != 0 else 0
    elif tree.isdigit():
        return int(tree)
    else:
        return get_var(tree)

def pretty_print_expr(tree):
    if isinstance(tree, tuple):
        op, left, right = tree
        return f"({op} {pretty_print_expr(left)} {pretty_print_expr(right)})"
    return tree

def generate_define():
    var = fresh_var()
    expr_tree = generate_expr_exc(var)
    expr_val = eval_expr_tree(expr_tree)
    set_var(var, expr_val)
    return f"(define {var} {pretty_print_expr(expr_tree)})"

def generate_print():
    if random.random() < 0.1:
        return f"(print {random.randint(1, 100)})"
    if not exist_vars:
        return generate_define()
    expr = random.choice(exist_vars)
    return f"(print {expr})"

statements = [generate_define, generate_print]

def generate_statement():
    return random.choice(statements)()

def generate_program(num_stat=random.randint(3, 5)):
    global exist_vars
    exist_vars = []
    env_stack.clear()
    env_stack.append({})
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
