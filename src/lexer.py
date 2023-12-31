import re
from tokens import (
    EOFTok,
    FloatTok,
    IdentifierTok,
    IntTok,
    OperatorTok,
    StringTok,
    Token,
)
from utils import error, unreachable

INTEGER = r"[0-9]+"
FLOAT = INTEGER + "." + INTEGER
STRING = r'"((\")?|\d|\D)*"'
COMMENT = r"//(\W|\w)*$"
OPERATOR = r"\(|\)|;|\+|-|\*|/|%|=|==|!=|<|>|{|}|[|]"
IDENTIFIER = r"([a-z_A-Z][a-z_0-9A-Z]*)"

RE_EXPRS = (FLOAT, INTEGER, STRING, COMMENT, OPERATOR, IDENTIFIER)


class Lexer:
    def __init__(self, src: str) -> None:
        self.src = src
        self.current_index = 0
        self.max_index = len(self.src)

    def advance(self, v: int = 1) -> None:
        self.current_index += v
        self.skip()

    def skip(self) -> None:
        while (
            self.current_index < self.max_index
            and self.src[self.current_index].isspace()
        ):
            self.advance()

    def next_token(self) -> Token:
        if self.current_index >= self.max_index:
            return EOFTok()

        results = []
        for i in RE_EXPRS:
            results.append(re.match(i, self.src[self.current_index :], re.MULTILINE))

        if any(results):
            if v := results[0]:
                begin, end = v.span()
                self.advance(end)
                return FloatTok(float(v.string[begin:end]))
            elif v := results[1]:
                begin, end = v.span()
                self.advance(end)
                return IntTok(int(v.string[begin:end]))
            elif v := results[2]:
                begin, end = v.span()
                self.advance(end)
                return StringTok(v.string[begin:end])
            elif v := results[3]:
                begin, end = v.span()
                self.advance(end)
                return self.next_token()
            elif v := results[4]:
                begin, end = v.span()
                self.advance(end)
                return OperatorTok(v.string[begin:end])
            elif v := results[5]:
                begin, end = v.span()
                self.advance(end)
                return IdentifierTok(v.string[begin:end])
            else:
                unreachable()
        else:
            error("Invalid Syntax.")

    def all(self) -> list[Token]:
        v: list[Token] = []
        while not isinstance((tok := self.next_token()), EOFTok):
            v.append(tok)
        return v
