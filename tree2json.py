import sys
import re
import json
from Queue import Queue


class Node(object):
    def __init__(self, data):
        self.data = data.rstrip()
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)


class NodeEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Node):
            return super(NodeEncoder, self).default(obj)

        return obj.__dict__


def peek_stack(stack):
        # No peek for list? No Stack for python?
        current_parent = stack[len(stack) - 1]
        return current_parent


def main():
    q = Queue()
    s = []
    stop_reading = False

    """
    Detecting depth:
        '|-- ' - A Child for the above node.
        '`-- ' - Last child for the above node.
        '|   ' - Parent is a child.
        '    ' - Parent is a child.
    """
    node_depth = re.compile(r"(\|\-\- |\|   |\`\-\- |    )")

    # Convert input to a queue
    for line in sys.stdin:
        if line is not "\n":
            q.put(line)

    # Grab the root node to create the tree
    tree = Node(q.get())
    s.append(tree)
    last_depth = 1
    last_node = s[0]

    # Start parsing the rest of the tree
    for elem in list(q.queue):
        current_depth = len(node_depth.findall(elem))
        try:
            current_node = Node(re.search("\w+\.?.*$", elem).group(0))
        except:
            current_node = None
            stop_reading = True

        if (current_node is not None) and (stop_reading is False):
            if current_depth == last_depth:
                current_parent = peek_stack(s)
                current_parent.add_child(current_node)
                last_node = current_node
                last_depth = current_depth
            elif current_depth > last_depth:
                s.append(last_node)
                current_parent = peek_stack(s)
                current_parent.add_child(current_node)
                last_node = current_node
                last_depth = current_depth
            elif current_depth < last_depth:
                #print "This must less: " + str((last_depth - current_depth))
                for i in xrange((last_depth - current_depth)):
                    s.pop()
                current_parent = peek_stack(s)
                current_parent.add_child(current_node)
                last_node = current_node
                last_depth = current_depth

    print json.dumps(tree, cls=NodeEncoder, indent=2, separators=(',', ': '))


if __name__ == '__main__':
    main()
