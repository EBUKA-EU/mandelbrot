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
    if type(max_iter) is not int or max_iter <= 0:
        raise ValueError("Iteration count must be a positive integer")
        
    for i in range(1, max_iter + 1):
        # calculate the next value of z, because c remains constant throughout the loop
        z = next_z(z, c)

        if abs(z) > 2:
            return i 
    return None 

def pixel_to_complex(x, y, width, height, real_min, real_max, imag_min, imag_max):
    """
    Convert a pixel coordinate to a complex number
    within the specified viewing boundaries.

    Args:
        x (int): Horizontal pixel coordinate.
        y (int): Vertical pixel coordinate.
        width (int): Image width in pixels.
        height (int): Image height in pixels.
        real_min (float): Minimum real coordinate.
        real_max (float): Maximum real coordinate.
        imag_min (float): Minimum imaginary coordinate.
        imag_max (float): Maximum imaginary coordinate.

    Returns:
        complex: The corresponding complex-plane coordinate.
    """
   
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
    # Validate iteration count
    if max_iter <= 0 or not isinstance(max_iter, int):
        raise ValueError("Iteration count must be a positive integer")
    
    if escape is None:
        return "#000000"

    # Normalize escape time to a value between 0 and 1
    norm_escape = escape / max_iter

    # Calculate the intensity of RGB channels
    red = int(round(255 * (1 - norm_escape)))
    green = 0
    blue = int(round(255 * norm_escape))

    # Convert to a hex value
    hex_color = f"#{red:02x}{green:02x}{blue:02x}"

    return hex_color

def render_mandelbrot_rows(image,width,height,max_iter, bounds):
    """
    Render a Mandelbrot image using the supplied viewing boundaries.

    Args:
        image (tk.PhotoImage): Image to populate.
        width (int): Image width.
        height (int): Image height.
        max_iter (int): Maximum Mandelbrot iterations.
        bounds (tuple): Current real and imaginary viewing boundaries.
    """
    for y in range(height):
        row_colors = []
        for x in range(width):
            # Convert this pixel into a complex number
            c = pixel_to_complex(x, y, width, height, *bounds)

            escape = escape_iterations(c, max_iter)
            color = escape_to_color(escape, max_iter)
            
            row_colors.append(color)
        # Join row colors into a Tk-compatible row string
        row_data = "{" + " ".join(row_colors) + "}"

        # Write the entire row to image
        image.put(row_data, to=(0, y))

def calculate_zoom_bounds(center, real_min, real_max, imag_min, imag_max, zoom_factor):
    """
    Calculate new complex-plane boundaries after zooming.

    Args:
        center (complex): Complex number at the zoom centre.
        real_min (float): Current minimum real coordinate.
        real_max (float): Current maximum real coordinate.
        imag_min (float): Current minimum imaginary coordinate.
        imag_max (float): Current maximum imaginary coordinate.
        zoom_factor (float): Scale factor greater than zero.
                             Values above 1 zoom in.

    Returns:
        tuple: (new_real_min, new_real_max,
                new_imag_min, new_imag_max)
    """
    if zoom_factor <= 0:
        raise ValueError("Zoom factor must be greater than zero")

    # Calculate the current real and imag spans
    real_span = real_max - real_min
    imag_span = imag_max - imag_min

    # Divide each span by zoom_factor and by 2 
    # to obatin the new half-width and half-height

    half_real_span = (real_span / zoom_factor) / 2
    half_imag_span = (imag_span / zoom_factor) / 2

    # Calculate the new boundaries around center.real and center.imag
    new_real_min = center.real - half_real_span
    new_real_max = center.real + half_real_span

    new_imag_min = center.imag - half_imag_span
    new_imag_max = center.imag + half_imag_span

    return (new_real_min, new_real_max, new_imag_min, new_imag_max)

def render_mandelbrot_batches(
    root, image, width, height, max_iter, bounds, batch_size=5
):
    """
    Render Mandelbrot rows in batches, cancelling outdated renders.

    Each new rendering request invalidates previously scheduled batches

    Args:
        root (tk.Tk): Tkinter application window.
        image (tk.PhotoImage): Image to populate.
        width (int): Image width in pixels.
        height (int): Image height in pixels.
        max_iter (int): Maximum Mandelbrot iterations.
        bounds (tuple): Current complex-plane boundaries.
        batch_size (int): Number of rows to render per batch.
    """
    if type(batch_size) is not int or batch_size <= 0:
        raise ValueError("Batch size must be a positive integer")

    # Increment root.render_id.
    # Assume root.render_id was initialized to 0 when
    # the application window was created.
    root.render_id += 1

    # Store the current render ID
    my_render_id = root.render_id

    #image.put("black", to=(0,0, width, height))

    current_row = 0

    def render_next_batch():
        """Render the next batch only if this render is current."""
        nonlocal current_row

        if my_render_id != root.render_id:
            return

        # Determine which row this batch should end at
        end_row = min(current_row + batch_size, height)

        # Loop from current_row to the end of this batch.
        for y in range(current_row, end_row):
            row_colors = []

            for x in range(width):
                c = pixel_to_complex(x, y, width, height, *bounds)
                escape = escape_iterations(c,max_iter)
                color = escape_to_color(escape,max_iter)

                row_colors.append(color)

            image.put("{" + " ".join(row_colors) + "}", to=(0, y))

        current_row = end_row

        if current_row < height:
            root.after(1, render_next_batch)

    render_next_batch()