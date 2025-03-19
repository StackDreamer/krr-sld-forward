from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Symbol:
    name: str
    is_solved: bool = False

    def __eq__(self, other: Symbol) -> bool:
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

### TODO: Operand inside operator can be other operator or a literal
###       how should we go about this?

@dataclass
class And:
    op1: Symbol
    op2: Symbol

    def __eq__(self, other: And) -> bool:
        return (
            (self.op1 == other.op1 and self.op2 == other.op2)
            or (self.op1 == other.op2 and self.op2 == other.op1)
        ) # because AND is commutative


@dataclass
class Or:
    op1: Symbol
    op2: Symbol

    def __eq__(self, other: Or) -> bool:
        return (
            (self.op1 == other.op1 and self.op2 == other.op2)
            or (self.op1 == other.op2 and self.op2 == other.op1)
        ) # because OR is commutative


@dataclass
class Not:
    symbol: Symbol

    def __eq__(self, other: Not) -> bool:
        return self.symbol == other.symbol


@dataclass
class Implies:
    premise: Symbol
    conclusion: Symbol

    def __eq__(self, other: Implies) -> bool:
        return self.premise == other.premise and self.conclusion == other.conclusion
    
    def to_cnf(self):
        return Or(Not(self.premise), self.conclusion)
