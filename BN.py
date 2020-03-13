import copy
class Node(object):
    def __init__(self, name=""):
        self.name = name
        self.parents = dict()
        self.children = dict()

    def add_parent(self, parent):
        if not isinstance(parent, Node):
            raise ValueError("Parent must be an instance of Node class.")
        pname = parent.name
        self.parents[pname] = parent

    def add_child(self, child):
        if not isinstance(child, Node):
            raise ValueError("Parent must be an instance of Node class.")
        cname = child.name
        self.children[cname] = child


class BN(object):
    def __init__(self):
        self.nodes = dict()

    def add_edge(self, edge):
        (pname, cname) = edge
        if pname not in self.nodes:
            self.nodes[pname] = Node(name=pname)
        if cname not in self.nodes:
            self.nodes[cname] = Node(name=cname)

        parent = self.nodes.get(pname)
        child = self.nodes.get(cname) 
        parent.add_child(child)
        child.add_parent(parent)

    def print_graph(self):
        print "Bayes Network for given input is as follows:- "
        for nname, node in self.nodes.iteritems():
            print "\tNode " + nname
            print "\t\tParents: " + str(node.parents.keys())
            print "\t\tChildren: " + str(node.children.keys())

    def find_givenZ_ancestors(self, givenZ):
        """
        Traverse the graph, find all nodes that have givenZ descendants.
        """
        visit_nodes = copy.copy(givenZ) ## nodes to visit
        givenZ_ancestors = set() ## givenZ nodes and their ancestors

        while len(visit_nodes) > 0:
            next_node = self.nodes[visit_nodes.pop()]
            for parent in next_node.parents:
                givenZ_ancestors.add(parent)

        return givenZ_ancestors

    def is_dsep(self, X_val, Y_val, givenZ):

        givenZ_ancestors = self.find_givenZ_ancestors(givenZ)

        via_nodes = [(X_val, "up")]
        visited = set() ## keep track of visited nodes to avoid cyclic paths

        while len(via_nodes) > 0: 
            (nname, direction) = via_nodes.pop()
            node = self.nodes[nname]

            ## skip visited nodes
            if (nname, direction) not in visited:
                visited.add((nname, direction)) 

                ## if reaches the node "Y_val", then it is not d-separated
                if nname not in givenZ and nname == Y_val:
                    return False

                if direction == "up" and nname not in givenZ:
                    for parent in node.parents:
                        via_nodes.append((parent, "up"))
                    for child in node.children:
                        via_nodes.append((child, "down"))
                ## if traversing from parents, then need to check v-structure
                elif direction == "down":
                    ## path to children is always active
                    if nname not in givenZ: 
                        for child in node.children:
                            via_nodes.append((child, "down"))
                    ## path to parent forms a v-structure
                    if nname in givenZ or nname in givenZ_ancestors: 
                        for parent in node.parents:
                            via_nodes.append((parent, "up"))
        return True

    # def get_skeleton(self):
    #     """
    #     Find the skeleton of the Bayesian Network.
    #     Returns: 
    #         a set of undirected edges (represented by tuples) in the skeleton. 
    #     """
    #     skeleton = set()
    #     for (nname, node) in self.nodes.iteritems():
    #         ## add edges to skeleton
    #         for parent in node.parents:
    #             if (nname, parent) not in skeleton and (parent, nname) not in skeleton:
    #                 skeleton.add((nname, parent))
    #         for child in node.parents:
    #             if (nname, child) not in skeleton and (child, nname) not in skeleton:
    #                 skeleton.add((nname, child))

    #     return skeleton

    # def get_skeleton_immor(self):
    #     """
    #     Find the skeleton and immoralities in the graph.
    #     Returns:
    #         a tuple, the first element is a set of edges in the skeleton,
    #         and the second element is a set of parent-pairs that have common child(ren)
    #         but are not connected.
    #     """
    #     ## skeleton: a list of edges (undirected)
    #     skeleton = self.get_skeleton()
    #     ## find immoralities
    #     immoral = set()
    #     for (nname, node) in self.nodes.iteritems():
    #         ## check each pair of parents
    #         if len(node.parents) > 1:
    #             parents = node.parents.keys()
    #             for i1 in xrange(len(parents)-1):
    #                 for i2 in xrange(i1+1, len(parents)):
    #                     p1, p2 = parents[i1], parents[i2]
    #                     ## parents are immoral if they are not connected
    #                     if ((p1, p2) not in skeleton and (p2, p1) not in skeleton 
    #                         and (p1, p2) not in immoral and (p2, p1) not in immoral):
    #                         immoral.add((p1, p2))

    #     return (skeleton, immoral)
