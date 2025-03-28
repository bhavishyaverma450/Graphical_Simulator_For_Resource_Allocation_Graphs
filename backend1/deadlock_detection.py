def detect_deadlock(nodes, edges):
    # Implement a simple cycle detection algorithm
    graph = build_graph(nodes, edges)
    visited = set()
    stack = set()

    def visit(node):
        if node in stack:
            return True
        if node in visited:
            return False
        visited.add(node)
        stack.add(node)
        for neighbor in graph.get(node, []):
            if visit(neighbor):
                return True
        stack.remove(node)
        return False

    for node in nodes:
        if visit(node):
            return True
    return False

def build_graph(nodes, edges):
    graph = {node: [] for node in nodes}
    for from_node, to_node in edges:
        graph[from_node].append(to_node)
    return graph
