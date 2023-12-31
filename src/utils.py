from typing import NoReturn, Optional


def error(msg: str = "Crashed for Unknown Reason.") -> NoReturn:
    raise RuntimeError(msg)


def unwrap[T](_v: Optional[T]) -> T:  # type: ignore
    if _v is not None:
        return _v
    else:
        error("Error While Unwraping: Unexpected None.")


def is_success[T](_v: Optional[T]) -> bool:  # type: ignore
    return _v is not None


def is_err[T](_v: Optional[T]) -> bool:  # type: ignore
    return _v is None


def unreachable() -> NoReturn:
    error("Unreachable Code.")
