import tkinter as tk
from funcs import render_mandelbrot_rows, pixel_to_complex, calculate_zoom_bounds

def draw_mandelbrot():
    """
        Render a color-based Mandelbrot set in a Tkinter window based on escape time
    """
    width = 500
    height = 500
    max_iter = 100

    bounds = (-2.0, 1.0, -1.5, 1.5)

    root = tk.Tk()
    root.title("Mandelbrot Explorer")
    root.geometry("800x800")

    # Create and pack a Canvas
    canvas = tk.Canvas(root, width=width, height=height, background="white")
    canvas.pack()
 
    # Create a PhotoImage matching the canvas dimensions
    image = tk.PhotoImage(width=width, height=height)

    render_mandelbrot_rows(image,width,height,max_iter, bounds)

    # Display the PhotoImage to the Canvas
    canvas.create_image(0,0,image=image, anchor="nw")
    # Keep a reference to the image
    canvas.image = image

    def handle_click(event):
        """
        Zoom into the Mandelbrot set around a clicked location.

        Args:
        event: Tkinter mouse event containing click coordinates.
        """
        nonlocal bounds

        # Convert the clicked pixel into complex number
        center = pixel_to_complex(event.x, event.y, width, height, *bounds)

        # Calculathe the xoom bounds around center
        bounds = calculate_zoom_bounds(center, *bounds, zoom_factor=2)

        render_mandelbrot_rows(image,width,height,max_iter, bounds)

        print(f"Current bounds: {bounds}")

    canvas.bind("<Button-1>", handle_click)

    root.mainloop()


if __name__ == "__main__":
    draw_mandelbrot()
