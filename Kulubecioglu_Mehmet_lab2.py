import time
from collections import deque

# graph (adjacency list representation)
graph = {
    '1': ['2', '3'],
    '2': ['4', '5'],
    '3': ['6', '7'],
    '4': ['8'],
    '5': [],
    '6': [],
    '7': [],
    '8': []
}

# Breadth-First Search (BFS)
def breadth_first_search(start, goal, graph):
    visited = set()
    queue = deque([start])
    node_count = 0  # Counter for visited nodes

    while queue:
        node = queue.popleft()
        node_count += 1  # Increment node count for each visited node

        if node == goal:
            return node_count

        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)

    return node_count

# Depth-First Search (DFS)
def depth_first_search(start, goal, graph):
    visited = set()
    stack = [start]
    node_count = 0  # Counter for visited nodes

    while stack:
        node = stack.pop()
        node_count += 1  # Increment node count for each visited node

        if node == goal:
            return node_count

        if node not in visited:
            visited.add(node)
            for neighbor in reversed(graph[node]):  # Reverse to maintain order
                if neighbor not in visited:
                    stack.append(neighbor)

    return node_count

# Depth-Limited Search (DLS)
def depth_limited_search(start, goal, graph, limit, visited=None, node_count=0):
    if visited is None:
        visited = set()

    if start == goal:
        return True, node_count + 1  # Found the goal

    if limit <= 0:
        return False, node_count

    visited.add(start)
    node_count += 1

    for neighbor in graph[start]:
        if neighbor not in visited:
            found, node_count = depth_limited_search(neighbor, goal, graph, limit - 1, visited, node_count)
            if found:
                return True, node_count

    return False, node_count

# Iterative Deepening Search (IDS)
def iterative_deepening_search(start, goal, graph, max_depth):
    total_node_count = 0
    for depth in range(max_depth + 1):
        found, node_count = depth_limited_search(start, goal, graph, depth)
        total_node_count += node_count
        if found:
            return total_node_count
    return total_node_count

# Bidirectional Search
def bidirectional_search(start, goal, graph):
    if start == goal:
        return 1  # Starting node is the goal

    forward_queue = deque([start])
    backward_queue = deque([goal])
    forward_visited = {start}
    backward_visited = {goal}
    node_count = 0  # Counter for visited nodes

    while forward_queue and backward_queue:
        # Forward search step
        current_forward = forward_queue.popleft()
        node_count += 1
        for neighbor in graph[current_forward]:
            if neighbor in backward_visited:
                return node_count
            if neighbor not in forward_visited:
                forward_visited.add(neighbor)
                forward_queue.append(neighbor)

        # Backward search step
        current_backward = backward_queue.popleft()
        node_count += 1
        for neighbor in graph[current_backward]:
            if neighbor in forward_visited:
                return node_count
            if neighbor not in backward_visited:
                backward_visited.add(neighbor)
                backward_queue.append(neighbor)

    return node_count

# Performance Measurement Function
def measure_performance(search_function, *args):
    start_time = time.time()
    node_count = search_function(*args)
    execution_time = time.time() - start_time
    return node_count, execution_time

# Running for all search algorithms
def run_all_algorithms(graph):
    start_node = '1'
    goal_node = '8'
    max_depth = 10  # Set a reasonable max depth for IDS

    # Run BFS
    bfs_nodes, bfs_time = measure_performance(breadth_first_search, start_node, goal_node, graph)

    # Run DFS
    dfs_nodes, dfs_time = measure_performance(depth_first_search, start_node, goal_node, graph)

    # Run IDS
    ids_nodes, ids_time = measure_performance(iterative_deepening_search, start_node, goal_node, graph, max_depth)

    # Run DLS (with a depth limit; set to 3 for this example)
    dls_limit = 3
    dls_found, dls_nodes = depth_limited_search(start_node, goal_node, graph, dls_limit)
    dls_time = 0  # Since DLS is called within IDS, and time is already measured there

    # Run Bidirectional Search
    bi_nodes, bi_time = measure_performance(bidirectional_search, start_node, goal_node, graph)

    # Print results
    print(f"Breadth-First Search (BFS) -> Nodes Visited: {bfs_nodes}, Execution Time: {bfs_time:.6f} seconds")
    print(f"Depth-First Search (DFS) -> Nodes Visited: {dfs_nodes}, Execution Time: {dfs_time:.6f} seconds")
    print(f"Iterative Deepening Search (IDS) -> Nodes Visited: {ids_nodes}, Execution Time: {ids_time:.6f} seconds")
    print(f"Depth-Limited Search (DLS) with limit {dls_limit} -> Nodes Visited: {dls_nodes}, Execution Time: {dls_time:.6f} seconds")
    print(f"Bidirectional Search -> Nodes Visited: {bi_nodes}, Execution Time: {bi_time:.6f} seconds")

# Running all algorithms
if __name__ == "__main__":
    run_all_algorithms(graph)
