import random
import math


class Boid:
    color_list = [
        "#007FFF",
        "#0000FF",
        "#0066b2",
        "#318CE7",
        "#6699CC",
        "#5072A7",
        "#0039A6",
        "#3457D5",
        "#00BFFF",
        "#4B9CD3",
        "#034694",
        "#2a52be",
        "#1F75FE",
    ]
    distance = 50
    max_vel = 5
    min_vel = -5

    def __init__(self, label) -> None:
        self.label = label
        self.color = random.choice(self.color_list)
        self.x = random.randrange(100, 700)
        self.y = random.randrange(100, 700)
        self.angle = random.uniform(0.0, 2.0 * math.pi)
        self.vx = 2 * math.cos(self.angle)
        self.vy = 2 * math.sin(self.angle)

    def control_max_vel(self):
        self.vx = self.max_vel if self.vx > self.max_vel else self.vx
        self.vy = self.max_vel if self.vy > self.max_vel else self.vy
        self.vx = self.min_vel if self.vx < self.min_vel else self.vx
        self.vy = self.min_vel if self.vy < self.min_vel else self.vy

    def turn(self, size_x, size_y):
        margin = 400
        turnfactor = 0.04
        leftmargin = margin
        rightmargin = size_x - margin
        bottommargin = size_y - margin
        topmargin = margin

        if self.x < leftmargin:
            self.vx = self.vx + turnfactor
        if self.x > rightmargin:
            self.vx = self.vx - turnfactor
        if self.y > bottommargin:
            self.vy = self.vy - turnfactor
        if self.y < topmargin:
            self.vy = self.vy + turnfactor

    def move(self, canvas, size_x, size_y):
        self.control_max_vel()
        self.turn(size_x, size_y)
        self.x += self.vx
        self.y += self.vy
        self.angle = math.atan2(self.vy, self.vx)
        # Wrap around
        # self.x = self.x % size_x
        # self.y = self.y % size_y

        canvas.delete(self.label)
        self.draw_boid(canvas)

    def draw_boid(self, canvas):
        size = 10
        x1 = self.x + size * math.cos(self.angle)
        x2 = self.y + size * math.sin(self.angle)

        canvas.create_line(
            self.x,
            self.y,
            x1,
            x2,
            fill=self.color,
            arrow="last",
            arrowshape=(10, 8, 8),
            width=2,
            tags=self.label,
        )

    def get_euclidean_distance(self, neighbour):
        d = math.sqrt((neighbour.x - self.x) ** 2 + (neighbour.y - self.y) ** 2)
        return d
