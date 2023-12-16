from flask import Flask, render_template, request
import sys

app = Flask(__name__)

# Sample graph represented as an adjacency matrix
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

def dijkstra(graph, start, end):
    # Dijkstra's algorithm implementation
    shortest_paths = {node: float('infinity') for node in graph}
    shortest_paths[start] = 0
    visited_nodes = set()

    while True:
        min_node = None
        for node in shortest_paths:
            if node not in visited_nodes:
                if min_node is None or shortest_paths[node] < shortest_paths[min_node]:
                    min_node = node

        if min_node is None or shortest_paths[min_node] == float('infinity'):
            break

        for neighbor, weight in graph[min_node].items():
            potential_path = shortest_paths[min_node] + weight
            if potential_path < shortest_paths[neighbor]:
                shortest_paths[neighbor] = potential_path

        visited_nodes.add(min_node)

    return shortest_paths[end], min(shortest_paths, key=shortest_paths.get)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    user_defined_point = request.form['user_defined_point']
    nearest_node = request.form['nearest_node']

    shortest_distance, nearest_node = dijkstra(graph, user_defined_point, nearest_node)

    if shortest_distance == float('infinity'):
        result = "No path found from {} to any of the destinations".format(user_defined_point)
    else:
        no_of_vehicles = int(request.form['no_of_vehicles'])
        if shortest_distance < 1500:
            result = "Green Signal. Time: {:.2f} seconds".format((1500 * no_of_vehicles) / 1000)
        else:
            result = "No nearest ambulance"

    return render_template('result.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
