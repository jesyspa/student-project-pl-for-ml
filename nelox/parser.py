from nelox.token_type import TokenType
from nelox.scanner import Scanner


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.scanner.scan_tokens()

    def parse(self):
        expressions = []
        while not self.scanner.is_at_end():
            expressions.append(self.expression())
        return expressions

    def expression(self):
        token = self.advance()
        match token.type:
            case TokenType.LEFT_PAREN:
                return self.list_expr()
            case TokenType.NUMBER | TokenType.STRING | TokenType.IDENTIFIER:
                return token.literal if token.literal is not None else token.lexeme
            case _:
                raise Exception(f"[line {token.line}] Unexpected token: {token.type}")

    def list_expr(self):
        items = []
        while not self.check(TokenType.RIGHT_PAREN):
            items.append(self.expression())
            if self.scanner.is_at_end():
                raise Exception("Unterminated list")
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after list.")
        return items

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        token = self.peek()
        raise Exception(f"[line {token.line}] Error: {message}")

    def check(self, token_type):
        if self.scanner.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self):
        return self.scanner.advance()

    def peek(self):
        return self.scanner.peek()
