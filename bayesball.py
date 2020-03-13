import sys
from BN import *

if __name__ == "__main__":
    header = sys.stdin.readline().rstrip().split(" ")
    if len(header) != 3:
        print("First line must specify number of nodes, edges and queries.")
        sys.exit(1)
    (nnode, nedge, nquery) = map(int, header)

    ## edges
    edges = []
    for line in xrange(nedge):
        edge = sys.stdin.readline().rstrip().split(" ")
        edges += [edge]

    ## queries
    queries = []
    for line in xrange(nquery):
        query = sys.stdin.readline().rstrip().split(" ")
        (X_val, Y_val, givenZ) = (query[0], query[1], query[3:])
        queries += [(X_val, Y_val, givenZ)]

    # Create Bayesian Network
    BayesNet = BN()
    for edge in edges:
        BayesNet.add_edge(edge)

    ## Check D-separation
    for (X_val, Y_val, givenZ) in queries:
        print BayesNet.is_dsep(X_val, Y_val, givenZ)

    # BayesNet.print_graph()

