import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Використовуємо бекенд Agg
import matplotlib.pyplot as plt
import os

def create_transport_network():
    # Створення графа
    G = nx.Graph()

    # Додавання вершин (станцій)
    stations = ["Центр", "Парк", "Університет", "Ринок", "Вокзал", 
                "Аеропорт", "Стадіон", "Лікарня", "Торговий центр", "Бібліотека"]
    G.add_nodes_from(stations)

    # Додавання ребер (з'єднань між станціями) з вагами (відстань у кілометрах)
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
    
    # Додаємо ребра з вагами
    G.add_weighted_edges_from(connections)
    
    return G

def analyze_network(G):
    print("\nАНАЛІЗ ХАРАКТЕРИСТИК МЕРЕЖІ:")
    print("-" * 40)
    
    # Базові характеристики
    print(f"1. Кількість вершин: {G.number_of_nodes()}")
    print(f"2. Кількість ребер: {G.number_of_edges()}")
    
    # Аналіз ступенів вершин
    print("\n3. Ступені вершин:")
    for node, degree in G.degree():
        print(f"   {node}: {degree} з'єднань")
    
    # Середній ступінь
    avg_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()
    print(f"\n4. Середній ступінь вершин: {avg_degree:.2f}")
    
    # Щільність графа
    density = nx.density(G)
    print(f"5. Щільність графа: {density:.3f}")
    
    # Діаметр та середня довжина шляху
    print(f"6. Діаметр мережі: {nx.diameter(G)}")
    avg_path_length = nx.average_shortest_path_length(G)
    print(f"7. Середня довжина шляху: {avg_path_length:.2f}")
    
    # Коефіцієнт кластеризації
    clustering_coef = nx.average_clustering(G)
    print(f"8. Середній коефіцієнт кластеризації: {clustering_coef:.3f}")
    
    # Центральність вершин
    print("\n9. Центральність вершин за ступенем:")
    degree_centrality = nx.degree_centrality(G)
    for node, centrality in sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True):
        print(f"   {node}: {centrality:.3f}")

def visualize_network(G, title):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    
    # Малюємо вузли
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=2000, alpha=0.7)
    
    # Малюємо ребра
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    
    # Додаємо підписи вузлів
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    # Додаємо ваги ребер
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    
    plt.title(title, fontsize=16, pad=20)
    plt.axis('off')
    
    # Зберігаємо графік
    filename = f"{title.replace(' ', '_')}.png"
    plt.savefig(filename, bbox_inches='tight')
    print(f"\nГрафік збережено як: {filename}")
    plt.close()

def main():
    # Створюємо мережу
    G = create_transport_network()
    
    # Аналізуємо мережу
    analyze_network(G)
    
    # Візуалізуємо мережу
    visualize_network(G, "Транспортна мережа міста")
    
    # Функція для відображення зображень
    def show_image(filename):
        os.system(f"xdg-open {filename}")
    
    # Запитуємо користувача про перегляд графіка
    view_plot = input("\nБажаєте переглянути згенерований графік? (так/ні): ").lower().strip()
    if view_plot == 'так':
        show_image("Транспортна_мережа_міста.png")

if __name__ == "__main__":
    main()