from nelox.Expr import Literal, Variable, List

def pretty(expr):
    if isinstance(expr, Literal):
        return str(expr.value)
    if isinstance(expr, Variable):
        return expr.name.lexeme
    if isinstance(expr, List):
        return f"({' '.join(pretty(e) for e in expr.elements)})"

def pretty_program(statements: list) -> str:
    return "\n".join(pretty(stmt) for stmt in statements)