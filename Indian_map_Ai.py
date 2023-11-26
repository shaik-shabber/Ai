import networkx as nx
import matplotlib.pyplot as plt
import heapq
import math

def create_indian_map():
    # Creating a graph for the map
    edges = [
        ("mumbai", "pune", {"weight": 210}),
        ("mumbai", "nashik", {"weight": 250}),
        ("pune", "nashik", {"weight": 230}),
        ("pune", "hyderabad", {"weight": 500}),
        ("nashik", "indore", {"weight": 450}),
        ("indore", "bhopal", {"weight": 200}),
        ("hyderabad", "bangalore", {"weight": 600}),
        ("hyderabad", "chennai", {"weight": 550}),
        ("bangalore", "chennai", {"weight": 350}),
        ("chennai", "madurai", {"weight": 400}),
        ("pune", "goa", {"weight": 350}),
        ("goa", "mangalore", {"weight": 300}),
        ("mangalore", "bangalore", {"weight": 350}),
        ("pune", "mangalore", {"weight": 550}),
        ("mangalore", "kochi", {"weight": 400}),
        ("kochi", "trivandrum", {"weight": 200}),
        ("mumbai", "ahmedabad", {"weight": 550}),
        ("ahmedabad", "jaipur", {"weight": 650}),
        ("jaipur", "delhi", {"weight": 300}),
        ("delhi", "agra", {"weight": 200}),
        ("agra", "lucknow", {"weight": 350}),
        ("lucknow", "kanpur", {"weight": 180}),
        ("kanpur", "varanasi", {"weight": 300}),
        ("varanasi", "allahabad", {"weight": 250}),
        ("lucknow", "bhopal", {"weight": 450}),
        ("bhopal", "nagpur", {"weight": 400}),
        ("nagpur", "hyderabad", {"weight": 500}),
        ("hyderabad", "vijayawada", {"weight": 250}),
        ("vijayawada", "chennai", {"weight": 400}),
        ("chennai", "puducherry", {"weight": 250}),
        ("puducherry", "trichy", {"weight": 200}),
        ("trichy", "madurai", {"weight": 150}),
        ("madurai", "coimbatore", {"weight": 250}),
        ("coimbatore", "kochi", {"weight": 180}),
        ("kochi", "kozhikode", {"weight": 220}),
        ("kozhikode", "mangalore", {"weight": 310}),
        ("mangalore", "hubli", {"weight": 300}),
        # ... (add more edges as needed)
    ]

    G = nx.Graph()
    G.add_edges_from(edges)

    return G

def visualize_indian_map(G):
    plt.figure(figsize=(12, 12))
    pos = nx.kamada_kawai_layout(G, scale=2.0)
    nx.draw(G, pos=pos, with_labels=True, node_size=900, font_size=8, font_color="black",
            font_weight="bold", edge_color="#888888", width=1.5, node_color="#86c7f3", cmap=plt.cm.Blues)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, font_color='#ff0000')
    plt.title("Distance between cities - Initial Layout")
    plt.show()

def euclidean_distance(node, goal_node, pos):
    x1, y1 = pos[node]
    x2, y2 = pos[goal_node]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def cost(node1, node2, G):
    return G[node1][node2]["weight"]

def neighbors(node, G):
    return list(G.neighbors(node))

def a_star(G, start, goal):
    if not G.has_node(start) or not G.has_node(goal):
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
                f_score = tentative_g_score + euclidean_distance(neighbor, goal, nx.kamada_kawai_layout(G, scale=2.0))
                heapq.heappush(open_set, (f_score, neighbor))

    return "No path found"

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def visualize_path(G, path):
    pos = nx.kamada_kawai_layout(G, scale=2.0)
    path_edges = list(zip(path, path[1:]))

    edge_labels = {(edge[0], edge[1]): G[edge[0]][edge[1]]['weight'] for edge in path_edges}

    plt.figure(figsize=(10, 12))
    nx.draw(G, pos, with_labels=True, node_size=900, font_size=8,
            font_color="black", font_weight="bold", edge_color="#888888", width=1.5)

    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="#ff69b4", width=2)

    nx.draw_networkx_nodes(G, pos, nodelist=[path[0]], node_color="#00ff00", node_size=900)
    nx.draw_networkx_nodes(G, pos, nodelist=[path[-1]], node_color="#00ff00", node_size=900)

    intermediate_nodes = set(path) - {path[0], path[-1]}
    nx.draw_networkx_nodes(G, pos, nodelist=intermediate_nodes, node_color="#add8e6", node_size=900)

    nx.draw_networkx_edge_labels(G.subgraph(path_edges), pos, edge_labels=edge_labels, font_color='#ff0000')

    plt.title("Optimal Path")
    plt.show()

def main():
    G = create_indian_map()

    visualize_indian_map(G)

    start_name = input("Enter the name of the start location: ").lower()
    goal_name = input("Enter the name of the goal location: ").lower()

    if G.has_node(start_name) and G.has_node(goal_name):
        if start_name == goal_name:
            print("Start and goal nodes are the same. The path is trivial.")
        else:
            path = a_star(G, start_name, goal_name)

            if isinstance(path, list):
                visualize_path(G, path)

                total_distance = sum(G[path[i]][path[i + 1]]["weight"] for i in range(len(path) - 1))
                print(f"Total Distance: {total_distance} km")
            else:
                print(path)
    else:
        print("Invalid start or goal location names.")

if __name__ == "__main__":
    main()
