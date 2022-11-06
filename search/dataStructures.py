class Stack:
    def __init__(self):
        self._stack = []

    def push(self, element):
        self._stack.append(element)

    def pop(self):
        if self.isEmpty():
            raise ValueError("Stack is empty!")
        return self._stack.pop(-1)

    def isEmpty(self):
        return len(self._stack) == 0
