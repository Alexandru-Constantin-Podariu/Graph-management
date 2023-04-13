from repository import TripleDictGraph, write_to_file, read_graph_from_file
from random import randint


class Ui:
    def __init__(self):
        self._graphs = []
        self._current = None

    @staticmethod
    def print_menu():
        print("*****************************************")
        print("What operation would you like to perform?")
        print("0. Close the application")
        print("1. Read a graph from a file")
        print("2. Write a graph to a file")
        print("3. Create a random graph")
        print("4. Copy the graph")
        print("5. Add an empty graph")
        print("6. Switch the graph")
        print("7. Get the number of vertices")
        print("8. Parse the vertices")
        print("9. Get the number of edges")
        print("10. List all edges with costs")
        print("11. Check the existence of a vertex")
        print("12. Find edge from x to y")
        print("13. Get the in degree and the out degree of a specified vertex")
        print("14. Parse the outbound edges of a vertex")
        print("15. Parse the inbound edges of a vertex")
        print("16. Get the cost of an edge")
        print("17. Update the cost of an edge")
        print("18. Add a vertex")
        print("19. Remove a vertex")
        print("20. Add an edge")
        print("21. Remove an edge")
        print("22. Find the shortest length path between 2 vertices")
        print("23. Find the shortest length path between 2 vertices in reverse")
        print("24. Find the lowest cost path between 2 vertices using the Bellman Ford algorithm")
        print("*****************************************")

    def read_graph(self):
        filename = input("Give the name of the file: ")
        if self._current is None:
            self._current = 0

        graph = read_graph_from_file(filename)
        self._graphs.append(graph)
        self._current = len(self._graphs) - 1

    def write_graph(self):
        current_graph = self._graphs[self._current]

        output_file = "output" + str(self._current) + ".txt"

        write_to_file(current_graph, output_file)
        print("New save file successfully created!")

    def add_empty_graph(self):
        if self._current is None:
            self._current = 0

        graph = TripleDictGraph(0, 0)
        self._graphs.append(graph)
        self._current = len(self._graphs) - 1

    def random_graph(self):
        vertices = int(input("Give the number of vertices: "))
        edges = int(input("Give the number of edges: "))
        graph = self.generate_random(vertices, edges)

        if self._current is None:
            self._current = 0
        self._graphs.append(graph)
        self._current = len(self._graphs) - 1
        print("Random graph has been successfully created!")

    @staticmethod
    def generate_random(vertices, edges):
        if edges > vertices * vertices:
            raise ValueError("Too many edges!")
        graph = TripleDictGraph(vertices, 0)

        i = 0
        while i < edges:
            x = randint(0, vertices - 1)
            y = randint(0, vertices - 1)
            cost = randint(0, 500)
            if graph.add_edge(x, y, cost):
                i += 1

        return graph

    def switch_graph(self):
        print("You are on the graph with the index: " + str(self._current))
        print("Available graphs range from 0 to {}" + str(len(self._graphs) - 1))

        number = int(input("Enter the index of the graph you want to switch to: "))

        if not 0 <= number < len(self._graphs):
            raise ValueError("Trying to switch to a non existing graph!")
        self._current = number
        print("You have successfully switched to graph number: " + str(number))

    def copy_a_graph(self):
        copy = self._graphs[self._current].make_copy()
        self._graphs.append(copy)

    def number_of_vertices(self):
        print("Number of vertices: " + str(len(self._graphs[self._current].parse_x())))

    def number_of_edges(self):
        print("Number of edges: " + str(len(self._graphs[self._current].parse_cost())))

    def parse_vertices(self):
        for x in self._graphs[self._current].parse_x():
            print(x)

    def check_edge(self):
        print("Give the vertices of the edge you want to check: ")
        x = int(input("x: "))
        if not self._graphs[self._current].check_vertex(x):
            print("Vertex does not exist!")
            return
        y = int(input("y: "))
        if not self._graphs[self._current].check_vertex(y):
            print("Vertex does not exist!")
            return

        if self._graphs[self._current].find_edge(int(x), int(y)):
            print("There is an edge from x to y with the cost: " + str(self._graphs[self._current].get_cost(x, y)))
        else:
            print("There is no edge from x to y!")

    def in_out_degree(self):
        print("Give the vertex you want the degree of: ")
        x = int(input("x: "))
        if not self._graphs[self._current].check_vertex(x):
            print("This vertex does not exist!")
            return

        print("Degree in:", str(self._graphs[self._current].degree_in(x)))
        print("Degree out:", str(self._graphs[self._current].degree_out(x)))

    def parse_outbound(self):
        print("Give the vertex you want the outbound edges of: ")
        x = int(input("x: "))
        if not self._graphs[self._current].parse_out(x):
            print("This vertex does not exist!")
            return
        for y in self._graphs[self._current].parse_out(x):
            print(y)

    def parse_inbound(self):
        print("Give the vertex you want the inbound edges of: ")
        y = int(input("y: "))
        if not self._graphs[self._current].parse_in(y):
            print("This vertex does not exist!")
            return
        for x in self._graphs[self._current].parse_in(y):
            print(x)

    def retrieve_cost(self):
        print("Give the vertices of the edge you want the cost of: ")
        x = int(input("x: "))
        y = int(input("y: "))
        if self._graphs[self._current].get_cost(x, y):
            print(self._graphs[self._current].get_cost(x, y))
        else:
            print("The edge does not exist!")

    def update_cost(self):
        print("Give the vertices of the edge you want to modify the cost of: ")
        x = int(input("x: "))
        y = int(input("y: "))
        z = int(input("New cost: "))
        if self._graphs[self._current].change_cost(x, y, z):
            print("The cost was updated!")
        else:
            print("The edge does not exist!")

    def add_a_vertex(self):
        print("Give the vertex you want to add: ")
        x = int(input("x: "))
        if not self._graphs[self._current].add_vertex(x):
            print("The vertex already exists!")
        else:
            print("Vertex has been successfully added!")

    def remove_a_vertex(self):
        print("Give the vertex you want to remove: ")
        x = int(input("x: "))
        if not self._graphs[self._current].remove_vertex(x):
            print("The vertex does not exist!")
        else:
            print("Vertex has been successfully removed!")

    def add_an_edge(self):
        print("Give the endpoints and the cost of the edge you want to add: ")
        x = int(input("x: "))
        y = int(input("y: "))
        c = int(input("Cost: "))
        if not self._graphs[self._current].add_edge(x, y, c):
            print("The edge already exists!")
        else:
            print("Edge has been successfully added!")

    def remove_an_edge(self):
        print("Give the endpoints of the edge you want to remove: ")
        x = int(input("x: "))
        y = int(input("y: "))
        if not self._graphs[self._current].remove_edge(x, y):
            print("The edge does not exist!")
        else:
            print("Edge has been successfully removed!")

    def list_all_costs(self):
        for key in self._graphs[self._current].parse_cost():
            print("(" + str(key[0]) + "," + str(key[1]) + ")" + " :" + str(self._graphs[self._current].dict_cost[key]))

    def check_existence(self):
        print("Give the vertex you want to check the existence of: ")
        x = int(input("x: "))
        if not self._graphs[self._current].check_vertex(x):
            print("This vertex does not exist!")
        else:
            print("This vertex does exits!")

    def shortest_path(self):
        x = int(input("x: "))
        if not self._graphs[self._current].check_vertex(x):
            print("This vertex does not exist!")
            return
        y = int(input("y: "))
        if not self._graphs[self._current].check_vertex(y):
            print("This vertex does not exist!")
            return
        n = self._graphs[self._current].find_shortest_path(x, y)
        if n == 0 or not n:
            print("There is no path between the two vertices!")
        else:
            print("is the path with the length " + str(n))

    def shortest_path_reverse(self):
        x = int(input("x: "))
        if not self._graphs[self._current].check_vertex(x):
            print("This vertex does not exist!")
            return
        y = int(input("y: "))
        if not self._graphs[self._current].check_vertex(y):
            print("This vertex does not exist!")
            return
        n = self._graphs[self._current].find_shortest_path_reverse(x, y)
        if n == 0 or not n:
            print("There is no path between the two vertices!")
        else:
            print("is the path with the length " + str(n))

    def Bellman(self):
        x = int(input("x: "))
        if not self._graphs[self._current].check_vertex(x):
            print("This vertex does not exist!")
            return
        y = int(input("y: "))
        if not self._graphs[self._current].check_vertex(y):
            print("This vertex does not exist!")
            return

        n = self._graphs[self._current].Bellman_Ford(x, y)
        if n == 0:
            print("The graph contains negative cycles!")
        elif n == -1:
            print("There is no walk from " + str(x) + " to " + str(y))
        else:
            print("is the path with the cost " + str(n))

    def start(self):
        print("Hello!")
        self.add_empty_graph()
        print("The current graph is empty!")
        print("You can select a file that contains a graph or add elements to this empty graph.")
        while True:
            try:
                self.print_menu()
                option = input("What is your option? ")
                if not option.isdigit():
                    print("You have to input a number!")
                else:
                    option = int(option)
                    if option == 0:
                        return

                    if option == 1:
                        self.read_graph()

                    if option == 2:
                        self.write_graph()

                    if option == 3:
                        self.random_graph()

                    if option == 4:
                        self.copy_a_graph()

                    if option == 5:
                        self.add_empty_graph()

                    if option == 6:
                        self.switch_graph()

                    if option == 7:
                        self.number_of_vertices()

                    if option == 8:
                        self.parse_vertices()

                    if option == 9:
                        self.number_of_edges()

                    if option == 10:
                        self.list_all_costs()

                    if option == 11:
                        self.check_existence()

                    if option == 12:
                        self.check_edge()

                    if option == 13:
                        self.in_out_degree()

                    if option == 14:
                        self.parse_outbound()

                    if option == 15:
                        self.parse_inbound()

                    if option == 16:
                        self.retrieve_cost()

                    if option == 17:
                        self.update_cost()

                    if option == 18:
                        self.add_a_vertex()

                    if option == 19:
                        self.remove_a_vertex()

                    if option == 20:
                        self.add_an_edge()

                    if option == 21:
                        self.remove_an_edge()

                    if option == 22:
                        self.shortest_path()

                    if option == 23:
                        self.shortest_path_reverse()

                    if option == 24:
                        self.Bellman()

            except ValueError as bad_input:
                print(str(bad_input))
            except FileNotFoundError as no_file:
                print(str(no_file).strip("[Errno 2] "))


ui = Ui()
ui.start()
