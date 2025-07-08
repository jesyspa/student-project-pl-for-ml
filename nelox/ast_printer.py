from typing import Any


class AstPrinter:
    def __init__(self):
        self.name = None

    def print_expr(self, expr):
        return expr.accept(self)

    def print_stmt(self, stmt):
        return stmt.accept(self)

    def visit_expression_stmt(self, stmt):
        return self.prefix(";", stmt.expression)

    def visit_function_stmt(self, stmt):
        parts = [b.accept(self) for b in stmt.body]
        parts.extend(p.lexeme for p in stmt.params)
        parts.append(stmt.name.lexeme)
        return f"(fun {stmt.name.lexeme} {' '.join(parts)})"

    def visit_if_stmt(self, stmt):
        if stmt.else_branch is None:
            return self.prefix("if", stmt.condition, stmt.then_branch)
        return self.prefix("if-else", stmt.condition, stmt.then_branch, stmt.else_branch)

    def visit_print_stmt(self, stmt):
        return self.prefix("print", stmt.expression)

    def visit_return_stmt(self, stmt):
        if stmt.value is None:
            return "(return)"
        return self.prefix("return", stmt.value)

    def visit_while_stmt(self, stmt):
        return self.prefix("while", stmt.condition, stmt.body)

    def visit_assign_expr(self, expr):
        return self.prefix("=", expr.name.name.lexeme, expr.value)

    def visit_binary_expr(self, expr):
        return self.prefix(expr.operator.lexeme, expr.left, expr.right)

    def visit_call_expr(self, expr):
        return self.prefix("call", expr.callee, expr.arguments)

    def visit_literal_expr(self, expr):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_logical_expr(self, expr):
        return self.prefix(expr.operator.lexeme, expr.left, expr.right)

    def visit_unary_expr(self, expr):
        return self.prefix(expr.operator.lexeme, expr.right)

    def visit_variable_expr(self, expr):
        return expr.name.lexeme

    def prefix(self, name: str, *parts: Any) -> str:
        flat = []
        for part in parts:
            flat.append(self.stringify(part))
        return f"( {name} {' '.join(flat)} )"

    def stringify(self, part: Any) -> str:
        if isinstance(part, list):
            return ' '.join(self.stringify(p) for p in part)
        elif hasattr(part, 'accept'):
            return part.accept(self)
        elif hasattr(part, 'lexeme'):
            return part.lexeme
        else:
            return str(part)
