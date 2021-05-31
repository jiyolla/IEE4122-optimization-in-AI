import math
import heapq


def solve(nodes, h, start_id, goal_id):
    distance = [math.inf] * len(nodes)
    distance[start_id] = 0
    f = math.inf
    # (h, node, depth)
    hq = [(h[start_id], nodes[start_id], 0)]
    found = False
    rollback_node = None
    while hq and not found:
        if hq[0][0] > f:
            # roll back
            max_depth = hq[0][2]
            min_h = math.inf
            new_hq = []
            for h_value, node, depth in hq:
                if depth > max_depth:
                    min_h = min(min_h, h_value)
                else:
                    heapq.heappush(new_hq, (h_value, node, depth))
            heapq.heappush(new_hq, (min_h, rollback_node, max_depth))
        else:
            _, node_src, depth = heapq.heappop(hq)
            for node_dst, dist_dst in node_src.get_neighbors().items():
                new_dist = distance[node_src.get_id()] + dist_dst
                if node_dst.get_id() == goal_id:
                    distance[goal_id] = new_dist
                    found = True
                    break
                if distance[node_dst.get_id()] > new_dist:
                    distance[node_dst.get_id()] = new_dist
                    heapq.heappush(hq, (h[node_dst.get_id()], node_dst, depth + 1))
                    if h[node_dst.get_id()] < f:
                        rollback_node = node_dst
                        f = h[node_dst.get_id()]
    return distance[goal_id] if found else False
