from collections import deque
from copy import copy
from dataclasses import dataclass, field
from typing import TypeVar

# Exercise 1 ==============================


@dataclass
class _Node:
    id: str = field(hash=True)


Vertex = TypeVar("Vertex", bound=_Node)


@dataclass(unsafe_hash=True)
class Movie(_Node):
    title: str
    rating: float

    actors: dict[str, "Actor"] = field(default_factory=dict, hash=False)


@dataclass(unsafe_hash=True)
class Actor(_Node):
    name: str

    movies: dict[str, Movie] = field(default_factory=dict, hash=False)

    @property
    def neighboring_actors(self) -> set["Actor"]:
        result = set()
        for movie in self.movies.values():
            result = result.union(movie.actors.values())
        return result

    def connecting_movie(self, actor: "Actor") -> Movie | None:
        for movie in self.movies:
            if actor in movie.actors.values():
                return movie


@dataclass
class Graph:
    movies: dict[str, Movie] = field(default_factory=dict)
    actors: dict[str, Actor] = field(default_factory=dict)

    @property
    def n_edges(self) -> int:
        return sum(len(movie.actors) for movie in self.movies.values())

    @property
    def n_vertices(self) -> int:
        return len(movies) + len(self.actors)

    @property
    def graph_metadta(self) -> str:
        # Exercise 1-2
        return f"Oppgave 1\nNodes: {self.n_vertices}\nEdges: {self.n_edges}"

    # def get_movie(self, movie_id: str) -> Movie:
    #     return self.movies[movie_id]

    # def get_actor(self, actor_id: str) -> Actor:
    #     return self.actors[actor_id]

    def cans_algorithm(self, start_id: str, destination_id: str) -> str:
        # Exercise 2

        start = self.actors[start_id]
        destination = self.actors[destination_id]

        pathing = []
        visited = {start}
        queue = deque([start])
        while queue:
            current: Actor = queue.popleft()
            pathing.append(current)
            for neighboring_actor in current.neighboring_actors:
                if neighboring_actor == destination:
                    pathing.append(destination)
                    break
                if neighboring_actor not in visited:
                    visited.add(neighboring_actor)
                    queue.append(neighboring_actor)

        shortest_path = []
        i = 0
        while len(pathing) > i:
            current_actor_in_path = pathing[i]
            shortest_path.append(current_actor_in_path)

            try:
                # I reverse it to stop at the actor closest to the destination
                for k, actor_ahead_in_path in enumerate(pathing[i + 1 :: -1]):
                    if actor_ahead_in_path in pathing:
                        pathing = pathing[len(pathing) - k :]
                        i = 0
                        break
            except IndexError:
                break

            i += 1

        print(shortest_path[0].name)
        for current_actor_in_path, actor_ahead_in_path in zip(
            shortest_path, shortest_path[1:]
        ):
            connecting_movie = current_actor_in_path.connecting_movie(
                actor_ahead_in_path
            )
            print(
                f"===[ {connecting_movie.title} ({connecting_movie.rating}) ] "
                f"===> {actor_ahead_in_path.name}"
            )

        if len(shortest_path) == 1:
            raise ValueError("Pathing is too short!")


my_movie_graph = Graph()

with open("data/movies.tsv", "r") as in_movies:
    for line in in_movies.readlines():
        movie_id, title, rating, _votes = line.strip().split("\t")
        my_movie_graph.movies[movie_id] = Movie(id=movie_id, title=title, rating=rating)

with open("data/actors.tsv", "r") as in_actors:
    for line in in_actors.readlines():
        row = line.strip().split("\t")

        actor_id = row[0]
        actor = Actor(id=actor_id, name=row[1])
        movies = {}
        for movie_id in row[2:]:
            if movie_id not in my_movie_graph.movies:
                continue

            movie = my_movie_graph.movies[movie_id]

            actor.movies[movie_id] = movie
            movie.actors[actor_id] = actor

            movies[movie_id] = movie

        actor.movies = movies
        my_movie_graph.actors[actor_id] = actor

# Exercise 1-2 ==============================
print(my_movie_graph.graph_metadta)

# Exercise 2 ==============================

my_movie_graph.cans_algorithm("nm2255973", "nm0000460")
