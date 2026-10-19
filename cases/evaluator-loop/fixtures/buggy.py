class MinStack:
    """Integer stack with constant-time minimum lookup."""
    def __init__(self):
        self.items = []
        self.minimums = []

    def push(self, x):
        self.items.append(x)
        if not self.minimums or x < self.minimums[-1]:
            self.minimums.append(x)

    def pop(self):
        if not self.items:
            raise IndexError('empty stack')
        value = self.items.pop()
        if value == self.minimums[-1]:
            self.minimums.pop()
        return value

    def getMin(self):
        if not self.minimums:
            raise IndexError('empty stack')
        return self.minimums[-1]
