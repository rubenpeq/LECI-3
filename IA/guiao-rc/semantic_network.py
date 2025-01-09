

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#     - AssocOne    - 
#     - AssocNum    - 

# TODO - exercises 15, 16; Bayesian Networks exercises

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# Subclasse AssocOne
class AssocOne(Relation):   # Ex 15a
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)
    
# Subclasse AssocNum
class AssocNum(Relation):   # Ex 15a
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)
        

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista

class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
        
    def __str__(self):
        return str(self.declarations)
    
    def insert(self,decl):
        self.declarations.append(decl)
    
    def query_local(self,user=None,e1=None,rel=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result
    
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    def list_associations(self):    # Ex 1
        lst = [d.relation.name for d in self.declarations if isinstance(d.relation, Association)]
        return set(lst)
        
    def list_objects(self): # Ex 2
        lst = [d.relation.entity1 for d in self.declarations if isinstance(d.relation, Member)]
        return set(lst)

    def list_users(self):   # Ex 3
        lst = [d.user for d in self.declarations]
        return set(lst)
    
    def list_types(self):   # Ex 4
        lst = [d.relation.entity2 for d in self.declarations if (isinstance(d.relation, Member) or isinstance(d.relation, Subtype))]
        return set(lst)
        
    def list_local_associations(self, obj): # Ex 5 
        lst = [d.relation.name for d in self.declarations if d.relation.entity1 == obj and isinstance(d.relation, Association)]
        return set(lst)
        
    def list_relations_by_user(self, user): # Ex 6
        lst = [d.relation.name for d in self.declarations if d.user == user]
        return set(lst)
    
    def associations_by_user(self, user):   # Ex 7
        assoc_set = {d.relation.name for d in self.declarations if d.user == user and isinstance(d.relation, Association)}
        return len(assoc_set)
    
    def list_local_associations_by_entity(self, obj):   # Ex 8
        lst = [(d.relation.name, d.user) for d in self.declarations if d.relation.entity1 == obj and isinstance(d.relation, Association)]
        return set(lst)
    
    def predecessor(self, type, obj):   # Ex 9
        ldeclartions = self.query_local(e1=obj)
        lparents = [ d.relation.entity2 for d in ldeclartions if not isinstance(d.relation, Association) ]

        if type in lparents:
            return True
        
        for p in lparents:
            if type == p or self.predecessor(type, p):
                return True

        return False
    
    def predecessor_path(self, type, obj):  # Ex 10
        ldeclartions = self.query_local(e1=obj)
        lparents = [ d.relation.entity2 for d in ldeclartions if not isinstance(d.relation, Association) ]

        if type in lparents:
            return [type, obj]
        
        for p in lparents:
            path = self.predecessor_path(type, p)
            if  path != None:
                return path + [obj]

        return None
    
    def query(self, entity, association=None):    # Ex 11a
        ldeclartions = self.query_local(e1=entity)
        lparents = [ d.relation.entity2 for d in ldeclartions if not isinstance(d.relation, Association) ]

        lassoc = [ d for d in ldeclartions if isinstance(d.relation, Association) 
                                            and (d.relation.name == association or association == None) ]
        
        for p in lparents:
            lassoc += self.query(p, association)
        return lassoc
    
    def query2(self, entity, relation=None):    # Ex 11b
        query_result = self.query(entity)

        ldeclartions = self.query_local(e1=entity)
        lassoc = [ d for d in ldeclartions if not isinstance(d.relation, Association) 
                                            and (d.relation.name == relation or relation == None) ]

        return query_result + lassoc

    def query_cancel(self, entity, association):    # Ex 12
        ldeclartions = self.query_local(e1=entity)
        lparents = [ d.relation.entity2 for d in ldeclartions if not isinstance(d.relation, Association) ]

        lassoc = [ d for d in ldeclartions if isinstance(d.relation, Association) and d.relation.name == association ]
        
        if lassoc == []:
            for p in lparents:
                lassoc += self.query_cancel(p, association)

        return lassoc
    
    def query_down(self, type, association, child=False):    # Ex 13
        ldeclartions = self.query_local(e2=type)
        lchildren = [ d.relation.entity1 for d in ldeclartions if not isinstance(d.relation, Association) ]

        lassoc = []
        if child:
            lassoc = [ d for d in self.query_local(e1=type) if isinstance(d.relation, Association) 
                                                                and d.relation.name == association ]
    
        for c in lchildren:
            lassoc += self.query_down(c, association, child=True)

        return lassoc

    def query_induce(self, type, association):   # Ex 14
        lassoc = self.query_down(type, association)   # list the associations
        count_dict = {} # dictionary to count relation ocurrence
        
        for x in lassoc:    # count ocurrences
            if x.relation.entity2 not in count_dict:
                count_dict[x.relation.entity2] = 1
            else:
                count_dict[x.relation.entity2] += 1
            
        return  max(count_dict, key=count_dict.get) # return entity with max count in dict
    
    def query_local_assoc():    # Ex 15b
        pass