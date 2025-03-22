from tmp import Symbol, And, Not, Or, Implies, sld_resolution, forward_chaining

rajin = Symbol("Rajin")
cermat = Symbol("Cermat")
lulus = Symbol("Lulus")
malas = Symbol("Malas")
ceroboh = Symbol("Ceroboh")
bahagia = Symbol("Bahagia")

knowledge_base = [
  Implies(And(rajin, cermat), lulus),
  Implies(Not(rajin), malas),
  Implies(Not(cermat), ceroboh),
  Implies(bahagia, And(Not(malas), Not(ceroboh))),
  Not(lulus)
]

goals = [
  Not(bahagia)
]

for i, rule in enumerate(knowledge_base):
  if isinstance(rule, Implies):
    knowledge_base[i] = rule.to_cnf()
for rule in knowledge_base:
  print(rule)
# Perform SLD resolution
result = sld_resolution(knowledge_base, goals)
print("Result:", result)  # Output: "YES" or "NO"