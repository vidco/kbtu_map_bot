from utils import NODES


class Nodes:

    def __init__(self):
        self.nodes = NODES

    def check_by_name(self, node_name):
        node_id = None

        for _id, data in self.nodes.items():
            if data.get('number') == node_name:
                node_id = _id
                break

        print(node_id)
        return node_id

    def get(self, node_id):
        return self.nodes.get(node_id)

    def path(self, path):
        return ' -> '.join(str(self.get(node).get('number')) for node in path)
