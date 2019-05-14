## list comprehension within classes
## js 20/11/06

class Test:
    def __init__(self):
        self.xs = [2*i for i in range(3)]
        self.boxes = ((i, j) for i in range(3) for j in range(3))
        