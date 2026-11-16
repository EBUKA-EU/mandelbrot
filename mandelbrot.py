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
    for i in range(1, max_iter + 1):
        # calculate the next value of z, because c remains constant throughout the loop
        z = next_z(z, c)

        if abs(z) > 2:
            return i 
    return None 
