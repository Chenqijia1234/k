from abc import ABC
from typing import Any


class Token(ABC):
    def __init__(self, value: Any) -> None:
        super().__init__()
        self.value = value

    def get_value(self) -> Any:
        return self.value

    def is_identifiertok(self) -> bool:
        return False

    def is_inttok(self) -> bool:
        return False

    def is_floattok(self) -> bool:
        return False

    def is_stringtok(self) -> bool:
        return False

    def is_numtok(self) -> bool:
        return False

    def is_eof(self) -> bool:
        return False

    def is_operator_tok(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f"<{type(self).__name__}: {self.value}>"


class NumTok(Token):
    def __init__(self, value: float | int) -> None:
        super().__init__(value)

    def is_numtok(self) -> bool:
        return True


class IntTok(NumTok):
    def __init__(self, value: int) -> None:
        super().__init__(value)

    def is_inttok(self) -> bool:
        return True


class FloatTok(NumTok):
    def __init__(self, value: float) -> None:
        super().__init__(value)

    def is_floattok(self) -> bool:
        return True


class StringTok(Token):
    def __init__(self, value: str) -> None:
        _value = (
            value.replace("\\t", "\t")
            .replace("\\n", "\n")
            .replace("\\r", "\r")
            .replace('"', '"')
        )
        super().__init__(_value)

    def is_stringtok(self) -> bool:
        return True


class IdentifierTok(Token):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    def is_identifiertok(self) -> bool:
        return True


class OperatorTok(Token):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    def is_operator_tok(self) -> bool:
        return True


class EOFTok(Token):
    def __init__(self) -> None:
        super().__init__(-1)

    def is_eof(self) -> bool:
        return True
