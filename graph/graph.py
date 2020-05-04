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

    def get_path_coordinates(self, path):
        nodes = []

        for node_id in path:
            data = self.get(node_id)
            x = data.get('x')
            y = data.get('y')

            if x or y:
                nodes.append((x, y))

        return nodes

    def path(self, path):
        return ' -> '.join(str(self.get(node).get('number')) for node in path)
