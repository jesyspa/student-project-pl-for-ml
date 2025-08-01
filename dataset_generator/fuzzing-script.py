import random
import os
from typing import Union
from nelox.Expr import Variable, Literal, List
from nelox.nelox_token import Token
from nelox.token_type import TokenType
from dataset_generator.EnvStack import EnvStack
from nelox.pretty_printer import pretty

OP = ["+", "-", "*", "/"]
NUM = [random.randint(1, 100) for _ in range(50)]
var_pool = ["x", "y", "z", "a", "b", "c", "d", "e", "f"]

def make_token(type_, lexeme):
    return Token(type_, lexeme, None, 0)

def make_op_token(op):
    return make_token(TokenType.IDENTIFIER, op)

def make_var_token(name):
    return make_token(TokenType.IDENTIFIER, name)

class Fuzzer:
    def __init__(self):
        self.env = EnvStack()
        self.statements = [self.generate_define, self.generate_print]

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
                [Literal(n) for n in NUM]
            )
        op = random.choice(OP)
        return List([
            Variable(make_op_token(op)),
            self.generate_expr(depth + 1),
            self.generate_expr(depth + 1)
        ])

    #replaces self-defining variable in the expression with a random integer
    def var_replacer(self,expr, var_name):
        if isinstance(expr, Variable):
            if expr.name.lexeme == var_name:
                return Literal(random.choice(NUM))
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
        if random.random() < 0.1:
            return List([
                Variable(make_var_token("print")),
                Literal(random.randint(1, 100))
            ])
        if not self.env.all_vars():
            return self.generate_define()
        return List([
            Variable(make_var_token("print")),
            Variable(make_var_token(random.choice(self.env.all_vars())))
        ])

    def generate_statement(self):
        return random.choice(self.statements)()

    def generate_program(self,num_stat=random.randint(3, 5)):
        self.env.reset()
        prog = [self.generate_statement() for _ in range(num_stat)]
        return "\n".join(pretty(stmt) for stmt in prog)

    def save_dataset(self, num_samples=500):
        output_dir = "dataset"
        os.makedirs(output_dir, exist_ok=True)
        for i in range(num_samples):
            code = self.generate_program()
            with open(os.path.join(output_dir, f"sample_{i+1}.txt"), "w") as f:
                f.write(code)

if __name__ == "__main__":
    Fuzzer().save_dataset()
