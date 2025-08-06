import random
import os

from typing import Union
from nelox.Expr import Variable, Literal, List
from nelox.nelox_token import Token
from nelox.token_type import TokenType
from dataset_generator.EnvStack import EnvStack
from nelox.pretty_printer import pretty_program


ops = ["+", "-", "*", "/"]
nums = [random.randint(1, 100) for _ in range(50)]
var_pool = ["x", "y", "z", "a", "b", "c", "d", "e", "f"]
func_names_pool = [f"fun{i}" for i in range(50)]

def save_dataset(output_dir="dataset", num_samples=50):
    os.makedirs(output_dir, exist_ok=True)
    for i in range(num_samples):
        fuzzer = Fuzzer()
        program = fuzzer.generate_program()
        code = pretty_program(program)
        with open(os.path.join(output_dir, f"sample_{i + 1}.txt"), "w") as f:
            f.write(code)

def make_token(type_, lexeme):
    return Token(type_, lexeme, None, 0)

def make_op_token(op):
    return make_token(TokenType.IDENTIFIER, op)

def make_var_token(name):
    return make_token(TokenType.IDENTIFIER, name)

class Fuzzer:
    def __init__(self):
        self.env = EnvStack()
        self.statements = [self.generate_define, self.generate_print,
                           self.generate_func_call,self.generate_func]
        self.func_statements = [self.generate_define, self.generate_print]

    def fresh_var(self):
        for v in var_pool:
            if not self.env.is_available(v):
                self.env.set_var(v)
                return v
        v = f"n{len(self.env.all_vars())}"
        self.env.set_var(v)
        return v

    def generate_expr(self,depth=0):
        vars_available = self.env.all_vars()
        if depth >= 1 or (vars_available and random.random() < 0.5):
            return random.choice(
                [Variable(make_var_token(v)) for v in vars_available] +
                [Literal(n) for n in nums]
            )
        op = random.choice(ops)
        return List([
            Variable(make_op_token(op)),
            self.generate_expr(depth + 1),
            self.generate_expr(depth + 1)
        ])

    #replaces self-defining variable in the expression with a random integer
    def var_replacer(self,expr, var_name):
        if isinstance(expr, Variable):
            if expr.name.lexeme == var_name:
                return Literal(random.choice(nums))
            return expr
        if isinstance(expr, List):
            return List([self.var_replacer(e, var_name) for e in expr.elements])
        return expr

    def generate_define(self) ->List:
        var = self.fresh_var()
        expr = self.generate_expr()
        expr = self.var_replacer(expr, var)
        return List([
            Variable(make_var_token("define")),
            Variable(make_var_token(var)),
            expr
        ])

    def generate_print(self) -> Union[List, None]:
        if not self.env.all_vars():
            return List([
            Variable(make_var_token("print")),
            Literal(random.choice(nums))
        ])
        return List([
            Variable(make_var_token("print")),
            self.generate_expr()
        ])

    def generate_func(self) -> List:
        func_name = random.choice(func_names_pool)
        param = self.fresh_var()
        num_statements = random.randint(1, 3)
        self.env.define_func(func_name)
        self.env.push()
        self.env.set_var(param)
        body = [self.generate_statement(self.func_statements) for _ in range(num_statements)]
        self.env.pop()
        return List([
            Variable(make_var_token("func")),
            Variable(make_var_token(func_name)),
            List([Variable(make_var_token(param))]),
            *body
        ])

    def generate_func_call(self) -> List:
        funcs_available = list(self.env.all_funcs())
        if not funcs_available:
            return self.generate_func()
        arg = self.generate_expr()
        func_name = random.choice(funcs_available)
        return List([
            Variable(make_var_token(func_name)),
            arg
        ])

    def generate_statement(self,statements):
        return random.choice(statements)()

    def generate_program(self, num_stat: int = None) -> list:
        if num_stat is None:
            num_stat = random.randint(3, 5)
        return [self.generate_statement(self.statements) for _ in range(num_stat)]

if __name__ == "__main__":
    save_dataset()