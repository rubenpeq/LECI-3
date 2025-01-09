#STUDENT NAME: Rúben Paulo Cunha Pequeno
#STUDENT NUMBER: 102480

#DISCUSSED TPI-1 WITH: (names and numbers): [] (empty list ^^)

# used as reference point for informeddepth_add_to_open() method sorting using multiple conditions
# https://stackoverflow.com/questions/57644038/python-sorting-a-list-using-lambda-function-with-multiple-conditions

from tree_search import *
from strips import *
from blocksworld import *

class MyNode(SearchNode):

    def __init__(self,state,parent,heuristic=None,cost=None,action=None,depth=None):
        super().__init__(state,parent)
        self.action = (state, state) if not parent else action # set action
        self.depth = 0 if not parent else parent.depth + 1  # calculate the depth of the node at initialization
        self.cost = 0 if not parent else parent.cost + cost # Total cost from root to current node
        self.heuristic = heuristic

class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth',improve=False):
        super().__init__(problem,strategy)
        self.improve = improve
        heuristic = self.problem.domain.heuristic(problem.initial, self.problem.goal) # estimated cost to reach goal
        root = MyNode(problem.initial, None, heuristic)     #
        self.open_nodes = [root]                            # change root to have the additional attributes (MyNode instead of SearchNode)
        self.num_open = 0       # number of open nodes - nodes in the queue
        self.num_solution = 0   # number of solution nodes found
        self.num_skipped = 0    # number of skipped nodes - nodes removed from the queue but not expanded
        self.num_closed = 0     # number of closed nodes - nodes removed from the queue and expanded

    def astar_add_to_open(self,lnewnodes):
        for new_node in lnewnodes:  # cycle through new nodes
            new_ecost = new_node.cost + new_node.heuristic
            inserted = False
            for i, node in enumerate(self.open_nodes):  # enumerate to get index
                ecost = node.cost + node.heuristic  # get estimated cost
                if new_ecost < ecost:   # check by estimated cost
                    self.open_nodes.insert(i, new_node)
                    inserted = True
                    break
                elif new_ecost == ecost:    # go check depth
                    if new_node.depth < node.depth:
                        self.open_nodes.insert(i, new_node)
                        inserted = True
                        break
                    elif new_node.depth == node.depth:  # go check alphabetical order
                        if new_node.state < node.state:
                            self.open_nodes.insert(i, new_node)
                            inserted = True
                            break
            if not inserted:    # worst estimated cost
                self.open_nodes.append(new_node)
                        

    def informeddepth_add_to_open(self, lnewnodes):
        lnewnodes = sorted(lnewnodes, key=lambda x: (x.heuristic + x.cost, x.state))    # sort new nodes based on estimated cost or alphabetically(2nd criteria)
        self.open_nodes[:0] = lnewnodes     # insert sorted new nodes at beggining of open_nodes

    def search2(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.num_solution += 1  # add 1 to number of solution nodes found
                if not self.improve:
                    self.solution = node
                    self.num_open = len(self.open_nodes)    # return number of open nodes when solution is found
                    return self.get_path(node)
                else:
                    self.num_skipped -= 1   # do not count solution as skipped
                    if not self.solution:
                        self.solution = node
                    elif node.cost < self.solution.cost:
                        self.solution = node
            if self.solution and node.cost + node.heuristic >= self.solution.cost:
                self.num_skipped += 1
            else:
                self.num_closed += 1    # add 1 to number of closed nodes, do not count if current node is the goal
                lnewnodes = []
                for a in self.problem.domain.actions(node.state):
                    newstate = self.problem.domain.result(node.state,a)
                    if newstate not in self.get_path(node):
                        cost = self.problem.domain.cost(node.state, a)  # cost of node action (total cost added in node initialization)
                        heuristic = self.problem.domain.heuristic(newstate, self.problem.goal) # estimated cost to reach goal
                        newnode = MyNode(newstate,node,heuristic,cost,a)
                        lnewnodes.append(newnode)
                self.add_to_open(lnewnodes)
        self.num_open = len(self.open_nodes)    # update number of open nodes before returning (always 0 at this point)
        return self.get_path(self.solution)
 
    def check_admissible(self,node):
        def isadmissible(n, total_cost):
            if n.parent is None:   # after checking every node in the path, return True
                return True
            elif n.heuristic + n.cost > total_cost:   # if a node heuristic in the path is greater, return False
                return False
            else:
                return isadmissible(n.parent, total_cost)
            
        return isadmissible(node, node.cost)    # recursively check if it's admissible


    def get_plan(self, node):
        def plan(n):
            if n.parent is None:    # after reaching root (do not count root action)
                return []
            else:                   # start returning list of actions
                return plan(n.parent) + [n.action]
            
        return plan(node)

    # if needed, auxiliary methods can be added here

class MyBlocksWorld(STRIPS):

    def heuristic(self, state, goal):
        value = 0
        for g in goal:  # loop through goal set
            if isinstance(g, Floor):
                if not any(isinstance(p, Floor) and p == g for p in state):  # check if the block is not on floor in the initial state
                    value += 1
            elif isinstance(g, On):
                b1, b2 = g.args
                if On(b1, b2) not in state: # check if b1 isn't above b2 in the initial state
                    value += 1
            elif isinstance(g, Free):
                if Free(g) not in state:    # check if goal block is free in the initial state
                    value += 1

        return value
