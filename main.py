import pygame
import time
from priority_queue import PriorityQueue
from graph import Graph
from vertex import Vertex
from edge import Edge

#Pygame screen formatting
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra's Algorithm Visualization")

pygame.display.flip()
pygame.event.pump()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

vertex_positions = {
    'A': (280.0, 196.0), 'B': (420.0, 134.0), 'C': (420.0, 306.0), 'D': (280.0, 434.0),
    'E': (540.0, 196.0), 'F': (540.0, 356.0), 'G': (420.0, 476.0), 'H': (660.0, 306.0)
}

#Implements Dijsktra's Algorithm
def dijkstra(graph, start, end):
    previous = {v: None for v in graph.adjacency_list.keys()}
    visited = {v: False for v in graph.adjacency_list.keys()}
    distances = {v: float("inf") for v in graph.adjacency_list.keys()}
    distances[start] = 0
    queue = PriorityQueue()
    queue.add_task(0, start)
    path = []

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        removed_distance, removed = queue.pop_task()

        draw_graph(graph, visited, previous, distances, removed)
        pygame.display.flip()
        time.sleep(0.5)

        visited[removed] = True

        if removed is end:
            temp_path = []
            current = end
            while previous[current]:
                temp_path.append(current)
                current = previous[current]
            temp_path.append(start)

            for i in range(len(temp_path)-1):
                draw_graph(graph, visited, previous, distances, temp_path[i])
                pygame.display.flip()
                time.sleep(0.5)
                start_pos = vertex_positions[temp_path[i].value]
                end_pos = vertex_positions[temp_path[i+1].value]
                pygame.draw.line(screen, RED, start_pos, end_pos, 3)
                pygame.display.flip()
                time.sleep(0.5)
            path = temp_path[::-1]

            print(f"Shortest distance from {start} to {end}: ", distances[end])
            print(f"Shortest path from {start} to {end}: ", [v.value for v in path])
            return path, distances[end]

        for edge in graph.adjacency_list[removed]:
            if visited[edge.vertex]:
                continue
            new_distance = removed_distance + edge.distance
            if new_distance < distances[edge.vertex]:
                distances[edge.vertex] = new_distance
                previous[edge.vertex] = removed
                queue.add_task(new_distance, edge.vertex)

        draw_graph(graph, visited, previous, distances, removed)
        pygame.display.flip()
        time.sleep(0.5)
    return None, None

#Draws graph in the pygame screen
def draw_graph(graph, visited, previous, distances, current_node = None):
    screen.fill(WHITE)

    for vertex, edges in graph.adjacency_list.items():
        for edge in edges:
            start_pos = vertex_positions[vertex.value]
            end_pos = vertex_positions[edge.vertex.value]
            pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)
            midpoint = ((start_pos[0] + end_pos[0]) // 2, (start_pos[1] + end_pos[1]) // 2)
            font = pygame.font.Font(None, 20)
            text = font.render(str(edge.distance), True, BLUE)
            screen.blit(text, midpoint)

    for vertex in graph.adjacency_list.keys():
        pos = vertex_positions[vertex.value]
        color = GREEN if visited[vertex] else BLACK
        if vertex == current_node:
            color = BLUE
        pygame.draw.circle(screen, color, pos, 10)
        font = pygame.font.Font(None, 20)
        text = font.render(vertex.value, True, RED)
        text_rect = text.get_rect(center=(pos[0], pos[1] + 20))
        screen.blit(text, text_rect)

    for vertex, dist in distances.items():
        pos = vertex_positions[vertex.value]
        font = pygame.font.Font(None, 20)
        text = font.render(str(round(dist, 2)), True, BLUE)
        text_rect = text.get_rect(center=(pos[0], pos[1] - 20))
        screen.blit(text, text_rect)

def main():
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dijkstra's Algorithm Visualization")

    vertices = [Vertex("A"), Vertex("B"), Vertex("C"), Vertex("D"), Vertex("E"), Vertex("F"), Vertex("G"), Vertex("H")]
    A, B, C, D, E, F, G, H = vertices
    adj_list = {
        A: [Edge(1.8, B), Edge(1.5, C), Edge(1.4, D)],
        B: [Edge(1.8, A), Edge(1.6, E)],
        C: [Edge(1.5, A), Edge(1.8, E), Edge(2.1, F)],
        D: [Edge(1.4, A), Edge(2.7, F), Edge(2.4, G)],
        E: [Edge(1.6, B), Edge(1.8, C), Edge(1.4, F), Edge(1.6, H)],
        F: [Edge(2.1, C), Edge(2.7, D), Edge(1.4, E), Edge(1.3, G), Edge(1.2, H)],
        G: [Edge(2.4, D), Edge(1.3, F), Edge(1.5, H)],
        H: [Edge(1.6, E), Edge(1.2, F), Edge(1.5, G)],
    }

    my_graph = Graph(adj_list)

    while True:
        starting_vertex, ending_vertex = input("Enter the vertices between which you want to find the shortest path (or type 'exit' to quit): ").split()

        if starting_vertex.lower() == 'exit' or ending_vertex.lower() == 'exit':
            print("Exiting the program.")
            break

        pygame.init()

        vertex_mapping = {
            'A': 0, 'B': 1, 'C': 2, 'D': 3,
            'E': 4, 'F': 5, 'G': 6, 'H': 7
        }
        starting_vertex = starting_vertex.upper()
        ending_vertex = ending_vertex.upper()

        try:
            start = vertices[vertex_mapping[starting_vertex]]
            end = vertices[vertex_mapping[ending_vertex]]
        except KeyError:
            print("Invalid vertices entered. Please try again.")
            continue

        path, distance = dijkstra(my_graph, start=start, end=end)

        choice = input("Do you want to find the shortest path for other vertices? (yes/no): ").lower()
        if choice != 'yes':
            print("Exiting the program.")
            break

        screen.fill(WHITE)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()