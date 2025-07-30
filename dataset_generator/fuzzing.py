import random
import os

OP = ["+", "-", "*", "/"]
NUM = [str(random.randint(1, 100)) for _ in range(50)]

exist_vars = []
var_pool = ["x", "y", "z", "a", "b", "c", "d", "e", "f"]

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

def generate_define():
    var = fresh_var()
    expr = generate_expr()
    return f"(define {var} {expr})"

def generate_print():
    if random.random() < 0.1:
        return f"print {random.randint(1,100)}"
    if not exist_vars:
        return generate_define()
    expr = random.choice(exist_vars)
    return f"(print {expr})"

def generate_statement():
    return generate_define() if random.random() < 0.5 else generate_print()

def generate_program(num_stat=random.randint(1, 5)):
    global exist_vars
    exist_vars = []
    return "\n".join(generate_statement() for _ in range(num_stat))

def save_dataset(num_samples=2):
    output_dir = "dataset"
    os.makedirs(output_dir, exist_ok=True)
    for i in range(num_samples):
        code = generate_program()
        with open(os.path.join(output_dir, f"sample_{i+1}.txt"), "w") as f:
            f.write(code)

if __name__ == "__main__":
    save_dataset()
