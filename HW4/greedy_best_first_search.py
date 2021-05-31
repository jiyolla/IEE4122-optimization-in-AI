import math
import heapq


def solve(nodes, h, start_id, goal_id):
    distance = [math.inf] * len(nodes)
    distance[start_id] = 0
    # (h, node)
    hq = [(h[start_id], nodes[start_id])]
    found = False
    while hq and not found:
        _, node_src = heapq.heappop(hq)
        for node_dst, dist_dst in node_src.get_neighbors().items():
            new_dist = distance[node_src.get_id()] + dist_dst
            if node_dst.get_id() == goal_id:
                distance[goal_id] = new_dist
                found = True
                break
            if distance[node_dst.get_id()] > new_dist:
                distance[node_dst.get_id()] = new_dist
                heapq.heappush(hq, (h[node_dst.get_id()], node_dst))
    return distance[goal_id] if found else False
