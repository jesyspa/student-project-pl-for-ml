from nelox.Expr import Literal, Variable, List

def pretty(expr, ind = 0):
    if isinstance(expr, Literal):
        return str(expr.value)
    if isinstance(expr, Variable):
        return expr.name.lexeme
    if isinstance(expr, List):
        if (expr.elements
        and isinstance(expr.elements[0], Variable)
        and expr.elements[0].name.lexeme == "func"):
            header = f"(func {pretty(expr.elements[1])} {pretty(expr.elements[2])}"
            body = "\n".join(
                "   " * (ind + 1) + pretty(e, ind + 1) for e in expr.elements[3:]
            )
            return f"{header}\n{body}\n{'    ' * ind})"
        return f"({' '.join(pretty(e, ind) for e in expr.elements)})"

def pretty_program(statements: list) -> str:
    return "\n".join(pretty(stmt) for stmt in statements)