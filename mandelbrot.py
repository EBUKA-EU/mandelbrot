import tkinter as tk
from funcs import render_mandelbrot_rows, pixel_to_complex, calculate_zoom_bounds

def draw_mandelbrot():
    """
        Render a color-based Mandelbrot set in a Tkinter window based on escape time
    """
    width = 500
    height = 500
    max_iter = 100

    initial_bounds = (-2.0, 1.0, -1.5, 1.5)
    bounds = initial_bounds


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

    def handle_right_click(event):
        """
        Zoom out around the complex coordinate selected by the user.

        Args:
            event: Tkinter right-click mouse event.
        """
        nonlocal bounds

        # Convert the clicked corrdinates into complex number
        center = pixel_to_complex(event.x, event.y, width, height, *bounds)

        # Calculate new bounds using zoomfactor=0.5
        bounds = calculate_zoom_bounds(center, *bounds, zoom_factor=0.5)

        render_mandelbrot_rows(image, width, height, max_iter, bounds)

    canvas.bind("<Button-3>", handle_right_click)

    def reset_view():
        """
        Restore the original Mandelbrot viewing boundaries
        and redraw the image.
        """
        nonlocal bounds

        # Restore the initial boundaries
        bounds = initial_bounds

        # Redraw the mandelbrot image
        render_mandelbrot_rows(image, width, height, max_iter, bounds)

    # Create a reset button
    reset_button = tk.Button(root, text="Reset View", command=reset_view)
    reset_button.pack()
    
    root.mainloop()


if __name__ == "__main__":
    draw_mandelbrot()
