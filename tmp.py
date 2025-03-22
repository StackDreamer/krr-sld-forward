# Hasil DeepSeek, please check again
# yang udah dibawah udah di cek dan berhasil
# tolong coba kasus lain

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Union

@dataclass
class Symbol:
    name: str

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
    
    def to_cnf(self):
        return self

@dataclass
class And:
    op1: Union[Symbol, Or, And, Not, Implies]
    op2: Union[Symbol, Or, And, Not, Implies]

    def __eq__(self, other: And) -> bool:
        return (
            (self.op1 == other.op1 and self.op2 == other.op2)
            or (self.op1 == other.op2 and self.op2 == other.op1)
        ) # because AND is commutative

    def to_cnf(self):
        return And(self.op1.to_cnf(), self.op2.to_cnf())

@dataclass
class Or:
    op1: Union[Symbol, Or, And, Not, Implies]
    op2: Union[Symbol, Or, And, Not, Implies]

    def __eq__(self, other: Or) -> bool:
        return (
            (self.op1 == other.op1 and self.op2 == other.op2)
            or (self.op1 == other.op2 and self.op2 == other.op1)
        ) # because OR is commutative

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
        return self.symbol == other.symbol

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
        return self.premise == other.premise and self.conclusion == other.conclusion
    
    def to_cnf(self):
        return Or(Not(self.premise), self.conclusion).to_cnf()

def forward_chaining(knowledge_base: List[Union[Symbol, Implies, And, Or, Not]]) -> List[Symbol]:
    inferred = set()
    new_facts = True

    while new_facts:
        new_facts = False
        for rule in knowledge_base:
            if isinstance(rule, Implies):
                premise = rule.premise
                conclusion = rule.conclusion
                if premise in inferred and conclusion not in inferred:
                    inferred.add(conclusion)
                    new_facts = True
            elif isinstance(rule, And):
                if rule.op1 in inferred and rule.op2 in inferred:
                    inferred.add(rule)
                    new_facts = True
            elif isinstance(rule, Symbol):
                if rule not in inferred:
                    inferred.add(rule)
                    new_facts = True

    return list(inferred)

def is_solved(solved: List[Union[Symbol, Implies, And, Or, Not]], query: Union[Symbol, Or, Not]) -> bool:
    if isinstance(query, Symbol):
        return query in solved
    
    if isinstance(query, Not):
        return query.symbol in solved

    return is_solved(solved, query.op1) and is_solved(solved, query.op2)

def sld_resolution(knowledge_base: List[Union[Symbol, Implies, And, Or, Not]], goals: List[Symbol]) -> str:
    solved = []

    while True:
        print(solved)
        # Step 1: If all goals are solved, return YES
        if all(goal in solved for goal in goals):
            return "YES"

        # Step 2: Find a clause [p, -p1, ..., -pn] where all -pi are solved and p is not solved
        found_clause = False
        for clause in knowledge_base:
            if isinstance(clause, Implies):
                # Convert implication to CNF: A → B ≡ ¬A ∨ B
                premise = clause.premise
                conclusion = clause.conclusion
                if isinstance(premise, Symbol) and premise in solved and conclusion not in solved:
                    solved.append(conclusion)
                    found_clause = True
                    break
            elif isinstance(clause, And):
                # Handle AND clauses (if needed)
                pass
            elif isinstance(clause, Or):
                # Handle OR clauses (if needed)
                if is_solved(solved, clause.op1) and isinstance(clause.op2, Symbol) and clause.op2 not in solved:
                    solved.append(clause.op2)
                    found_clause = True
                    break
            elif isinstance(clause, Symbol):
                # Handle atomic symbols
                if clause not in solved:
                    solved.append(clause)
                    found_clause = True
                    break

        # Step 4: If no such clause is found, return NO
        if not found_clause:
            return "NO"

first_grade = Symbol("FirstGrade")
child = Symbol("Child")
male = Symbol("Male")
boy = Symbol("Boy")
kindergarten = Symbol("Kindergarten")
female = Symbol("Female")
girl = Symbol("Girl")

# Define knowledge base
knowledge_base = [
    first_grade,
    Implies(first_grade, child),
    Implies(And(child, male), boy),
    Implies(kindergarten, child),
    Implies(And(child, female), girl),
    female
]

# Define goals
goals = [girl]

for i, rule in enumerate(knowledge_base):
    if isinstance(rule, Implies):
        knowledge_base[i] = rule.to_cnf()
print(knowledge_base)
# Perform SLD resolution
result = sld_resolution(knowledge_base, goals)
print("Result:", result)  # Output: "YES" or "NO"
