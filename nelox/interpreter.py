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


def _builtin_get(lst, index):
    if not isinstance(lst, list):
        raise RuntimeError(f"'get': expected list, got {type(lst)}")
    if not isinstance(index, int):
        raise RuntimeError(f"'get': expected integer index, got {type(index)}")
    try:
        return lst[index]
    except IndexError:
        raise RuntimeError("'get': index out of bounds")


def _builtin_length(lst):
    if not isinstance(lst, list):
        raise RuntimeError(f"'length': expected list, got {type(lst)}")
    return len(lst)


def _comparison(op):
    def compare(a, b):
        if isinstance(a, list) and isinstance(b, list):
            return [op(x, y) for x, y in zip(a, b)]
        elif isinstance(a, list):
            return [op(x, b) for x in a]
        elif isinstance(b, list):
            return [op(a, y) for y in b]
        else:
            return op(a, b)
    return compare


def _apply(op, *args):
    if not args:
        raise RuntimeError("Operation requires at least one argument")

    result = args[0]
    for arg in args[1:]:
        if isinstance(result, list) and isinstance(arg, (int, float)):
            result = [op(x, arg) for x in result]
        elif isinstance(result, (int, float)) and isinstance(arg, list):
            result = [op(result, x) for x in arg]
        elif isinstance(result, list) and isinstance(arg, list):
            result = [op(x, y) for x, y in zip(result, arg)]
        elif isinstance(result, (int, float)) and isinstance(arg, (int, float)):
            result = op(result, arg)
        else:
            if op == operator.add:
                result = str(result) + str(arg)
            else:
                raise RuntimeError(f"Unsupported operands for {op}: {type(result)} and {type(arg)}")
    return result


def _define_builtins(env):
    env.define("list", lambda *args: list(args))
    env.define("get", _builtin_get)
    env.define("length", _builtin_length)
    env.define("true", True)
    env.define("false", False)
    env.define("+", lambda *args: _apply(operator.add, *args))
    env.define("-", lambda *args: _apply(operator.sub, *args))
    env.define("*", lambda *args: _apply(operator.mul, *args))
    env.define("/", lambda *args: _apply(operator.truediv, *args))
    env.define(">", _comparison(operator.gt))
    env.define("<", _comparison(operator.lt))
    env.define(">=", _comparison(operator.ge))
    env.define("<=", _comparison(operator.le))
    env.define("=", _comparison(operator.eq))
    env.define("print", lambda *args: print(*args))


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
                    body = args[1]
                    param_names = [tok.name.lexeme for tok in param_tokens]

                    def fn(*call_args):
                        local = Environment(parent=env)
                        for pname, param_val in zip(param_names, call_args):
                            local.define(pname, param_val)
                        return self.evaluate(body, local)

                    return fn

                elif name == "begin":
                    result = None
                    for expr_ in args:
                        result = self.evaluate(expr_, env)
                    return result

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
                    lst1 = self.evaluate(args[0], env)
                    lst2 = self.evaluate(args[1], env)
                    if not isinstance(lst1, list) or not isinstance(lst2, list):
                        raise RuntimeError("'append' expects two lists")
                    return lst1 + lst2

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

            func = self.evaluate(head, env)
            evaluated_args = [self.evaluate(arg, env) for arg in args]
            return func(*evaluated_args)

        else:
            raise RuntimeError("Unknown expression type")
