#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <algorithm>
#include <vector>
#include <sstream>
#include <fstream>

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
	int getId() {
	    return this->id;
	}
};

struct Graph {
	std::vector<Node> g;

	Graph(std::string path) {
		std::ifstream fin;
		fin.open(path);
		std::vector<std::string> row;
		std::vector<int> adjacent;
		std::string temp, line, word;

		while (!fin.eof()) {
			row.clear();
			adjacent.clear();
			fin >> line;
			std::stringstream s(line);
			while (getline(s, word, ',')) {
				row.push_back(word);
			}
			int id = stoi(row[0]);
			std::string location = row[1];
			int x = stoi(row[2]);
			int y = stoi(row[3]);
			std::string floor = row[4];
			std::stringstream adj(row[5]);
			std::string nei;
			while (getline(adj, nei, '-')) {
				adjacent.push_back(stoi(nei));
			}
			Node *node = new Node(id, location, x, y, floor, adjacent);
			g.push_back(*node);
		}
	}

	Node getNode(int id) {
		return g[id];	
	}
};

PYBIND11_MODULE(main, m) {
    py::class_<Node>(m, "Node")
    	.def(py::init<int, std::string, int, int, std::string, std::vector<int> >())
    	.def("get_id", &Node::getId);

    py::class_<Graph>(m, "Graph")
    	.def(py::init<std::string>())
    	.def("get_node", &Graph::getNode);
}
