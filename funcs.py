def next_z(z, c):
    """Computes the next value in the Mandelbrot iteration sequence.

    Applies one step of the quadratic polynomial function:
    z_n+1 = (z_n)**2 + c

    Args:
    z (complex): The current complex value.
    c (complex): The constant complex coordinate being evaluated.

    Returns:
    complex: The resulting next value of z.
    """
    return z**2 + c

def escape_iterations(c, max_iter):
    """Calculates the escape time for a complex number in the Mandelbrot set.

    Repeatedly applies the quadratic recurrence relation z = z**2 + c starting
    from z = 0, up to a specified maximum number of iterations.

    Args:
        c (complex): The complex number being tested for Mandelbrot set
          membership.
        max_iter (int): The maximum number of iterations allowed before
          assuming the point remains bounded.

    Returns:
        int | None: The iteration number (escape time) when the magnitude of z
        first exceeds 2, or None if the value does not escape within max_iter
        iterations.
    """
    z = 0

    # Validate iteration count
    if max_iter <= 0 or not isinstance(max_iter, int):
        raise ValueError("Iteration count must be a positive integer")
        
    for i in range(1, max_iter + 1):
        # calculate the next value of z, because c remains constant throughout the loop
        z = next_z(z, c)

        if abs(z) > 2:
            return i 
    return None 

def pixel_to_complex(x, y, width, height):
    """Map 2D pixel coordinates (x, y) to a point on the complex plane.

    Scales screen coordinates within a (width x height) viewport to the default
    Mandelbrot viewing region (real: [-2.0, 1.0], imag: [-1.5, 1.5]),
    inverting the y-axis.
    """
    real_min, real_max = -2.0, 1.0
    imag_min, imag_max = -1.5, 1.5

    # Calculate real
    real = real_min + (x/(width - 1))*(real_max - real_min)

    # Calculate imag
    imag = imag_max - (y/(height - 1))*(imag_max - imag_min)

    # Return a complex number
    return complex(real, imag)

def escape_to_color(escape, max_iter):
    """
    Convert a Mandelbrot escape-time result into an RGB gradient color.

    Args:
        escape (int | None): Number of iterations before escape,
                             or None if no escape was detected.
        max_iter(int): Maximum number of iterations

    Returns:
        str: A Tkinter-compatible hexadecimal colour.
    """
    if escape is None:
        return "#000000"

    # Validate iteration count
    if max_iter <= 0 or not isinstance(max_iter, int):
        raise ValueError("Iteration count must be a positive integer")
    
    # Normalize escape time to a value between 0 and 1
    norm_escape = escape / max_iter

    # Calculate the intensity of RGB channels
    red = int(round(255 * (1 - norm_escape)))
    green = 0
    blue = int(round(255 * norm_escape))

    # Convert to a hex value
    hex_color = f"#{red:02x}{green:02x}{blue:02x}"

    return hex_color

def render_mandelbrot_rows(image,width,height,max_iter):

    """
    Render Mandelbrot colours into a PhotoImage one row at a time.

    Args:
        image (tk.PhotoImage): Image to populate.
        width (int): Image width in pixels.
        height (int): Image height in pixels.
        max_iter (int): Maximum Mandelbrot iterations.
    """
    for y in range(height):
        row_colors = []
        for x in range(width):
            # Convert this pixel into a complex number
            c = pixel_to_complex(x, y, width, height)

            escape = escape_iterations(c, max_iter)
            color = escape_to_color(escape, max_iter)
            
            row_colors.append(color)
        # Join row colors into a Tk-compatible row string
        row_data = "{" + " ".join(row_colors) + "}"

        # Write the entire row to image
        image.put(row_data, to=(0, y))

def handle_click(event):
    """
    Handle a left mouse click on the Mandelbrot Canvas.

    Args:
        event: Tkinter mouse event containing click coordinates.
    """
    # Get the pixel coordinte from the event
    x = event.x
    y = event.y
    width = event.x_root
    height = event.y_root

    # Convert to complex number
    c = pixel_to_complex(x, y, width, height)

    print(f"Complex value: {c}")
    print(f"Pixel coords: ({event.x}, {event.y})")
    print(f"Screen coords: ({event.x_root}, {event.y_root})")



