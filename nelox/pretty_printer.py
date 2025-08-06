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
