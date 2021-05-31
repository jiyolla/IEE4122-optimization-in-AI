import math
from collections import deque


def solve(nodes, start_id, goal_id):
    d_s = [math.inf] * len(nodes)
    d_g = [math.inf] * len(nodes)
    d_s[start_id] = 0
    d_g[goal_id] = 0
    q_s = deque()
    q_g = deque()
    
    # (node, dist)
    q_s.append((nodes[start_id], 0))
    q_g.append((nodes[goal_id], 0))
    
    found = False
    while q_s and q_g and not found:
        node_src_s, dist_src_s = q_s.popleft()
        node_src_g, dist_src_g = q_g.popleft()

        for node_dst, dist_dst in node_src_s.get_neighbors().items():
            new_dist = dist_src_s + dist_dst
            if d_s[node_dst.get_id()] > new_dist:
                d_s[node_dst.get_id()] = new_dist
                if not math.isinf(d_g[node_dst.get_id()]):
                    found = node_dst.get_id()
                    break
                q_s.append((node_dst, new_dist))
        for node_dst, dist_dst in node_src_g.get_neighbors().items():
            new_dist = dist_src_g + dist_dst
            if d_g[node_dst.get_id()] > new_dist:
                d_g[node_dst.get_id()] = new_dist
                if not math.isinf(d_s[node_dst.get_id()]):
                    found = node_dst.get_id()
                    break
                q_g.append((node_dst, new_dist))
        
    return d_s[found] + d_g[found] if found else False
        