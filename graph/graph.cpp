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
	std::string side;
	std::vector<int> adjacents;

	Node(int id, std::string location, int x, int y, int floor, std::string side, std::vector<int> adjacents) {
		this->id = id;
		this->location = location;
		this->x = x;
		this->y = y;
		this->floor = floor;
		this->side = side;
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

	std::string getSide() {
	    return this->side;
	}

	std::vector<int> getAdjacents() {
		return this->adjacents;
	}

	std::pair<int, int> getSideCoordinates(int delta) {
	    if (this->side == "left") {
	        return std::make_pair(this->x - delta, this->y);
	    } else if (this->side == "right") {
	        return std::make_pair(this->x + delta, this->y);
	    } else if (this->side == "up") {
	        return std::make_pair(this->x, this->y - delta);
	    } else {
	        return std::make_pair(this->x, this->y + delta);
	    }
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
			std::string side = row[5];
			std::stringstream adj(row[6]);

			std::string nei;
			while (getline(adj, nei, '-')) {
				adjacents.push_back(stoi(nei));
			}

			Node *node = new Node(id, location, x, y, floor, side, adjacents);
			g.push_back(*node);
		}
	}

	Node getNode(int id) {
		for (int i = 0; i < int(g.size()); i++) {
			if (g[i].getId() == id) {
				return g[i];
			}
		}
		return Node{-1, "", -1, -1, -1, "", std::vector<int>(0)};
	}

	int checkByName(std::string location) {
		for (int i = 0; i < int(g.size()); i++) {
			if (g[i].getLocation() == location) {
				return g[i].getId();
			}
		}
		return -1;
	}

	Direction getDirection(std::pair<int, int> from, std::pair<int, int> to) {
		int xd = to.first - from.first;
		int yd = to.second - from.second;
		if (!xd) {
			if (yd > 0) {
				return DOWN;
			} else {
				return UP;
			}
		} else {
			if (xd > 0) {
				return RIGHT;
			} else {
				return LEFT;
			}
		}
	}

	Direction getDirectionBySide(std::string direction) {
	    if (direction == "left") {
	        return RIGHT;
	    } else if (direction == "right") {
	        return LEFT;
	    } else if (direction == "down") {
	        return UP;
	    } else {
	        return DOWN;
	    }
	}

	Direction getReverseDirection(Direction direction) {
		if (direction == UP) {
			return DOWN;
		} else if (direction == DOWN) {
			return UP;
		} else if (direction == LEFT) {
			return RIGHT;
		} else {
			return LEFT;
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

	std::string getStairsDirection(int prevFloor, int nextFloor) {
		if (prevFloor > nextFloor) {
			return "go downstairs to the ";
		} else {
			return "go upstairs to the ";
		}
	}

	std::string floorToString(int floor) {

		std::string floorString = std::to_string(floor);

		if (floor == 1) {
			floorString += "st ";
		} else if (floor == 2) {
			floorString += "nd ";
		} else if (floor == 3) {
			floorString += "rd ";
		} else {
			floorString += "th ";
		}

		floorString += "floor";

		return floorString;
	}

	std::pair<std::vector<int>, std::vector<int> > BFS(int start) {
		std::queue<int> q;
		std::vector<int> dist(int(g.size()) + 1, 0);
		std::vector<int> ancestors(int(g.size()) + 1, 0);

		q.push(start);

		while (!q.empty()) {
			int nodeId = q.front();
			q.pop();
			Node node = getNode(nodeId);
			std::vector<int> adjacents = node.getAdjacents();
			for (int i = 0; i < (int) adjacents.size(); i++) {
				int toId = adjacents[i];
				if (dist[toId] == 0) {
					dist[toId] = dist[nodeId] + 1;
					ancestors[toId] = nodeId;
					q.push(toId);
				}
			}
		}

		return std::make_pair(dist, ancestors);
	}

	std::vector<int> restorePath(std::vector<int> ancestors, int start, int end) {
		std::vector<int> path;

		while (end != start) {
			path.push_back(end);
			end = ancestors[end];
		}
		path.push_back(start);
		std::reverse(path.begin(), path.end());

		return path;
	}

	std::vector<int> getMinDistToFloor(int start, int floor) {
		std::pair<std::vector<int>, std::vector<int> > BFSFromStart = BFS(start);
		std::vector<int> dist = BFSFromStart.first;
		std::vector<int> ancestors = BFSFromStart.second;

		int closestNodeId = -1;

		for (int i = 0; i < (int) g.size(); i++) {
			Node node = g[i];
			int nodeId = node.getId();

			if (node.getFloor() != floor) {
				continue;
			}

			if (closestNodeId == -1) {
				closestNodeId = nodeId;
			} else {
				if (dist[nodeId] < dist[closestNodeId]) {
					closestNodeId = nodeId;
				}
			}
		}

		return restorePath(ancestors, start, closestNodeId);
	}

	std::vector<int> getMinDist(int start, int end) {
		std::pair<std::vector<int>, std::vector<int> > BFSFromStart = BFS(start);
		std::vector<int> ancestors = BFSFromStart.second;
		std::vector<int> path;

		return restorePath(ancestors, start, end);
	}

	std::string pathDescription(std::vector<int> path) {

		std::string textPath = "";

		for (int i = 0; i < int(path.size()); i++) {

            Node currentNode = getNode(path[i]);
			std::string location = currentNode.getLocation();

			if (location == "cross" or (location == "ladder" and getNode(path[i + 1]).getLocation() != "ladder")) {

				std::pair<int, int> prevCoords = getNode(path[i - 1]).getCoordinates();
				std::pair<int, int> curCoords = currentNode.getCoordinates();
				std::pair<int, int> nextCoords = getNode(path[i + 1]).getCoordinates();

				Direction first = getDirection(prevCoords, curCoords);
				Direction second = getDirection(curCoords, nextCoords);

				textPath += getCross(first, second);

			} else if (location == "ladder") {

				int prevFloor = currentNode.getFloor();

				while (location == "ladder") {
					i++;
					location = getNode(path[i]).getLocation();
				}
				i--;

				Node currentNode = getNode(path[i]);    // Because of iteration in while, new current node

				int nextFloor = currentNode.getFloor();
				textPath += getStairsDirection(prevFloor, nextFloor);
				textPath += floorToString(nextFloor);

                Direction first = getDirectionBySide(currentNode.getSide());
                std::pair<int, int> curCoords = currentNode.getCoordinates();
				std::pair<int, int> nextCoords = getNode(path[i + 1]).getCoordinates();
				Direction second = getDirection(curCoords, nextCoords);

                textPath += " -> ";
				textPath += getCross(first, second);

			} else {

				textPath += location;

				if (i == 0) {
					Direction first = getDirectionBySide(currentNode.getSide());
					std::pair<int, int> curCoords = currentNode.getCoordinates();
					std::pair<int, int> nextCoords = getNode(path[i + 1]).getCoordinates();
					Direction second = getDirection(curCoords, nextCoords);
                    textPath += " -> ";
				    textPath += getCross(first, second);
				} else if (i == int(path.size()) - 1) {

					Direction second = getReverseDirection(getDirectionBySide(currentNode.getSide()));
					std::pair<int, int> curCoords = currentNode.getCoordinates();
					std::pair<int, int> prevCoords = getNode(path[i - 1]).getCoordinates();
					Direction first = getDirection(prevCoords, curCoords);
					textPath += " -> ";
                    textPath += getCross(first, second);
				}
			}

			if (i != int(path.size()) - 1) {
				textPath += " -> ";
			}
		}

		return textPath;
	}

	std::map<int, std::vector<std::vector<std::pair<int, int> > > > getPathOnFloor(std::vector<int> path, int delta) {

		std::map<int, std::vector<std::vector<std::pair<int, int> > > > pathOnFloor;
		std::vector<std::pair<int, int> > currentPath;
		int currentFloor;

		Node node = getNode(path[0]);
        currentPath.push_back(node.getSideCoordinates(delta));
		currentPath.push_back(node.getCoordinates());
		currentFloor = node.getFloor();

		for (int i = 1; i < int(path.size()); i++) {
			node = getNode(path[i]);
			if (node.getFloor() != currentFloor) {
				if (currentPath.size() > 1) {
                    currentPath.push_back(getNode(path[i - 1]).getSideCoordinates(delta));
					pathOnFloor[currentFloor].push_back(currentPath);
                }
				currentPath.clear();
                currentPath.push_back(node.getSideCoordinates(delta));
				currentFloor = node.getFloor();
			}
			currentPath.push_back(node.getCoordinates());
		}
		
		if (currentPath.size() > 1) {
            currentPath.push_back(getNode(path[int(path.size()) - 1]).getSideCoordinates(delta));
			pathOnFloor[currentFloor].push_back(currentPath);
		}
		return pathOnFloor;
	}
};

PYBIND11_MODULE(graph, m) {
    py::class_<Node>(m, "Node")
    	.def(py::init<int, std::string, int, int, int, std::string, std::vector<int> >())
    	.def("get_id", &Node::getId)
    	.def("get_location", &Node::getLocation)
    	.def("get_coordinates", &Node::getCoordinates)
    	.def("get_floor", &Node::getFloor)
    	.def("get_side", &Node::getSide)
    	.def("get_adjacents", &Node::getAdjacents)
    	.def("get_side_coordinates", &Node::getSideCoordinates);

    py::class_<Graph>(m, "Graph")
    	.def(py::init<std::string>())
    	.def("check_by_name", &Graph::checkByName)
    	.def("get_node", &Graph::getNode)
    	.def("bfs", &Graph::BFS)
    	.def("restore_path", &Graph::restorePath)
    	.def("get_min_dist", &Graph::getMinDist)
    	.def("get_min_dist_to_floor", &Graph::getMinDistToFloor)
    	.def("get_path_on_floor", &Graph::getPathOnFloor)
    	.def("get_direction", &Graph::getDirection)
    	.def("get_reverse_direction", &Graph::getReverseDirection)
    	.def("get_cross", &Graph::getCross)
    	.def("path_description", &Graph::pathDescription)
    	.def("get_stairs_direction", &Graph::getStairsDirection)
    	.def("floor_to_string", &Graph::floorToString)
        .def("get_direction_by_side", &Graph::getDirectionBySide);

    py::enum_<Direction>(m, "Direction")
    	.value("UP", Direction::UP)
    	.value("DOWN", Direction::DOWN)
    	.value("LEFT", Direction::LEFT)
    	.value("RIGHT", Direction::RIGHT)
    	.export_values();
}
