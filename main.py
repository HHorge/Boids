import tkinter as tk
import Boid

no_of_boids = 150
screen_x = 1200
screen_y = 900
distance = 50
close_distance = 20


def initialise_canvas(window, x, y):
    canvas = tk.Canvas(window, width=x, height=y)
    canvas.pack()
    window.resizable(False, False)
    return canvas


def draw_boids(no_of_boids, canvas):
    list_of_boids = []
    for n in range(no_of_boids):
        boid = Boid.Boid("boid" + str(n))
        list_of_boids.append(boid)
        boid.draw_boid(canvas)
    return list_of_boids


def update_boids(
    list_of_boids, canvas, matching_factor, separation_factor, centering_factor
):
    for boid in list_of_boids:
        neighbours = []
        close_neighbours = []

        for boid2 in list_of_boids:
            d = boid.get_euclidean_distance(boid2)

            if d < close_distance and d != 0:
                close_neighbours.append(boid2)
            elif d < distance and d != 0:
                neighbours.append(boid2)

        if neighbours:
            alignment(boid, neighbours, matching_factor)
            cohesion(boid, neighbours, centering_factor)
        if close_neighbours:
            separation(boid, close_neighbours, separation_factor)

        boid.move(canvas, screen_x, screen_y)

    canvas.after(
        15,
        update_boids,
        list_of_boids,
        canvas,
        matching_factor,
        separation_factor,
        centering_factor,
    )


def alignment(boid, neighbours, matching_factor):
    x_vel_avg = 0.0
    y_vel_avg = 0.0

    for n in neighbours:
        x_vel_avg += n.vx
        y_vel_avg += n.vy

    x_vel_avg /= len(neighbours)
    y_vel_avg /= len(neighbours)
    boid.vx += (x_vel_avg - boid.vx) * matching_factor.get()
    boid.vy += (y_vel_avg - boid.vy) * matching_factor.get()


def separation(boid, neighbours, separation_factor):
    close_dx = 0.0
    close_dy = 0.0
    for n in neighbours:
        close_dx += boid.x - n.x
        close_dy += boid.y - n.y
    boid.vx += close_dx * separation_factor.get()
    boid.vy += close_dy * separation_factor.get()


def cohesion(boid, neighbours, centering_factor):
    xpos_avg = 0.0
    ypos_avg = 0.0
    for n in neighbours:
        xpos_avg += n.x
        ypos_avg += n.y

    xpos_avg /= len(neighbours)
    ypos_avg /= len(neighbours)
    boid.vx += (xpos_avg - boid.x) * centering_factor.get()
    boid.vy += (ypos_avg - boid.y) * centering_factor.get()


def motion(event):
    x, y = event.x, event.y

    print("{}, {}".format(x, y))


def hello(event):
    x, y = event.x, event.y

    print("{}, {}".format(x, y))


def main():
    window = tk.Tk()

    canvas = initialise_canvas(window, screen_x, screen_y)
    list_of_boids = draw_boids(no_of_boids, canvas)

    matching_factor = tk.DoubleVar()
    separation_factor = tk.DoubleVar()
    centering_factor = tk.DoubleVar()
    update_boids(
        list_of_boids, canvas, matching_factor, separation_factor, centering_factor
    )
    alignment_slider = tk.Scale(
        window,
        from_=0.0,
        to=0.1,
        digits=3,
        resolution=0.001,
        orient="horizontal",
        variable=matching_factor,
        label="Alignment",
    )

    separation_slider = tk.Scale(
        window,
        from_=0.0,
        to=0.1,
        digits=3,
        resolution=0.001,
        orient="horizontal",
        variable=separation_factor,
        label="Separation",
    )
    centering_slider = tk.Scale(
        window,
        from_=0.0,
        to=0.001,
        digits=4,
        resolution=0.0001,
        orient="horizontal",
        variable=centering_factor,
        label="Centering",
    )
    alignment_slider.pack(side=tk.LEFT)
    separation_slider.pack(side=tk.LEFT)
    centering_slider.pack(side=tk.LEFT)
    widget = tk.Button(None, text="Mouse Clicks")
    widget.pack()
    widget.bind("<Button-1>", hello)

    window.bind("<Motion>", motion)

    window.mainloop()


main()
