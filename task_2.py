import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from collections import deque

def create_transport_network():
    G = nx.Graph()
    
    # Додавання вершин (станцій)
    stations = ["Центр", "Парк", "Університет", "Ринок", "Вокзал", 
                "Аеропорт", "Стадіон", "Лікарня", "Торговий центр", "Бібліотека"]
    G.add_nodes_from(stations)
    
    # Додавання ребер з вагами
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

def dfs_path(graph, start, end, path=None, visited=None):
    if path is None:
        path = []
        visited = set()
    
    path = path + [start]
    visited.add(start)
    
    if start == end:
        return path, visited
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            new_path, new_visited = dfs_path(graph, neighbor, end, path, visited)
            if new_path:
                return new_path, new_visited
    
    return None, visited

def bfs_path(graph, start, end):
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        vertex, path = queue.popleft()
        for neighbor in graph[vertex]:
            if neighbor == end:
                return path + [neighbor], visited
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None, visited

def visualize_paths(G, title, paths=None, visited_nodes=None):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    
    # Малюємо всі вузли сірим кольором
    nx.draw_networkx_nodes(G, pos, node_color='lightgray', 
                          node_size=2000, alpha=0.7)
    
    # Малюємо відвідані вузли іншим кольором
    if visited_nodes:
        nx.draw_networkx_nodes(G, pos, 
                             nodelist=list(visited_nodes),
                             node_color='lightblue',
                             node_size=2000, alpha=0.7)
    
    # Малюємо всі ребра
    nx.draw_networkx_edges(G, pos, alpha=0.2)
    
    # Малюємо шляхи різними кольорами
    if paths:
        colors = ['r', 'g']
        for path, color in zip(paths, colors):
            if path:
                path_edges = list(zip(path[:-1], path[1:]))
                nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                                     edge_color=color, width=2, alpha=1)
    
    # Додаємо підписи вузлів
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    # Додаємо ваги ребер
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    
    plt.title(title, fontsize=16, pad=20)
    plt.axis('off')
    
    # Змінюємо спосіб формування імені файлу
    filename = "path_comparison.png"  
    plt.savefig(filename, bbox_inches='tight')
    print(f"\nГрафік збережено як: {filename}")
    plt.close()
    
    return filename

def analyze_paths(start, end, dfs_result, bfs_result):
    print("\nАНАЛІЗ ЗНАЙДЕНИХ ШЛЯХІВ:")
    print("-" * 40)
    
    dfs_path, dfs_visited = dfs_result
    bfs_path, bfs_visited = bfs_result
    
    # Аналіз DFS
    print(f"\n1. DFS (Пошук у глибину):")
    print(f"   Шлях: {' -> '.join(dfs_path)}")
    print(f"   Довжина шляху: {len(dfs_path) - 1} переходів")
    print(f"   Кількість відвіданих вершин: {len(dfs_visited)}")
    
    # Аналіз BFS
    print(f"\n2. BFS (Пошук у ширину):")
    print(f"   Шлях: {' -> '.join(bfs_path)}")
    print(f"   Довжина шляху: {len(bfs_path) - 1} переходів")
    print(f"   Кількість відвіданих вершин: {len(bfs_visited)}")
    
    # Порівняння алгоритмів
    print("\n3. Порівняння алгоритмів:")
    print("   3.1. Довжина шляху:")
    if len(dfs_path) == len(bfs_path):
        print("   - Обидва алгоритми знайшли шляхи однакової довжини")
    else:
        print(f"   - DFS: {len(dfs_path) - 1} переходів")
        print(f"   - BFS: {len(bfs_path) - 1} переходів")
        print(f"   - Різниця: {abs(len(dfs_path) - len(bfs_path))} переходів")
    
    print("\n   3.2. Ефективність пошуку:")
    print(f"   - DFS відвідав {len(dfs_visited)} вершин")
    print(f"   - BFS відвідав {len(bfs_visited)} вершин")
    
    print("\n4. Пояснення результатів:")
    print("   4.1. Характеристики DFS:")
    print("   - Заглиблюється в одному напрямку до кінця")
    print("   - Може знайти довший шлях, якщо перший знайдений шлях не є найкоротшим")
    print("   - Ефективний для глибоких графів")
    
    print("\n   4.2. Характеристики BFS:")
    print("   - Досліджує всі сусідні вершини перед переходом далі")
    print("   - Гарантовано знаходить найкоротший шлях у невиваженому графі")
    print("   - Ефективний для широких графів")

def main():
    # Створюємо мережу
    G = create_transport_network()
    
    # Вибираємо початкову та кінцеву точки
    start = "Центр"
    end = "Аеропорт"
    
    # Знаходимо шляхи
    dfs_result = dfs_path(G, start, end)
    bfs_result = bfs_path(G, start, end)
    
    # Аналізуємо результати
    analyze_paths(start, end, dfs_result, bfs_result)
    
    # Візуалізуємо результати і отримуємо ім'я файлу
    filename = visualize_paths(G, "Порівняння шляхів DFS (червоний) і BFS (зелений)", 
                             paths=[dfs_result[0], bfs_result[0]],
                             visited_nodes=dfs_result[1].union(bfs_result[1]))
    
    # Запитуємо користувача про перегляд графіка
    view_plot = input("\nБажаєте переглянути згенерований графік? (так/ні): ").lower().strip()
    if view_plot == 'так':
        try:
            os.system(f"xdg-open {filename}")
        except Exception as e:
            print(f"Помилка при відкритті файлу: {e}")
            print(f"Спробуйте відкрити файл '{filename}' вручну з поточної директорії")

if __name__ == "__main__":
    main()