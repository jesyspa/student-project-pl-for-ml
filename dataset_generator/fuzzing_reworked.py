import random
import os

OP = ["+", "-", "*", "/"]
NUM = [str(random.randint(1, 100)) for _ in range(50)]
conditions = ['<', '>']
exist_vars = []
var_pool = ["x", "y", "z", "a", "b", "c", "d", "e", "f"]
func_names = []
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

def expr_eval(expr: str):
    tokens = tokenize(expr)
    return eval_tokens(tokens)

def generate_define():
    var = fresh_var()
    expr = generate_expr()
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

def branch_checker(cond, cond_num, cond_var) -> bool:
    cond_num = int(cond_num)
    cond_expr = cond_var if cond_var in var_values else "0"
    val = expr_eval(cond_expr)
    if cond == "<":
        return val < cond_num
    elif cond == ">":
        return val > cond_num

non_if = [generate_print, generate_define]

def generate_if():
    if not exist_vars:
        return generate_define()
    cond_var = random.choice(exist_vars)
    cond_num = random.choice(NUM)
    cond = random.choice(conditions)
    condition = f"({cond} {cond_var} {cond_num})"
    pos_branch = random.choice(non_if)()
    neg_branch = random.choice(non_if)()
    if branch_checker(cond, cond_num, cond_var):
        if neg_branch.startswith('(define'):
            defined_var = neg_branch.split()[1]
            if defined_var in exist_vars:
                exist_vars.remove(defined_var)
                var_values.pop(defined_var, None)
    else:
        if pos_branch.startswith('(define'):
            defined_var = pos_branch.split()[1]
            if defined_var in exist_vars:
                exist_vars.remove(defined_var)
                var_values.pop(defined_var, None)

    return f"(if {condition}\n\t{pos_branch}\n\t{neg_branch}\n)"


def generate_if_two_vars():
    if len(exist_vars) < 2:
        return generate_if()
    var1, var2 = random.sample(exist_vars, 2)
    cond = random.choice(conditions)
    condition = f"({cond} {var1} {var2})"
    pos_branch = random.choice(non_if)()
    neg_branch = random.choice(non_if)()

    val1 = var_values.get(var1)
    val2 = var_values.get(var2)
    condition_result = (int(val1) < int(val2)) if cond == "<" else (int(val1) > int(val2))
    if condition_result:
        if neg_branch.startswith('(define'):
            defined_var = neg_branch.split()[1]
            if defined_var in exist_vars:
                exist_vars.remove(defined_var)
                var_values.pop(defined_var, None)
    else:
        if pos_branch.startswith('(define'):
            defined_var = pos_branch.split()[1]
            if defined_var in exist_vars:
                exist_vars.remove(defined_var)
                var_values.pop(defined_var, None)
    return f"(if {condition}\n\t{pos_branch}\n\t{neg_branch}\n)"

non_func = [generate_if, generate_define, generate_print]

def generate_func():
    global exist_vars, var_values
    func_name = f"f{random.randint(1, 100)}"
    func_names.append(func_name)
    arg = fresh_var()
    exist_vars.pop(-1)
    outer_vars = exist_vars
    outer_values = var_values

    #create a local scope for the function
    local_vars = [arg]
    local_values = {arg: random.randint(1, 100)}

    #switch to local scope
    exist_vars = local_vars
    var_values = local_values
    body = random.choice(non_func)()
    tabbed = "\n".join("\t" + line for line in body.splitlines())

    #return to global scope
    exist_vars = outer_vars
    var_values = outer_values
    return f"(func {func_name} ({arg})\n{tabbed}\n)"

def generate_call():
    if not func_names:
        return generate_func()
    fun_name = random.choice(func_names)
    if exist_vars:
        arg = random.choice(exist_vars)
    else:
        arg = random.choice(NUM)
    return f"({fun_name} {arg})"

statements = [generate_if, generate_define, generate_print, generate_func, generate_call]

def generate_statement():
    return random.choice(statements)()

def generate_program(num_stat=random.randint(3, 5)):
    global exist_vars, func_names, var_values
    exist_vars = []
    func_names = []
    var_values = {}
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
