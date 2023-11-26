import networkx as nx
import matplotlib.pyplot as plt
import heapq
import math

def euclidean_distance(node, goal_node, pos):
    x1, y1 = pos[node]
    x2, y2 = pos[goal_node]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def cost(node1, node2, G):
    return G[node1][node2]["weight"]

def neighbors(node, G):
    return list(G.neighbors(node))

def a_star(G, start, goal, pos):
    if start not in G or goal not in G:
        return "Start or goal node not in the graph."

    open_set = [(0, start)]  # Priority queue with (f_score, node)
    came_from = {}  # Dictionary to store the parent of each node
    g_score = {start: 0}   # Dictionary to store the cost from the start node to each node

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in neighbors(current, G):
            tentative_g_score = g_score[current] + cost(current, neighbor, G)

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + euclidean_distance(neighbor, goal, pos)
                heapq.heappush(open_set, (f_score, neighbor))

    return "No path found"

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def visualize_path(G, pos, path):
    # Visualizing the path
    path_edges = list(zip(path, path[1:]))

    edge_labels = {(edge[0], edge[1]): G[edge[0]][edge[1]]['weight'] for edge in path_edges}

    plt.figure(figsize=(10, 12))

    # Draw the entire graph with gray edges
    nx.draw(G, pos, with_labels=True, node_size=700, font_size=8,
            font_color="black", font_weight="bold", edge_color="gray", width=0.5)

    # Highlight the path with thicker pink edges
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="pink", width=2)

    # Draw start and end nodes in green
    nx.draw_networkx_nodes(G, pos, nodelist=[path[0]], node_color="green", node_size=700)
    nx.draw_networkx_nodes(G, pos, nodelist=[path[-1]], node_color="green", node_size=700)

    # Draw intermediate nodes with a different color (e.g., light blue)
    intermediate_nodes = set(path) - {path[0], path[-1]}
    nx.draw_networkx_nodes(G, pos, nodelist=intermediate_nodes, node_color="lightblue", node_size=700)

    # Draw edge labels in red
    nx.draw_networkx_edge_labels(G.subgraph(path_edges), pos, edge_labels=edge_labels, font_color='red')

    plt.show()


# Creating a graph for the map
edges = [
     ("Arad", "Zerind", {"weight": 75}),
    ("Arad", "Timisoara", {"weight": 118}),
    ("Arad", "Sibiu", {"weight": 140}),
    ("Zerind", "Oradea", {"weight": 71}),
    ("Timisoara", "Lugoj", {"weight": 111}),
    ("Sibiu", "Oradea", {"weight": 151}),
    ("Sibiu", "Fagaras", {"weight": 99}),
    ("Lugoj", "Mehadia", {"weight": 70}),
    ("Fagaras", "Bucharest", {"weight": 211}),
    ("Mehadia", "Dobreta", {"weight": 75}),
    ("Dobreta", "Craiova", {"weight": 120}),
    ("Craiova", "Rimnicu Vilcea", {"weight": 146}),
    ("Craiova", "Pitesti", {"weight": 138}),
    ("Rimnicu Vilcea", "Sibiu", {"weight": 80}),
    ("Rimnicu Vilcea", "Pitesti", {"weight": 97}),
    ("Bucharest", "Pitesti", {"weight": 101}),
    ("Bucharest", "Giurgiu", {"weight": 90}),
    ("Bucharest", "Urziceni", {"weight": 85}),
    ("Urziceni", "Hirsova", {"weight": 98}),
    ("Hirsova", "Eforie", {"weight": 86}),
    ("Urziceni", "Vaslui", {"weight": 142}),
    ("Vaslui", "Iasi", {"weight": 92}),
    ("Iasi", "Neamt", {"weight": 87}),
    ("Dobreta", "Czirceni", {"weight": 120}),
    ("Zerind", "Seamt", {"weight": 90}),
    ("Seamt", "Neamt", {"weight": 45}),
    ("Oradea", "Czirceni", {"weight": 80}),
    ("Czirceni", "Vaslui", {"weight": 60}),
    ("Vaslui", "Eforie", {"weight": 75}),
    ("Eforie", "Hirsova", {"weight": 40}),
    ("Timisoara", "Dobreta", {"weight": 75}),
    ("Hirsova", "Giurgiu", {"weight": 105}),
    ("Giurgiu", "Bucharest", {"weight": 60}),
    ("Iasi", "Sibiu", {"weight": 140}),
    ("Sibiu", "Eforie", {"weight": 180}),
    # Adding more cities and links
    ("Seamt", "Targu Mures", {"weight": 75}),
    ("Targu Mures", "Cluj", {"weight": 110}),
    ("Cluj", "Turda", {"weight": 45}),
    ("Turda", "Alba Iulia", {"weight": 60}),
]

G = nx.Graph()
pos_dict = {
    "Arad": (0, 0), "Zerind": (1, 1), "Timisoara": (2, 2), "Sibiu": (3, 3), "Fagaras": (4, 4),
    "Bucharest": (5, 5), "Craiova": (6, 6), "Dobreta": (7, 7), "Eforie": (8, 8), "Giurgiu": (9, 9),
    "Iasi": (10, 10), "Lugoj": (11, 11), "Mehadia": (12, 12), "Oradea": (13, 13), "Pitesti": (14, 14),
    "Rimnicu Vilcea": (15, 15), "Czirceni": (16, 16), "Vaslui": (17, 17), "Urziceni": (18, 18),
    "Hirsova": (19, 19), "Eforie": (20, 20), "Seamt": (21, 21), "Neamt": (22, 22),"Targu Mures": (23, 23),"Cluj": (24, 24),
    "Turda": (25, 25),"Alba Iulia": (26, 26),
}

G.add_nodes_from(pos_dict.keys())
G.add_edges_from(edges)

# Improved initial visualization using Kamada-Kawai layout with increased scale
plt.figure(figsize=(12, 14))
initial_pos = nx.kamada_kawai_layout(G, scale=2.0)
nx.draw(G, initial_pos, with_labels=True, node_size=700, font_size=8, font_color="black",
        font_weight="bold", edge_color="gray", width=1.5)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, initial_pos, edge_labels=edge_labels, font_color='red')
plt.show()

# Taking user input for start and goal states
start_name = input("Enter the name of the start location: ").lower()
goal_name = input("Enter the name of the goal location: ").lower()

# Finding coordinates based on names
start_node = next((node for node, _coords in pos_dict.items() if node.lower() == start_name), None)
goal_node = next((node for node, _coords in pos_dict.items() if node.lower() == goal_name), None)

if start_node is not None and goal_node is not None:
    if start_node.lower() == goal_node.lower():
        print("Start and goal nodes are the same. The path is trivial.")
    else:
        # Running A* algorithm
        path = a_star(G, start_node, goal_node, pos_dict)

        if isinstance(path, list):
            # Visualizing the path
            visualize_path(G, initial_pos, path)

            # Calculating total distance
            total_distance = sum(G[path[i]][path[i + 1]]["weight"] for i in range(len(path) - 1))
            print(f"Total Distance: {total_distance} km")
        else:
            print(path)
else:
    print("Invalid start or goal location names.")