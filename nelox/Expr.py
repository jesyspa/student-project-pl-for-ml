class Expr:
    def accept(self, visitor):
        raise NotImplementedError()

class ExprVisitor:
    def visit_Assign_Expr(self, expr):
        pass
    def visit_Binary_Expr(self, expr):
        pass
    def visit_Call_Expr(self, expr):
        pass
    def visit_Literal_Expr(self, expr):
        pass
    def visit_Logical_Expr(self, expr):
        pass
    def visit_Unary_Expr(self, expr):
        pass
    def visit_Variable_Expr(self, expr):
        pass
    def visit_Lambda_Expr(self, expr):
        pass
    def visit_If_Expr(self, expr):
        pass

class Assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_Assign_Expr(self)

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_Binary_Expr(self)

class Call(Expr):
    def __init__(self, callee, paren, arguments):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_Call_Expr(self)

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_Literal_Expr(self)

class Logical(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_Logical_Expr(self)

class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_Unary_Expr(self)

class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_Variable_Expr(self)

class Lambda(Expr):
    def __init__(self, params, body):
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_Lambda_Expr(self)

class If(Expr):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_If_Expr(self)

