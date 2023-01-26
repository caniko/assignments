    def cans_shortest_path(self, start_id: str, destination_id: str) -> None:
        # Exercise 2
        start = self.vertices[start_id]
        destination = self.vertices[destination_id]

        print(f"\nShortest path from {start_id} to {destination_id}")
        print(start.name)

        queue_edges = {}
        queue = Queue()
        queue.put(start)

        visited = set()

        current: Union[Vertex, None] = None
        while not queue.empty():
            if current:
                next_vertex = queue.get()
                traversed_edge = queue_edges.pop(next_vertex)
                _path_traversal_announcer(
                    traversed_edge.name, traversed_edge.rating, next_vertex.name
                )

                current = next_vertex
            else:
                current = queue.get()

            try:
                edge = current.neighbour_to_edge[destination]
                return _path_traversal_announcer(
                    edge.name, edge.rating, destination.name
                )
            except KeyError:
                pass

            for vertex, edge in current.neighbour_to_edge.items():
                if vertex not in visited:
                    visited.add(vertex)
                    queue.put(vertex)
                    queue_edges[vertex] = edge