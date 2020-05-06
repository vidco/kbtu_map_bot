#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <vector>

namespace py = pybind11;

struct Node {
	int id;
	std::string location;
	int x;
	int y;
	std::string floor;
	std::vector<int> adjacent;

	Node(int id, std::string location, int x, int y, std::string floor, std::vector<int> adjacent) {
		this->id = id;
		this->location = location;
		this->x = x;
		this->y = y;
		this->floor = floor;
		this->adjacent = adjacent;
	}
};

struct Graph {
	std::vector<Node> g;

	Graph(string path) {
		ifstream fin;
		fin.open(path);
		std::vector<string> row;
		std::vector<int> adjacent;
		std::string temp, line, word;

		while (!fin.eof()) {
			row.clear();
			adjacent.clear();
			fin >> line;
			stringstream s(line);
			while (getline(s, word, ',')) {
				row.push_back(word);
			}
			int id = stoi(row[0]);
			std::string location = row[1];
			int x = stoi(row[2]);
			int y = stoi(row[3]);
			std::string floor = row[4];
			stringstream adj(row[5]);
			std::string nei;
			while (getline(adj, nei, '-')) {
				adjacent.push_back(stoi(nei));
			}
			Node *node = new Node(id, location, x, y, floor, adjacent);
			//cout << id << " " << location << " " << x << " " << y << " " << floor << endl;
			//Node node{id, location, x, y, floor};
			g.push_back(*node);
		}
	}

	Node getNode(int id) {
		return g[id];	
	}

	// void print() {
	// 	for (int i = 0; i < int(g.size()); i++) {
	// 		Node node = g[i];
	// 		cout << node.id << " " << node.location << " " << node.floor << endl;
	// 		cout << "Neighbors: ";
	// 		for (int j = 0; j < int(node.adjacent.size()); j++) {
	// 			cout << node.adjacent[j] << " ";
	// 		}
	// 		cout << endl;
	// 	}
	// }

};

PYBIND11_MODULE(path2, m) {
    py::class_<Node>(m, "Node")
    	.def(py::init<int, std::string, int, int, std::string, std::vector<int> >());

    py::class_<Graph>(m, "Graph")
    	.def(py::init<std::string>())
    	.def("get_node", &Graph::getNode);
}

// int main() {
// 	string path = "nodes.csv";
// 	Graph *graph = new Graph(path);
// 	graph->print();
// 	cout << graph->g.size() << endl;
// }