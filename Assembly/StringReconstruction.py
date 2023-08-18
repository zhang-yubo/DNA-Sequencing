import time
import json
import random

start_time = time.time()

# f_debug = open("debug.txt", "w")

# given an array of kmers (list), construct a DB graph (dictionary) 
def WalkDB(patterns):
    graph = {}
    for p in patterns:
        s1 = p[:-1]
        s2 = p[1:]
        next = graph.get(s1)
        if next:
            next.append(s2)
            graph.update({s1 : next})
        else:
            graph.update({s1 : [s2]})
    return graph

# given a graph (dictionary with each nodes' adjacency list), return a cycle that is a Euler path (list)
#  ------------find path--------------
def EulerPath(graph):

#  ------------find unbalanced nodes--------------

    # count edge
    edge_count = 0
    for k in graph.keys():
        edge_count += len(graph.get(k))

    nodes_degrees = {}
    for k in graph.keys():
        next_list = graph.get(k)
        k_degrees = nodes_degrees.get(k)

        # add k's out degree
        if k_degrees:
            k_degrees[1] += len(next_list)
        else:
            nodes_degrees.update({k : [0, len(next_list)]})
        
        # add next nodes' in degree
        for next in next_list:
            next_degrees = nodes_degrees.get(next)
            if next_degrees:
                next_degrees[0] += 1
            else:
                nodes_degrees.update({next : [1, 0]})

    unbalanced = [None, None]
    for k in nodes_degrees.keys():
        degrees = nodes_degrees.get(k)
        if degrees[0] > degrees[1]:  # in greater than out
            unbalanced[0] = k
        elif degrees[0] < degrees[1]: # in less than out
            unbalanced[1] = k

    if None in unbalanced:
        print("Graph is not pseudo balanced")
        exit()

    #  ------------add extra edge to graph, 0 to 1--------------

    unb1_list = graph.get(unbalanced[0])
    if unb1_list:
        unb1_list.append(unbalanced[1])
        graph.update({unbalanced[0] : unb1_list})
    else:
        graph.update({unbalanced[0] : [unbalanced[1]]})

    edge_count += 1

    #  ------------find eulerian cycle--------------

    cycle = []

    all_nodes = list(graph.keys())
    rand_indx = random.randrange(len(all_nodes))
    current_node = all_nodes[rand_indx]
    cycle.append(current_node)

    current_index = 0

    while edge_count > 0:

        # print("**********debug")
        # print(current_node)
        # print(cycle)
        # print(graph)

        prev_node = current_node
        has_next = False
        next_list = graph.get(current_node)

        # normal case
        # f_debug.write(current_node + json.dumps(next_list) + '\n')
        if len(next_list) > 0:
            # if len(next_list) > 1:
            #     f_debug.write(json.dumps(next_list) + '\n')
            next = next_list[0]
            current_node = next
            has_next = True
            next_list.pop(0)
            graph.update({prev_node : next_list})
            edge_count -= 1   

        if has_next:
            current_index += 1
            cycle.insert(current_index, current_node)

        # end of cycle
        else:
            for node in cycle:
                next_list = graph.get(node)
                if next_list:
                    current_node = node
                    has_next = True
                    # f_debug.write(current_node + '\n')
                    break
            
            if not has_next:
                print("not a valid graph")
                exit()
            
            current_index = cycle.index(current_node)
        
    #  ------------modifie cycle to path--------------
    start_pos = None
    for i, n in enumerate(cycle[:-1]):
        if cycle[i] == unbalanced[0] and cycle[i+1] == unbalanced[1]:
            start_pos = i + 1
            break

    # print(cycle)
    cycle = cycle[start_pos:-1] + cycle[:start_pos]

    return cycle

# given path (list of kmers in order), combine them (string)
def ReconWalk(path):
    s = path[0]
    for p in path[1:]:
        s += p[-1]
    return s


# nothing important
def CycleStringToIndex(cycle, patterns):
    index_dict = {}
    index_cycle = []
    for s in cycle:
        index_dict.update({s : [i for i, x in enumerate(patterns) if x == s]})
    for s in cycle:
        indexes = index_dict.get(s)
        index_cycle.append(indexes[0])
        indexes.remove(indexes[0])
        index_dict.update({s : indexes})
    return index_cycle
        


# DB, then Euler, then Recon

f = open("spectrum.txt", "r")
patterns = f.readlines()
f.close()

patterns = [x.strip() for x in patterns]

k = len(patterns[0])


DB = WalkDB(patterns)
cycle = EulerPath(DB)
recon = ReconWalk(cycle)


f1 = open("output.txt", "w")

f1.write(recon)

# for i in range(len(recon_s) - k + 1):
#     kmer = recon_s[i:i+k]
#     if kmer in patterns:
#         f1.write(">read_" + str(patterns.index(kmer)) + "\n")

f1.close()

end_time = time.time()

print("runtime: " + str(end_time - start_time) + "s")