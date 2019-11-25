from graph import Node, Graph
from time import time
from random import randint, random
from math import sqrt

# construct a one-level graph from input file and run power iteration
g = Graph("0")

with open("input.txt", "r") as f:
	line = f.readline()
	nDomains = int(line)
	line = f.readline()
	pagesPerDomain = int(line)

	for i in range(nDomains):
		for j in range(pagesPerDomain):
			g.add_node(Node(str(i) + "-" + str(j)))

	edges = []
	line = f.readline()
	while line:
		edge = line.rsplit('\n')[0].split(' ')
		edges.append(edge)
		line = f.readline()
	# remove duplicate edges
	newEdges = []
	for edge in set(map(tuple, edges)):
		newEdges.append(edge)
	for edge in newEdges:
		g.add_edge(str(edge[0]) + "-" + str(edge[1]), str(edge[2]) + "-" + str(edge[3]))

g.init_ranks()
g.calc_ranks()

# construct a two-level graph from input file and run power iteration in each subgraph
g2 = Graph("main")

with open("input.txt", "r") as f:
	line = f.readline()
	nDomains = int(line)
	line = f.readline()
	pagesPerDomain = int(line)

	for i in range(nDomains):
		tmp = Graph(str(i))
		g2.add_node(tmp)
		for j in range(pagesPerDomain):
			tmp.add_node(Node(str(i) + "-" + str(j)))

	edges = []
	line = f.readline()
	while line:
		edge = line.rsplit('\n')[0].split(' ')
		edges.append(edge)
		line = f.readline()
	# remove duplicate edges
	newEdges = []
	for edge in set(map(tuple, edges)):
		newEdges.append(edge)
	for edge in newEdges:
		g2.add_edge(str(edge[0]) + "-" + str(edge[1]), str(edge[2]) + "-" + str(edge[3]))

g2.init_ranks()
g2.calc_ranks()

# compare the orderings of ranking values in each graph
ranks1 = g.get_ranks()
ranks2 = g2.get_ranks()
order1 = sorted(ranks1, key=ranks1.get)
order2 = sorted(ranks2, key=ranks2.get)
nodes = []
for i in range(nDomains):
	for j in range(pagesPerDomain):
		nodes.append(str(i) + "-" + str(j))
numerator = 0
denominator = len(nodes) * (len(nodes) - 1)
for i in nodes:
	print(i)
	for j in nodes:
		if i == j:
			continue
		d1 = order1.index(i) - order1.index(j)
		d2 = order2.index(i) - order2.index(j)
		if d1 * d2 < 0:
			numerator += 1
print("distance of orderings: " + str(numerator / denominator))

# perform one hundred updates on each graph and compare the time took
start = time()
for i in range(100):
	g.add_edge(str(randint(0, nDomains - 1)) + "-" + str(randint(0, pagesPerDomain - 1)), str(randint(0, nDomains - 1)) + "-" + str(randint(0, pagesPerDomain - 1)))
	g.calc_ranks()
end = time()
print("updating time 1: " + str(end - start) + "s")

start = time()
for i in range(100):
	if random() < 0.8:
		domain = str(randint(0, nDomains - 1))
		g2.add_and_update(domain + "-" + str(randint(0, pagesPerDomain - 1)), domain + "-" + str(randint(0, pagesPerDomain - 1)))
	else:
		g2.add_and_update(str(randint(0, nDomains - 1)) + "-" + str(randint(0, pagesPerDomain - 1)), str(randint(0, nDomains - 1)) + "-" + str(randint(0, pagesPerDomain - 1)))
end = time()
print("updating time 2: " + str(end - start) + "s")