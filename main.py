from model import Symbol, Or, And, Not, Implies

first_grade = Symbol("FirstGrade")
child = Symbol("Child")
male = Symbol("Male")
boy = Symbol("Boy")
kindergarten = Symbol("Kindergarten")
female = Symbol("Female")
girl = Symbol("Girl")

knowledge_base = [
    first_grade,
    Implies(first_grade, child),
    Implies(And(child, male), boy),
    Implies(kindergarten, child),
    Implies(And(child, female), girl),
    female
]

for i, rule in enumerate(knowledge_base):
    if isinstance(rule, Implies):
        knowledge_base[i] = rule.to_cnf()

query = girl

# want to show KB |= Girl

def sld_fwd_chain(kb: list[Symbol], query: Symbol) -> bool:
    kb = kb.copy()
    for rule in kb:
        if isinstance(rule, Symbol) and rule == query:
            return True
    

            

def is_condition_satisfied(premise, facts):
    premises = premise.split(' and ')
    all_premises_satisfied = True
    for cond in premises:
        if cond not in facts:
            all_premises_satisfied = False
            break

    return all_premises_satisfied

def forward_chaining(initial_facts, rules):
    facts = initial_facts.copy()

    print("\nNew Facts: ")
    new_facts = []
    while True:
        newly_derived_facts = []

        for rule in rules:
            premise, conclusion = rule
            if is_condition_satisfied(premise, facts) and conclusion not in facts:
                newly_derived_facts.append(conclusion)
                facts.append(conclusion)
                
        new_facts.extend(newly_derived_facts)
            

        if not newly_derived_facts:
            break   

    print("\n".join(map(str, new_facts)))
    return facts # To update facts
