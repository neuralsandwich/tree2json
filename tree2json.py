import sys
import re
import json
from Queue import Queue


class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Node):
            return super(MyEncoder, self).default(obj)

        return obj.__dict__


def peek_stack(stack):
        # No peek for list? No Stack for python?
        current_parent = stack[len(stack) - 1]
        return current_parent


def main():
    q = Queue()
    s = []
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
        current_node = Node(re.search("\w+\.?.*$", elem).group(0))

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

    print json.dumps(tree, cls=MyEncoder)


if __name__ == '__main__':
    main()
