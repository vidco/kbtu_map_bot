import csv


class Node2:

    def __init__(self, _id, location, x, y, floor, adjacent):
        self.id = _id
        self.location = location
        self.x = x
        self.y = y
        self.floor = floor
        self.adjacent = adjacent

    def get_id(self):
        return self.id


class Graph2:

    def __init__(self, path):
        self.graph = []

        with open(path, newline='') as file:
            rows = csv.reader(file, delimiter=',', quotechar='|')

            for row in rows:
                _id = int(row[0])
                location = row[1]
                x = int(row[2])
                y = int(row[3])
                floor = row[4]
                adjacent = [int(item) for item in row[5].split('-')]

                self.graph.append(Node2(_id, location, x, y, floor, adjacent))

    def get_node(self, i):
        return self.graph[i]
