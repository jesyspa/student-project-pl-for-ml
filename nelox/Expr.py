class Expr:
    def accept(self, visitor):
        raise NotImplementedError()


class ExprVisitor:

    def visit_literal_expr(self, expr):
        pass

    def visit_variable_expr(self, expr):
        pass

    def visit_list_expr(self, expr):
        pass


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)


class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)


class ListExpr(Expr):
    def __init__(self, elements):
        self.elements = elements

    def accept(self, visitor):
        return visitor.visit_list_expr(self)
