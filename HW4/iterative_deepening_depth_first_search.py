import math


def solve_with_depth_limit(nodes, start_id, goal_id, depth_limit):
    distance = [math.inf] * len(nodes)
    distance[start_id] = 0
    # (node, dist, depth)
    stack = [(nodes[start_id], 0, 0)]
    found = False
    while stack and not found:
        node_src, dist_src, depth = stack.pop()
        if depth >= depth_limit:
            continue
        for node_dst, dist_dst in node_src.get_neighbors().items():
            new_dist = dist_src + dist_dst
            if node_dst.get_id() == goal_id:
                distance[goal_id] = new_dist
                found = True
                break
            if distance[node_dst.get_id()] > new_dist:
                distance[node_dst.get_id()] = new_dist
                stack.append((node_dst, new_dist, depth + 1))
    return distance[goal_id] if found else False

def solve(nodes, start_id, goal_id, initial_depth_limit=1):
    for i in range(initial_depth_limit, len(nodes)):
        ans = solve_with_depth_limit(nodes, start_id, goal_id, i)
        if ans:
            return ans
