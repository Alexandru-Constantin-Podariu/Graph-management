import copy


class TripleDictGraph:
    def __init__(self, n, m):
        self._vertices = n
        self._edges = m
        self._dict_out = {}
        self._dict_in = {}
        self._dict_cost = {}
        for i in range(n):
            self._dict_out[i] = []
            self._dict_in[i] = []

    def parse_x(self):
        return self._dict_out.keys()

    def parse_out(self, x):
        if x not in self._dict_out.keys():
            return False
        return self._dict_out[x]

    def parse_in(self, x):
        if x not in self._dict_in.keys():
            return False
        return self._dict_in[x]

    def parse_cost(self):
        return list(self._dict_cost.keys())

    @property
    def dict_cost(self):
        return self._dict_cost

    @property
    def dict_in(self):
        return self._dict_in

    @property
    def dict_out(self):
        return self._dict_out

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges

    def degree_out(self, x):
        if x not in self._dict_out.keys():
            return False
        return len(self._dict_out[x])

    def check_vertex(self, x):
        if x not in self._dict_out.keys() and x not in self._dict_in.keys():
            return False
        return True

    def degree_in(self, x):

        if x not in self._dict_in.keys():
            return False
        return len(self._dict_in[x])

    def get_cost(self, x, y):
        if (x, y) not in self._dict_cost.keys():
            return False
        return self._dict_cost[(x, y)]

    def add_vertex(self, x):
        if x in self._dict_in.keys() and x in self._dict_out.keys():
            return False
        self._dict_in[x] = []
        self._dict_out[x] = []
        self._vertices += 1
        return True

    def remove_vertex(self, x):
        if x not in self._dict_in.keys() and x not in self._dict_out.keys():
            return False

        for y in self.dict_in[x]:
            self.dict_cost.pop((y, x))
            self._dict_out[y].remove(x)
            self._edges -= 1

        self._dict_in.pop(x)

        for y in self.dict_out[x]:
            self._dict_cost.pop((x, y))
            self._dict_in[y].remove(x)
            self._edges -= 1

        self._dict_out.pop(x)

        return True

    def add_edge(self, x, y, z):
        if x in self._dict_in[y]:
            return False
        elif y in self._dict_out[x]:
            return False
        elif (x, y) in self._dict_cost.keys():
            return False
        self._dict_out[x].append(y)
        self._dict_in[y].append(x)
        self._dict_cost[(x, y)] = z
        self._edges += 1
        return True

    def print_path(self, parent, j):
        path_length = 1
        if parent[j] == -1 and j < self.vertices:
            print(j, end=" ")
            return 0
        predecessors = self.print_path(parent, parent[j])
        path_length = predecessors + path_length
        if j < self.vertices:
            print(j, end=" ")

        return path_length

    def find_shortest_path(self, x, y):
        visited = [False] * self.vertices
        parent = [-1] * self.vertices

        queue = [x]
        visited[x] = True

        while queue:

            # Dequeue a vertex from queue
            s = queue.pop(0)
            for i in self._dict_out[s]:
                if s == y:
                    visited[i] = True
                    parent[i] = s
                    return self.print_path(parent, s)
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True
                    parent[i] = s

    def print_path_reverse(self, parent, j):
        path_length = 1
        if parent[j] == -1 and j < self.vertices:
            print(j, end=" ")
            return 0
        predecessors = self.print_path(parent, parent[j])
        path_length = predecessors + path_length
        if j < self.vertices:
            print(j, end=" ")

        return path_length

    def find_shortest_path_reverse(self, x, y):
        visited = [False] * self.vertices
        parent = [-1] * self.vertices

        queue = [y]
        visited[y] = True

        while queue:

            # Dequeue a vertex from queue
            s = queue.pop(0)
            for i in self._dict_in[s]:
                if s == x:
                    visited[i] = True
                    parent[i] = s
                    return self.print_path(parent, s)
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True
                    parent[i] = s

    # Function that prints the lowest cost path between two vertices
    def path(self, parent, distance, j):
        # If the current vertex is the start vertex
        if parent[j] == -1 and j < self.vertices:
            print(j, end=" ")
            return 0
        self.path(parent, distance, parent[j])
        # Otherwise print vertex
        if j < self.vertices:
            print(j, end=" ")

        return 1

    # Implementation of the Bellman Ford Algorithm
    def Bellman_Ford(self, start, end):
        # Initializing the distance and parent lists
        distance = [float("Inf")] * self.vertices
        distance[start] = 0  # The start vertex has the distance 0
        parent = [-1] * self.vertices

        changed = True

        # While there are still changes made to the distances
        for i in range(1, self.vertices):
            changed = False
            # We go through all the edges and check whether we can improve the cost of the path
            # from a vertex to another using the edge between them
            for key in self.dict_cost:
                if distance[key[0]] != float("Inf") and distance[key[0]] + self.dict_cost[key] < distance[key[1]]:
                    # We modify the distance of the second vertex, change its parent to the first vertex
                    distance[key[1]] = distance[key[0]] + self.dict_cost[key]
                    parent[key[1]] = key[0]
                    # We are still making changes
                    changed = True
            if not changed:
                break

        # Second Traversal for Identifying whether or not we have negative cycles
        for key in self.dict_cost:
            if distance[key[0]] != float("Inf") and distance[key[0]] + self.dict_cost[key] < distance[key[1]]:
                return 0
        # If we did not find a path to the edn vertex
        if distance[end] == float("Inf"):
            return -1
        # Print the path from the start vertex to the evd vertex
        self.path(parent, distance, end)
        # Return the cost of the path
        return distance[end]

    def remove_edge(self, x, y):
        if x not in self._dict_in.keys() or y not in self._dict_in.keys():
            return False
        if x not in self._dict_in[y]:
            return False
        elif y not in self._dict_out[x]:
            return False
        elif (x, y) not in self._dict_cost.keys():
            return False
        self._dict_in[y].remove(x)
        self._dict_out[x].remove(y)
        self._dict_cost.pop((x, y))
        self._edges -= 1
        return True

    def find_edge(self, x, y):
        if x in self._dict_in[y]:
            return self._dict_cost[(x, y)]
        if y in self._dict_out[x]:
            return self._dict_cost[(x, y)]
        return False

    def change_cost(self, x, y, cost):
        if (x, y) not in self._dict_cost.keys():
            return False
        self._dict_cost[(x, y)] = cost
        return True

    def make_copy(self):
        return copy.deepcopy(self)


def write_to_file(graph, file):
    file = open(file, "w")
    line = str(graph.vertices) + ' ' + str(graph.edges) + '\n'
    file.write(line)

    if len(graph.dict_cost) == 0 and len(graph.dict_in) == 0:
        raise ValueError("There is nothing that can be written!")

    for edge in graph.dict_cost.keys():
        new_line = "{} {} {}\n".format(edge[0], edge[1], graph.dict_cost[edge])
        file.write(new_line)

    for vertex in graph.dict_in.keys():
        if len(graph.dict_in[vertex]) == 0 and len(graph.dict_out[vertex]) == 0:
            new_line = "{}\n".format(vertex)
            file.write(new_line)

    file.close()


def read_graph_from_file(filename):
    file = open(filename, "r")
    line = file.readline()
    line = line.strip()

    vertices, edges = line.split(' ')
    graph = TripleDictGraph(int(vertices), int(edges))
    line = file.readline().strip()

    while len(line) > 0:
        line = line.split(' ')
        if len(line) == 1:
            graph.dict_in[int(line[0])] = []

            graph.dict_out[int(line[0])] = []

        else:
            graph.dict_in[int(line[1])].append(int(line[0]))
            graph.dict_out[int(line[0])].append(int(line[1]))
            graph.dict_cost[(int(line[0]), int(line[1]))] = int(line[2])

        line = file.readline().strip()
    file.close()
    return graph
