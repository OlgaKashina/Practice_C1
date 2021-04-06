class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def str(self):
        return f"Rectangle ({self.x}, {self.y}, {self.width}, {self.height})"


rect = Rectangle(5, 10, 50, 100)

print(rect.str())
