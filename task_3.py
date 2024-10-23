import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from collections import defaultdict
import numpy as np

def create_weighted_transport_network():
    G = nx.Graph()
    
    # Додавання вершин (станцій)
    stations = ["Центр", "Парк", "Університет", "Ринок", "Вокзал", 
                "Аеропорт", "Стадіон", "Лікарня", "Торговий центр", "Бібліотека"]
    G.add_nodes_from(stations)
    
    # Додавання ребер з вагами (відстань у кілометрах)
    connections = [
        ("Центр", "Парк", 2), 
        ("Центр", "Університет", 3),
        ("Центр", "Ринок", 1),
        ("Парк", "Стадіон", 2),
        ("Університет", "Лікарня", 4),
        ("Ринок", "Вокзал", 3),
        ("Вокзал", "Аеропорт", 8),
        ("Парк", "Бібліотека", 2),
        ("Ринок", "Торговий центр", 1),
        ("Торговий центр", "Університет", 3)
    ]
    G.add_weighted_edges_from(connections)
    return G

def dijkstra(graph, start):
    distances = {node: float('infinity') for node in graph.nodes()}
    distances[start] = 0
    predecessors = {node: None for node in graph.nodes()}
    unvisited = list(graph.nodes())
    
    while unvisited:
        current = min(unvisited, key=lambda node: distances[node])
        
        if distances[current] == float('infinity'):
            break
            
        unvisited.remove(current)
        
        for neighbor in graph.neighbors(current):
            if neighbor in unvisited:
                distance = distances[current] + graph[current][neighbor]['weight']
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current
    
    return distances, predecessors

def find_path(predecessors, start, end):
    path = []
    current = end
    
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    return list(reversed(path))

def visualize_shortest_paths(G, paths, start_node):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    
    # Малюємо всі вузли та ребра
    nx.draw_networkx_nodes(G, pos, node_color='lightgray', 
                          node_size=2000, alpha=0.7)
    nx.draw_networkx_edges(G, pos, alpha=0.2)
    
    # Виділяємо всі найкоротші шляхи різними кольорами
    colors = plt.cm.rainbow(np.linspace(0, 1, len(paths)))
    for (end_node, path), color in zip(paths.items(), colors):
        if path:
            path_edges = list(zip(path[:-1], path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                                 edge_color=[color], width=2, alpha=0.7)
    
    # Додаємо підписи вузлів
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    # Додаємо ваги ребер
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    
    plt.title(f"Найкоротші шляхи від вершини {start_node}", fontsize=16, pad=20)
    plt.axis('off')
    
    filename = f"shortest_paths_from_{start_node}.png"
    plt.savefig(filename, bbox_inches='tight')
    print(f"\nГрафік збережено як: {filename}")
    plt.close()
    
    return filename

def analyze_shortest_paths(G):
    print("\nАНАЛІЗ НАЙКОРОТШИХ ШЛЯХІВ:")
    print("-" * 60)
    
    all_paths = {}
    all_distances = {}
    
    # Знаходимо найкоротші шляхи від кожної вершини
    for start in G.nodes():
        distances, predecessors = dijkstra(G, start)
        all_distances[start] = distances
        
        paths = {}
        for end in G.nodes():
            if end != start:
                path = find_path(predecessors, start, end)
                paths[end] = path
                print(f"\nНайкоротший шлях від {start} до {end}:")
                print(f"Шлях: {' -> '.join(path)}")
                print(f"Відстань: {distances[end]:.1f} км")
        
        all_paths[start] = paths
        print("\n" + "-" * 60)
    
    # Обчислюємо статистику
    print("\nСТАТИСТИКА НАЙКОРОТШИХ ШЛЯХІВ:")
    print("-" * 40)
    
    # Середня довжина найкоротшого шляху
    all_distances_list = [dist for distances in all_distances.values() 
                         for node, dist in distances.items() if node != list(distances.keys())[0]]
    avg_distance = sum(all_distances_list) / len(all_distances_list)
    print(f"\nСередня довжина найкоротшого шляху: {avg_distance:.2f} км")
    
    return all_paths, all_distances

def main():
    # Створюємо зважений граф
    G = create_weighted_transport_network()
    
    # Аналізуємо найкоротші шляхи
    all_paths, all_distances = analyze_shortest_paths(G)
    
    # Візуалізуємо найкоротші шляхи для кожної початкової вершини
    filenames = []
    for start_node in G.nodes():
        filename = visualize_shortest_paths(G, all_paths[start_node], start_node)
        filenames.append(filename)
    
    # Запитуємо користувача про перегляд графіків
    view_plot = input("\nБажаєте переглянути згенеровані графіки? (так/ні): ").lower().strip()
    if view_plot == 'так':
        try:
            for filename in filenames:
                os.system(f"xdg-open {filename}")
        except Exception as e:
            print(f"Помилка при відкритті файлів: {e}")
            print("Спробуйте відкрити файли вручну з поточної директорії:")
            for filename in filenames:
                print(f"- {filename}")

if __name__ == "__main__":
    main()