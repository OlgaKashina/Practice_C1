class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def get_area(self):
        return self.length * self.width


rect = Rectangle(10, 15)

print(rect.get_area())
