#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <algorithm>
#include <vector>
#include <queue>

namespace py = pybind11;

struct Graph {
	Graph() {
		g[1] = {2};
		g[2] = {1, 3};
		g[3] = {2, 4};
		g[4] = {3, 5};
		g[5] = {4, 6};
		g[6] = {5, 7};
		g[7] = {6, 8};
		g[8] = {7, 9, 19};
		g[9] = {8, 10};
		g[10] = {9, 11};
		g[11] = {10, 18};
		g[12] = {18, 13};
		g[13] = {12, 14};
		g[14] = {13, 15};
		g[15] = {14, 16};
		g[16] = {15, 17};
		g[17] = {16};
		g[18] = {11, 12};
		g[19] = {8, 20};
		g[20] = {19, 21};
		g[21] = {20};
	}
	const std::vector<int> mindist(int a, int b) {
		std::vector<int> dist(25, 0);
		std::vector<int> p(25, 0);
		std::vector<int> ans;
		std::queue<int> q;

		q.push(a);

		while (!q.empty()) {
			int v = q.front();
			q.pop();

			bool qwe = false;

			for (int i = 0; i < (int) g[v].size(); i++) {
				int to = g[v][i];
				if (!dist[to]) {
					dist[to] = dist[v] + 1;
					p[to] = v;
					q.push(to);
				}

				if (to == b) {
					qwe = true;
					break;
				}
			}

			if (qwe) {
				break;
			}
		}

		while (b != a) {
			ans.push_back(b);
			b = p[b];
		}

		ans.push_back(a);
		std::reverse(ans.begin(), ans.end());

		return ans;
	}

	std::vector<int> g[25];
};

PYBIND11_MODULE(graph, m) {
    // m.def("add", &add, "A function which adds two numbers");

    py::class_<Graph>(m, "Graph")
    	.def(py::init<>())
    	.def("mindist", &Graph::mindist);
}