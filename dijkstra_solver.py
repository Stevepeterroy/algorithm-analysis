import heapq

OUTPUT_FILE = "dijkstra_output.txt"

graph = {
    0: [(1, 4),  (7, 8)],
    1: [(0, 4),  (2, 8),  (7, 11)],
    2: [(1, 8),  (3, 7),  (5, 4),  (8, 2)],
    3: [(2, 7),  (4, 9),  (5, 14)],
    4: [(3, 9),  (5, 10)],
    5: [(2, 4),  (3, 14), (4, 10), (6, 2)],
    6: [(5, 2),  (7, 1),  (8, 6)],
    7: [(0, 8),  (1, 11), (6, 1),  (8, 7)],
    8: [(2, 2),  (6, 6),  (7, 7)],
}

def dijkstra(graph, source):
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[source] = 0
    pq = [(0, source)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(pq, (alt, v))

    return dist, prev

def reconstruct_path(prev, target):
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path

def format_results(source, dist, prev):
    lines = []
    sep = "=" * 55
    lines.append(sep)
    lines.append("        DIJKSTRA'S SHORTEST PATH ALGORITHM")
    lines.append(sep)
    lines.append(f"  Source Node : {source}")
    lines.append(f"  Nodes       : {sorted(graph.keys())}")
    lines.append("")
    lines.append(f"  {'Node':<8} {'Distance':<12} {'Shortest Path'}")
    lines.append("  " + "-" * 50)
    for node in sorted(dist):
        path = reconstruct_path(prev, node)
        path_str = " -> ".join(str(n) for n in path)
        dist_str = str(dist[node]) if dist[node] != float('inf') else "INF"
        lines.append(f"  {node:<8} {dist_str:<12} {path_str}")
    lines.append("")
    lines.append(sep)
    lines.append(f"  Minimum total distance sum : {sum(v for v in dist.values() if v != float('inf'))}")
    lines.append(sep)
    return "\n".join(lines)

def main():
    source = 0
    dist, prev = dijkstra(graph, source)
    output = format_results(source, dist, prev)

    print(output)

    with open(OUTPUT_FILE, "w") as f:
        f.write(output + "\n")

    print(f"\n  Results saved to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()
