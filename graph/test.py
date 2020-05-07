from graph import Graph, Node
from p_graph import Graph2, Node2
import time
import timeit


start = time.time()
graph = Graph('nodes.csv')
print(graph.get_node(2).get_id())
# c = time.time() - start

# start = time.time()
# graph = Graph2('nodes.csv')
# print(graph.get_node(2).get_id())
QWE = graph.get_min_dist(21, 22)
print(QWE)
PATH = graph.get_path_on_floor(QWE)
print(PATH)
print(graph.path_description(QWE))
p = time.time() - start
print(p)

# c = timeit.timeit('''graph = Graph('nodes.csv')''', setup='from main import Graph, Node', number=1000)
#
# p = timeit.timeit('''graph = Graph2('nodes.csv')''', setup='from qwe import Graph2, Node2', number=1000)
#
# print("faster " + str(p / c))
