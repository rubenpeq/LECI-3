#encoding: utf8

# YOUR NAME:    Rúben Pequeno
# YOUR NUMBER:  102480

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT (names, numbers):
# - ...
# - ...

from semantic_network import *
from constraintsearch import *
from bayes_net import *

class MySN(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)
        # ADD CODE HERE IF NEEDED
        pass

    # General query method, processing different types of
    # relations according to their specificities
    def query(self,entity,relname): # Exercise 1 - 30%
        local_decl = self.query_local(e1=entity, relname=relname)
        inherited_decl = self.get_inherited_declarations(entity, relname)

        # Merge local and inherited declarations
        decl = list(set(local_decl + inherited_decl))

        if not decl:
            return []  # No relations found

        if relname in ['member', 'subtype']:
            return [d.relation.entity2 for d in local_decl]

        # Determine the type of the relation
        relation_type = self.determine_relation_type(decl)

        # Process based on relation type
        if relation_type == "AssocOne":
            return self.process_assoc_one(decl)
        elif relation_type == "AssocNum":
            return self.process_assoc_num(decl)
        elif relation_type == "AssocSome":
            return self.process_assoc_some(decl)
        else:
            return []
        
    def process_assoc_one(self, decl):
        # Return the most common value
        values = [d.relation.entity2 for d in decl if isinstance(d.relation, AssocOne)]
        return [max(set(values), key=values.count)] if values else []
    
    def process_assoc_num(self, decl):
        # Calculate the average of numeric values
        values = [d.relation.entity2 for d in decl if isinstance(d.relation, AssocNum)]
        return [sum(values) / len(values)] if values else []

    def process_assoc_some(self, decl):
        # Combine all values without filtering
        return list(set([d.relation.entity2 for d in decl if isinstance(d.relation, AssocSome)]))

    def get_inherited_declarations(self, entity, relname):
        """
        Get inherited declarations for a given entity and relation name, with support for cancelling.
        """
        inherited_declarations = []
        visited = set()  # To avoid infinite loops in case of cycles
        to_visit = [entity]  # Start with the given entity

        while to_visit:
            current = to_visit.pop()
            if current in visited:
                continue
            visited.add(current)

            # Query all local declarations for the current entity and relation name
            local_declarations = self.query_local(e1=current, relname=relname)

            # Check for cancelling (AssocOne and AssocNum stop inheritance)
            if relname in ['AssocOne', 'AssocNum']:
                if any(isinstance(decl.relation, (AssocOne, AssocNum)) for decl in local_declarations):
                    # Add only the local declarations for AssocOne or AssocNum
                    inherited_declarations.extend(local_declarations)
                    break  # Stop further inheritance traversal
            else:
                # For other relation types, keep traversing
                inherited_declarations.extend(local_declarations)

            # Add parents (supertype relations) to the queue for further traversal
            parent_relations = self.query_local(e1=current, relname="subtype")
            parent_relations += self.query_local(e1=current, relname="member")
            to_visit.extend([rel.relation.entity2 for rel in parent_relations])

        return inherited_declarations
    
    def determine_relation_type(self, declarations):
        "Determines which type of declaration should be used."
        # Count frequency of each relation type
        type_counts = {"AssocOne": 0, "AssocNum": 0, "AssocSome": 0}
        for decl in declarations:
            if isinstance(decl.relation, AssocOne):
                type_counts["AssocOne"] += 1
            elif isinstance(decl.relation, AssocNum):
                type_counts["AssocNum"] += 1
            elif isinstance(decl.relation, AssocSome):
                type_counts["AssocSome"] += 1
        # Return the most common type
        return max(type_counts, key=type_counts.get)

class MyBN(BayesNet):

    def __init__(self):
        BayesNet.__init__(self)
        # ADD CODE HERE IF NEEDED
        pass

    def test_independence(self,v1,v2,given):    # Exercise 2 - 40%
        vars = {v1, v2} | set(given)
        ancestors = set()
        for var in vars:
            ancestors.update(self.get_ancestors(var))

        graph = set()
        for var in vars | ancestors:
            # Connect variable to its parents
            for parent_list, _, _ in self.dependencies.get(var, []):
                for parent in parent_list:
                    graph.add(tuple(sorted((var, parent))))

            # Connect parents to each other
            for parent_list, _, _ in self.dependencies.get(var, []):
                for i, p1 in enumerate(parent_list):
                    for p2 in parent_list[i + 1:]:
                        graph.add(tuple(sorted((p1, p2))))

        # Remove edges involving any given variables
        graph = {edge for edge in graph if not (edge[0] in given or edge[1] in given)}

        independent = not self.has_path(graph, v1, v2)
        return list(graph), independent
    
    def get_ancestors(self, var, visited=None):
        "Find all ancestors of variables."
        def get_ancestors_recursive(var, visited=None):
            if visited is None:
                visited = set()
            if var in visited:
                return set()
            visited.add(var)
            ancestors = set()
            for parent_list, _, _ in self.dependencies.get(var, []):
                for parent in parent_list:
                    ancestors.add(parent)
                    ancestors.update(get_ancestors_recursive(parent, visited))
            return ancestors
        
        return get_ancestors_recursive(var, visited)
    
    def has_path(self, graph, start, end):
        "Check for a path between start and end."
        visited = set()
        queue = [start]
        while queue:
            current = queue.pop(0)
            if current == end:
                return True
            if current in visited:
                continue
            visited.add(current)
            neighbors = {v for u, v in graph if u == current} | {u for u, v in graph if v == current}
            queue.extend(neighbors - visited)
        return False

class MyCS(ConstraintSearch):

    def __init__(self,domains,constraints):
        ConstraintSearch.__init__(self,domains,constraints)
        # ADD CODE HERE IF NEEDED
        pass

    def search_all(self, domains=None):
        self.calls += 1

        if domains is None:
            domains = self.domains

        # If any variable has an empty domain
        if any([len(values) == 0 for values in domains.values()]):
            return []

        # If all variables have exactly one value
        if all([len(values) == 1 for values in domains.values()]):
            return [{var: values[0] for var, values in domains.items()}]

        # Choose variable with the smallest domain > 1
        var = min((n for n in domains if len(domains[n]) > 1), key=lambda x: len(domains[x]))

        solutions = []

        for value in domains[var]:
            new_domains_dict = dict(domains)
            new_domains_dict[var] = [value]
            self.propagate(new_domains_dict, var)
            for solution in self.search_all(new_domains_dict):
                if solution not in solutions:  # Avoid repetitions
                    solutions.append(solution)

        return solutions

def handle_ho_constraint(domains,constraints,variables,constraint): # Exercise 4 - 15%
    from itertools import product

    aux_var = "".join(variables)
    aux_domain = [t for t in product(*(domains[var] for var in variables)) if constraint(t)]

    # Add the aux variable to the domains
    domains[aux_var] = aux_domain

    # Binary constraints between the aux variable and each original variable
    for i, var in enumerate(variables):
        def binary_constraint(vj, xj, vi, xi, i=i):
            if vi == aux_var:
                return isinstance(xj, tuple) and xj[i] == xi
            return isinstance(xj, tuple) and xi == xj[i]

        constraints[(aux_var, var)] = binary_constraint
        constraints[(var, aux_var)] = binary_constraint

    return domains, constraints