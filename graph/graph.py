from .coord import NODES


class Graph:

    def __init__(self):
        self.nodes = NODES

    def check_by_name(self, node_name):
        node_id = None

        for _id, data in self.nodes.items():
            if data.get('number') == node_name:
                node_id = _id
                break

        return node_id

    def get(self, node_id):
        return self.nodes.get(node_id)

    def get_coords(self, node_id):
        node = self.get(node_id)
        return node.get('x'), node.get('y')

    def get_floor(self, node_id):
        return self.get(node_id).get('floor')

    def get_delimited_path(self, path):
        d = {}
        current_path = [self.get_coords(path[0])]

        for i in range(1, len(path)):
            if self.get_floor(path[i - 1]) == self.get_floor(path[i]):
                current_path.append(self.get_coords(path[i]))
            else:
                if len(current_path) > 1:
                    floor = self.get_floor(path[i - 1])
                    if floor not in d:
                        d[floor] = []
                    d[floor].append(current_path)
                current_path = [self.get_coords(path[i])]

        if len(current_path) > 1:
            floor = self.get_floor(path[-1])
            if floor not in d:
                d[floor] = []
            d[floor].append(current_path)

        return d

    def path(self, path):
        return ' -> '.join(str(self.get(node).get('number')) for node in path)
