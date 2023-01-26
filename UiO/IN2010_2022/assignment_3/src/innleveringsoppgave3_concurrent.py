from collections import defaultdict, deque
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from functools import cached_property, partial
from itertools import permutations
from queue import PriorityQueue

IDS_TO_CHECK = (
    ("nm2255973", "nm0000460"),
    ("nm0424060", "nm0000243"),
    ("nm4689420", "nm0000365"),
    ("nm0000288", "nm0001401"),
    ("nm0031483", "nm0931324"),
)


@dataclass
class Base:
    id: str = field(hash=True)
    name: str = field(hash=False)


@dataclass(unsafe_hash=True)
class Vertex(Base):
    edges: list["Edge", ...] = field(default_factory=list, hash=False)

    @cached_property
    def neighbour_to_edge(self) -> dict["Vertex", "Edge"]:
        return {
            edge.vertex_b if edge.vertex_a == self else edge.vertex_a: edge
            for edge in self.edges
        }
        # result = {}
        # for edge in self.edges:
        #     key = edge.vertex_b if edge.vertex_a == self else edge.vertex_a
        #     result[key] = edge
        # return result


@dataclass
class Edge(Base):
    rating: float

    vertex_a: Vertex
    vertex_b: Vertex

    @cached_property
    def priority(self) -> float:
        return 10.0 - self.rating


@dataclass(order=True)
class VertexDistance:
    vertex: Vertex = field(compare=False)
    priority: float


@dataclass
class Graph:
    vertices: dict[str, Vertex] = field(default_factory=dict)
    edges: list[Edge, ...] = field(default_factory=list)

    @cached_property
    def n_vertices(self) -> int:
        return len(self.vertices)

    @cached_property
    def n_edges(self) -> int:
        return len(self.edges)

    def graph_metadta(self) -> str:
        # Exercise 1-2
        return f"Oppgave 1\nNodes: {self.n_vertices}\nEdges: {self.n_edges}\n"

    def component_size_to_count(self):
        result = {}
        vertices = set(self.vertices.values())

        while vertices:
            current = vertices.pop()
            parents = self.bfs_shortest_paths_from(current.id)
            component_size = len(parents)

            vertices.difference_update(set(parents))

            if component_size in result:
                result[component_size] += 1
            else:
                result[component_size] = 1

        for size, count in result.items():
            print(f"There are {count} components of size {size}")

    def bfs_shortest_paths_from(self, start_id: str):
        start = self.vertices[start_id]

        parents = {start: None}
        queue = deque([start])

        while queue:
            current = deque.popleft(queue)
            for vertex, edge in current.neighbour_to_edge.items():
                if vertex not in parents:
                    parents[vertex] = (current, edge)
                    queue.append(vertex)
        return parents

    def bfs_shortest_path_between(self, start_id: str, destination_id: str):
        parents = self.bfs_shortest_paths_from(start_id)

        start = self.vertices[start_id]
        destination = self.vertices[destination_id]

        if destination not in parents:
            return f"{start.name} has no path to {destination.name}"

        path = []
        current = destination
        edge = None
        while current:
            path.append((current, edge))
            try:
                current, edge = parents[current]
            except TypeError:
                break

        result = []
        for start_vertex, traversing_edge in path[::-1]:
            if not traversing_edge:
                result.append(f"{start_vertex.name}\n")
            else:
                result.append(
                    f"{start_vertex.name} ===[ {traversing_edge.name} ({traversing_edge.rating}) ] ===> "
                )

        return "\n".join(result)

    def dijkstras_shortest_path(self, start_id: str):
        start = self.vertices[start_id]

        parents = {start: None}
        visited = set()
        dist = defaultdict(partial(float, "inf"))
        dist[start] = 0

        queue = PriorityQueue()
        queue.put(VertexDistance(vertex=start, priority=0))

        while not queue.empty() and len(parents) < self.n_vertices:
            current = queue.get().vertex
            if current not in visited:
                visited.add(current)
                for vertex, edge in current.neighbour_to_edge.items():
                    c = dist[current] + edge.priority
                    if c < dist[vertex]:
                        dist[vertex] = c
                        parents[vertex] = (current, edge)
                        queue.put(VertexDistance(vertex=vertex, priority=c))
        return parents, dist

    def dijkstras_shortest_between(self, start_id: str, destination_id: str):
        parents, dist = self.dijkstras_shortest_path(start_id)

        start = self.vertices[start_id]
        destination = self.vertices[destination_id]

        if destination not in parents:
            return f"{start.name} has no path to {destination.name}"

        path = []

        current = destination
        edge = None
        while current:
            path.append((current, edge))
            try:
                current, edge = parents[current]
            except TypeError:
                break

        result = []
        for start_vertex, traversing_edge in path[::-1]:
            if not traversing_edge:
                result.append(start_vertex.name)
            else:
                result.append(
                    f"{start_vertex.name} ===[ {traversing_edge.name} ({traversing_edge.rating}) ] ===> "
                )

        result.append(f"Total weight: {dist[destination]}\n")

        return "\n".join(result)


my_movie_graph = Graph()
movie_participants = defaultdict(list)

with open("data/actors.tsv", "r") as in_actors:
    for line in in_actors.readlines():
        row = line.split("\t")
        actor_id = row[0]
        my_movie_graph.vertices[actor_id] = Vertex(id=actor_id, name=row[1])
        for movie_id in row[2:]:
            movie_participants[movie_id].append(actor_id)

with open("data/movies.tsv", "r") as in_movies:
    for line in in_movies.readlines():
        movie_id, title, rating, _votes = line.strip().split("\t")
        for va, vb in permutations(movie_participants[movie_id], 2):
            a, b = my_movie_graph.vertices[va], my_movie_graph.vertices[vb]
            edge = Edge(movie_id, title, float(rating), a, b)
            a.edges.append(edge)
            b.edges.append(edge)

            my_movie_graph.edges.append(edge)

results = defaultdict(list)
with ProcessPoolExecutor() as executor:
    # Exercise 1-2 ===============================================
    results[1].append(executor.submit(my_movie_graph.graph_metadta))

    """
    Nodes: 119205
    Edges: 7444630
    """

    # Exercise 2 =================================================
    for id_1, id_2 in IDS_TO_CHECK:
        results[2].append(
            executor.submit(my_movie_graph.bfs_shortest_path_between, id_1, id_2)
        )

    """
    Donald Glover ===[ Lennon or McCartney (5.4) ] ===> 
    Robert De Niro ===[ The Mission (7.4) ] ===> 
    Jeremy Irons

    Scarlett Johansson ===[ North (4.5) ] ===> 
    George Cheung ===[ Ricochet (6.1) ] ===> 
    Denzel Washington

    Carrie Coon ===[ Avengers: Infinity War (8.4) ] ===> 
    Robert Downey Jr. ===[ Avengers: Age of Ultron (7.3) ] ===> 
    Julie Delpy

    Christian Bale ===[ Empire of the Sun (7.7) ] ===> 
    Leslie Phillips ===[ Lara Croft: Tomb Raider (5.7) ] ===> 
    Angelina Jolie

    Atle Antonsen ===[ The Trip (6.9) ] ===> 
    Noomi Rapace ===[ Alien: Covenant (6.4) ] ===> 
    Guy Pearce ===[ The Road (7.2) ] ===> 
    Michael K. Williams
    """

    # Exercise 3 =================================================
    for id_1, id_2 in IDS_TO_CHECK:
        results[3].append(
            executor.submit(my_movie_graph.dijkstras_shortest_between, id_1, id_2)
        )

    """
    Donald Glover ===[ The Martian (8.0) ] ===> 
    Enzo Cilenti ===[ The Man Who Knew Infinity (7.2) ] ===> 
    Jeremy Irons
    Total weight: 4.8

    Scarlett Johansson ===[ Avengers: Endgame (8.4) ] ===> 
    Josh Brolin ===[ American Gangster (7.8) ] ===> 
    Denzel Washington
    Total weight: 3.8

    Carrie Coon ===[ Avengers: Infinity War (8.4) ] ===> 
    Robert Downey Jr. ===[ Avengers: Age of Ultron (7.3) ] ===> 
    Julie Delpy
    Total weight: 4.3

    Christian Bale ===[ Batman Begins (8.2) ] ===> 
    Liam Neeson ===[ For the Love of Spock (7.6) ] ===> 
    Angelina Jolie
    Total weight: 4.200000000000001

    Atle Antonsen ===[ The Trip (6.9) ] ===> 
    Aksel Hennie ===[ The Martian (8.0) ] ===> 
    Chiwetel Ejiofor ===[ 12 Years a Slave (8.1) ] ===> 
    Michael K. Williams
    Total weight: 7.0
    """

    # Exercise 4 =================================================
    results[4].append(executor.submit(my_movie_graph.component_size_to_count))
    # my_movie_graph.component_size_to_count()
    """
    There are 47971 components of size 1
    There are 1 components of size 70904
    There are 19 components of size 3
    There are 7 components of size 4
    There are 104 components of size 2
    There are 1 components of size 11
    There are 1 components of size 10
    There are 2 components of size 5
    There are 1 components of size 6
    """

for exercise, answers in results.items():
    print(f"Exercise {exercise}")
    for answer in answers:
        print(answers)
    print("=" * 50)
