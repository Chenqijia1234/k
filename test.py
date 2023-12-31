import enum


class KOperatorType(enum.Enum):
    ADD = object()
    SUB = object()
    MUL = object()
    DIV = object()
    MOD = object()

    EQUAL = object()
    NOT_EQUAL = object()
    MORE_THAN = object()
    LESS_THAN = object()

    CALL = object()
    CONSTRCUTOR = object()

    GET_ATTR = object()
    SET_ATTR = object()

    INPLACE_ADD = object()
    INPLACE_SUB = object()
    INPLACE_MUL = object()
    INPLACE_DIV = object()
    INPLACE_MOD = object()


for i in dir(KOperatorType):
    if not i.startswith("_"):
        print(
            f"""\
        case {KOperatorType.__name__}.{i}:
            pass"""
        )
