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
	Direction direction;
	std::vector<int> neighbors;

	Node(int id, std::string location, int x, int y, int floor, std::string direction, std::vector<int> neighbors) {
		this->id = id;
		this->location = location;
		this->x = x;
		this->y = y;
		this->floor = floor;
		this->setDirection(direction);
		this->neighbors = neighbors;
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

	Direction getDirection() {
	    return this->direction;
	}

	Direction getReverseDirection() {
		switch (this->direction) {
            case LEFT:
                return RIGHT;
            case RIGHT:
                return LEFT;
            case UP:
                return DOWN;
            case DOWN:
            default:
                return UP;
        }
	}

	void setDirection(std::string direction) {
	    if (direction == "left") {
	        this->direction = LEFT;
	    } else if (direction == "right") {
	        this->direction = RIGHT;
	    } else if (direction == "up") {
	        this->direction = UP;
	    } else {
	        this->direction = DOWN;
	    }
	}

	std::vector<int> getNeighbors() {
		return this->neighbors;
	}

	std::pair<int, int> getShiftedCoordinates(int delta) {
        switch (this->direction) {
            case LEFT:
                return std::make_pair(this->x - delta, this->y);
            case RIGHT:
                return std::make_pair(this->x + delta, this->y);
            case UP:
                return std::make_pair(this->x, this->y - delta);
            case DOWN:
            default:
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
		std::vector<int> neighbors;
		std::string temp, line, word;

		while (!fin.eof()) {
			row.clear();
			neighbors.clear();

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
			std::string direction = row[5];
			std::stringstream neighborsStream(row[6]);

			std::string nei;
			while (getline(neighborsStream, nei, '-')) {
				neighbors.push_back(stoi(nei));
			}

			Node *node = new Node(id, location, x, y, floor, direction, neighbors);
			g.push_back(*node);
		}
	}

	Node getNode(int id) {
		for (int i = 0; i < int(g.size()); i++) {
			if (g[i].getId() == id) {
				return g[i];
			}
		}
		return Node{-1, "", -1, -1, -1, "", std::vector<int>(0)};   // Todo: fix or check it!
	}

	int getIdByLocation(std::string location) {
		for (int i = 0; i < int(g.size()); i++) {
			if (g[i].getLocation() == location) {
				return g[i].getId();
			}
		}
		return -1;
	}

	bool isValidFloor(int floor) {
		for (int i = 0; i < int(g.size()); i++) {
			if (g[i].getFloor() == floor) {
				return true;
			}
		}
		return false;
	}

	Direction getDirection(Node from, Node to) {
		int xd = to.getCoordinates().first - from.getCoordinates().first;
		int yd = to.getCoordinates().second - from.getCoordinates().second;

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
			return "down_" + std::to_string(nextFloor);
		} else {
			return "up_" + std::to_string(nextFloor);
		}
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
			std::vector<int> neighbors = node.getNeighbors();
			for (int i = 0; i < int(neighbors.size()); i++) {
				int toId = neighbors[i];
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

		for (int i = 0; i < int(g.size()); i++) {
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

	std::vector<string> pathDescription(std::vector<int> path) {

		std::vector<string> pathList;

		for (int i = 0; i < int(path.size()); i++) {

            Node currentNode = getNode(path[i]);
            Node nextNode = getNode(path[i + 1]);
			std::string location = currentNode.getLocation();

			if (location == "cross" or (location == "ladder" and nextNode.getLocation() != "ladder")) {

				Direction first = getDirection(getNode(path[i - 1]), currentNode);
				Direction second = getDirection(currentNode, nextNode);

				std::string cross = getCross(first, second);
				if (cross != "straight") {
					pathList.push_back(cross);
				}

			} else if (location == "ladder") {

				int prevFloor = currentNode.getFloor();

				while (location == "ladder") {
					i++;
					location = getNode(path[i]).getLocation();
				}
				i--;

				Node currentNode = getNode(path[i]);    // Because of iteration in while, new current node

				int nextFloor = currentNode.getFloor();
				pathList.push_back(getStairsDirection(prevFloor, nextFloor));

                Direction first = currentNode.getReverseDirection();
				Direction second = getDirection(currentNode, getNode(path[i + 1]));

				std::string cross = getCross(first, second);
				if (cross != "straight") {
					pathList.push_back(cross);
				}

			} else {

				pathList.push_back(location);

				if (i == 0) {
					Direction first = currentNode.getReverseDirection();
					Direction second = getDirection(currentNode, nextNode);
					std::string cross = getCross(first, second);
					if (cross != "straight") {
						pathList.push_back(cross)
					}
				} else if (i == int(path.size()) - 1) {
					Direction first = getDirection(getNode(path[i - 1]), currentNode);
					Direction second = currentNode.getDirection();
                    std::string cross = getCross(first, second);
					if (cross != "straight") {
						pathList.push_back(cross)
					}
				}
			}
		}

		return pathList;
	}

	std::map<int, std::vector<std::vector<std::pair<int, int> > > > getPathOnFloor(std::vector<int> path, int delta) {

		std::map<int, std::vector<std::vector<std::pair<int, int> > > > pathOnFloor;
		std::vector<std::pair<int, int> > currentPath;
		int currentFloor;

		Node node = getNode(path[0]);
        currentPath.push_back(node.getShiftedCoordinates(delta));
		currentPath.push_back(node.getCoordinates());
		currentFloor = node.getFloor();

		for (int i = 1; i < int(path.size()); i++) {
			node = getNode(path[i]);
			if (node.getFloor() != currentFloor) {
				if (currentPath.size() > 1) {
                    currentPath.push_back(getNode(path[i - 1]).getShiftedCoordinates(delta));
					pathOnFloor[currentFloor].push_back(currentPath);
                }
				currentPath.clear();
                currentPath.push_back(node.getShiftedCoordinates(delta));
				currentFloor = node.getFloor();
			}
			currentPath.push_back(node.getCoordinates());
		}
		
		if (currentPath.size() > 1) {
		    Node node = getNode(path[int(path.size()) - 1]);
            currentPath.push_back(node.getShiftedCoordinates(delta));
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
    	.def("get_direction", &Node::getDirection)
        .def("get_reverse_direction", &Node::getReverseDirection)
        .def("set_direction", &Node::setDirection)
    	.def("get_neighbors", &Node::getNeighbors)
    	.def("get_shifted_coordinates", &Node::getShiftedCoordinates);

    py::class_<Graph>(m, "Graph")
    	.def(py::init<std::string>())
    	.def("get_id_by_location", &Graph::getIdByLocation)
    	.def("is_valid_floor", &Graph::isValidFloor)
    	.def("get_node", &Graph::getNode)
    	.def("bfs", &Graph::BFS)
    	.def("restore_path", &Graph::restorePath)
    	.def("get_min_dist", &Graph::getMinDist)
    	.def("get_min_dist_to_floor", &Graph::getMinDistToFloor)
    	.def("get_path_on_floor", &Graph::getPathOnFloor)
    	.def("get_direction", &Graph::getDirection)
    	.def("get_cross", &Graph::getCross)
    	.def("path_description", &Graph::pathDescription)
    	.def("get_stairs_direction", &Graph::getStairsDirection);
    	
    py::enum_<Direction>(m, "Direction")
    	.value("UP", Direction::UP)
    	.value("DOWN", Direction::DOWN)
    	.value("LEFT", Direction::LEFT)
    	.value("RIGHT", Direction::RIGHT)
    	.export_values();
}
