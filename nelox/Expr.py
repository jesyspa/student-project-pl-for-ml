class Expr:
    def accept(self, visitor):
        raise NotImplementedError()


class ExprVisitor:
    def visit_Literal_Expr(self, expr):
        pass

    def visit_Variable_Expr(self, expr):
        pass

    def visit_List_Expr(self, expr):
        pass


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_Literal_Expr(self)


class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_Variable_Expr(self)


class List(Expr):
    def __init__(self, elements):
        self.elements = elements

    def accept(self, visitor):
        return visitor.visit_List_Expr(self)

