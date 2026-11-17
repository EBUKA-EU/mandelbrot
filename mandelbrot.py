import tkinter as tk
from funcs import escape_iterations, pixel_to_complex, escape_to_color

def draw_mandelbrot():
    """
        Render a color-based Mandelbrot set in a Tkinter window based on escape time
    """
    width = 180
    height = 180
    max_iter = 100

    root = tk.Tk()
    root.title("Mandelbrot Explorer")

    # Create and pack a Canvas
    canvas = tk.Canvas(root, width=width, height=height, background="white")
    canvas.pack()

    # Create a PhotoImage matching the canvas dimensions
    image = tk.PhotoImage(width=width, height=height)

    for y in range(height):
        for x in range(width):
            # Convert this pixel into a complex number
            c = pixel_to_complex(x, y, width, height)

            # Calculate the escape time
            escape = escape_iterations(c, max_iter)
            # Colour points based on whether they escaped the Mandelbrot set
            color = escape_to_color(escape=escape)

            # Write color to pixel
            image.put(color, to=(x, y))

    # Display the PhotoImage to the Canvas
    canvas.create_image(0,0,image=image, anchor="nw")
    # Keep a reference to the image
    canvas.image = image

    root.mainloop()

if __name__ == "__main__":
    draw_mandelbrot()
