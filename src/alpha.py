from graph import MyGraph

# source: https://github.com/tdi/pypm
class Alpha:
    def __init__(self, log):
        self.log = log
        self.direct_succession = None
        self.start_events = None
        self.end_events = None
        self.parallel_events = None

        self.get_direct_succession()
        self.get_causality()
        self.get_inv_causality()
        self.get_start_events()
        self.get_end_events()
        self.get_parallel_events()

    def get_direct_succession(self):
        self.direct_succession = set()
        if self.log is None:
            return
        for event_list in self.log:
            for event_a, event_b in zip(event_list, event_list[1:]):
                self.direct_succession.add((event_a, event_b))

    def get_causality(self):
        self.causality = {}
        for events_pair in self.direct_succession:
            if events_pair[::-1] not in self.direct_succession:
                if events_pair[0] in self.causality.keys():
                    self.causality[events_pair[0]].append(events_pair[1])
                else:
                    self.causality[events_pair[0]] = [events_pair[1]]

    def get_inv_causality(self):
        self.inv_causality = {}
        for key, values in self.causality.items():
            if len(values) == 1:
                if values[0] in self.inv_causality.keys():
                    self.inv_causality[values[0]].append(key)
                else:
                    self.inv_causality[values[0]] = [key]

    def get_start_events(self):
        self.start_events = set()
        if self.log is None:
            return
        for event_list in self.log:
            self.start_events.add(event_list[0])

    def get_end_events(self):
        self.end_events = set()
        if self.log is None:
            return
        for event_list in self.log:
            self.end_events.add(event_list[-1])

    def get_parallel_events(self):
        self.parallel_events = set()
        for pair in self.direct_succession:
            if pair[::-1] in self.direct_succession:
                self.parallel_events.add(pair)

    # source: https://ai.ia.agh.edu.pl/pl:dydaktyka:dss:lab03
    def create_graph(self, filename='graph'):
        G = MyGraph()
        causality = self.causality
        parallel_events = self.parallel_events
        inv_causality = self.inv_causality
        start_set_events = self.start_events
        end_set_events = self.end_events

        # adding split gateways based on causality
        for event in causality:
            if len(causality[event]) > 1:
                if tuple(causality[event]) in parallel_events:
                    G.add_and_split_gateway(event, causality[event])
                else:
                    G.add_xor_split_gateway(event, causality[event])

        # adding merge gateways based on inverted causality
        for event in inv_causality:
            if len(inv_causality[event]) > 1:
                if tuple(inv_causality[event]) in parallel_events:
                    G.add_and_merge_gateway(inv_causality[event], event)
                else:
                    G.add_xor_merge_gateway(inv_causality[event], event)
            elif len(inv_causality[event]) == 1:
                source = list(inv_causality[event])[0]
                G.edge(source, event)

        # adding start event
        G.add_event("start")
        if len(start_set_events) > 1:
            if tuple(start_set_events) in parallel_events:
                G.add_and_split_gateway(event, start_set_events)
            else:
                G.add_xor_split_gateway(event, start_set_events)
        else:
            G.edge("start", list(start_set_events)[0])

        # adding end event
        G.add_event("end")
        if len(end_set_events) > 1:
            if tuple(end_set_events) in parallel_events:
                G.add_and_merge_gateway(end_set_events, event)
            else:
                G.add_xor_merge_gateway(end_set_events, event)
        else:
            G.edge(list(end_set_events)[0], "end")

        G.render('../graphs/' + filename, view=True)
        # G.view('simple_graphviz_graph')
