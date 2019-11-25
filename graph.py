# Simple Python implementation of node and directed graph

class Node(object):
    def __init__(self, name):
        self.name = name
        self.inlinks = []
        self.outlinks = []
        self.rank = 0.0
        self.new_rank = 0.0

    def add_outlink(self, node):
        # Add directed edge from this node to another node
        self.outlinks.append(node)

    def add_inlink(self, node):
        # Add directed edge from another node to this node
        self.inlinks.append(node)

    def add_weight(self, weight):
        self.new_rank += weight

    def update(self):
        self.rank = self.new_rank
        self.new_rank = 0.0

    def get_name(self):
        return self.name

    def get_inlinks(self):
        return self.inlinks

    def get_outlinks(self):
        return self.outlinks

    def get_weight(self):
        if len(self.outlinks) == 0:
            return 0
        return self.rank / len(self.outlinks)

    def get_diff(self):
        return self.new_rank - self.rank

    def get_rank(self):
        return self.rank

# Note: Does not account for error-checking
# A dictionary of Nodes. Key is node name, value is node object
# nodes of the graph could also be another graph
# the top level graph is assumed to have the name "main"
# see project.py for usage
class Graph(object):
    def __init__(self, name):
        self.name = name
        self.nodes = {"proxy": Node("proxy")}
        self.size = 1
        self.inlinks = []
        self.outlinks = []
        self.rank = 0.0
        self.new_rank = 0.0
        self.beta = 0.8
        self.epsilon = 0.000001

    def get_nodes(self):
        # Return a list of nodes
        nodes = list(self.nodes.values())
        return nodes

    def get_node(self, node_name):
        return self.nodes[node_name]

    def get_name(self):
        return self.name

    def get_inlinks(self):
        return self.inlinks

    def get_outlinks(self):
        return self.outlinks

    def get_size(self):
        return self.size

    def get_weight(self):
        if len(self.outlinks) == 0:
            return 0
        return self.rank / len(self.outlinks)

    def get_diff(self):
        return self.new_rank - self.rank

    def get_rank(self):
        return self.rank

    def add_node(self, node):
        # Add node to graph
        self.nodes[node.get_name()] = node
        self.size += 1

    def add_edge(self, start_node, end_node):
        # Add edge from start node to end node
        if self.name == "main":
            start_parent = self.nodes[start_node.split("-")[0]]
            end_parent = self.nodes[end_node.split("-")[0]]
            if start_parent == end_parent:
                start_parent.add_edge(start_node, end_node)
            else:
                start_parent.add_outlink(end_parent)
                end_parent.add_inlink(start_parent)
                start_parent.add_edge(start_node, "proxy")
                end_parent.add_edge("proxy", end_node)
        else:
            start = self.nodes[start_node]
            end = self.nodes[end_node]
            start.add_outlink(end)
            end.add_inlink(start)

    def add_outlink(self, graph):
        # Add directed edge from this graph to another graph
        self.outlinks.append(graph)

    def add_inlink(self, graph):
        # Add directed edge from another graph to this graph
        self.inlinks.append(graph)

    def add_weight(self, weight):
        self.new_rank += weight

    def update(self):
        self.rank = self.new_rank
        self.new_rank = 0.0

    def init_ranks(self):
        for node in self.get_nodes():
            node.add_weight(1 / self.size)
            node.update()
            if self.name == "main" and node.get_name() != "proxy":
                node.init_ranks()

    def iterate(self):
        for source in self.get_nodes():
            if source.get_weight() == 0:
                weight = source.get_rank() / self.size
                for dest in self.get_nodes():
                    dest.add_weight(self.beta * weight)
            else:
                weight = source.get_weight()
                for dest in source.get_outlinks():
                    dest.add_weight(self.beta * weight)
        for node in self.get_nodes():
            weight = (1 - self.beta) / self.size
            node.add_weight(weight)

    def update(self):
        self.rank = self.new_rank
        self.new_rank = 0.0

    def update_nodes(self):
        for node in self.get_nodes():
            node.update()

    def check_update(self):
        ret = False
        for node in self.get_nodes():
            if node.get_diff() > self.epsilon or node.get_diff() < (-1) * self.epsilon:
                ret = True
        return ret

    def calc_ranks(self):
        self.iterate()
        while(self.check_update()):
            self.update_nodes()
            self.iterate()
        self.update_nodes()
        if self.name == "main":
            for node in self.get_nodes():
                if node.get_name() != "proxy":
                    node.calc_ranks()

    def get_ranks(self):
        ranks = {}
        if self.name == "main":
            for node in self.get_nodes():
                if node.get_name() != "proxy":
                    tmp = {k: v * node.get_rank() for k, v in node.get_ranks().items()}
                    ranks.update(tmp)
        else:
            for node in self.get_nodes():
                ranks[node.get_name()] = node.get_rank()
            ranks.pop("proxy")
        return ranks

    def add_and_update(self, start_node, end_node):
        start_parent = self.nodes[start_node.split("-")[0]]
        end_parent = self.nodes[end_node.split("-")[0]]
        if start_parent == end_parent:
            start_parent.add_edge(start_node, end_node)
            start_parent.calc_ranks()
        else:
            start_parent.add_outlink(end_parent)
            end_parent.add_inlink(start_parent)
            start_parent.add_edge(start_node, "proxy")
            end_parent.add_edge("proxy", end_node)
            start_parent.calc_ranks()
            end_parent.calc_ranks()
            self.iterate()
            while(self.check_update()):
                self.update_nodes()
                self.iterate()
            self.update_nodes()