import tkinter as tk

def create_window():
   """Create a Tkinter window with a Canvas for graphics."""
   root = tk.Tk()
   root.title("Mandelbrot Explorer")

   # Create a 500 x 500 Canvas with a white background.
   canvas = tk.Canvas(root, width=500, height=500, bg="white")
   # Add the canvas to the window
   canvas.pack()
   canvas.create_rectangle(100,100,300,300, fill="blue")
   # Keeps the application running and processe user events
   root.mainloop()


if __name__ == "__main__":
  create_window()
   
