class Node:

    def __init__(self, status):
        self.status = status
        self.parent = None
        self.current_operator = None
        self.previous_operators = None
        self.node_depth = 0
        self.steps_gx = 0
        self.hx = 0
        self.fx = 0