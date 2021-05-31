# Solve problem by each algorithm
# Compare the running time of each algorithm
import random
import time
import math
import heapq

import iterative_deepening_depth_first_search as iddfs
import bidirectional_search as bs
import greedy_best_first_search as gbfs
import a_star_search as ass
import recursive_best_first_search as rbfs


class Problem:
    def __init__(self, seed=None, num_nodes=100, prob=0.05, weight_min=10, weight_max=20):
        if seed is not None:
            random.seed(seed)
        self.nodes = [Node(i) for i in range(num_nodes)]
        self.edges = []
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if random.random() < prob:
                    weight = random.randint(weight_min, weight_max)
                    self.nodes[i].add_neighbor(self.nodes[j], weight)
                    self.edges.append((i, j, weight))
        self.generate_h()
                    
    def generate_h(self):
        # Calculate shortest path between every pair with floyd warshall algorithm
        # Introduce some random amount of negative deviation to shortest paths
        # The modified shortest paths are eligible as h()
        distance = [[math.inf] * len(self.nodes) for _ in range(len(self.nodes))]
        for src, dst, w in self.edges:
            distance[src][dst] = w
            distance[dst][src] = w
        for node in self.nodes:
            distance[node.get_id()][node.get_id()] = 0
        for k in range(len(self.nodes)):
            for src in range(len(self.nodes)):
                for dst in range(len(self.nodes)):
                    if distance[src][dst] > distance[src][k] + distance[k][dst]:
                        distance[src][dst] = distance[src][k] + distance[k][dst]

        # This randomizer breaks consistency premise of h(n), so it's disabled
        """
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                distance[i][j] *= random.random()
                distance[j][i] = distance[i][j]
        """

        self.h = distance
        
    def get_nodes(self):
        return self.nodes
    
    def get_h(self):
        return self.h


class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.adjacent_nodes = {}

    def add_neighbor(self, node, weight):
        self.adjacent_nodes[node] = weight
        node.adjacent_nodes[self] = weight

    def has_neighbor(self, node):
        return node in self.adjacent_nodes
    
    def get_neighbors(self):
        return self.adjacent_nodes
    
    def get_id(self):
        return self.node_id

    def __lt__(self, other):
        # No ordering between nodes
        return self
        
    def __repr__(self):
        return f'Node#{self.node_id}: {len(self.adjacent_nodes)} neighbors'

                                               
def main():
    num_p = 10
    records = [[] for _ in range(5)]
    for i in range(num_p):
        p = Problem()
        print(f'Problem#{i}: {len(p.get_nodes())} nodes, {len(p.edges)} edges')
        start_id = 0
        goal_id = 99
        s = time.perf_counter_ns()
        print(f'IDDFS: {iddfs.solve(p.get_nodes(), start_id, goal_id)}')
        e = time.perf_counter_ns()
        records[0].append(e - s)
        s = time.perf_counter_ns()
        print(f'Bidirectional Search: {bs.solve(p.get_nodes(), start_id, goal_id)}')
        e = time.perf_counter_ns()
        records[1].append(e - s)
        s = time.perf_counter_ns()
        print(f'Greedy Best First Search: {gbfs.solve(p.get_nodes(), p.get_h()[goal_id], start_id, goal_id)}')
        e = time.perf_counter_ns()
        records[2].append(e - s)
        s = time.perf_counter_ns()
        print(f'A* Search: {ass.solve(p.get_nodes(), p.get_h()[goal_id], start_id, goal_id)}')
        e = time.perf_counter_ns()
        records[3].append(e - s)
        s = time.perf_counter_ns()
        print(f'RBFS: {rbfs.solve(p.get_nodes(), p.get_h()[goal_id], start_id, goal_id)}\n')
        e = time.perf_counter_ns()
        records[4].append(e - s)
    print(f'IDDFS average running time: {sum(records[0])/num_p/10**6}ms')
    print(f'Bidirectional Search average running time: {sum(records[1])/num_p/10**6}ms')
    print(f'Greedy Best First Search average running time: {sum(records[2])/num_p/10**6}ms')
    print(f'A* Search average running time: {sum(records[3])/num_p/10**6}ms')
    print(f'RBFS average running time: {sum(records[4])/num_p/10**6}ms')
    

if __name__ == '__main__':
    main()
