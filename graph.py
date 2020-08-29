import csv
import pandas as pd

data = pd.read_csv("responses.csv")
# user graph, email as keys
user_graph = dict.fromkeys(data['Email address'], set())

def edge_overlap_cuisine(row_1, row_2):
    return True
# returns true if 
def edge_overlap_teach(row_1, row_2):
    if (type(row_1[5]) == float or type(row_2[5]) == float) or (type(row_1[6]) == float or type(row_2[6]) == float):
        return False
    teach_1 = set(row_1[5].split(','))
    teach_2 = set(row_2[5].split(','))
    learn_1 = set(row_1[6].split(','))
    learn_2 = set(row_2[6].split(','))
    return len(teach_1.intersection(learn_2)) > 0 or len(teach_2.intersection(learn_1)) > 0 
    
for i, row_1 in data.iterrows():
    for indx, row_2 in data.iterrows():
        if edge_overlap_teach(row_1, row_2):
            user_graph[row_1['Email address']].add(row_2['Email address'])
            user_graph[row_2['Email address']].add(row_1['Email address'])

print(user_graph)
def seq_blossom_recursion(G, M, forest, v, w):
    blossom = shortest_path(forest, v, w) + [v] # blossom
    G_contracted = G
    # contract all blossom nodes into w
    M_contracted = M
    # contract all blossom nodes into w
    P_contracted = seq_find_aug_path(G_contracted, M_contracted)
    if (w in P_contracted):
        path = P_contracted # lifted w blossom b
        return path
    else:
        return P_contracted
def shortest_path(forest, v, w):
    return
def seq_return_aug_path(forest, v, w, node_to_root):
    root_v = node_to_root(v)
    root_w = node_to_root(w)
    path_1 = shortest_path(forest, root_v, v)
    path_2 = shortest_path(forest, w, root_w)
    return path_1 + path_2

def seq_add_to_forest(M, forest, v, w):
    # x = vertex adjacent to w in M
    # add (v, w), (w, x) to tree(v) in F
    # add vertex x to nodes_to_check
    node_to_root(w) = node_to_root(v)
    node_to_root(x) = node_to_root(v)

def seq_find_aug_path(G, M):
    forest = set()# empty forest
    nodes_to_check = set() # exposed vertices in G
    for v in nodes_to_check:
        forest.add(v)
        node_to_root(v) = v
    # mark all matched edges (all edges in M)
    for v in forest_nodes:
        while():# unmarked edge e = (v,w) exists
            if w not in forest:
                seq_add_to_forest(M, forest, v, w)
            else:
                if (): # length of path (w, node_to_root(w)) % 2 == 0:
                    if (node_to_root(v) != node_to_root(w)):
                        path = seq_return_aug_path(F, v, w, node_to_root)
                    else:
                        path = seq_blossom_recursion(G, M, F, v, w)
                    return path
                else:
                    pass
            # mark edge e
    return []


def seq_find_maximum_matching(G, M):
    path = seq_find_aug_path(G, M)
    if len(path) == 0:
        return M
    else:
        # add alternating edges of path to M
        return seq_find_maximum_matching(G, M)