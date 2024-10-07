from collections import defaultdict, deque
import graphviz 

# Graph representation using adjacency list and capacity dictionary
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.capacity = defaultdict(lambda: defaultdict(int))
        self.adj = defaultdict(list)
        self.flow = defaultdict(lambda: defaultdict(int))  # Track flow along edges
        self.original_edges = {}

    # Add edge to the graph
    def add_edge(self, u, v, cap):
        self.capacity[u][v] = cap
        self.original_edges[(u,v)] = 0
        self.adj[u].append(v)
        self.adj[v].append(u)  # reverse edge for the residual graph

    # Breadth-First Search to find an augmenting path
    def bfs(self, s, t, parent):
        visited = [False] * self.V
        queue = deque([(s, float('Inf'))])
        visited[s] = True
        parent[s] = -1

        while queue:
            cur, flow = queue.popleft()
            for next in self.adj[cur]:
                if not visited[next] and self.capacity[cur][next] > 0:
                    parent[next] = cur
                    new_flow = min(flow, self.capacity[cur][next])
                    if next == t:
                        return new_flow
                    queue.append((next, new_flow))
                    visited[next] = True
        return 0

    # Ford-Fulkerson implementation
    def ford_fulkerson(self, s, t):
        parent = [-1] * self.V
        max_flow = 0

        # Augment the flow while there is a path from s to t
        while True:
            new_flow = self.bfs(s, t, parent)
            if new_flow == 0:
                break
            max_flow += new_flow
            cur = t
            while cur != s:
                prev = parent[cur]
                self.capacity[prev][cur] -= new_flow
                self.capacity[cur][prev] += new_flow
                self.flow[prev][cur] += new_flow  # Track the flow
                self.flow[cur][prev] -= new_flow  # For residual graph
                cur = prev

        return max_flow

# Function to handle multiple sources and sinks
def max_flow_multiple_sources_sinks(graph, sources, sinks, source_capacities, sink_capacities):
    V = graph.V
    super_source = V      # New super source index
    super_sink = V + 1    # New super sink index

    # Create a new graph with additional vertices
    augmented_graph = Graph(V + 2)

    # Copy existing edges to the augmented graph
    for u in range(V):
        for v in graph.adj[u]:
            if (u,v) in graph.original_edges:
                augmented_graph.add_edge(u, v, graph.capacity[u][v])

    # Connect super_source to all original sources with specified capacities
    for i in range(len(sources)):
        augmented_graph.add_edge(super_source, sources[i], source_capacities[i])

    # Connect all original sinks to super_sink with specified capacities
    for i in range(len(sinks)):
        augmented_graph.add_edge(sinks[i], super_sink, 1e5)

    # Calculate maximum flow from super_source to super_sink
    max_flow = augmented_graph.ford_fulkerson(super_source, super_sink)

    # Visualize the graph
    dot = graphviz.Digraph(comment='Graph Visualization', format='png')
    
    # Adding nodes for the graph
    for u in range(augmented_graph.V):
        if u == super_source:
            # dot.node(str(u), label=f'Super Source', color='red', shape='doublecircle')
            continue
        elif u == super_sink: 
            # dot.node(str(u), label=f'Super Sink', color='blue', shape='doublecircle')
            continue
        elif u in sources:
            dot.node(str(u), label=f'Node {u}', color='red', shape='doublecircle')
        elif u in sinks:
            dot.node(str(u), label=f'Node {u}', color='blue', shape='doublecircle')
        else:
            dot.node(str(u), label=f'Node {u}')

    # Adding edges based on the augmented_graph's flow information
    for u in range(augmented_graph.V):
        for v in augmented_graph.adj[u]:
            if u == super_source or v == super_sink or u == super_sink or v == super_source:
                # Special handling for super source/sink edges
                continue
            # Only draw forward edges with positive capacity
            if (u,v) in graph.original_edges:
                dot.edge(str(u), str(v), label=f'{augmented_graph.flow[u][v]}/{graph.capacity[u][v]}')

    # # Visualize edges connected to the super source
    # for i, src in enumerate(sources):
    #     dot.edge(str(super_source), str(src), label=str(augmented_graph.flow[super_source][src]), color='red')
    
    # # Visualize edges connected to the super sink
    # for i, sink in enumerate(sinks):
    #     dot.edge(str(sink), str(super_sink), label=str(augmented_graph.flow[sink][super_sink]), color='blue')

    dot.render('static/Graph_visualization', view=False)
    return max_flow

def network_flow_api(node_number, edge_number, edges, sources, sinks, source_capacities):

    V = int(node_number.split(' ')[0])
    E = int(edge_number.split(' ')[0])
    graph = Graph(V)
    edges = edges.split('\n')
    print(edges)
    for i in range(E):
        u,v,w = edges[i].strip().split(' ')
        graph.add_edge(int(u),int(v),int(w))
    
    sources = sources.strip().split(' ')
    for i in range(len(sources)):
        sources[i] = int(sources[i])

    sinks = sinks.strip().split(' ')
    for i in range(len(sinks)):
        sinks[i] = int(sinks[i])

    src_capacities = []
    for c in source_capacities.split(' '):
        src_capacities.append(int(c))

    sink_capacities = []
    # for c in lines[ptr].split():
    #     sink_capacities.append(int(c))

    max_flow = max_flow_multiple_sources_sinks(graph, sources, sinks, src_capacities, sink_capacities)
    return max_flow