from nelox.Expr import Literal, Variable, List

def pretty(expr, ind = 0):
    if isinstance(expr, Literal):
        return str(expr.value)
    if isinstance(expr, Variable):
        return expr.name.lexeme
    if isinstance(expr, List):
        if func_recognizer(expr):
            header = f"(func {pretty(expr.elements[1])} {pretty(expr.elements[2])}"
            body_lines = [
                "   " * (ind + 1) + pretty(e, ind + 1) for e in expr.elements[3:]
            ]
            if body_lines:
                body_lines[-1] += ")"
                return f"{header}\n" + "\n".join(body_lines)
            else:
                return f"{header})"
        if if_statement_recognizer(expr):
            cond = pretty(expr.elements[1], ind + 1)
            then_branch = pretty(expr.elements[2], ind + 1)
            else_branch = pretty(expr.elements[3], ind + 1)
            spaces = "   " * ind
            return (
                f"{spaces}(if {cond}\n"
                f"{'   ' * (ind + 1)}{then_branch}\n"
                f"{'   ' * (ind + 1)}{else_branch})"
            )
        return f"({' '.join(pretty(e, ind) for e in expr.elements)})"


def pretty_program(statements: list) -> str:
    return "\n".join(pretty(stmt) for stmt in statements)

def func_recognizer(expr):
    if not expr.elements:
        return False
    if not isinstance(expr.elements[0], Variable):
        return False
    if expr.elements[0].name.lexeme != "func":
        return False
    return True

def if_statement_recognizer(expr):
    return (
        isinstance(expr, List)
        and len(expr.elements) == 4
        and isinstance(expr.elements[0], Variable)
        and expr.elements[0].name.lexeme == "if"
    )
