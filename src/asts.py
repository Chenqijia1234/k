from __future__ import annotations
from typing import Any
from runtime import (
    Environment,
    KCallable,
    KError,
    KFloat,
    KFunctionReturn,
    KInt,
    KObjectRef,
    KString,
)
from tokens import FloatTok, IdentifierTok, IntTok, StringTok


class ASTNode:
    def eval(self, env: Environment) -> KObjectRef:
        raise NotImplementedError


class Literal(ASTNode):
    def eval(self, env: Environment) -> KObjectRef:
        raise NotImplementedError


class NumberLiteral(Literal):
    def eval(self, env: Environment) -> KObjectRef:
        raise NotImplementedError


class FloatLiteral(NumberLiteral):
    def __init__(self, tok: FloatTok) -> None:
        self.tok = tok

    def eval(self, _: Environment) -> KObjectRef:
        return KFloat(self.tok.get_value())


class IntLiteral(NumberLiteral):
    def __init__(self, tok: IntTok) -> None:
        self.tok = tok

    def eval(self, _: Environment) -> KObjectRef:
        return KInt(self.tok.get_value())


class StringLiteral(Literal):
    def __init__(self, tok: StringTok) -> None:
        self.tok = tok

    def eval(self, _: Environment) -> KObjectRef:
        return KString(self.tok.get_value())


class NameLiteral(Literal):
    def __init__(self, tok: IdentifierTok) -> None:
        self.tok = tok

    def eval(self, env: Environment) -> KObjectRef:
        if v := env.get(self.tok.get_value()):
            return v
        else:
            raise KError(f"No such name: {self.tok.get_value()}")


class ParamLiteral(Literal):
    def __init__(self, params: tuple[Any]) -> None:
        self.params = params

    def eval(self, env: Environment) -> KObjectRef:
        raise NotImplementedError()


class Expr(ASTNode):
    ...


class BinOp(Expr):
    def __init__(self, a: ASTNode, b: ASTNode) -> None:
        self.a = a
        self.b = b
        super().__init__()


class BinAdd(BinOp):
    def eval(self, env: Environment) -> KObjectRef:
        left = self.a.eval(env)
        right = self.b.eval(env)
        if isinstance(left, KInt):
            if isinstance(right, KInt):
                return left.add(right)
            elif isinstance(right, KFloat):
                return KFloat(left.v + right.v)
            else:
                raise KError(f"Obj {left}, {right} do not support to add.")
        elif isinstance(left, KFloat):
            if isinstance(right, KInt):
                return left.add(right)
            elif isinstance(right, KFloat):
                return KFloat(left.v + right.v)
            else:
                raise KError(f"Obj {right} do not support to add.")
        else:
            raise KError(f"obj {left} do not support to add.")


class BinSub(BinOp):
    def eval(self, env: Environment) -> KObjectRef:
        left = self.a.eval(env)
        right = self.b.eval(env)
        if isinstance(left, KInt):
            if isinstance(right, KInt):
                return left.sub(right)
            elif isinstance(right, KFloat):
                return KFloat(left.v - right.v)
            else:
                raise KError(f"Obj {left}, {right} do not support to sub.")
        elif isinstance(left, KFloat):
            if isinstance(right, KInt):
                return left.sub(right)
            elif isinstance(right, KFloat):
                return KFloat(left.v - right.v)
            else:
                raise KError(f"Obj {right} do not support to sub.")
        else:
            raise KError(f"obj {left} do not support to sub.")


class BinMul(BinOp):
    def eval(self, env: Environment) -> KObjectRef:
        left = self.a.eval(env)
        right = self.b.eval(env)
        if isinstance(left, KInt):
            if isinstance(right, KInt):
                return left.mul(right)
            elif isinstance(right, KFloat):
                return KFloat(left.v * right.v)
            else:
                raise KError(f"Obj {left}, {right} do not support to mul.")
        elif isinstance(left, KFloat):
            if isinstance(right, KInt):
                return left.mul(right)
            elif isinstance(right, KFloat):
                return KFloat(left.v * right.v)
            else:
                raise KError(f"Obj {right} do not support to mul.")
        else:
            raise KError(f"obj {left} do not support to mul.")


class BinDiv(BinOp):
    def eval(self, env: Environment) -> KObjectRef:
        left = self.a.eval(env)
        right = self.b.eval(env)
        if isinstance(left, KInt):
            if isinstance(right, KInt):
                return left.div(right)
            elif isinstance(right, KFloat):
                return KFloat(left.v / right.v)
            else:
                raise KError(f"Obj {left}, {right} do not support to div.")
        elif isinstance(left, KFloat):
            if isinstance(right, KInt):
                return left.div(right)
            elif isinstance(right, KFloat):
                return KFloat(left.v / right.v)
            else:
                raise KError(f"Obj {right} do not support to div.")
        else:
            raise KError(f"obj {left} do not support to div.")


class BinEq(BinOp):
    def eval(self, env: Environment) -> KObjectRef:
        left, right = self.a.eval(env), self.b.eval(env)
        if isinstance(left, KInt | KFloat) and isinstance(right, KInt | KFloat):
            return KInt(1) if left.v == right.v else KInt(0)
        raise KError(f"obj {left} do not support to eq.")


class BinNotEq(BinOp):
    def eval(self, env: Environment) -> KObjectRef:
        left, right = self.a.eval(env), self.b.eval(env)
        if isinstance(left, KInt | KFloat) and isinstance(right, KInt | KFloat):
            return KInt(1) if left.v != right.v else KInt(0)
        raise KError(f"obj {left} do not support to eq.")


class BinMt(BinOp):
    def eval(self, env: Environment) -> KObjectRef:
        left, right = self.a.eval(env), self.b.eval(env)
        if isinstance(left, KInt | KFloat) and isinstance(right, KInt | KFloat):
            return KInt(1) if left.v > right.v else KInt(0)
        raise KError(f"obj {left} do not support to eq.")


class BinSt(BinOp):
    def eval(self, env: Environment) -> KObjectRef:
        left, right = self.a.eval(env), self.b.eval(env)
        if isinstance(left, KInt | KFloat) and isinstance(right, KInt | KFloat):
            return KInt(1) if left.v < right.v else KInt(0)
        raise KError(f"obj {left} do not support to eq.")


# class UnaryOp(Expr):
#     ...


class VarDeclExpr(Expr):
    def __init__(self, name: str) -> None:
        self.name = name

    def eval(self, env: Environment) -> KObjectRef:
        env.set(self.name, None)
        return None


class VarAssignExpr(Expr):
    def __init__(self, name: str, liter: Literal) -> None:
        self.name = name
        self.v = liter

    def eval(self, env: Environment) -> KObjectRef:
        env.set(self.name, self.v.eval(env))
        return None


class VarDeclAssignExpr(Expr):
    def __init__(self, name: str, liter: Literal) -> None:
        self.name = name
        self.v = liter

    def eval(self, env: Environment) -> KObjectRef:
        env.set(self.name, self.v.eval(env))
        return None


class FunctionCallExpr(Expr):
    def __init__(self, name: str, params: ParamLiteral) -> None:
        self.name, self.params = name, params

    def eval(self, env: Environment) -> KObjectRef:
        return env.get(self.name)(self.params.eval(env))  # type:ignore


class Statement(ASTNode):
    ...


class IfStatement(Statement):
    def __init__(self, cond: Expr, body: Statement) -> None:
        self.cond, self.body = cond, body

    def eval(self, env: Environment) -> KObjectRef:
        if self.cond.eval(env):
            self.body.eval(env)
        return None


class ReturnStatement(Statement):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr

    def eval(self, env: Environment) -> KObjectRef:
        raise KFunctionReturn(self.expr.eval(env))


class FuntionDeclStatement(Statement):
    def __init__(self, fn_name: str, params: ParamLiteral, body: Statement) -> None:
        self.name = fn_name
        self.params = params
        self.body = body

    def apply(self, args: ParamLiteral) -> KObjectRef:
        local_env = zip(self.params.params, args.params, strict=True)
        try:
            self.body.eval(Environment(dict(local_env)))
        except KFunctionReturn as return_v:
            return return_v.value
        else:
            return None

    def eval(self, env: Environment) -> KObjectRef:
        fn = KCallable(self.apply)
        env.set(self.name, fn)
        return None
