from __future__ import annotations
from dataclasses import dataclass
from typing import Union

@dataclass
class Symbol:
    name: str

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: Symbol) -> bool:
        if not isinstance(other, Symbol):
            return False
        return self.name == other.name

    def __or__(self, other: Symbol) -> Or:
        return Or(self, other)

    def __and__(self, other: Symbol) -> And:
        return And(self, other)

    def __invert__(self) -> Not:
        return Not(self)

    def __rshift__(self, other: Symbol) -> Implies:
        return Implies(self, other)

    def __lshift__(self, other: Symbol) -> Implies:
        return Implies(other, self)

    def to_cnf(self):
        return self

@dataclass
class And:
    op1: Union[Symbol, Or, And, Not, Implies]
    op2: Union[Symbol, Or, And, Not, Implies]

    def __eq__(self, other: And) -> bool:
        if not isinstance(other, And):
            return False
        return (
            (self.op1 == other.op1 and self.op2 == other.op2)
            or (self.op1 == other.op2 and self.op2 == other.op1)
        ) # because AND is commutative

    def __hash__(self):
        return hash((self.op1, self.op2))

    def to_cnf(self):
        return And(self.op1.to_cnf(), self.op2.to_cnf())

@dataclass
class Or:
    op1: Union[Symbol, Or, And, Not, Implies]
    op2: Union[Symbol, Or, And, Not, Implies]

    def __eq__(self, other: Or) -> bool:
        if not isinstance(other, Or):
            return False
        return (
            (self.op1 == other.op1 and self.op2 == other.op2)
            or (self.op1 == other.op2 and self.op2 == other.op1)
        ) # because OR is commutative

    def __hash__(self):
        return hash((self.op1, self.op2))

    def to_cnf(self):
        if isinstance(self.op1, And):
            return And(Or(self.op1.op1, self.op2), Or(self.op1.op2, self.op2)).to_cnf()
        elif isinstance(self.op2, And):
            return And(Or(self.op1, self.op2.op1), Or(self.op1, self.op2.op2)).to_cnf()
        else:
            return Or(self.op1.to_cnf(), self.op2.to_cnf())

@dataclass
class Not:
    symbol: Union[Symbol, Or, And, Not, Implies]

    def __eq__(self, other: Not) -> bool:
        if not isinstance(other, Not):
            return False
        return self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)

    def to_cnf(self):
        if isinstance(self.symbol, Not):
            return self.symbol.symbol.to_cnf()
        elif isinstance(self.symbol, And):
            return Or(Not(self.symbol.op1), Not(self.symbol.op2)).to_cnf()
        elif isinstance(self.symbol, Or):
            return And(Not(self.symbol.op1).to_cnf(), Not(self.symbol.op2).to_cnf())
        else:
            return Not(self.symbol)

@dataclass
class Implies:
    premise: Union[Symbol, Or, And, Not, Implies]
    conclusion: Union[Symbol, Or, And, Not, Implies]

    def __eq__(self, other: Implies) -> bool:
        if not isinstance(other, Implies):
            return False
        return self.premise == other.premise and self.conclusion == other.conclusion

    def __hash__(self):
        return hash((self.premise, self.conclusion))

    def to_cnf(self):
        return Or(Not(self.premise), self.conclusion).to_cnf()