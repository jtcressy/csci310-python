import sys
import datetime

class Vertex:
    def __init__(self, node, time, isDeparturePoint=False):
        self.id = node
        self.time = time
        self.isDeparturePoint = isDeparturePoint
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node, time, isDeparturePoint=False):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node, time, isDeparturePoint=isDeparturePoint)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            raise ValueError("{} does not exist in the graph".format(frm))
        if to not in self.vert_dict:
            raise ValueError("{} does not exist in the graph".format(to))

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()


def process(graph, start, stop):
    ""


def time_sum(time_a, time_b):  # time: str = "hh:mm"
    hh_a, mm_a = time_a.split(':')
    hh_b, mm_b = time_b.split(':')
    mm_t = int(mm_a) + int(mm_b)
    hh_t = int(hh_a) + int(hh_b)
    hh_f = mm_t // 60 + hh_t
    mm_f = mm_t % 60
    return "{}:{}".format(hh_f, mm_f)


def hhmm_to_mins(time):
    hh, mm = map(int, time.split(':'))
    return mm + hh * 60


def parse(lines):  # parses one testcase and returns the rest of the lines omitting the data in this test case
    graph = Graph()
    num_routes = int(lines[0])
    routelines = lines[1:num_routes+1]
    for line in routelines:
        last_vertex = ""
        for i, time in enumerate(line[1:][::2]):
            name = line[1:][i+1]
            graph.add_vertex(name, time, i == 0)
            if i > 0:
                graph.add_edge(
                    last_vertex,
                    name,
                    cost=hhmm_to_mins(graph.get_vertex(name).time)
                )
                last_vertex = name
    start, end = lines[num_routes+1].split()
    process(graph, start, end)
    return lines[num_routes+1:]


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    lines = [line.strip for line in lines]
    num_cases = int(lines[0])
    lines.pop(-1)
    for i in range(0, num_cases):
        lines = parse(lines)

