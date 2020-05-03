#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <algorithm>
#include <vector>
#include <queue>

namespace py = pybind11;

struct Graph {
	Graph() {
		g[1] = {2, 4, 7};
		g[2] = {1, 3, 4, 5};
		g[3] = {2, 6};
		g[4] = {1, 2, 6, 10};
		g[5] = {2};
		g[6] = {3, 4, 9};
		g[7] = {1, 8};
		g[8] = {7};
		g[9] = {6};
		g[10] = {4};
	}
	const std::vector<int> mindist(int a, int b) {
		std::vector<int> dist(10 + 1, 0);
		std::vector<int> p(10 + 1);
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

	std::vector<int> g[11];
};

PYBIND11_MODULE(graph, m) {
    // m.def("add", &add, "A function which adds two numbers");

    py::class_<Graph>(m, "Graph")
    	.def(py::init<>())
    	.def("mindist", &Graph::mindist);
}