#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <algorithm>
#include <vector>
#include <queue>
#include <sstream>
#include <fstream>

namespace py = pybind11;

struct Node {
	int id;
	std::string location;
	int x;
	int y;
	std::string floor;
	std::vector<int> adjacents;

	Node(int id, std::string location, int x, int y, std::string floor, std::vector<int> adjacents) {
		this->id = id;
		this->location = location;
		this->x = x;
		this->y = y;
		this->floor = floor;
		this->adjacents = adjacents;
	}

	int getId() {
	    return this->id;
	}

	std::string getLocation() {
		return this->location;
	}

	std::pair<int, int> getCoordinates() {
		return std::make_pair(this->x, this->y);
	}

	std::string getFloor() {
		return this->floor;
	}

	std::vector<int> getAdjacents() {
		return this->adjacents;
	}
};

struct Graph {
	std::vector<Node> g;

	Graph(std::string path) {
		std::ifstream fin;
		fin.open(path);
		std::vector<std::string> row;
		std::vector<int> adjacents;
		std::string temp, line, word;

		while (!fin.eof()) {
			row.clear();
			adjacents.clear();
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
				adjacents.push_back(stoi(nei));
			}
			Node *node = new Node(id, location, x, y, floor, adjacents);
			g.push_back(*node);
		}
	}

	Node getNode(int id) {
		for (int i = 0; i < int(g.size()); i++) {
			if (g[i].getId() == id) {
				return g[i];
			}
		}
		return Node{-1, "", -1, -1, "", std::vector<int>(0)};
	}

	int checkByName(std::string location) {
		for (int i = 0; i < int(g.size()); i++) {
			if (g[i].getLocation() == location) {
				return g[i].getId();
			}
		}
		return -1;
	}

	std::vector<int> getMinDist(int a, int b) {
		std::queue<int> q;
		std::vector<int> dist(int(g.size()) + 1, 0);
		std::vector<int> p(int(g.size()) + 1, 0);
		q.push(a);
		while (!q.empty()) {
			int nodeId = q.front();
			q.pop();
			Node node = getNode(nodeId);
			std::vector<int> adjacents = node.getAdjacents();
			for (int i = 0; i < (int) adjacents.size(); i++) {
				int toId = adjacents[i];
				if (dist[toId] == 0) {
					dist[toId] = dist[nodeId] + 1;
					p[toId] = nodeId;
					q.push(toId);
				}
			}
		}
		std::vector<int> path;
		while (b != a) {
			path.push_back(b);
			b = p[b];
		}
		path.push_back(a);
		std::reverse(path.begin(), path.end());
		return path;
	}

	std::map<std::string, std::vector<std::vector<std::pair<int, int> > > > getPathOnFloor(std::vector<int> path) {
		std::map<std::string, std::vector<std::vector<std::pair<int, int> > > > pathOnFloor;
		std::vector<std::pair<int, int> > currentPath;
		std::string currentFloor;
		currentPath.push_back(getNode(path[0]).getCoordinates());
		currentFloor = getNode(path[0]).getFloor();
		for (int i = 1; i < int(path.size()); i++) {
			if (getNode(path[i]).getFloor() != currentFloor) {
				if (currentPath.size() > 1) {
					pathOnFloor[currentFloor].push_back(currentPath);
				}
				currentPath.clear();
				currentFloor = getNode(path[i]).getFloor();
			}
			currentPath.push_back(getNode(path[i]).getCoordinates());
		}
		if (currentPath.size() > 1) {
			pathOnFloor[currentFloor].push_back(currentPath);
		}
		return pathOnFloor;
	}
};

PYBIND11_MODULE(graph, m) {
    py::class_<Node>(m, "Node")
    	.def(py::init<int, std::string, int, int, std::string, std::vector<int> >())
    	.def("get_id", &Node::getId)
    	.def("get_location", &Node::getLocation)
    	.def("get_coordinates", &Node::getCoordinates)
    	.def("get_floor", &Node::getFloor)
    	.def("get_adjacents", &Node::getAdjacents);

    py::class_<Graph>(m, "Graph")
    	.def(py::init<std::string>())
    	.def("check_by_name", &Graph::checkByName)
    	.def("get_node", &Graph::getNode)
    	.def("get_min_dist", &Graph::getMinDist)
    	.def("get_path_on_floor", &Graph::getPathOnFloor);
}
