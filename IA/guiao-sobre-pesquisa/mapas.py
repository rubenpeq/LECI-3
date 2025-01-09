from constraintsearch import *

region = ['A','B','C','D','E']
colors = ['red','blue','green','yellow','white']

domains = {r:colors for r in region}

edges = [ ('E', r) for r in region if r!='E' ]
edges += [ ('A','B'),('B','C'),('C','D'),('D','A') ]
edges += [ (v2,v1) for (v1,v2) in edges ]

constraints = {(r1, r2):(lambda r1,c1,r2,c2: c1!=c2) for (r1, r2) in edges}

cs = ConstraintSearch(domains, constraints)

print(cs.search())