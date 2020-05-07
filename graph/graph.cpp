#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <algorithm>
#include <vector>
#include <queue>
#include <sstream>
#include <fstream>
#include <string>

namespace py = pybind11;

enum Direction {
	UP = 1,
	RIGHT = 2,
	DOWN = 3,
	LEFT = 4
};

struct Node {
	int id;
	std::string location;
	int x;
	int y;
	int floor;
	std::vector<int> adjacents;

	Node(int id, std::string location, int x, int y, int floor, std::vector<int> adjacents) {
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

	int getFloor() {
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
			int floor = stoi(row[4]);
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

	Direction getDirection(std::pair<int, int> from, std::pair<int, int> to) {
		int xd = to.first - from.first;
		int yd = to.second - from.second;
		if (!xd) {
			if (yd > 0) {
				return Direction.DOWN;
			} else {
				return Direction.UP;
			}
		} else {
			if (xd > 0) {
				return Direction.RIGHT;
			} else {
				return Direction.LEFT;
			}
		}
	}

	std::string getCross(Direction first, Direction second) {
		if (first == second) {
			return "straight";
		} else if ((second - first + 4) % 4 == 1) {
			return "right";
		} else {
			return "left";
		}
	} 

	std::string pathDescription(std::vector<int> path) {
		std::string textPath = "";
		for (int i = 0; i < int(path.size()); i++) {
			string location = getNode(path[i]).getLocation();
			if (location == "cross") {
				std::pair<int, int> prevCoords = getNode(path[i - 1]).getCoordinates();
				std::pair<int, int> curCoords = getNode(path[i]).getCoordinates();
				std::pair<int, int> nextCoords = getNode(path[i + 1]).getCoordinates();
				Direction first = getDirection(prevCoords, curCoords);
				Direction second = getDirection(curCoords, nextCoords);
				std::string cross = getCross(first, second);
				textPath += cross;
			} else if (location == "ladder") {
				int prevFloor = getNode(path[i]).getFloor();
				while (location == "ladder") {
					i++;
					location = getNode(path[i]).getLocation();
				}
				i--;
				int nextFloor = getNode(path[i]).getFloor();
				if (nextFloor > prevFloor) {
					textPath += "go upstairs to the ";
				} else {
					textPath += "go downstairs to the ";
				}
				textPath += to_string(nextFloor);
				textPath += " floor";
			} else {
				textPath += location;
			}

			if (i != int(path.size())) {
				textPath += " -> ";
			}
		}
	}

	std::map<int, std::vector<std::vector<std::pair<int, int> > > > getPathOnFloor(std::vector<int> path) {
		std::map<int, std::vector<std::vector<std::pair<int, int> > > > pathOnFloor;
		std::vector<std::pair<int, int> > currentPath;
		int currentFloor;
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
    	.def(py::init<int, std::string, int, int, int, std::vector<int> >())
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
    	.def("get_path_on_floor", &Graph::getPathOnFloor)
    	.def("get_direction", &Graph::getDirection)
    	.def("get_cross", &Graph::getCross)
    	.def("path_description", &Graph::pathDescription);

    py::enum_<Direction>(m, "Direction")
    	.value("UP", Direction::UP)
    	.value("DOWN", Direction::DOWN)
    	.value("LEFT", Direction::LEFT)
    	.value("RIGHT", Direction::RIGHT)
    	.export_values();
}
