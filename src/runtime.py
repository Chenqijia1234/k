from __future__ import annotations
from typing import Any, Callable, Mapping, Optional


class KError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class KFunctionReturn(BaseException):
    def __init__(self, value) -> None:
        self.value: KObjectRef = value


class Environment:
    def __init__(
        self,
        dict_: Optional[Mapping[str, KObjectRef]] = None,
        parent: Optional[Environment] = None,
    ) -> None:
        self.parent = parent
        self.env: Mapping[str, KObjectRef] = dict_ if dict_ is not None else {}

    def get(self, name: str) -> Optional[KObjectRef]:
        if name in self.env.keys():
            return self.env[name]
        if self.parent:
            outer_env_v = self.parent.get(name)
            if outer_env_v:
                return outer_env_v
        return None

    def set(self, name: str, v: KObjectRef) -> None:
        self.env[name] = v  # type:ignore


class KType:
    """
    对类型的元描述
    """

    def __init__(
        self,
        name: str,
        base_cls: list[KType],
        cls_env: Environment | dict[str, KObject],
    ) -> None:
        self.type_name = name
        self.base_cls = base_cls
        self.env = cls_env if isinstance(cls_env, Environment) else Environment(cls_env)

    def get_ctor(self) -> KObjectRef:
        if v := self.get("__ctor__"):
            return v
        raise KError(f"Type {self.type_name} has no constructor.")

    def new_instance(self, args: list[KObjectRef]) -> KObject:
        if v := self.get_ctor().get("__call__"):  # type:ignore
            if isinstance(v, KCallable):
                return v(args)  # type:ignore
        raise KError(f"Type {self.type_name}'s constructor is not callable.")

    def get(self, name: str) -> Optional[KObjectRef]:
        return self.env.get(name)


class KObject:
    "类型的实例"

    def __init__(self) -> None:
        self.env = Environment(None)

    def get(self, name: str) -> Optional[KObjectRef]:
        return self.env.get(name)


class KCallable(KObject):
    def __init__(
        self,
        fn_impl: Callable,
    ) -> None:
        self.fn = fn_impl
        super().__init__()

    @classmethod
    def ctor(cls, fn: KCallable) -> KCallable:
        return KCallable(fn.fn)

    def __call__(self, args: list[KObject]) -> None:
        self.fn(args)


class KInt:
    def __init__(self, value: int) -> None:
        self.v = value

    def add(self, obj: Any) -> KInt:
        if isinstance(obj, KInt):
            return KInt(self.v + obj.v)
        elif isinstance(obj, KFloat):
            return KInt(int(self.v + obj.v))
        elif isinstance(obj, KObject):
            raise NotImplementedError()
        else:
            raise KError(f"KInt does not support to add with {obj}")

    def sub(self, obj: Any) -> KInt:
        if isinstance(obj, KInt):
            return KInt(self.v - obj.v)
        elif isinstance(obj, KFloat):
            return KInt(int(self.v - obj.v))
        elif isinstance(obj, KObject):
            raise NotImplementedError()
        else:
            raise KError(f"KInt does not support to add with {obj}")

    def mul(self, obj: Any) -> KInt:
        if isinstance(obj, KInt):
            return KInt(self.v * obj.v)
        elif isinstance(obj, KFloat):
            return KInt(int(self.v * obj.v))
        elif isinstance(obj, KObject):
            raise NotImplementedError()
        else:
            raise KError(f"KInt does not support to add with {obj}")

    def div(self, obj: Any) -> KInt:
        if isinstance(obj, KInt):
            return KInt(int(self.v / obj.v))
        elif isinstance(obj, KFloat):
            return KInt(int(self.v / obj.v))
        elif isinstance(obj, KObject):
            raise NotImplementedError()
        else:
            raise KError(f"KInt does not support to add with {obj}")


class KFloat:
    def __init__(self, value: float) -> None:
        self.v = value

    def add(self, obj: Any) -> KFloat:
        if isinstance(obj, KFloat):
            return KFloat(self.v + obj.v)
        elif isinstance(obj, KFloat):
            return KFloat(self.v + obj.v)
        elif isinstance(obj, KObject):
            raise NotImplementedError()
        else:
            raise KError(f"KFloat does not support to add with {obj}")

    def sub(self, obj: Any) -> KFloat:
        if isinstance(obj, KFloat):
            return KFloat(self.v - obj.v)
        elif isinstance(obj, KFloat):
            return KFloat(self.v - obj.v)
        elif isinstance(obj, KObject):
            raise NotImplementedError()
        else:
            raise KError(f"KFloat does not support to sub with {obj}")

    def mul(self, obj: Any) -> KFloat:
        if isinstance(obj, KFloat):
            return KFloat(self.v * obj.v)
        elif isinstance(obj, KFloat):
            return KFloat(self.v * obj.v)
        elif isinstance(obj, KObject):
            raise NotImplementedError()
        else:
            raise KError(f"KFloat does not support to mul with {obj}")

    def div(self, obj: Any) -> KFloat:
        if isinstance(obj, KFloat):
            return KFloat(int(self.v / obj.v))
        elif isinstance(obj, KFloat):
            return KFloat(int(self.v / obj.v))
        elif isinstance(obj, KObject):
            raise NotImplementedError()
        else:
            raise KError(f"KFloat does not support to div with {obj}")


class KString:
    def __init__(self, v: str) -> None:
        self.value = v

    def extend(self, s: KString) -> KString:
        return KString(self.value + s.value)


type KObjectRef = KInt | KFloat | KString | KType | KObject | KCallable | None  # type: ignore
