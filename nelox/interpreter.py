from nelox.Expr import Literal, Variable, List
import operator

from nelox.nelox_token import Token
from nelox.token_type import TokenType


class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def find_env(self, name):
        if name in self.values:
            return self
        elif self.parent:
            return self.parent.find_env(name)
        return None

    def get(self, name):
        env = self.find_env(name)
        if env:
            return env.values[name]
        else:
            raise RuntimeError(f"Undefined variable '{name}'")

    def define(self, name, value):
        if name in self.values:
            raise RuntimeError(f"Variable '{name}' is already defined")
        self.values[name] = value

    def set(self, name, value):
        env = self.find_env(name)
        if env:
            env.values[name] = value
        else:
            raise RuntimeError(f"Undefined variable '{name}'")


def _builtin_get(seq, index):
    if not isinstance(seq, (list, str)):
        raise RuntimeError(f"'get': expected list or string, got {type(seq)}")
    if not isinstance(index, int):
        raise RuntimeError(f"'get': expected integer index, got {type(index)}")
    try:
        return seq[index]
    except IndexError:
        raise RuntimeError("'get': index out of bounds")


def _builtin_length(lst):
    if not isinstance(lst, list):
        raise RuntimeError(f"'length': expected list, got {type(lst)}")
    return len(lst)


def _comparison(op):
    return op


def _apply(op, *args):
    if not args:
        raise RuntimeError("Operation requires at least one argument")

    result = args[0]
    for arg in args[1:]:
        result = op(result, arg)
    return result


def _not_equal(*args):
    if len(args) != 2:
        raise RuntimeError("'!=' expects exactly 2 arguments")
    return args[0] != args[1]


def _builtin_get_ascii(c):
    if not isinstance(c, str) or len(c) != 1:
        raise RuntimeError("'get-ascii' expects a single character")
    return ord(c)


def raise_(msg):
    raise RuntimeError(msg)


def _define_builtins(env):
    env.define("true", True)
    env.define("false", False)
    env.define("+", lambda *args: _apply(operator.add, *args))
    env.define("-", lambda *args: _apply(operator.sub, *args))
    env.define("*", lambda *args: _apply(operator.mul, *args))
    env.define("/", lambda *args: _apply(operator.truediv, *args))
    env.define("mod", lambda a, b: operator.mod(a, b))
    env.define("div", lambda *args: _apply(operator.floordiv, *args))
    env.define(">", _comparison(operator.gt))
    env.define("<", _comparison(operator.lt))
    env.define(">=", _comparison(operator.ge))
    env.define("<=", _comparison(operator.le))
    env.define("=", _comparison(operator.eq))
    env.define("not", lambda x: not x)
    env.define("!=", _comparison(operator.ne))
    env.define("print", lambda *args: print(*args))
    env.define("list", lambda *args: list(args))
    env.define("get", _builtin_get)
    env.define("length", _builtin_length)
    env.define("str", lambda *args: str(args))
    env.define("all-unique", lambda lst: list(set(lst)))
    env.define("to-list", lambda s: list(s))
    env.define("to-lower", lambda s: s.lower())
    env.define("to-upper", lambda s: s.upper())
    env.define("get-ascii", _builtin_get_ascii)


class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        _define_builtins(self.global_env)

    def interpret(self, expressions):
        result = None
        for expr in expressions:
            result = self.evaluate(expr, self.global_env)
            if "_" in self.global_env.values:
                self.global_env.set("_", result)
            else:
                self.global_env.define("_", result)
        return result

    def evaluate(self, expr, env):
        if isinstance(expr, Literal):
            return expr.value

        elif isinstance(expr, Variable):
            return env.get(expr.name.lexeme)

        elif isinstance(expr, List):
            if not expr.elements:
                return None

            head = expr.elements[0]
            args = expr.elements[1:]

            if isinstance(head, Variable):
                name = head.name.lexeme

                if name == "func":
                    fn_name = args[0]
                    lambda_expr = List([
                        Variable(Token(TokenType.IDENTIFIER, "lambda", None, 0)),
                        args[1],
                        args[2]
                    ])
                    define_expr = List([
                        Variable(Token(TokenType.IDENTIFIER, "define", None, 0)),
                        fn_name,
                        lambda_expr
                    ])
                    return self.evaluate(define_expr, env)

                elif name == "define":
                    var_name = args[0].name.lexeme
                    value = self.evaluate(args[1], env)
                    env.define(var_name, value)
                    return value

                elif name == "set":
                    var_name = args[0].name.lexeme
                    value = self.evaluate(args[1], env)
                    env.set(var_name, value)
                    return value

                elif name == "if":
                    condition = self.evaluate(args[0], env)
                    branch = args[1] if condition else args[2]
                    return self.evaluate(branch, env)

                elif name == "lambda":
                    param_tokens = args[0].elements
                    body_expres = args[1:]
                    param_names = [tok.name.lexeme for tok in param_tokens]

                    def fn(*call_args):
                        local = Environment(parent=env)
                        for pname, param_val in zip(param_names, call_args):
                            local.define(pname, param_val)
                        result_ = None
                        for express in body_expres:
                            result_ = self.evaluate(express, local)
                        return result_
                    return fn

                elif name == "while":
                    condition = args[0]
                    body__expr = args[1:]
                    result = None
                    while self.evaluate(condition, env):
                        for expr in body__expr:
                            result = self.evaluate(expr, env)
                    return result

                elif name == "and":
                    for arg in args:
                        if not self.evaluate(arg, env):
                            return False
                    return True

                elif name == "or":
                    for arg in args:
                        if self.evaluate(arg, env):
                            return True
                    return False

                elif name == "head":
                    lst = self.evaluate(args[0], env)
                    if not isinstance(lst, list):
                        raise RuntimeError(f"'head' expects a list, got {type(lst)}")
                    return lst[0] if lst else None

                elif name == "tail":
                    lst = self.evaluate(args[0], env)
                    if not isinstance(lst, list):
                        raise RuntimeError(f"'tail' expects a list, got {type(lst)}")
                    return lst[1:] if len(lst) > 0 else []

                elif name == "append":
                    val1 = self.evaluate(args[0], env)
                    val2 = self.evaluate(args[1], env)
                    if isinstance(val1, list) and isinstance(val2, list):
                        return val1 + val2
                    elif isinstance(val1, str) and isinstance(val2, str):
                        return val1 + val2
                    else:
                        raise RuntimeError("'append' expects two lists or two strings")

                elif name == "reverse":
                    lst = self.evaluate(args[0], env)
                    if not isinstance(lst, list):
                        raise RuntimeError("'reverse' expects a list")
                    return list(reversed(lst))

                elif name == "push":
                    element = self.evaluate(args[0], env)
                    lst = self.evaluate(args[1], env)
                    if not isinstance(lst, list):
                        raise RuntimeError("'push' expects a list as the second argument")
                    return [element] + lst

                elif name == "empty?":
                    lst = self.evaluate(args[0], env)
                    if not isinstance(lst, list):
                        raise RuntimeError("'empty?' expects a list")
                    return len(lst) == 0

                elif name == "read-line":
                    var_name = args[0].name.lexeme
                    value = input()
                    env.set(var_name, value)
                    return value

                elif name == "for":
                    var_token = args[0].name
                    start = self.evaluate(args[1], env)
                    end = self.evaluate(args[2], env)
                    body = args[3]

                    result = None
                    for i in range(start, end):
                        loop_env = Environment(parent=env)
                        loop_env.define(var_token.lexeme, i)
                        result = self.evaluate(body, loop_env)
                    return result

                elif name == "read-int":
                    if len(args) != 1:
                        raise RuntimeError("'read-int' expects exactly one variable")
                    var_name = args[0].name.lexeme
                    try:
                        value = int(input())
                    except ValueError:
                        raise RuntimeError("'read-int' expects a single integer input")
                    if env.find_env(var_name):
                        env.set(var_name, value)
                    else:
                        env.define(var_name, value)
                    return value

                elif name == "read-ints":
                    var_tokens = [arg.name.lexeme for arg in args]
                    try:
                        values = list(map(int, input().split()))
                    except ValueError:
                        raise RuntimeError("'read-ints' expects integer input")
                    if len(values) != len(var_tokens):
                        raise RuntimeError(f"'read-ints' expected {len(var_tokens)} values, got {len(values)}")
                    for var_name, val in zip(var_tokens, values):
                        if env.find_env(var_name):
                            env.set(var_name, val)
                        else:
                            env.define(var_name, val)
                    return values

            func = self.evaluate(head, env)
            evaluated_args = [self.evaluate(arg, env) for arg in args]
            return func(*evaluated_args)

        else:
            raise RuntimeError("Unknown expression type")
