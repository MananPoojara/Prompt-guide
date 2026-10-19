class MinStack:
    class _Node:
        __slots__ = ("value", "minimum", "next")

        def __init__(self, value, minimum, next_node):
            self.value = value
            self.minimum = minimum
            self.next = next_node

    def __init__(self):
        self._head = None

    def push(self, x):
        head = self._head
        minimum = x if head is None else min(x, head.minimum)
        self._head = self._Node(x, minimum, head)

    def pop(self):
        if self._head is None:
            raise IndexError("empty stack")
        node = self._head
        self._head = node.next
        return node.value

    def getMin(self):
        if self._head is None:
            raise IndexError("empty stack")
        return self._head.minimum
