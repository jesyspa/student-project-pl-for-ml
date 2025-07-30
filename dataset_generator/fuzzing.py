import random
import os

OP = ["+", "-", "*", "/"]
NUM = [str(random.randint(1, 100)) for _ in range(50)]
conditions = ['<','>']
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
    if expr == var:
        expr = random.choice(NUM)
    return f"(define {var} {expr})"

def generate_print():
    if random.random() < 0.1:
        return f"(print {random.randint(1,100)})"
    if not exist_vars:
        return generate_define()
    expr = random.choice(exist_vars)
    return f"(print {expr})"

non_if = [generate_print,generate_define]

def branch_checker(cond, cond_num, cond_var) -> bool:
    if cond == "<":
        return cond_var < cond_num
    elif cond == ">":
        return  cond_var > cond_num

def generate_if():
    if not exist_vars:
        return generate_define()
    cond_var = random.choice(exist_vars)
    cond_num = random.choice(NUM)
    cond = random.choice(conditions)
    condition = f"({cond} {cond_var} {cond_num})"
    pos_branch = random.choice(non_if)()
    neg_branch = random.choice(non_if)()
    #deleting a branch variable from existing to prevent from using undefined vars
    if branch_checker(cond, cond_num, cond_var):
        if neg_branch[1] == 'd':
           exist_vars.pop(-1)
    else:
        if pos_branch[1] == 'd':
           exist_vars.pop(-1)
    return f"(if {condition}\n  {pos_branch}\n  {neg_branch}\n)"

statements = [generate_if, generate_define, generate_print]

def generate_if_two_vars():
    if len(exist_vars) < 2:
        return generate_if()

def generate_statement():
    return random.choice(statements)()

def generate_program(num_stat=random.randint(3, 5)):
    global exist_vars
    exist_vars = []
    return "\n".join(generate_statement() for _ in range(num_stat))

def save_dataset(num_samples=20):
    output_dir = "dataset"
    os.makedirs(output_dir, exist_ok=True)
    for i in range(num_samples):
        code = generate_program()
        with open(os.path.join(output_dir, f"sample_{i+1}.txt"), "w") as f:
            f.write(code)

if __name__ == "__main__":
    save_dataset()
