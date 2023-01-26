# IN2010: Assignment 3
By Can Hicabi Tartanoglu

I implemented the graph as the first suggestion in the assignment: The vertices are the actors, and the edges are the movies.

You can run the code, `innleveringsoppgave3.py`, to print out the solution to all exercises to the terminal. You must place `actors.tsv` and `movie.tsv` in directory `data`. `data` must be in the same directory as `innleveringsoppgave3.py`.

Please understand that I usually work on my desktop. This time, I had to do assignment 3 while traveling for a marathon in Turkey. This forced me to use a laptop with 4 cores, and 8 Gb of RAM; happy days! I think it went fine.

## Runtime complexity

### Exercise 1b
Here I used Python's `len` function.

Time Used: 0.000031295 seconds

### Exercise 2
I used bredth-first algorithm, to determine the shortest path from start to destination, which is known to be O(|V| + |E|). We iterate over all edges of every vertex, but only once (`parents` stores vertices that have been visited).

Time Used: 48.304091173 seconds

### Exercise 3
I used Dijkstra's algorithm to determine the shortest path using `10 - movie.rating` as the weights for the edges. I used the implementation of Dijkstra from the lecture, no deacrease priority; to my knowledge, it is still O((|V| +|E|) log(|V|)).

Time Used: 82.653031319 seconds

### Exercise 4
Using `parents` from BFS, in exercise 1, to determine the size of each component. I am a little alarmed by how many actors have no movies; components with a size of 1. Could be that we live in a tough world, my MDB is quite incomplete, or that I made a mistake. Probably a mix of all three reasons.

Time Used: 5.21667333 seconds
