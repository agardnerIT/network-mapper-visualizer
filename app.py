import networkx as nx
import matplotlib.pyplot as plt
import yaml

# Function to read YAML file and handle multiple documents
def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return list(yaml.safe_load_all(file))

# Read the YAML file
yaml_data = read_yaml('data.yaml')

# Extract the namespace from the metadata
namespace = yaml_data[0]['metadata']['namespace']

# Create a directed graph
G = nx.DiGraph()

# Process each ClientIntents resource
for item in yaml_data:
    workload_name = item['spec']['workload']['name']
    workload_kind = item['spec']['workload']['kind']

    item_targets = []

    for target in item['spec']['targets']:
        target_name = ""
        try:
            target_name = target['kubernetes']['name']
            print(f"{workload_name} calls {target['kubernetes']['name']}")
            item_targets.append(target_name)
        except:
            pass

    # Add nodes
    G.add_node(workload_name, kind=workload_kind)
    for target_service in item_targets:
        G.add_node(target_service, kind="Service")

        # Add edges
        G.add_edge(workload_name, target_service)

# Draw the graph
pos = nx.spring_layout(G)  # Positions for all nodes
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold", arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(workload_name, target_service): "calls" for workload_name, target_service in G.edges()})

# Get the bounding box of the nodes
x_values, y_values = zip(*pos.values())
x_min, x_max = min(x_values), max(x_values)
y_min, y_max = min(y_values), max(y_values)

# Add a label for the namespace
plt.text(x_min+0.22, y_max, namespace, fontsize=12, fontweight='bold', verticalalignment='bottom', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.5))

# Display the graph
plt.title("ClientIntents Visualization")
plt.show()
