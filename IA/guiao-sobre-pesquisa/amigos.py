from constraintsearch import *

amigos = ["Andre", "Bernardo", "Claudio"]

domains = {a:[(b,c) for b in amigos for c in amigos if a!=b and a!=c and b!=c] for a in amigos}

edges = [(a1,a2) for a1 in amigos for a2 in amigos if a1!=a2]

constraints = {e: (lambda a1,t1,a2,t2: t1[0]!=t2[0] and t1[1]!=t2[1]) for e in edges}

cs = ConstraintSearch(domains, constraints)

print(cs.search())