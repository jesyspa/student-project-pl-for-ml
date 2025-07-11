from nelox.Expr import Literal, Variable, List


class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def get(self, name):
        if name in self.values:
            return self.values[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise RuntimeError(f"Undefined variable '{name}'")

    def set(self, name, value):
        if name in self.values:
            self.values[name] = value
        elif self.parent:
            try:
                self.parent.set(name, value)
            except RuntimeError:
                self.values[name] = value
        else:
            self.values[name] = value


def _add(*args):
    if not args:
        raise RuntimeError("'+' requires at least one argument")

    result = args[0]
    for arg in args[1:]:

        if isinstance(result, list) and isinstance(arg, (int, float)):
            result = [x + arg for x in result]
        elif isinstance(result, (int, float)) and isinstance(arg, list):
            result = [result + x for x in arg]

        elif isinstance(result, (int, float)) and isinstance(arg, (int, float)):
            result = result + arg

        else:
            result = str(result) + str(arg)
    return result


def _sub(*args):
    if not args:
        raise RuntimeError("'-' requires at least one argument")

    result = args[0]

    for arg in args[1:]:

        if isinstance(result, (int, float)) and isinstance(arg, (int, float)):
            result -= arg

        elif isinstance(result, list) and isinstance(arg, (int, float)):
            result = [x - arg for x in result]

        elif isinstance(result, (int, float)) and isinstance(arg, list):
            result = [result - x for x in arg]

        else:
            raise RuntimeError(f"Unsupported operands for '-': {type(result)} and {type(arg)}")
    return result


def _mult(*args):
    if not args:
        raise RuntimeError("'*' requires at least one argument")

    result = args[0]
    for arg in args[1:]:

        if isinstance(result, list) and isinstance(arg, (int, float)):
            result = [x * arg for x in result]
        elif isinstance(result, (int, float)) and isinstance(arg, list):
            result = [result * x for x in arg]

        elif isinstance(result, (int, float)) and isinstance(arg, (int, float)):
            result = result * arg

        else:
            raise RuntimeError(f"Unsupported operands for '*': {type(result)} and {type(arg)}")

    return result


def _div(*args):
    if not args:
        raise RuntimeError("'/' requires at least one argument")

    result = args[0]

    for arg in args[1:]:

        if isinstance(result, (int, float)) and isinstance(arg, (int, float)):
            result /= arg

        elif isinstance(result, list) and isinstance(arg, (int, float)):
            result = [x / arg for x in result]

        elif isinstance(result, (int, float)) and isinstance(arg, list):
            result = [result / x for x in arg]

        else:
            raise RuntimeError(f"Unsupported operands for '/': {type(result)} and {type(arg)}")
    return result


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


def _define_builtins(env):
    env.set("list", lambda *args: list(args))
    env.set("get", _builtin_get)
    env.set("length", _builtin_length)
    env.set("true", True)
    env.set("false", False)
    env.set("+", _add)
    env.set("-", _sub)
    env.set("*", _mult)
    env.set("/", _div)
    env.set(">", lambda a, b: a > b)
    env.set("<", lambda a, b: a < b)
    env.set(">=", lambda a, b: a >= b)
    env.set("<=", lambda a, b: a <= b)
    env.set("=", lambda a, b: a == b)
    env.set("print", lambda *args: print(*args))


class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        _define_builtins(self.global_env)

    def interpret(self, expressions):
        result = None
        for expr in expressions:
            result = self.evaluate(expr, self.global_env)
            self.global_env.set("_", result)
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

                    fn_name = args[0].name.lexeme
                    param_tokens = args[1].elements
                    body = args[2]
                    param_names = [tok.name.lexeme for tok in param_tokens]

                    def fn(*call_args):
                        local_env = Environment(parent=env)
                        for pname, param_val in zip(param_names, call_args):
                            local_env.set(pname, param_val)
                        return self.evaluate(body, local_env)

                    env.set(fn_name, fn)
                    return fn

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
                            local.set(pname, param_val)
                        return self.evaluate(body, local)

                    return fn

            func = self.evaluate(head, env)
            evaluated_args = [self.evaluate(arg, env) for arg in args]
            return func(*evaluated_args)

        else:
            raise RuntimeError("Unknown expression type")
