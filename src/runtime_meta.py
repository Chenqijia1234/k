from __future__ import annotations
import abc
import enum
from typing import Any, MutableMapping, TypeAlias, override
import weakref


class KResult[T, E]:
    def __init__(self, success: bool, value: T | None, err: E | None) -> None:
        self.success = success
        self.value, self.err = value, err

    def unwrap(self) -> T:
        assert self.success and self.value is not None
        return self.value

    def expect(self, msg: str) -> T:
        assert self.success and self.value is not None, msg
        return self.value

    @staticmethod
    def Err(err: Any | None = None) -> KResult:
        return KResult(False, None, err)

    @staticmethod
    def Ok(v: Any) -> KResult:
        return KResult(True, v, None)


@enum.unique
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


class KObjectUtils:
    ...


class KMetaInfo:
    def __init__(
        self,
        name: str,
        bind_: weakref.ref[KValue],
        attr: list[str],
        base: list[str],
    ) -> None:
        self.name, self.bind, self.attr, self.base = name, bind_, attr, base

    def is_subclass_of(self, base: KValue) -> bool:
        meta_info = base.get_meta_info()
        return meta_info in (cls.get_meta_info() for cls in self.base)

    def is_instance_of(self, base: KValue) -> bool:
        return self == base.get_meta_info()

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, KMetaInfo)
            and __value.attr == self.attr
            and __value.bind == self.bind
            and __value.base == self.base
            and __value.name == self.name
        )


class KObject(abc.ABC):
    @abc.abstractmethod
    def get_meta_info(self) -> KMetaInfo:
        ...

    @abc.abstractmethod
    def send_msg(
        self, operator: KOperatorType, params: list[Any]
    ) -> KResult[KValue, str]:
        ...

    @abc.abstractmethod
    def support(self, operator: KOperatorType) -> bool:
        ...


class KUserDefinedObject(KObject):
    def __init__(self, name: str, attr: dict[str, KValue], base: list[str]) -> None:
        self.meta_info = KMetaInfo(name, weakref.ref(self), list(attr.keys()), base)
        self.name, self.attr, self.base = name, attr, base

    @override
    def get_meta_info(self) -> KMetaInfo:
        return self.meta_info

    @override
    def send_msg(
        self, operator: KOperatorType, params: list[Any]
    ) -> KResult[KValue, str]:
        match operator:
            case KOperatorType.ADD if len(params) == 1:
                if "__add__" in self.attr:
                    return self.attr["__add__"].send_msg(KOperatorType.CALL, params)
            case KOperatorType.CALL:
                if "__call__" in self.attr:
                    return self.attr["__call__"].send_msg(KOperatorType.CALL, params)
            case KOperatorType.CONSTRCUTOR:
                raise NotImplementedError
            case KOperatorType.DIV:
                pass
            case KOperatorType.EQUAL:
                pass
            case KOperatorType.GET_ATTR if len(params) == 1:
                return (
                    KResult.Ok(self.attr[params[0]])
                    if params[0] in self.attr
                    else KResult.Err()
                )
            case KOperatorType.INPLACE_ADD:
                pass
            case KOperatorType.INPLACE_DIV:
                pass
            case KOperatorType.INPLACE_MOD:
                pass
            case KOperatorType.INPLACE_MUL:
                pass
            case KOperatorType.INPLACE_SUB:
                pass
            case KOperatorType.LESS_THAN:
                pass
            case KOperatorType.MOD:
                pass
            case KOperatorType.MORE_THAN:
                pass
            case KOperatorType.MUL:
                pass
            case KOperatorType.NOT_EQUAL:
                pass
            case KOperatorType.SET_ATTR:
                pass
            case KOperatorType.SUB:
                pass
            case _:
                return KResult.Err()


class KExtensionObject(KObject):
    ...


KValue: TypeAlias = KObject


class EvaluateContext:
    def __init__(self, parent: MutableMapping[str, KValue] | None = None) -> None:
        self.parent = parent


class GlobalEnvironmentManager:
    ...


class KExtensionTypeAttributeWrapper:
    ...


class KExportFunction:
    ...


class KExportConstructor:
    ...


class KExportType:
    ...


class KGloablObjectPool:
    ...
